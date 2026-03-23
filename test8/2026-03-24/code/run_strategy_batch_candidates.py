from __future__ import annotations

import json
from pathlib import Path

CANDIDATES = [
    "squeeze_breakout",
    "insidebar_trend",
    "base_breakout",
    "retest_breakout",
    "pullback_trend",
]


OUTPUT_SCHEMA = {
    "strategy": "string",
    "trades": "int",
    "final_asset": "float",
    "final_return": "float",
    "peak_asset": "float",
    "peak_growth": "float",
    "win_rate": "float",
    "pf": "float",
    "mdd": "float",
    "max_conc": "int",
}


def main() -> None:
    payload = {
        "status": "runner_template_only",
        "benchmark_to_compare": "overextension_reversion_v1",
        "candidates": CANDIDATES,
        "output_schema": OUTPUT_SCHEMA,
        "note": "Implement each candidate with the same evaluator and save aggregate/per_symbol/trades outputs.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
