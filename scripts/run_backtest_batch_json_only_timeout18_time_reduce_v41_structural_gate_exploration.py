from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v41_structural_gate_exploration.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v41_structural_gate_exploration.json'
V27 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py'

spec = importlib.util.spec_from_file_location('v27mod', str(V27))
v27mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v27mod)


def safe_threshold(v):
    return float('-inf') if v is None else float(v)


def evaluate_structural(trades, initial_asset, position_fraction, tc):
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

    total_block = tc.get('entry_block_total_threshold')
    short_block = tc.get('entry_block_short_threshold')
    long_block = tc.get('entry_block_long_threshold')
    dominant_side_mode = str(tc.get('dominant_side_mode', 'none'))
    dominance_ratio = float(tc.get('dominance_ratio', 3.0))
    dominance_min_count = int(tc.get('dominance_min_count', 60))
    conflict_mode = str(tc.get('conflict_mode', 'none'))
    conflict_min_total = int(tc.get('conflict_min_total', 40))
    active_freeze_threshold = tc.get('active_freeze_threshold')
    active_freeze_steps = int(tc.get('active_freeze_steps', 0))
    active_side_bias_block = str(tc.get('active_side_bias_block', 'none'))
    active_side_gap = int(tc.get('active_side_gap', 80))
    active_side_ratio = float(tc.get('active_side_ratio', 1.5))

    freeze_left = 0

    for ts in timestamps:
        exit_idxs = by_exit.get(ts, [])
        normal_exit_idxs = [idx for idx in exit_idxs if trades[idx]['entry_ts'] < ts]
        same_bar_exit_idxs = [idx for idx in exit_idxs if trades[idx]['entry_ts'] == ts]

        for idx in normal_exit_idxs:
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
        if not entry_idxs:
            continue

        long_idxs = [i for i in entry_idxs if trades[i].get('side') == 1 and trades[i].get('score', 0.0) >= score_min_long]
        short_idxs = [i for i in entry_idxs if trades[i].get('side') == -1 and trades[i].get('score', 0.0) >= score_min_short]

        if freeze_left > 0:
            freeze_left -= 1
            long_idxs, short_idxs = [], []
        else:
            total_count = len(long_idxs) + len(short_idxs)
            long_count = len(long_idxs)
            short_count = len(short_idxs)

            if active_freeze_threshold is not None and len(active) >= int(active_freeze_threshold):
                freeze_left = max(0, active_freeze_steps - 1)
                long_idxs, short_idxs = [], []
            else:
                if total_block is not None and total_count >= int(total_block):
                    long_idxs, short_idxs = [], []
                else:
                    if short_block is not None and short_count >= int(short_block):
                        short_idxs = []
                        short_count = 0
                    if long_block is not None and long_count >= int(long_block):
                        long_idxs = []
                        long_count = 0

                    if dominant_side_mode != 'none':
                        if dominant_side_mode == 'block_short' and short_count >= dominance_min_count and short_count >= max(1, int(long_count * dominance_ratio)):
                            short_idxs = []
                            short_count = 0
                        elif dominant_side_mode == 'block_long' and long_count >= dominance_min_count and long_count >= max(1, int(short_count * dominance_ratio)):
                            long_idxs = []
                            long_count = 0
                        elif dominant_side_mode == 'block_dominant':
                            if short_count >= dominance_min_count and short_count >= max(1, int(long_count * dominance_ratio)):
                                short_idxs = []
                                short_count = 0
                            elif long_count >= dominance_min_count and long_count >= max(1, int(short_count * dominance_ratio)):
                                long_idxs = []
                                long_count = 0

                    if conflict_mode == 'minority_only':
                        total_count = len(long_idxs) + len(short_idxs)
                        if len(long_idxs) > 0 and len(short_idxs) > 0 and total_count >= conflict_min_total:
                            if len(long_idxs) < len(short_idxs):
                                short_idxs = []
                            elif len(short_idxs) < len(long_idxs):
                                long_idxs = []

                    active_long = sum(1 for p in active.values() if p['side'] == 1)
                    active_short = sum(1 for p in active.values() if p['side'] == -1)
                    if active_side_bias_block == 'block_new_shorts_if_short_heavy':
                        if active_short >= active_long * active_side_ratio + active_side_gap:
                            short_idxs = []
                    elif active_side_bias_block == 'block_new_longs_if_long_heavy':
                        if active_long >= active_short * active_side_ratio + active_side_gap:
                            long_idxs = []

        selected = long_idxs + short_idxs
        selected_set = set(selected)
        for idx in selected:
            tr = trades[idx]
            notional = equity * float(position_fraction)
            active[idx] = {'notional': notional, 'entry_ts': tr['entry_ts'], 'symbol': tr['symbol'], 'side': tr['side']}
            executed.add(idx)
        max_conc = max(max_conc, len(active))
        max_conc_symbols = max(max_conc_symbols, len({p['symbol'] for p in active.values()}))

        for idx in same_bar_exit_idxs:
            if idx in selected_set:
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
        s = evaluate_structural(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        s.update({'strategy':f"{cfg['strategy_name']}_{name}",'experiment_name':name,'initial_asset':float(cfg['initial_asset']),'position_fraction':float(cfg['position_fraction']),'fee_per_side':float(cfg['fee_per_side']),'effective_config':cfg,'engine_mode':'strict_time_axis_structural_gates'})
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({'experiment':name,'trades':s['trades'],'final_asset':s['final_asset'],'final_return':s['final_return'],'peak_asset':s['peak_asset'],'peak_growth':s['peak_growth'],'win_rate':s['win_rate'],'pf':s['pf'],'mdd':s['mdd'],'max_conc':s['max_conc'],'max_conc_unique_symbols':s['max_conc_unique_symbols'],'same_bar_trades':s['same_bar_trades'],'active_leftover':s['active_leftover']})
    d = ROOT / base['results_dir']
    d.mkdir(parents=True, exist_ok=True)
    v27mod.pd.DataFrame(out).to_csv(d / 'lane_summary.csv', index=False)
