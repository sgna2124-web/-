from __future__ import annotations

from pathlib import Path

import run_backtest_batch_json_only_short_strict as base

ROOT = Path(__file__).resolve().parents[1]
base.BASE_CONFIG_PATH = ROOT / "experiments" / "base_config_json_only_long_strict_mdd.json"
base.SINGLE_CHANGES_PATH = ROOT / "experiments" / "single_changes_json_only_long_strict_mdd.json"

if __name__ == "__main__":
    base.main()
