from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / 'results_json_only_short_strict'
BASELINE_NAME = 'baseline'


def load_summary(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def safe_float(x):
    if x is None:
        return np.nan
    try:
        return float(x)
    except Exception:
        return np.nan


def judge_row(experiment: str, return_retention_pct: float, delta_pf: float, delta_mdd_pct: float, delta_max_conc: float) -> str:
    if experiment == BASELINE_NAME:
        return 'baseline'
    pass_cond = (
        pd.notna(delta_mdd_pct)
        and pd.notna(delta_pf)
        and pd.notna(return_retention_pct)
        and pd.notna(delta_max_conc)
        and delta_mdd_pct >= 1.0
        and delta_pf >= 0.0
        and return_retention_pct >= 90.0
        and delta_max_conc <= 0
    )
    hold_cond = (
        pd.notna(delta_mdd_pct)
        and pd.notna(return_retention_pct)
        and pd.notna(delta_max_conc)
        and delta_mdd_pct > 0.0
        and return_retention_pct >= 75.0
    )
    if pass_cond:
        return 'pass'
    if hold_cond:
        return 'hold'
    return 'fail'


def compute_cd_value(initial_asset: float, final_return_pct: float, mdd_pct: float) -> float:
    if pd.isna(initial_asset) or pd.isna(final_return_pct) or pd.isna(mdd_pct):
        return np.nan
    return float(initial_asset * (1.0 + (mdd_pct / 100.0)) * (1.0 + (final_return_pct / 100.0)))


def main() -> None:
    rows = []
    if not RESULTS_DIR.exists():
        print('results directory does not exist.')
        return

    for exp_dir in sorted(RESULTS_DIR.iterdir()):
        if not exp_dir.is_dir():
            continue
        summary_path = exp_dir / 'summary.json'
        if not summary_path.exists():
            continue
        s = load_summary(summary_path)
        rows.append({
            'experiment_group': 'json_only_short_strict_cd',
            'experiment': s.get('experiment_name', exp_dir.name),
            'strategy': s.get('strategy'),
            'symbols': safe_float(s.get('symbols')),
            'trades': safe_float(s.get('trades')),
            'initial_asset': safe_float(s.get('initial_asset')),
            'final_asset': safe_float(s.get('final_asset')),
            'final_return_pct': safe_float(s.get('final_return')) * 100.0,
            'peak_asset': safe_float(s.get('peak_asset')),
            'peak_growth_pct': safe_float(s.get('peak_growth')) * 100.0,
            'win_rate_pct': safe_float(s.get('win_rate')) * 100.0,
            'pf': safe_float(s.get('pf')),
            'mdd_pct': safe_float(s.get('mdd')) * 100.0,
            'max_conc': safe_float(s.get('max_conc')),
            'position_fraction': safe_float(s.get('position_fraction')),
            'fee_per_side': safe_float(s.get('fee_per_side')),
            'summary_path': str(summary_path.relative_to(ROOT)),
        })

    if not rows:
        print('No experiment summaries found.')
        return

    df = pd.DataFrame(rows)
    df['cd_value'] = df.apply(lambda row: compute_cd_value(row['initial_asset'], row['final_return_pct'], row['mdd_pct']), axis=1)
    df['mdd_under_5pct'] = df['mdd_pct'] > -5.0

    baseline_df = df[df['experiment'] == BASELINE_NAME]
    if baseline_df.empty:
        raise ValueError('baseline summary.json 이 없습니다.')

    baseline = baseline_df.iloc[0]
    baseline_final_return_pct = safe_float(baseline['final_return_pct'])
    baseline_pf = safe_float(baseline['pf'])
    baseline_mdd_pct = safe_float(baseline['mdd_pct'])
    baseline_max_conc = safe_float(baseline['max_conc'])
    baseline_cd_value = safe_float(baseline['cd_value'])

    df['delta_final_return_pct'] = df['final_return_pct'] - baseline_final_return_pct
    df['delta_pf'] = df['pf'] - baseline_pf
    df['delta_mdd_pct'] = df['mdd_pct'] - baseline_mdd_pct
    df['delta_max_conc'] = df['max_conc'] - baseline_max_conc
    df['delta_cd_value'] = df['cd_value'] - baseline_cd_value

    if pd.notna(baseline_final_return_pct) and baseline_final_return_pct != 0:
        df['return_retention_pct'] = (df['final_return_pct'] / baseline_final_return_pct) * 100.0
    else:
        df['return_retention_pct'] = np.nan

    df['verdict'] = df.apply(
        lambda row: judge_row(
            experiment=row['experiment'],
            return_retention_pct=row['return_retention_pct'],
            delta_pf=row['delta_pf'],
            delta_mdd_pct=row['delta_mdd_pct'],
            delta_max_conc=row['delta_max_conc'],
        ),
        axis=1,
    )

    verdict_rank = {'baseline': 0, 'pass': 1, 'hold': 2, 'fail': 3}
    df['verdict_rank'] = df['verdict'].map(verdict_rank).fillna(9)
    df = df.sort_values(by=['verdict_rank', 'delta_mdd_pct', 'delta_pf', 'final_return_pct'], ascending=[True, False, False, False]).reset_index(drop=True)

    out_csv = RESULTS_DIR / 'master_summary.csv'
    out_json = RESULTS_DIR / 'master_summary.json'
    out_txt = RESULTS_DIR / 'master_summary.txt'

    export_df = df.drop(columns=['verdict_rank'])
    export_df.to_csv(out_csv, index=False)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(export_df.to_dict(orient='records'), f, ensure_ascii=False, indent=2)

    lines = ['master_summary_json_only_short_strict_cd', '']
    for _, row in export_df.iterrows():
        parts = [
            f"experiment={row['experiment']}",
            f"verdict={row['verdict']}",
            f"final_return_pct={row['final_return_pct']:.4f}",
            f"delta_final_return_pct={row['delta_final_return_pct']:.4f}",
            f"pf={row['pf']:.6f}" if pd.notna(row['pf']) else 'pf=nan',
            f"delta_pf={row['delta_pf']:.6f}" if pd.notna(row['delta_pf']) else 'delta_pf=nan',
            f"mdd_pct={row['mdd_pct']:.4f}",
            f"delta_mdd_pct={row['delta_mdd_pct']:.4f}",
            f"max_conc={int(row['max_conc']) if pd.notna(row['max_conc']) else 'nan'}",
            f"delta_max_conc={int(row['delta_max_conc']) if pd.notna(row['delta_max_conc']) else 'nan'}",
            f"cd_value={row['cd_value']:.4f}" if pd.notna(row['cd_value']) else 'cd_value=nan',
            f"delta_cd_value={row['delta_cd_value']:.4f}" if pd.notna(row['delta_cd_value']) else 'delta_cd_value=nan',
            f"return_retention_pct={row['return_retention_pct']:.2f}" if pd.notna(row['return_retention_pct']) else 'return_retention_pct=nan',
        ]
        lines.append(' | '.join(parts))

    out_txt.write_text('\n'.join(lines), encoding='utf-8')
    print(export_df.to_string(index=False))
    print(f'\nsaved: {out_csv}')
    print(f'saved: {out_json}')
    print(f'saved: {out_txt}')


if __name__ == '__main__':
    main()
