from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments' / 'base_config_json_only_timeout18_time_reduce_v63a_long_only_multimethod_architectures.json'
COMB = ROOT / 'experiments' / 'combinations_json_only_timeout18_time_reduce_v63a_long_only_multimethod_architectures.json'
VSRC = ROOT / 'scripts' / 'run_backtest_batch_json_only_timeout18_multimethod.py'

spec = importlib.util.spec_from_file_location('vmultimod', str(VSRC))
vmultimod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vmultimod)

vmultimod.BASE_CONFIG_PATH = BASE
vmultimod.SINGLE_CHANGES_PATH = COMB


def run_single_experiment_envfix(experiment: dict) -> dict:
    exp_name = experiment['name']
    cfg = experiment['effective_config']
    data_dir = Path(os.environ.get('DATA_DIR', str(vmultimod.ROOT / cfg['data_dir'])))
    result_dir = vmultimod.ROOT / cfg['results_dir'] / exp_name
    result_dir.mkdir(parents=True, exist_ok=True)

    min_bars = int(cfg['min_bars'])
    position_fraction = float(cfg['position_fraction'])
    all_trades = []
    trade_rows = []
    symbol_rows = []

    top_n = cfg['trade_control'].get('top_n_per_timestamp')
    if top_n is not None:
        raise NotImplementedError('top_n_per_timestamp는 현재 구조에서 지원하지 않습니다.')

    for csv_path in sorted(data_dir.glob('*.csv')):
        df = vmultimod.load_symbol_df(csv_path)
        if len(df) < min_bars:
            continue
        symbol_trades = vmultimod.run_symbol(df, cfg)
        all_trades.extend((en, ex, ret) for en, ex, ret, _ in symbol_trades)
        wins = sum(1 for _, _, r, _ in symbol_trades if r > 0)
        losses = sum(1 for _, _, r, _ in symbol_trades if r <= 0)
        gp = sum(r for _, _, r, _ in symbol_trades if r > 0)
        gl = -sum(r for _, _, r, _ in symbol_trades if r <= 0)
        symbol_rows.append({
            'symbol': csv_path.stem,
            'bars': len(df),
            'trades': len(symbol_trades),
            'wins': wins,
            'losses': losses,
            'win_rate': (wins / len(symbol_trades)) if symbol_trades else 0.0,
            'pf': (gp / gl) if gl > 0 else None,
            'sum_r': sum(r for _, _, r, _ in symbol_trades),
        })
        for en, ex, ret, side in symbol_trades:
            trade_rows.append({'symbol': csv_path.stem, 'entry_ts': en, 'exit_ts': ex, 'ret': ret, 'side': side})

    summary = vmultimod.evaluate_trades_cfg(all_trades, position_fraction)
    summary['strategy'] = f"{cfg['strategy_name']}_{exp_name}"
    summary['experiment_name'] = exp_name
    summary['initial_asset'] = float(cfg['initial_asset'])
    summary['position_fraction'] = float(cfg['position_fraction'])
    summary['fee_per_side'] = float(cfg['fee_per_side'])
    summary['symbols'] = len(symbol_rows)
    summary['effective_config'] = cfg

    trades_df = vmultimod.pd.DataFrame(trade_rows)
    if not trades_df.empty:
        trades_df = trades_df.sort_values(['entry_ts', 'symbol'])
    by_symbol_df = vmultimod.pd.DataFrame(symbol_rows)
    if not by_symbol_df.empty:
        by_symbol_df = by_symbol_df.sort_values(['trades', 'sum_r'], ascending=[False, False])
    trades_df.to_csv(result_dir / 'trades.csv', index=False)
    by_symbol_df.to_csv(result_dir / 'by_symbol.csv', index=False)
    with open(result_dir / 'summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


vmultimod.run_single_experiment = run_single_experiment_envfix

if __name__ == '__main__':
    vmultimod.main()
