from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path


def quarter_of_month(month: int) -> int:
    return ((month - 1) // 3) + 1


def split_symbol_from_name(path: Path) -> str:
    name = path.stem
    if name.endswith("_5m"):
        return name[:-3]
    return name


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def row_date(row: dict) -> str:
    for key in ["date", "datetime", "timestamp", "time", "open_time", "candle_date_time_utc", "candle_date_time_kst"]:
        if key in row and row[key]:
            return str(row[key])
    raise ValueError(f"No date-like column found in row keys: {list(row.keys())}")


def normalize_header(fieldnames: list[str]) -> list[str]:
    return [str(x).strip().replace("\ufeff", "") for x in fieldnames]


def process_file(src_csv: Path, out_dir: Path) -> list[dict]:
    symbol = split_symbol_from_name(src_csv)
    buckets: dict[tuple[int, int], list[dict]] = defaultdict(list)

    with open(src_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"No header in {src_csv}")
        reader.fieldnames = normalize_header(reader.fieldnames)
        for row in reader:
            dt = row_date(row)
            year = int(dt[0:4])
            month = int(dt[5:7])
            q = quarter_of_month(month)
            buckets[(year, q)].append(row)

        header = reader.fieldnames

    manifest_rows = []
    for (year, q), rows in sorted(buckets.items()):
        out_name = f"{symbol}_{year}_Q{q}_5m.csv.gz"
        out_path = out_dir / out_name
        with gzip.open(out_path, "wt", encoding="utf-8", newline="") as gz:
            writer = csv.DictWriter(gz, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)

        manifest_rows.append(
            {
                "symbol": symbol,
                "start_date": row_date(rows[0])[:10],
                "end_date": row_date(rows[-1])[:10],
                "rows": len(rows),
                "filename": out_name,
            }
        )
    return manifest_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, help="Directory containing source *.csv files")
    parser.add_argument("--output-dir", required=True, help="Directory to write *.csv.gz files and data_manifest.json")
    parser.add_argument("--timeframe", default="5m")
    parser.add_argument("--version", default="data-5m-v1")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    all_rows = []
    for src_csv in sorted(input_dir.glob("*.csv")):
        print(f"processing {src_csv.name}")
        all_rows.extend(process_file(src_csv, output_dir))

    manifest = {
        "version": args.version,
        "timeframe": args.timeframe,
        "format": "csv.gz",
        "files": all_rows,
    }

    manifest_path = output_dir / "data_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved manifest: {manifest_path}")


if __name__ == "__main__":
    main()
