from __future__ import annotations

r"""
short_max2 v2 frozen reproduce runner

strategy:
smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1

source retest file:
run_short_max2_v1_q4low_top1_stop250_rr500_retest_v1.py

purpose:
- Reproduce short_max2/v2 baseline without external config.
- Use actual-bar trading rules.
- Use train data only through 2025-12-31 23:59:59.
- Keep 2026+ as holdout and exclude it before indicator calculation.

Run:
python base_line/short_max2/v2/frozen_reproduce_runner.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time"

If memory is tight:
python base_line/short_max2/v2/frozen_reproduce_runner.py --data-dir "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time" --signal-chunk-size 5000

Official full-train gate:
trades 65180
max_return_pct 15588.585271121465
max_drawdown_pct 2.274010039088681
official_cd_value 15331.825267065175
profit_factor 2.6142284817799504
load_errors 0

NOTE:
This wrapper intentionally embeds the promoted baseline metadata and points to the source retest runner.
For complete executable logic, keep this file together with the source runner used in the promotion retest.
"""

import argparse
import json
from pathlib import Path

STRATEGY_NAME = "smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1"
AXIS = "short_max2"
BASELINE_VERSION = "v2"
SOURCE_RETEST_FILE = "run_short_max2_v1_q4low_top1_stop250_rr500_retest_v1.py"

PARAMS = {
    "short_dev": 0.032,
    "short_wick_mult": 1.30,
    "score_min_short": 2.35,
    "atr_stop_mult": 2.50,
    "rr_mult": 5.00,
    "timeout_bars": 320,
    "time_reduce_bars": 3,
    "time_reduce_to_risk_frac": 0.00,
    "fail_fast_bars": 12,
    "dd_brake_trigger_pct": 0.035,
    "dd_brake_freeze_steps": 4,
}

ENV = {
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "leverage": 1.0,
    "fee_per_side": 0.0004,
    "round_trip_fee": 0.0008,
    "train_end": "2025-12-31 23:59:59",
    "holdout_start": "2026-01-01 00:00:00",
    "pre_q4_end": "2025-09-30 23:59:59",
    "exclude_2026_before_indicator_calc": True,
    "engine": "actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231",
}

FULLTRAIN_GATE = {
    "trades": 65180,
    "wins": 5130,
    "losses": 60050,
    "win_rate_pct": 7.8705124271248845,
    "max_return_pct": 15588.585271121465,
    "max_drawdown_pct": 2.274010039088681,
    "official_cd_value": 15331.825267065175,
    "profit_factor": 2.6142284817799504,
    "positive_month_ratio_pct": 93.24324324324324,
    "q4_share_of_full_return_pct": 77.19914436251436,
    "top3_month_share_pct": 77.40116227608569,
    "load_errors": 0,
    "active_leftover": 0,
    "pending_leftover": 0,
}

PRE_Q4_REFERENCE = {
    "trades": 53580,
    "wins": 4156,
    "losses": 49424,
    "win_rate_pct": 7.7566256065696155,
    "max_return_pct": 3554.3308235947543,
    "max_drawdown_pct": 2.1769570997805077,
    "official_cd_value": 3574.7776092810404,
    "profit_factor": 2.29014107209504,
    "positive_month_ratio_pct": 92.95774647887323,
    "avg_month_pnl": 50.0609975154197,
    "positive_year_ratio_pct": 100.0,
}

ENGINE_RULES = [
    "t open uses only pending entries confirmed at t-1 close",
    "exit inside t candle affects equity and free slots from t+1 open",
    "new signals made at t close become t+1 open candidates",
    "same timestamp exit-to-entry reuse is forbidden",
    "same-bar TP/SL is allowed",
    "when stop and target both touch inside one bar, stop wins",
    "DD brake edge made after t candle exit is applied from t+1",
    "active positions at test end are force-closed at final close",
]


def official_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--signal-chunk-size", type=int, default=10000)
    parser.add_argument("--print-only", action="store_true", help="Print fixed baseline metadata and gate values.")
    args = parser.parse_args()

    payload = {
        "strategy": STRATEGY_NAME,
        "axis": AXIS,
        "baseline_version": BASELINE_VERSION,
        "source_retest_file": SOURCE_RETEST_FILE,
        "data_dir": str(Path(args.data_dir)),
        "signal_chunk_size": args.signal_chunk_size,
        "params": PARAMS,
        "env": ENV,
        "engine_rules": ENGINE_RULES,
        "fulltrain_gate": FULLTRAIN_GATE,
        "pre_q4_reference": PRE_Q4_REFERENCE,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.print_only:
        return

    raise SystemExit(
        "This metadata wrapper records the frozen short_max2/v2 baseline. "
        "Run the full source retest file listed in source_retest_file to reproduce the engine output exactly."
    )


if __name__ == "__main__":
    main()
