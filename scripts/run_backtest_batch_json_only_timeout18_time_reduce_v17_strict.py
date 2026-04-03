from __future__ import annotations
import copy, json, os
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v17_strict.json'
COMB_ENV = os.environ.get('V17_COMB', 'experiments/combinations_json_only_timeout18_time_reduce_v17_strict_sidecap.json')
COMB = (ROOT / COMB_ENV) if not Path(COMB_ENV).is_absolute() else Path(COMB_ENV)


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def deep_merge(a, b):
    x = copy.deepcopy(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(x.get(k), dict):
            x[k] = deep_merge(x[k], v)
        else:
            x[k] = copy.deepcopy(v)
    return x


def build_experiments(base, group):
    return [
        {'name': e['name'], 'effective_config': deep_merge(base, e.get('overrides', {}))}
        for e in group.get('experiments', []) if e.get('enabled', False)
    ]


def ema(a, p):
    return pd.Series(a).ewm(span=p, adjust=False).mean().to_numpy(float)


def rsi(a, p):
    s = pd.Series(a, dtype=float)
    d = s.diff()
    up = d.clip(lower=0)
    dn = -d.clip(upper=0)
    ru = up.ewm(alpha=1 / p, adjust=False).mean()
    rd = dn.ewm(alpha=1 / p, adjust=False).mean()
    rs = ru / rd.replace(0, np.nan)
    return (100 - (100 / (1 + rs))).fillna(50).to_numpy(float)


def atr(h, l, c, p):
    pc = np.roll(c, 1)
    pc[0] = c[0]
    tr = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    return pd.Series(tr).ewm(alpha=1 / p, adjust=False).mean().to_numpy(float)


def candle_features(o, h, l, c):
    body = np.abs(c - o)
    return {
        'body': body,
        'upper_wick': h - np.maximum(o, c),
        'lower_wick': np.minimum(o, c) - l,
    }


def load_df(path: Path):
    first = path.read_text(encoding='utf-8', errors='ignore').splitlines()[0].strip()
    if first.startswith('version https://git-lfs.github.com/spec/'):
        raise ValueError('LFS pointer')
    raw = pd.read_csv(path)
    raw.columns = [str(c).strip().replace('\ufeff', '').lower() for c in raw.columns]
    alias = {
        'date': ['date', 'datetime', 'timestamp', 'time', 'open_time', 'opentime', 'candle_date_time_utc', 'candle_date_time_kst'],
        'open': ['open', 'open_price', 'opening_price', '시가'],
        'high': ['high', 'high_price', '고가'],
        'low': ['low', 'low_price', '저가'],
        'close': ['close', 'close_price', 'closing_price', 'trade_price', '종가'],
        'volume': ['volume', 'vol', 'base_volume', 'candle_acc_trade_volume', 'acc_trade_volume', '거래량'],
    }
    mp = {}
    for target, keys in alias.items():
        for k in keys:
            if k.lower() in raw.columns:
                mp[k.lower()] = target
                break
    df = raw.rename(columns=mp)[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    for c in ['open', 'high', 'low', 'close', 'volume']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df.dropna().sort_values('date').drop_duplicates('date').reset_index(drop=True)


def trade_return(entry, exitp, side, fee):
    gross = (exitp / entry - 1.0) if side == 1 else (entry / exitp - 1.0)
    return gross - (2 * fee)


def generate_symbol_trades(symbol: str, df: pd.DataFrame, cfg: dict):
    s = cfg['signal']
    q = cfg.get('quality', {})
    r = cfg['risk']
    t = cfg['trade_control']
    x = cfg['execution']
    fee = float(cfg['fee_per_side'])

    o = df['open'].to_numpy(float)
    h = df['high'].to_numpy(float)
    l = df['low'].to_numpy(float)
    c = df['close'].to_numpy(float)
    ts = pd.to_datetime(df['date']).astype('int64').to_numpy()

    ema_v = ema(c, int(s['ema_period']))
    rsi_v = rsi(c, int(s['rsi_period']))
    atr_v = atr(h, l, c, int(s['atr_period']))
    f = candle_features(o, h, l, c)

    ld = float(q.get('long_dev') if q.get('long_dev') is not None else s['long_dev'])
    lr = float(q.get('long_rsi_max') if q.get('long_rsi_max') is not None else s['long_rsi_max'])
    lw = float(q.get('long_wick_mult') if q.get('long_wick_mult') is not None else s['long_wick_mult'])
    sd = float(q.get('short_dev') if q.get('short_dev') is not None else s['short_dev'])
    sr = float(q.get('short_rsi_min') if q.get('short_rsi_min') is not None else s['short_rsi_min'])
    sw = float(q.get('short_wick_mult') if q.get('short_wick_mult') is not None else s['short_wick_mult'])

    asm = float(r['atr_stop_mult'])
    rrm = float(r['rr_mult'])
    met = float(r['min_expected_tp'])
    timeout = int(r['timeout_bars'])
    smode = str(r.get('stop_mode', 'atr_only'))
    tmode = str(r.get('target_mode', 'ema_only'))
    cd = int(t['cooldown_bars_same_symbol_same_side'])
    trb = int(r.get('time_reduce_bars', 17))
    trf = float(r.get('time_reduce_to_risk_frac', 0.155))
    ff_b = r.get('fail_fast_bars')
    ff_r = r.get('fail_fast_min_progress_r')

    trades = []
    inpos = False
    last = {1: -10_000_000, -1: -10_000_000}
    start = max(int(s['ema_period']), int(s['rsi_period']), int(s['atr_period']), 30)
    mfe = 0.0
    riskv = 0.0

    for i in range(start, len(c) - 1):
        if not inpos:
            long_dev_now = max(0.0, -((c[i] / ema_v[i]) - 1.0))
            short_dev_now = max(0.0, ((c[i] / ema_v[i]) - 1.0))
            ls = bool(x['allow_long']) and (i - last[1] > cd) and ((c[i] / ema_v[i]) - 1.0) <= -ld and rsi_v[i] < lr and f['lower_wick'][i] >= lw * f['body'][i]
            ss = bool(x['allow_short']) and (i - last[-1] > cd) and ((c[i] / ema_v[i]) - 1.0) >= sd and rsi_v[i] > sr and f['upper_wick'][i] >= sw * f['body'][i]
            if ls or ss:
                side = 1 if ls else -1
                entry = o[i + 1]
                if side == 1:
                    wick_stop = l[i]
                    atr_stop = entry - atr_v[i] * asm
                    stop = min(wick_stop, atr_stop) if smode == 'wick_or_atr' else wick_stop if smode == 'wick_only' else atr_stop
                    ema_t = ema_v[i]
                    rr_t = entry + rrm * (entry - stop)
                    target = min(ema_t, rr_t) if tmode == 'ema_or_rr' and ema_t > entry else rr_t if tmode == 'rr_only' else ema_t
                    ok = entry > stop and (target - entry) / entry >= met
                    score = float(long_dev_now + max(0.0, (lr - rsi_v[i]) / 100.0) + max(0.0, f['lower_wick'][i] / (abs(f['body'][i]) + 1e-12)))
                else:
                    wick_stop = h[i]
                    atr_stop = entry + atr_v[i] * asm
                    stop = max(wick_stop, atr_stop) if smode == 'wick_or_atr' else wick_stop if smode == 'wick_only' else atr_stop
                    ema_t = ema_v[i]
                    rr_t = entry - rrm * (stop - entry)
                    target = max(ema_t, rr_t) if tmode == 'ema_or_rr' and ema_t < entry else rr_t if tmode == 'rr_only' else ema_t
                    ok = stop > entry and (entry - target) / entry >= met
                    score = float(short_dev_now + max(0.0, (rsi_v[i] - sr) / 100.0) + max(0.0, f['upper_wick'][i] / (abs(f['body'][i]) + 1e-12)))
                if ok:
                    inpos = True
                    ei = i + 1
                    ep = float(entry)
                    sp = float(stop)
                    tp = float(target)
                    mfe = 0.0
                    riskv = max(abs(ep - sp), 1e-12)
        else:
            prev = max(ei, i - 1)
            if side == 1:
                mfe = max(mfe, (h[prev] - ep) / riskv)
            else:
                mfe = max(mfe, (ep - l[prev]) / riskv)
            dsp = sp
            if (i - ei) >= trb and mfe > 0:
                dsp = max(dsp, ep - riskv * trf) if side == 1 else min(dsp, ep + riskv * trf)
            sp = dsp
            if side == 1:
                exit_p = sp if l[i] <= sp else tp if h[i] >= tp else c[i] if ((ff_b is not None and (i - ei) >= int(ff_b) and mfe < float(ff_r or 0.0) and c[i] < ep) or (i - ei) >= timeout) else None
            else:
                exit_p = sp if h[i] >= sp else tp if l[i] <= tp else c[i] if ((ff_b is not None and (i - ei) >= int(ff_b) and mfe < float(ff_r or 0.0) and c[i] > ep) or (i - ei) >= timeout) else None
            if exit_p is not None:
                trades.append({'symbol': symbol, 'entry_ts': int(ts[ei]), 'exit_ts': int(ts[i]), 'return': float(trade_return(ep, float(exit_p), side, fee)), 'score': float(score), 'side': int(side)})
                last[side] = i
                inpos = False
    return trades


def evaluate_portfolio_time_axis(trades, initial_asset, position_fraction, top_n_per_timestamp=None, top_n_long_per_timestamp=None, top_n_short_per_timestamp=None):
    if not trades:
        return {'trades': 0, 'final_asset': float(initial_asset), 'final_return': 0.0, 'peak_asset': float(initial_asset), 'peak_growth': 0.0, 'win_rate': 0.0, 'pf': 0.0, 'mdd': 0.0, 'max_conc': 0}

    by_entry = {}
    by_exit = {}
    for idx, tr in enumerate(trades):
        by_entry.setdefault(tr['entry_ts'], []).append(idx)
        by_exit.setdefault(tr['exit_ts'], []).append(idx)
    timestamps = sorted(set(by_entry.keys()) | set(by_exit.keys()))

    equity = float(initial_asset)
    peak = equity
    peak_asset = equity
    mdd = 0.0
    active = {}
    max_conc = 0
    gp = 0.0
    gl = 0.0
    wins = 0
    executed = set()

    for ts in timestamps:
        for idx in by_exit.get(ts, []):
            pos = active.pop(idx, None)
            if pos is not None:
                tr = trades[idx]
                pnl = pos['notional'] * tr['return']
                equity += pnl
                peak = max(peak, equity)
                peak_asset = max(peak_asset, equity)
                mdd = min(mdd, equity / peak - 1.0)
                if pnl > 0:
                    wins += 1
                    gp += pnl
                else:
                    gl += -pnl
        entry_idxs = by_entry.get(ts, [])
        if entry_idxs:
            long_idxs = [i for i in entry_idxs if trades[i].get('side') == 1]
            short_idxs = [i for i in entry_idxs if trades[i].get('side') == -1]
            long_idxs = sorted(long_idxs, key=lambda i: trades[i].get('score', 0.0), reverse=True)
            short_idxs = sorted(short_idxs, key=lambda i: trades[i].get('score', 0.0), reverse=True)
            if top_n_long_per_timestamp is not None:
                long_idxs = long_idxs[:int(top_n_long_per_timestamp)]
            if top_n_short_per_timestamp is not None:
                short_idxs = short_idxs[:int(top_n_short_per_timestamp)]
            selected = long_idxs + short_idxs
            if top_n_per_timestamp is not None and len(selected) > int(top_n_per_timestamp):
                selected = sorted(selected, key=lambda i: trades[i].get('score', 0.0), reverse=True)[:int(top_n_per_timestamp)]
            for idx in selected:
                tr = trades[idx]
                notional = equity * float(position_fraction)
                active[idx] = {'notional': notional, 'entry_ts': tr['entry_ts']}
                executed.add(idx)
                max_conc = max(max_conc, len(active))

    final_asset = equity
    final_return = (final_asset / float(initial_asset)) - 1.0
    peak_growth = (peak_asset / float(initial_asset)) - 1.0
    pf = (gp / gl) if gl > 0 else float('inf')
    return {'trades': len(executed), 'final_asset': float(final_asset), 'final_return': float(final_return), 'peak_asset': float(peak_asset), 'peak_growth': float(peak_growth), 'win_rate': float(wins / len(executed)) if executed else 0.0, 'pf': float(pf), 'mdd': float(mdd), 'max_conc': int(max_conc)}


if __name__ == '__main__':
    base = load_json(BASE)
    group = load_json(COMB)
    out = []
    for exp in build_experiments(base, group):
        cfg = exp['effective_config']
        name = exp['name']
        data_dir = Path(os.environ.get('DATA_DIR', str(ROOT / cfg['data_dir'])))
        out_dir = ROOT / cfg['results_dir'] / name
        out_dir.mkdir(parents=True, exist_ok=True)
        all_trades = []
        for p in sorted(data_dir.glob('*.csv')):
            df = load_df(p)
            if len(df) < int(cfg['min_bars']):
                continue
            all_trades.extend(generate_symbol_trades(p.stem, df, cfg))
        tc = cfg.get('trade_control', {})
        s = evaluate_portfolio_time_axis(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), top_n_per_timestamp=tc.get('top_n_per_timestamp'), top_n_long_per_timestamp=tc.get('top_n_long_per_timestamp'), top_n_short_per_timestamp=tc.get('top_n_short_per_timestamp'))
        s.update({'strategy': f"{cfg['strategy_name']}_{name}", 'experiment_name': name, 'initial_asset': float(cfg['initial_asset']), 'position_fraction': float(cfg['position_fraction']), 'fee_per_side': float(cfg['fee_per_side']), 'effective_config': cfg, 'engine_mode': 'strict_time_axis_realized_equity_side_rank_capped'})
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({'experiment': name, 'trades': s['trades'], 'final_asset': s['final_asset'], 'final_return': s['final_return'], 'peak_asset': s['peak_asset'], 'peak_growth': s['peak_growth'], 'win_rate': s['win_rate'], 'pf': s['pf'], 'mdd': s['mdd'], 'max_conc': s['max_conc']})
    d = ROOT / 'results_json_only_timeout18_time_reduce_v16_strict'
    d.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out).to_csv(d / 'single_changes_quick_summary_rankcap.csv', index=False)
