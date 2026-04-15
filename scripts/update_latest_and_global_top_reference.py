import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOBAL_REF = ROOT / 'state' / 'global_top_reference_under_mdd5_cd.json'


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def dump_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write('\n')


def sort_key(row):
    mdd = float(row.get('mdd_pct', 999999.0))
    cdv = float(row.get('cd_value', -999999.0))
    ret = float(row.get('final_return_pct', -999999.0))
    return (mdd < 5.0, cdv, ret)


def pick_top1(rows):
    ordered = sorted(rows, key=sort_key, reverse=True)
    for row in ordered:
        if float(row.get('mdd_pct', 999999.0)) < 5.0:
            return row
    if not ordered:
        raise ValueError('No rows in master summary')
    return ordered[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--side', required=True, choices=['long', 'short'])
    parser.add_argument('--family', required=True)
    parser.add_argument('--master', required=True)
    parser.add_argument('--latest', required=True)
    args = parser.parse_args()

    master_path = ROOT / args.master
    latest_path = ROOT / args.latest

    rows = load_json(master_path)
    top1 = pick_top1(rows)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    latest_payload = {
        'updated_at_utc': now,
        'side': args.side,
        'family': args.family,
        'rule': {
            'mdd_threshold_pct': 5.0,
            'sort_priority': ['cd_value_desc'],
            'cd_formula': '100 * (1 - abs(mdd_pct)/100) * (1 + final_return_pct/100)'
        },
        'top1': top1
    }
    dump_json(latest_path, latest_payload)

    global_payload = load_json(GLOBAL_REF) if GLOBAL_REF.exists() else {
        'rule': {
            'mdd_threshold_pct': 5.0,
            'sort_priority': ['cd_value_desc'],
            'cd_formula': '100 * (1 - abs(mdd_pct)/100) * (1 + final_return_pct/100)'
        }
    }

    current = global_payload.get(args.side)
    should_replace = False
    if current is None:
        should_replace = True
    else:
        current_cd = float(current.get('cd_value', -999999.0))
        current_mdd = float(current.get('mdd_pct', 999999.0))
        new_cd = float(top1.get('cd_value', -999999.0))
        new_mdd = float(top1.get('mdd_pct', 999999.0))
        if new_mdd < 5.0 and (current_mdd >= 5.0 or new_cd > current_cd):
            should_replace = True

    if should_replace:
        global_payload[args.side] = {
            'family': args.family,
            **top1
        }
        dump_json(GLOBAL_REF, global_payload)


if __name__ == '__main__':
    main()
