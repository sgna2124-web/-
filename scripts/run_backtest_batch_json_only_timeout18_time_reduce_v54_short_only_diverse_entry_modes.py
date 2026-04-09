from __future__ import annotations
import importlib.util
import json
from collections import deque
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v54_short_only_diverse_entry_modes.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v54_short_only_diverse_entry_modes.json'
V27 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py'

spec = importlib.util.spec_from_file_location('v27mod', str(V27))
v27mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v27mod)


def safe_threshold(v):
    return float('-inf') if v is None else float(v)


def bars_diff(a, b):
    return int((pd.Timestamp(a) - pd.Timestamp(b)).total_seconds() // 300)


def evaluate_diverse(trades, initial_asset, position_fraction, tc):
    if not trades:
        return {'trades':0,'final_asset':float(initial_asset),'final_return':0.0,'peak_asset':float(initial_asset),'peak_growth':0.0,'win_rate':0.0,'pf':0.0,'mdd':0.0,'max_conc':0,'max_conc_unique_symbols':0,'same_bar_trades':0,'active_leftover':0}
    by_entry = {}
    by_exit = {}
    signal_history = {}
    for idx, tr in enumerate(trades):
        by_entry.setdefault(tr['entry_ts'], []).append(idx)
        by_exit.setdefault(tr['exit_ts'], []).append(idx)
        signal_history.setdefault(tr['symbol'], []).append(pd.Timestamp(tr['entry_ts']))
    for sym in signal_history:
        signal_history[sym].sort()
    timestamps = sorted(set(by_entry.keys()) | set(by_exit.keys()))

    equity = float(initial_asset)
    peak = equity
    peak_asset = equity
    mdd = 0.0
    active = {}
    max_conc = 0
    max_conc_symbols = 0
    gp = 0.0
    gl = 0.0
    wins = 0
    executed = set()
    same_bar_trades = sum(1 for tr in trades if tr.get('same_bar'))

    score_min_all = safe_threshold(tc.get('score_min'))
    score_min_long = score_min_all if tc.get('score_min_long') is None else float(tc.get('score_min_long'))
    score_min_short = score_min_all if tc.get('score_min_short') is None else float(tc.get('score_min_short'))

    dd_brake_trigger_pct = tc.get('dd_brake_trigger_pct')
    dd_brake_freeze_steps = int(tc.get('dd_brake_freeze_steps', 0) or 0)
    reentry_gap_after_close_bars = tc.get('reentry_gap_after_close_bars')
    entry_gap_same_symbol_bars = tc.get('entry_gap_same_symbol_bars')
    require_prior_signals_same_symbol = tc.get('require_prior_signals_same_symbol')
    prior_signal_window_bars = tc.get('prior_signal_window_bars')
    first_signal_after_quiet_bars = tc.get('first_signal_after_quiet_bars')
    allowed_entry_hours_utc = tc.get('allowed_entry_hours_utc')
    skip_dense_ts_threshold = tc.get('skip_dense_ts_threshold')

    dd_freeze_left = 0
    prev_dd_below = False
    last_entry_ts_by_symbol = {}
    last_exit_ts_by_symbol = {}

    def count_prior_signals(sym, ts, window_bars):
        cur = pd.Timestamp(ts)
        cnt = 0
        for old in signal_history.get(sym, []):
            if old >= cur:
                break
            if bars_diff(cur, old) <= int(window_bars):
                cnt += 1
        return cnt

    for ts in timestamps:
        exit_idxs = by_exit.get(ts, [])
        normal_exit_idxs = [idx for idx in exit_idxs if trades[idx]['entry_ts'] < ts]
        same_bar_exit_idxs = [idx for idx in exit_idxs if trades[idx]['entry_ts'] == ts]

        def close_idx(idx):
            nonlocal equity, peak, peak_asset, mdd, gp, gl, wins
            pos = active.pop(idx, None)
            if pos is None:
                return
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
            last_exit_ts_by_symbol[tr['symbol']] = pd.Timestamp(tr['exit_ts'])

        for idx in normal_exit_idxs:
            close_idx(idx)

        current_dd = equity / peak - 1.0
        dd_below = (dd_brake_trigger_pct is not None) and (current_dd <= -float(dd_brake_trigger_pct))
        if dd_below and not prev_dd_below:
            dd_freeze_left = max(dd_freeze_left, dd_brake_freeze_steps)
        prev_dd_below = bool(dd_below)

        entry_idxs = by_entry.get(ts, [])
        if not entry_idxs:
            continue

        candidates = []
        for i in entry_idxs:
            side = trades[i].get('side')
            score = trades[i].get('score', 0.0)
            if side == 1 and score < score_min_long:
                continue
            if side == -1 and score < score_min_short:
                continue
            sym = trades[i]['symbol']
            t = pd.Timestamp(trades[i]['entry_ts'])
            if allowed_entry_hours_utc is not None and int(t.hour) not in set(int(x) for x in allowed_entry_hours_utc):
                continue
            if require_prior_signals_same_symbol is not None and prior_signal_window_bars is not None:
                if count_prior_signals(sym, t, prior_signal_window_bars) < int(require_prior_signals_same_symbol):
                    continue
            if first_signal_after_quiet_bars is not None:
                if count_prior_signals(sym, t, first_signal_after_quiet_bars) > 0:
                    continue
            if entry_gap_same_symbol_bars is not None and sym in last_entry_ts_by_symbol:
                if bars_diff(t, last_entry_ts_by_symbol[sym]) < int(entry_gap_same_symbol_bars):
                    continue
            if reentry_gap_after_close_bars is not None and sym in last_exit_ts_by_symbol:
                if bars_diff(t, last_exit_ts_by_symbol[sym]) < int(reentry_gap_after_close_bars):
                    continue
            candidates.append(i)

        if skip_dense_ts_threshold is not None and len(candidates) > int(skip_dense_ts_threshold):
            candidates = []

        if dd_freeze_left > 0:
            dd_freeze_left -= 1
            candidates = []

        selected_set = set(candidates)
        for idx in candidates:
            tr = trades[idx]
            notional = equity * float(position_fraction)
            active[idx] = {'notional': notional, 'entry_ts': tr['entry_ts'], 'symbol': tr['symbol'], 'side': tr['side']}
            executed.add(idx)
            last_entry_ts_by_symbol[tr['symbol']] = pd.Timestamp(tr['entry_ts'])
        max_conc = max(max_conc, len(active))
        max_conc_symbols = max(max_conc_symbols, len({p['symbol'] for p in active.values()}))

        for idx in same_bar_exit_idxs:
            if idx in selected_set:
                close_idx(idx)

    final_asset = equity
    final_return = final_asset / float(initial_asset) - 1.0
    peak_growth = peak_asset / float(initial_asset) - 1.0
    pf = (gp / gl) if gl > 0 else float('inf')
    return {'trades':len(executed),'final_asset':float(final_asset),'final_return':float(final_return),'peak_asset':float(peak_asset),'peak_growth':float(peak_growth),'win_rate':float(wins / len(executed)) if executed else 0.0,'pf':float(pf),'mdd':float(mdd),'max_conc':int(max_conc),'max_conc_unique_symbols':int(max_conc_symbols),'same_bar_trades':int(same_bar_trades),'active_leftover':int(len(active))}


if __name__ == '__main__':
    base = v27mod.load_json(BASE)
    group = v27mod.load_json(COMB)
    out = []
    for exp in v27mod.build_experiments(base, group):
        cfg = exp['effective_config']
        name = exp['name']
        data_dir = Path(v27mod.os.environ.get('DATA_DIR', str(ROOT / cfg['data_dir'])))
        out_dir = ROOT / cfg['results_dir'] / name
        out_dir.mkdir(parents=True, exist_ok=True)
        all_trades = []
        for p in sorted(data_dir.glob('*.csv')):
            df = v27mod.load_df(p)
            if len(df) < int(cfg['min_bars']):
                continue
            all_trades.extend(v27mod.generate_symbol_trades(p.stem, df, cfg))
        tc = cfg.get('trade_control', {})
        s = evaluate_diverse(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        s.update({'strategy':f"{cfg['strategy_name']}_{name}",'experiment_name':name,'initial_asset':float(cfg['initial_asset']),'position_fraction':float(cfg['position_fraction']),'fee_per_side':float(cfg['fee_per_side']),'effective_config':cfg,'engine_mode':'strict_time_axis_diverse_entry_modes'})
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({'experiment':name,'trades':s['trades'],'final_asset':s['final_asset'],'final_return':s['final_return'],'peak_asset':s['peak_asset'],'peak_growth':s['peak_growth'],'win_rate':s['win_rate'],'pf':s['pf'],'mdd':s['mdd'],'max_conc':s['max_conc'],'max_conc_unique_symbols':s['max_conc_unique_symbols'],'same_bar_trades':s['same_bar_trades'],'active_leftover':s['active_leftover']})
    d = ROOT / base['results_dir']
    d.mkdir(parents=True, exist_ok=True)
    v27mod.pd.DataFrame(out).to_csv(d / 'lane_summary.csv', index=False)
