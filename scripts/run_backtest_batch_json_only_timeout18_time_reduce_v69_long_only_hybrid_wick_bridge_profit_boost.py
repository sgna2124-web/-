from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost.json'
VSPLIT = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_split_entry.py'
V56 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v56_short_only_hybrid_guards_and_entry_modes.py'

spec_split = importlib.util.spec_from_file_location('vsplitmod', str(VSPLIT))
vsplitmod = importlib.util.module_from_spec(spec_split)
spec_split.loader.exec_module(vsplitmod)

spec_v56 = importlib.util.spec_from_file_location('v56mod', str(V56))
v56mod = importlib.util.module_from_spec(spec_v56)
spec_v56.loader.exec_module(v56mod)


def build_trade_dicts(symbol: str, symbol_trades: list[tuple[int, int, float, float, str]]) -> list[dict]:
    rows = []
    for en, ex, ret, frac, side_name in symbol_trades:
        side = 1 if side_name == 'long' else -1
        rows.append({
            'symbol': symbol,
            'entry_ts': pd.to_datetime(int(en), unit='ns'),
            'exit_ts': pd.to_datetime(int(ex), unit='ns'),
            'return': float(ret) * float(frac),
            'side': side,
            'score': 0.0,
            'same_bar': bool(int(en) == int(ex)),
        })
    return rows


if __name__ == '__main__':
    base = vsplitmod.load_json(BASE)
    group = vsplitmod.load_json(COMB)
    out_rows = []
    for exp in vsplitmod.build_experiments(base, group):
        cfg = exp['effective_config']
        name = exp['name']
        data_dir = Path(os.environ.get('DATA_DIR', str(ROOT / cfg['data_dir'])))
        out_dir = ROOT / cfg['results_dir'] / name
        out_dir.mkdir(parents=True, exist_ok=True)
        all_trades = []
        for p in sorted(data_dir.glob('*.csv')):
            df = vsplitmod.load_symbol_df(p)
            if len(df) < int(cfg['min_bars']):
                continue
            all_trades.extend(build_trade_dicts(p.stem, vsplitmod.run_symbol(df, cfg)))
        tc = cfg.get('trade_control', {})
        summary = v56mod.evaluate_hybrid(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        summary.update({
            'strategy': f"{cfg['strategy_name']}_{name}",
            'experiment_name': name,
            'initial_asset': float(cfg['initial_asset']),
            'position_fraction': float(cfg['position_fraction']),
            'fee_per_side': float(cfg['fee_per_side']),
            'effective_config': cfg,
            'engine_mode': 'hybrid_wick_bridge_profit_boost_long',
        })
        (out_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        out_rows.append({
            'experiment': name,
            'trades': summary['trades'],
            'final_asset': summary['final_asset'],
            'final_return': summary['final_return'],
            'peak_asset': summary['peak_asset'],
            'peak_growth': summary['peak_growth'],
            'win_rate': summary['win_rate'],
            'pf': summary['pf'],
            'mdd': summary['mdd'],
            'max_conc': summary['max_conc'],
            'max_conc_unique_symbols': summary['max_conc_unique_symbols'],
            'same_bar_trades': summary['same_bar_trades'],
            'active_leftover': summary['active_leftover'],
        })
    result_dir = ROOT / base['results_dir']
    result_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out_rows).to_csv(result_dir / 'lane_summary.csv', index=False)
