#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict

EXPECTED = {
    "preq4_trades": 88892,
    "preq4_final_return_pct": 5636.697084804827,
    "preq4_max_drawdown_pct": 5.655961392725716,
    "preq4_official_cd_value": 5412.231712470644,
    "preq4_profit_factor": 1.9410396856986845,
    "full2025_trades": 104753,
    "full2025_final_return_pct": 19461.28974837902,
    "full2025_max_drawdown_pct": 5.655961392725716,
    "full2025_official_cd_value": 18454.91075229149,
    "full2025_profit_factor": 2.0040638913290496,
    "all_trades": 106337,
    "all_final_return_pct": 20964.787242703645,
    "all_max_drawdown_pct": 5.655961392725716,
    "all_official_cd_value": 19873.371008796516,
    "all_profit_factor": 2.0010696725618833,
}

EXPECTED_PERIOD_CD = {
    "2023_FULL_ONLY": 155.1021534263226,
    "2024_FULL_ONLY": 230.31636637103094,
    "2025_FULL_ONLY": 1537.5543844098192,
    "2026_FULL_ONLY": 106.63924313928375,
}


def as_float(x: Any) -> float:
    return float(x)


def check_close(name: str, got: Any, expected: Any, tol: float) -> None:
    g = float(got)
    e = float(expected)
    if abs(g - e) > tol:
        raise AssertionError(f"{name}: got={g}, expected={e}, diff={g - e}")


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result-dir", default="local_results/short_max/short_max2_v2_N02_stop257_rr5075_solo_retest_2023_2026_periods_1h_v2_MEMSAFE_FIXED3_results")
    ap.add_argument("--float-tol", type=float, default=1e-6)
    args = ap.parse_args()

    result_dir = Path(args.result_dir).expanduser().resolve()
    gate_path = result_dir / "retest_gate_2025.json"
    period_path = result_dir / "period_summary.csv"

    if not gate_path.exists():
        raise FileNotFoundError(gate_path)
    if not period_path.exists():
        raise FileNotFoundError(period_path)

    gate = load_json(gate_path)
    if gate.get("gate_ok") is not True:
        raise AssertionError(f"gate_ok is not true: {gate.get('gate_ok')}")
    if gate.get("gate_misses") != []:
        raise AssertionError(f"gate_misses not empty: {gate.get('gate_misses')}")

    pre = gate["got_preq4"]
    full = gate["got_full2025"]
    allr = gate["got_all_through_2026"]

    check_close("preq4_trades", pre["trades"], EXPECTED["preq4_trades"], 0)
    check_close("preq4_final_return_pct", pre["final_return_pct"], EXPECTED["preq4_final_return_pct"], args.float_tol)
    check_close("preq4_max_drawdown_pct", pre["max_drawdown_pct"], EXPECTED["preq4_max_drawdown_pct"], args.float_tol)
    check_close("preq4_official_cd_value", pre["official_cd_value"], EXPECTED["preq4_official_cd_value"], args.float_tol)
    check_close("preq4_profit_factor", pre["profit_factor"], EXPECTED["preq4_profit_factor"], args.float_tol)

    check_close("full2025_trades", full["trades"], EXPECTED["full2025_trades"], 0)
    check_close("full2025_final_return_pct", full["final_return_pct"], EXPECTED["full2025_final_return_pct"], args.float_tol)
    check_close("full2025_max_drawdown_pct", full["max_drawdown_pct"], EXPECTED["full2025_max_drawdown_pct"], args.float_tol)
    check_close("full2025_official_cd_value", full["official_cd_value"], EXPECTED["full2025_official_cd_value"], args.float_tol)
    check_close("full2025_profit_factor", full["profit_factor"], EXPECTED["full2025_profit_factor"], args.float_tol)

    check_close("all_trades", allr["trades"], EXPECTED["all_trades"], 0)
    check_close("all_final_return_pct", allr["final_return_pct"], EXPECTED["all_final_return_pct"], args.float_tol)
    check_close("all_max_drawdown_pct", allr["max_drawdown_pct"], EXPECTED["all_max_drawdown_pct"], args.float_tol)
    check_close("all_official_cd_value", allr["official_cd_value"], EXPECTED["all_official_cd_value"], args.float_tol)
    check_close("all_profit_factor", allr["profit_factor"], EXPECTED["all_profit_factor"], args.float_tol)

    periods: Dict[str, Dict[str, str]] = {}
    with period_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            periods[row["period"]] = row

    for period, expected_cd in EXPECTED_PERIOD_CD.items():
        if period not in periods:
            raise AssertionError(f"missing period: {period}")
        check_close(f"{period}.official_cd_value", periods[period]["official_cd_value"], expected_cd, args.float_tol)

    print("[OK] short_max2 v3_highperf_N02 frozen result verification passed")
    print(f"[RESULT_DIR] {result_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
