"""
short_main2 v3 official frozen runner entrypoint

This file is an execution entrypoint for the official short_main2/v3 baseline.
Official strategy: MIX05_A02_A03_failfast14_rr630

It intentionally delegates to the full standalone runner located at repository root:
short_main2_v2_MIX05_single_retest_v1_6_envlocked.py

The file name of the full runner contains v2 because it was created during the v2-to-v3 promotion process.
The promoted official baseline is short_main2/v3.
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path

EXPECTED = {
    "strategy": "MIX05_A02_A03_failfast14_rr630",
    "trades": 150791,
    "official_cd_value": 81528.0994560266,
    "max_drawdown_pct": 5.879344393880359,
    "profit_factor": 1.882073174356906,
    "mtm_worstbar_cd_value": 74307.00038895881,
}

FULL_RUNNER_NAME = "short_main2_v2_MIX05_single_retest_v1_6_envlocked.py"
DEFAULT_OUT_DIR = "./local_results/short_main/SHORT_MAIN2_V3_MIX05_OFFICIAL_RETEST"


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / FULL_RUNNER_NAME).exists():
            return p
    # common layout: this file is under base_line/short_main2/v3
    p = cur
    for _ in range(4):
        p = p.parent
    return p


def main() -> None:
    parser = argparse.ArgumentParser(description="short_main2/v3 official frozen runner entrypoint")
    parser.add_argument("--data-dir", default=None, help="OHLCV CSV folder. If omitted, full runner auto-detects common local paths.")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    parser.add_argument("--max-files", default=None)
    parser.add_argument("--progress-every", default=None)
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    repo_root = find_repo_root(here)
    runner = repo_root / FULL_RUNNER_NAME

    print("[SHORT_MAIN2/V3 OFFICIAL FROZEN RUNNER]")
    print(f"strategy={EXPECTED['strategy']}")
    print(f"expected_trades={EXPECTED['trades']}")
    print(f"expected_official_cd_value={EXPECTED['official_cd_value']}")
    print(f"expected_max_drawdown_pct={EXPECTED['max_drawdown_pct']}")
    print(f"expected_profit_factor={EXPECTED['profit_factor']}")
    print(f"expected_mtm_worstbar_cd_value={EXPECTED['mtm_worstbar_cd_value']}")
    print(f"full_runner={runner}")

    if not runner.exists():
        raise FileNotFoundError(
            f"Required full runner not found: {runner}\n"
            f"Place {FULL_RUNNER_NAME} at repository root or run that file directly."
        )

    argv = [str(runner), "--out-dir", args.out_dir]
    if args.data_dir:
        argv.extend(["--data-dir", args.data_dir])
    if args.max_files:
        argv.extend(["--max-files", str(args.max_files)])
    if args.progress_every:
        argv.extend(["--progress-every", str(args.progress_every)])

    sys.argv = argv
    runpy.run_path(str(runner), run_name="__main__")


if __name__ == "__main__":
    main()
