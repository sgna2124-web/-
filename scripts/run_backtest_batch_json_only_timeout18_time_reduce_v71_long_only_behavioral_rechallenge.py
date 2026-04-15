from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v71_long_only_behavioral_rechallenge.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v71_long_only_behavioral_rechallenge.json'
V57 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v57_long_only_hybrid_guards_and_entry_modes.py'

spec = importlib.util.spec_from_file_location('v57mod', str(V57))
v57mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v57mod)

if __name__ == '__main__':
    base = v57mod.v56mod.v27mod.load_json(BASE)
    group = v57mod.v56mod.v27mod.load_json(COMB)
    out = []
    for exp in v57mod.v56mod.v27mod.build_experiments(base, group):
        cfg = exp['effective_config']
        name = exp['name']
        data_dir = Path(v57mod.v56mod.v27mod.os.environ.get('DATA_DIR', str(ROOT / cfg['data_dir'])))
        out_dir = ROOT / cfg['results_dir'] / name
        out_dir.mkdir(parents=True, exist_ok=True)
        all_trades = []
        for p in sorted(data_dir.glob('*.csv')):
            df = v57mod.v56mod.v27mod.load_df(p)
            if len(df) < int(cfg['min_bars']):
                continue
            all_trades.extend(v57mod.v56mod.v27mod.generate_symbol_trades(p.stem, df, cfg))
        tc = cfg.get('trade_control', {})
        s = v57mod.v56mod.evaluate_hybrid(all_trades, float(cfg['initial_asset']), float(cfg['position_fraction']), tc)
        s.update({
            'strategy': f"{cfg['strategy_name']}_{name}",
            'experiment_name': name,
            'initial_asset': float(cfg['initial_asset']),
            'position_fraction': float(cfg['position_fraction']),
            'fee_per_side': float(cfg['fee_per_side']),
            'effective_config': cfg,
            'engine_mode': 'behavioral_rechallenge_long',
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
    v57mod.v56mod.v27mod.pd.DataFrame(out).to_csv(d / 'lane_summary.csv', index=False)
