from __future__ import annotations
import importlib.util
import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json'
V27 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py'

spec = importlib.util.spec_from_file_location('v27mod', str(V27))
v27mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v27mod)


def safe_threshold(v):
    return float('-inf') if v is None else float(v)


def evaluate_behavioral(trades, initial_asset, position_fraction, tc):
    if not trades:
        return {'trades':0,'final_asset':float(initial_asset),'final_return':0.0,'peak_asset':float(initial_asset),'peak_growth':0.0,'win_rate':0.0,'pf':0.0,'mdd':0.0,'max_conc':0,'max_conc_unique_symbols':0,'same_bar_trades':0,'active_leftover':0}
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
    max_conc_symbols = 0
    gp = 0.0
    gl = 0.0
    wins = 0
    executed = set()
    same_bar_trades = sum(1 for tr in trades if tr.get('same_bar'))

    score_min_all = safe_threshold(tc.get('score_min'))
    score_min_long = score_min_all if tc.get('score_min_long') is None else float(tc.get('score_min_long'))
    score_min_short = score_min_all if tc.get('score_min_short') is None else float(tc.get('score_min_short'))

    max_active_cap = tc.get('max_active_cap')
    max_per_symbol = tc.get('max_per_symbol')
    loss_streak_trigger_losses = tc.get('loss_streak_trigger_losses')
    loss_streak_window = tc.get('loss_streak_window')
    loss_streak_freeze_steps = int(tc.get('loss_streak_freeze_steps', 0) or 0)
    dd_brake_trigger_pct = tc.get('dd_brake_trigger_pct')
    dd_brake_freeze_steps = int(tc.get('dd_brake_freeze_steps', 0) or 0)

    recent_closed = deque(maxlen=int(loss_streak_window or 1))
    loss_freeze_left = 0
    dd_freeze_left = 0
    prev_dd_below = False

    for ts in timestamps:
        exit_idxs = by_exit.get(ts, [])
        normal_exit_idxs = [idx for idx in exit_idxs if trades[idx]['entry_ts'] < ts]
        same_bar_exit_idxs = [idx for idx in exit_idxs if trades[idx]['entry_ts'] == ts]

        def close_idx(idx):
            nonlocal equity, peak, peak_asset, mdd, gp, gl, wins
            pos = active.pop(idx, None)
            if pos is None:
                return None
            tr = trades[idx]
            pnl = pos['notional'] * tr['return']
            equity += pnl
            peak = max(peak, equity)
            peak_asset = max(peak_asset, equity)
            mdd = min(mdd, equity / peak - 1.0)
            if pnl > 0:
                wins += 1
                gp += pnl
                recent_closed.append(1)
            else:
                gl += -pnl
                recent_closed.append(0)
            return pnl

        for idx in normal_exit_idxs:
            close_idx(idx)

        if loss_streak_trigger_losses is not None and loss_streak_window is not None and len(recent_closed) == int(loss_streak_window):
            if sum(1 for x in recent_closed if x == 0) >= int(loss_streak_trigger_losses):
                loss_freeze_left = max(loss_freeze_left, loss_streak_freeze_steps)
                recent_closed.clear()

        current_dd = equity / peak - 1.0
        dd_below = (dd_brake_trigger_pct is not None) and (current_dd <= -float(dd_brake_trigger_pct))
        if dd_below and not prev_dd_below:
            dd_freeze_left = max(dd_freeze_left, dd_brake_freeze_steps)
        prev_dd_below = bool(dd_below)

        entry_idxs = by_entry.get(ts, [])
        if not entry_idxs:
            continue

        long_idxs = [i for i in entry_idxs if trades[i].get('side') == 1 and trades[i].get('score', 0.0) >= score_min_long]
        short_idxs = [i for i in entry_idxs if trades[i].get('side') == -1 and trades[i].get('score', 0.0) >= score_min_short]
        selected = long_idxs + short_idxs

        if loss_freeze_left > 0:
            loss_freeze_left -= 1
            selected = []
        if dd_freeze_left > 0:
            dd_freeze_left -= 1
            selected = []

        final_selected = []
        symbol_counts = {}
        for p in active.values():
            symbol_counts[p['symbol']] = symbol_counts.get(p['symbol'], 0) + 1

        for idx in selected:
            if max_active_cap is not None and len(active) + len(final_selected) >= int(max_active_cap):
                break
            sym = trades[idx]['symbol']
            current_sym_count = symbol_counts.get(sym, 0) + sum(1 for j in final_selected if trades[j]['symbol'] == sym)
            if max_per_symbol is not None and current_sym_count >= int(max_per_symbol):
                continue
            final_selected.append(idx)

        selected_set = set(final_selected)
        for idx in final_selected:
            tr = trades[idx]
            notional = equity * float(position_fraction)
            active[idx] = {'notional': notional, 'entry_ts': tr['entry_ts'], 'symbol': tr['symbol'], 'side': tr['side']}
            executed.add(idx)
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
        s = evaluate_behavioral(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        s.update({'strategy':f"{cfg['strategy_name']}_{name}",'experiment_name':name,'initial_asset':float(cfg['initial_asset']),'position_fraction':float(cfg['position_fraction']),'fee_per_side':float(cfg['fee_per_side']),'effective_config':cfg,'engine_mode':'strict_time_axis_behavioral_guards'})
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({'experiment':name,'trades':s['trades'],'final_asset':s['final_asset'],'final_return':s['final_return'],'peak_asset':s['peak_asset'],'peak_growth':s['peak_growth'],'win_rate':s['win_rate'],'pf':s['pf'],'mdd':s['mdd'],'max_conc':s['max_conc'],'max_conc_unique_symbols':s['max_conc_unique_symbols'],'same_bar_trades':s['same_bar_trades'],'active_leftover':s['active_leftover']})
    d = ROOT / base['results_dir']
    d.mkdir(parents=True, exist_ok=True)
    v27mod.pd.DataFrame(out).to_csv(d / 'lane_summary.csv', index=False)
