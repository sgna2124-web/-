from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_SRC = ROOT / 'experiments' / 'v80_short_base.json'
V78 = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_time_reduce_v78_short_lane_governor.py'

spec = importlib.util.spec_from_file_location('v78mod', str(V78))
v78mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v78mod)

GROUP = {
    'group_name': 'v84_short_lane_governor_reclaim_runnable',
    'experiments': [
        {
            'name': 'v84_short_reclaim_asia_prior1_quiet18',
            'enabled': True,
            'overrides': {
                'trade_control': {
                    'require_prior_signals_same_symbol': 1,
                    'prior_signal_window_bars': 48,
                    'first_signal_after_quiet_bars': 18,
                    'allowed_entry_hours_utc': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                },
                'governor': {
                    'hot_prior_required': 1,
                    'hot_prior_window_bars': 48,
                    'drop_standard_when_hot': True,
                    'hot_disable_reentry': True,
                    'hot_disable_entrygap': True
                }
            }
        },
        {
            'name': 'v84_short_reclaim_hot_all_day_relax_symbol',
            'enabled': True,
            'overrides': {
                'trade_control': {
                    'max_active_cap': 70,
                    'first_signal_after_quiet_bars': 24,
                    'dd_brake_trigger_pct': 0.025,
                    'dd_brake_freeze_steps': 6
                },
                'governor': {
                    'hot_prior_required': 1,
                    'hot_prior_window_bars': 36,
                    'hot_hours_utc': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                    'drop_standard_when_hot': True,
                    'hot_disable_reentry': True,
                    'hot_disable_entrygap': True,
                    'hot_relax_symbol_cap': True
                }
            }
        },
        {
            'name': 'v84_short_reclaim_hot_asia_quiet12_stack',
            'enabled': True,
            'overrides': {
                'trade_control': {
                    'require_prior_signals_same_symbol': 1,
                    'prior_signal_window_bars': 36,
                    'first_signal_after_quiet_bars': 12,
                    'entry_gap_same_symbol_bars': 18,
                    'allowed_entry_hours_utc': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                },
                'governor': {
                    'hot_prior_required': 1,
                    'hot_prior_window_bars': 36,
                    'quiet_bars': 12,
                    'drop_standard_when_hot': True,
                    'drop_standard_when_quiet': True,
                    'hot_disable_reentry': True,
                    'hot_disable_entrygap': True,
                    'hot_relax_symbol_cap': True
                }
            }
        },
        {
            'name': 'v84_short_reclaim_asia_guarded_dense_skip',
            'enabled': True,
            'overrides': {
                'trade_control': {
                    'require_prior_signals_same_symbol': 1,
                    'prior_signal_window_bars': 48,
                    'first_signal_after_quiet_bars': 24,
                    'skip_dense_ts_threshold': 20,
                    'max_active_cap': 60,
                    'allowed_entry_hours_utc': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                },
                'governor': {
                    'hot_prior_required': 2,
                    'hot_prior_window_bars': 48,
                    'drop_standard_when_hot': True,
                    'hot_disable_reentry': True,
                    'hot_disable_entrygap': True
                }
            }
        }
    ]
}


def run_batch():
    base = v78mod.v56mod.v27mod.load_json(BASE_SRC)
    base['strategy_name'] = 'overextension_reversion_v1_json_only_timeout18_time_reduce_v84_short_lane_governor_reclaim_runnable'
    base['results_dir'] = 'results_json_only_timeout18_time_reduce_v84_short_lane_governor_reclaim_runnable'
    out = []
    for exp in v78mod.v56mod.v27mod.build_experiments(base, GROUP):
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
            'engine_mode': 'short_lane_governor_reclaim_runnable',
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
