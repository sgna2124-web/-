from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v65_long_only_guarded_wick_split_hybrid.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v65_long_only_guarded_wick_split_hybrid.json'
VSPLIT = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_split_entry.py'
V56 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v56_short_only_hybrid_guards_and_entry_modes.py'

spec_split = importlib.util.spec_from_file_location('vsplitmod', str(VSPLIT))
vsplitmod = importlib.util.module_from_spec(spec_split)
spec_split.loader.exec_module(vsplitmod)

spec_v56 = importlib.util.spec_from_file_location('v56mod', str(V56))
v56mod = importlib.util.module_from_spec(spec_v56)
spec_v56.loader.exec_module(v56mod)


def build_trade_dicts(symbol: str, symbol_trades: list[tuple[int, int, float, float, str]]) -> list[dict]:
    out = []
    for en, ex, ret, frac, side_name in symbol_trades:
        side = 1 if side_name == 'long' else -1
        out.append({
            'symbol': symbol,
            'entry_ts': pd.to_datetime(int(en), unit='ns'),
            'exit_ts': pd.to_datetime(int(ex), unit='ns'),
            'return': float(ret) * float(frac),
            'side': side,
            'score': 0.0,
            'same_bar': bool(int(en) == int(ex)),
        })
    return out


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
            symbol_trades = vsplitmod.run_symbol(df, cfg)
            all_trades.extend(build_trade_dicts(p.stem, symbol_trades))

        tc = cfg.get('trade_control', {})
        s = v56mod.evaluate_hybrid(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        s.update({
            'strategy': f"{cfg['strategy_name']}_{name}",
            'experiment_name': name,
            'initial_asset': float(cfg['initial_asset']),
            'position_fraction': float(cfg['position_fraction']),
            'fee_per_side': float(cfg['fee_per_side']),
            'effective_config': cfg,
            'engine_mode': 'guarded_wick_split_hybrid_long',
        })
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out_rows.append({
            'experiment': name,
            'trades': s['trades'],
            'final_asset': s['final_asset'],
            'final_return': s['final_return'],
            'peak_asset': s['peak_asset'],
            'peak_growth': s['peak_growth'],
            'win_rate': s['win_rate'],
            'pf': s['pf'],
            'mdd': s['mdd'],
            'max_conc': s['max_conc'],
            'max_conc_unique_symbols': s['max_conc_unique_symbols'],
            'same_bar_trades': s['same_bar_trades'],
            'active_leftover': s['active_leftover'],
        })

    d = ROOT / base['results_dir']
    d.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out_rows).to_csv(d / 'lane_summary.csv', index=False)
