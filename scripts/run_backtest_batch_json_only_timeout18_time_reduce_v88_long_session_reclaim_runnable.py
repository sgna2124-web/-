import copy
import csv
import json
import os
from pathlib import Path

import pandas as pd

import run_backtest_batch_json_only_timeout18_time_reduce_v56_short_only_hybrid_guards_and_entry_modes as hybrid_mod
import run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn as v27mod

BASE_PATH = Path('experiments/v88_long_base.json')
COMB_PATH = Path('experiments/v88_long_combinations.json')
MDD_THRESHOLD_PCT = 5.0


def compute_cd_value(final_return_pct, mdd_pct):
    return 100.0 * (1.0 - abs(mdd_pct) / 100.0) * (1.0 + final_return_pct / 100.0)


def compact_row(name, summary):
    final_return_pct = float(summary['final_return']) * 100.0
    mdd_pct = abs(float(summary['mdd']) * 100.0)
    return {
        'experiment': name,
        'final_return_pct': final_return_pct,
        'mdd_pct': mdd_pct,
        'cd_value': compute_cd_value(final_return_pct, mdd_pct),
        'trades': int(summary.get('trades', 0)),
        'win_rate_pct': float(summary.get('win_rate', 0.0)) * 100.0,
        'pf': float(summary.get('pf', 0.0)),
        'max_conc': int(summary.get('max_conc', 0)),
        'same_bar_trades': int(summary.get('same_bar_trades', 0)),
    }


def sort_rows(rows):
    return sorted(
        rows,
        key=lambda r: (
            float(r['mdd_pct']) < MDD_THRESHOLD_PCT,
            float(r['cd_value']),
            float(r['final_return_pct']),
        ),
        reverse=True,
    )


def write_master_outputs(results_dir: Path, rows):
    ordered = sort_rows(rows)
    results_dir.mkdir(parents=True, exist_ok=True)

    with (results_dir / 'master_summary.json').open('w', encoding='utf-8') as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)
        f.write('\n')

    with (results_dir / 'master_summary.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(ordered[0].keys()))
        writer.writeheader()
        writer.writerows(ordered)

    with (results_dir / 'master_summary.txt').open('w', encoding='utf-8') as f:
        f.write('master_summary_json_only_long_strict_cd\n\n')
        for row in ordered:
            f.write(
                'experiment={experiment} | final_return_pct={final_return_pct:.4f} | '
                'mdd_pct={mdd_pct:.4f} | cd_value={cd_value:.4f} | trades={trades} | '
                'win_rate_pct={win_rate_pct:.4f} | pf={pf:.4f} | max_conc={max_conc} | '
                'same_bar_trades={same_bar_trades}\n'.format(**row)
            )


def run_batch():
    base = json.loads(BASE_PATH.read_text(encoding='utf-8'))
    combinations = json.loads(COMB_PATH.read_text(encoding='utf-8'))['experiments']
    data_dir = Path(base['data_dir'])
    results_dir = Path(base['results_dir'])
    results_dir.mkdir(parents=True, exist_ok=True)

    if not data_dir.exists():
        raise FileNotFoundError(f'Missing data_dir: {data_dir}')

    paths = sorted(data_dir.glob('*.csv'))
    if not paths:
        raise FileNotFoundError(f'No csv files found in {data_dir}')

    all_rows = []
    for experiment in combinations:
        if not experiment.get('enabled', True):
            continue
        cfg = copy.deepcopy(base)
        cfg = v27mod.deep_update(cfg, experiment.get('overrides', {}))
        name = experiment['name']
        out_dir = results_dir / name
        out_dir.mkdir(parents=True, exist_ok=True)

        summaries = []
        for p in paths:
            try:
                df = v27mod.load_df(p)
                trades = hybrid_mod.generate_symbol_trades(df, cfg)
                s = v27mod.compute_summary_from_trades(trades, initial_asset=cfg.get('initial_asset', 100.0))
                summaries.append(s)
            except Exception as exc:
                print(f'[WARN] {name} {p.name}: {exc}')

        if not summaries:
            print(f'[WARN] no summaries for {name}')
            continue

        portfolio = v27mod.combine_portfolio_equity(summaries, initial_asset=cfg.get('initial_asset', 100.0), position_fraction=cfg.get('position_fraction', 0.01))
        summary = v27mod.compute_portfolio_summary(portfolio, initial_asset=cfg.get('initial_asset', 100.0))

        with (out_dir / 'summary.json').open('w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            f.write('\n')

        lane_df = pd.DataFrame(summaries)
        lane_df.to_csv(out_dir / 'lane_summary.csv', index=False)

        row = compact_row(name, summary)
        all_rows.append(row)
        print(json.dumps(row, ensure_ascii=False))

    if not all_rows:
        raise RuntimeError('No experiment rows were produced')

    write_master_outputs(results_dir, all_rows)


if __name__ == '__main__':
    os.environ.setdefault('PYTHONHASHSEED', '0')
    run_batch()
