from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'v84_short_base_fixed.json'
COMB = ROOT / 'experiments' / 'v84_short_combinations_fixed.json'
V78 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v78_short_lane_governor.py'

spec = importlib.util.spec_from_file_location('v78mod', str(V78))
v78mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v78mod)


def run_batch(base_path: Path = BASE, comb_path: Path = COMB):
    base = v78mod.v56mod.v27mod.load_json(base_path)
    group = v78mod.v56mod.v27mod.load_json(comb_path)
    out = []
    for exp in v78mod.v56mod.v27mod.build_experiments(base, group):
        cfg = exp['effective_config']
        name = exp['name']
        data_dir = Path(v78mod.v56mod.v27mod.os.environ.get('DATA_DIR', str(ROOT / cfg['data_dir'])))
        out_dir = ROOT / cfg['results_dir'] / name
        out_dir.mkdir(parents=True, exist_ok=True)
        all_trades = []
        for p in sorted(data_dir.glob('*.csv')):
            df = v78mod.v56mod.v27mod.load_df(p)
            if len(df) < int(cfg['min_bars']):
                continue
            all_trades.extend(v78mod.v56mod.v27mod.generate_symbol_trades(p.stem, df, cfg))
        s = v78mod.evaluate_governor(
            all_trades,
            float(cfg['initial_asset']),
            float(cfg['position_fraction']),
            cfg.get('trade_control', {}),
            cfg.get('governor', {}),
        )
        s.update({
            'strategy': f"{cfg['strategy_name']}_{name}",
            'experiment_name': name,
            'initial_asset': float(cfg['initial_asset']),
            'position_fraction': float(cfg['position_fraction']),
            'fee_per_side': float(cfg['fee_per_side']),
            'effective_config': cfg,
            'engine_mode': 'short_lane_governor_reclaim_fixed',
        })
        (out_dir / 'summary.json').write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(s, ensure_ascii=False, indent=2))
        out.append({
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
    v78mod.v56mod.v27mod.pd.DataFrame(out).to_csv(d / 'lane_summary.csv', index=False)
    return out


if __name__ == '__main__':
    run_batch()
