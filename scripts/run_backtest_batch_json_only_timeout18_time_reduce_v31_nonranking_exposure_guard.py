from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v31_nonranking_exposure_guard.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v31_nonranking_exposure_guard.json'
V27 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py'

spec = importlib.util.spec_from_file_location('v27mod', str(V27))
v27mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v27mod)


def safe_threshold(v):
    return float('-inf') if v is None else float(v)


def dynamic_floor(base_floor, active_count, soft_cap, step, boost_per_step, burst_count, burst_threshold, burst_boost):
    floor = float(base_floor)
    if soft_cap is not None and active_count > int(soft_cap):
        s = max(0, active_count - int(soft_cap))
        k = ((s - 1) // max(1, int(step))) + 1
        floor += float(k) * float(boost_per_step)
    if burst_threshold is not None and burst_count >= int(burst_threshold):
        floor += float(burst_boost)
    return floor


def evaluate_portfolio_time_axis_exposure_guard(trades, initial_asset, position_fraction, tc):
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
    base_long = score_min_all if tc.get('score_min_long') is None else float(tc.get('score_min_long'))
    base_short = score_min_all if tc.get('score_min_short') is None else float(tc.get('score_min_short'))

    soft_cap = tc.get('exposure_active_soft_cap')
    step = int(tc.get('exposure_active_step', 25))
    long_boost = float(tc.get('exposure_long_boost_per_step', 0.0))
    short_boost = float(tc.get('exposure_short_boost_per_step', 0.0))
    burst_threshold = tc.get('exposure_burst_threshold')
    long_burst_boost = float(tc.get('exposure_long_burst_boost', 0.0))
    short_burst_boost = float(tc.get('exposure_short_burst_boost', 0.0))

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
        if entry_idxs:
            active_count = len(active)
            burst_count = len(entry_idxs)
            dyn_long = dynamic_floor(base_long, active_count, soft_cap, step, long_boost, burst_count, burst_threshold, long_burst_boost)
            dyn_short = dynamic_floor(base_short, active_count, soft_cap, step, short_boost, burst_count, burst_threshold, short_burst_boost)

            selected = [i for i in entry_idxs if ((trades[i].get('side') == 1 and trades[i].get('score', 0.0) >= dyn_long) or (trades[i].get('side') == -1 and trades[i].get('score', 0.0) >= dyn_short))]
            selected_set = set(selected)
            for idx in selected:
                tr = trades[idx]
                notional = equity * float(position_fraction)
                active[idx] = {'notional': notional, 'entry_ts': tr['entry_ts'], 'symbol': tr['symbol']}
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
        s = evaluate_portfolio_time_axis_exposure_guard(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        s.update({'strategy':f"{cfg['strategy_name']}_{name}",'experiment_name':name,'initial_asset':float(cfg['initial_asset']),'position_fraction':float(cfg['position_fraction']),'fee_per_side':float(cfg['fee_per_side']),'effective_config':cfg,'engine_mode':'strict_time_axis_revalidated_nonranking_exposure_guard'})
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({'experiment':name,'trades':s['trades'],'final_asset':s['final_asset'],'final_return':s['final_return'],'peak_asset':s['peak_asset'],'peak_growth':s['peak_growth'],'win_rate':s['win_rate'],'pf':s['pf'],'mdd':s['mdd'],'max_conc':s['max_conc'],'max_conc_unique_symbols':s['max_conc_unique_symbols'],'same_bar_trades':s['same_bar_trades'],'active_leftover':s['active_leftover']})
    d = ROOT / base['results_dir']
    d.mkdir(parents=True, exist_ok=True)
    v27mod.pd.DataFrame(out).to_csv(d / 'lane_summary.csv', index=False)
