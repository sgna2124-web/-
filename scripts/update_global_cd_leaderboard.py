from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / 'results'
MDD_LIMIT_PCT = 5.0


def safe_float(v: Any, default: float = 0.0) -> float:
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


def compute_cd_value(final_return_pct: float, mdd_pct: float) -> float:
    return 100.0 * (1.0 - abs(mdd_pct) / 100.0) * (1.0 + final_return_pct / 100.0)


def infer_side(name: str, source_hint: str) -> str:
    text = f'{name} {source_hint}'.lower()
    if 'short' in text:
        return 'short'
    if 'long' in text:
        return 'long'
    return 'unknown'


def normalize_row(row: dict[str, Any], source_file: Path) -> dict[str, Any]:
    final_return_pct = row.get('final_return_pct')
    if final_return_pct is None and 'final_return' in row:
        final_return_pct = safe_float(row.get('final_return')) * 100.0
    final_return_pct = safe_float(final_return_pct)

    mdd_pct = row.get('mdd_pct')
    if mdd_pct is None and 'mdd' in row:
        mdd_pct = abs(safe_float(row.get('mdd')) * 100.0)
    mdd_pct = abs(safe_float(mdd_pct))

    cd_value = row.get('cd_value')
    if cd_value is None or safe_float(cd_value) <= 0:
        cd_value = compute_cd_value(final_return_pct, mdd_pct)
    else:
        cd_value = safe_float(cd_value)

    experiment = str(row.get('experiment') or row.get('experiment_name') or row.get('strategy') or source_file.parent.name)
    side = infer_side(experiment, str(source_file))

    return {
        'experiment': experiment,
        'final_return_pct': final_return_pct,
        'mdd_pct': mdd_pct,
        'cd_value': cd_value,
        'trades': int(safe_float(row.get('trades'))),
        'win_rate_pct': safe_float(row.get('win_rate_pct'), safe_float(row.get('win_rate')) * 100.0),
        'pf': safe_float(row.get('pf')),
        'max_conc': int(safe_float(row.get('max_conc'))),
        'same_bar_trades': int(safe_float(row.get('same_bar_trades'))),
        'source_file': str(source_file.relative_to(ROOT)),
        'side': side,
    }


def collect_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in ROOT.rglob('master_summary.json'):
        if '.git/' in str(p):
            continue
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for row in data:
            if isinstance(row, dict):
                rows.append(normalize_row(row, p))
    return rows


def sort_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filtered = [r for r in rows if r['side'] in {'long', 'short'} and r['mdd_pct'] < MDD_LIMIT_PCT]
    return sorted(filtered, key=lambda r: (-r['cd_value'], r['mdd_pct'], -r['final_return_pct'], r['experiment']))


def top_by_side(rows: list[dict[str, Any]], side: str) -> dict[str, Any] | None:
    for row in rows:
        if row['side'] == side:
            return row
    return None


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-dir', default='', help='Fresh result dir to compare against global winners')
    parser.add_argument('--side', choices=['long', 'short', 'unknown'], default='unknown')
    parser.add_argument('--label', default='latest_run')
    args = parser.parse_args()

    rows = sort_rows(collect_rows())
    long_best = top_by_side(rows, 'long')
    short_best = top_by_side(rows, 'short')

    global_payload = {
        'rule': {
            'mdd_filter_pct': MDD_LIMIT_PCT,
            'cd_value_formula': '100 * (1 - abs(mdd_pct)/100) * (1 + final_return_pct/100)',
            'sort': ['cd_value desc', 'mdd_pct asc', 'final_return_pct desc'],
        },
        'long_best': long_best,
        'short_best': short_best,
        'top3_long': [r for r in rows if r['side'] == 'long'][:3],
        'top3_short': [r for r in rows if r['side'] == 'short'][:3],
    }
    write_json(RESULTS_ROOT / 'global_cd_leaderboard.json', global_payload)

    latest_payload = None
    if args.result_dir:
        result_dir = ROOT / args.result_dir
        master = result_dir / 'master_summary.json'
        if master.exists():
            data = json.loads(master.read_text(encoding='utf-8'))
            normalized = sort_rows([normalize_row(row, master) for row in data if isinstance(row, dict)])
            latest_best = normalized[0] if normalized else None
            global_best = long_best if args.side == 'long' else short_best if args.side == 'short' else None
            latest_payload = {
                'label': args.label,
                'side': args.side,
                'latest_best': latest_best,
                'global_best': global_best,
                'delta_cd_vs_global': None if not latest_best or not global_best else latest_best['cd_value'] - global_best['cd_value'],
                'delta_return_pct_vs_global': None if not latest_best or not global_best else latest_best['final_return_pct'] - global_best['final_return_pct'],
                'delta_mdd_pct_vs_global': None if not latest_best or not global_best else latest_best['mdd_pct'] - global_best['mdd_pct'],
            }
            write_json(RESULTS_ROOT / f'{args.label}.json', latest_payload)

    print(json.dumps({'global': global_payload, 'latest': latest_payload}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
