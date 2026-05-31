#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
short_main2/v2 official frozen runner launcher.

This launcher keeps the executable entry point inside the baseline folder.
It resolves and executes the official full runner file:
short_main2_v2_C03_single_retest_v1_3_envlocked.py

If the full runner is not present in the repository root or current working
folder, extract the same file from the ChatGPT artifact used for this baseline
and place it at the repository root. The baseline specification and exact gate
values are stored in this folder.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

OFFICIAL_RUNNER_NAME = "short_main2_v2_C03_single_retest_v1_3_envlocked.py"
EXPECTED_STRATEGY = "SM60_C03_stop240_score270_timeout315"
EXPECTED_TRADES = 152030
EXPECTED_OFFICIAL_CD_VALUE = 69498.03075622236
EXPECTED_MAX_DRAWDOWN_PCT = 5.888592725709996
EXPECTED_PROFIT_FACTOR = 1.8286053579584032


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / "base_line" / "short_main2" / "v2").exists():
            return p
    return cur


def find_official_runner() -> Path:
    here = Path(__file__).resolve()
    repo_root = find_repo_root(here.parent)
    candidates = [
        repo_root / OFFICIAL_RUNNER_NAME,
        Path.cwd() / OFFICIAL_RUNNER_NAME,
        here.parent / OFFICIAL_RUNNER_NAME,
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            return p.resolve()

    checked = "\n".join(str(p) for p in candidates)
    raise FileNotFoundError(
        "Official full runner file was not found.\n"
        f"Required file: {OFFICIAL_RUNNER_NAME}\n"
        "Checked paths:\n"
        f"{checked}\n\n"
        "Place the official full runner at the repository root, or run it directly.\n"
        "The expected result gate is recorded in EXPECTED_RESULT.md."
    )


def main() -> None:
    runner = find_official_runner()
    print(f"[OFFICIAL_FROZEN_RUNNER] strategy={EXPECTED_STRATEGY}")
    print(f"[OFFICIAL_FROZEN_RUNNER] runner={runner}")
    print(f"[OFFICIAL_FROZEN_RUNNER] expected_trades={EXPECTED_TRADES}")
    print(f"[OFFICIAL_FROZEN_RUNNER] expected_official_cd_value={EXPECTED_OFFICIAL_CD_VALUE}")
    print(f"[OFFICIAL_FROZEN_RUNNER] expected_max_drawdown_pct={EXPECTED_MAX_DRAWDOWN_PCT}")
    print(f"[OFFICIAL_FROZEN_RUNNER] expected_profit_factor={EXPECTED_PROFIT_FACTOR}")
    sys.argv[0] = str(runner)
    runpy.run_path(str(runner), run_name="__main__")


if __name__ == "__main__":
    main()
