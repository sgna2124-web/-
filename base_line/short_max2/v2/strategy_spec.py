"""
short_max2 v2 strategy spec
strategy: smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1

This file records the exact promoted parameter set and reproduction gates.
The full promotion retest runner used to produce the official values was:
run_short_max2_v1_q4low_top1_stop250_rr500_retest_v1.py
"""

STRATEGY_NAME = "smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1"
AXIS = "short_max2"
BASELINE_VERSION = "v2"
PREVIOUS_BASELINE_VERSION = "v1"
SELECTION_POLICY = "Q4_LOW_WEIGHT_GENERAL_IMPROVEMENT"

ENGINE = "actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231"

DATA_POLICY = {
    "data_dir": "C:/Users/user/Desktop/LCD/파이썬/코인/Data/time",
    "train_end": "2025-12-31 23:59:59",
    "holdout_start": "2026-01-01 00:00:00",
    "pre_q4_end": "2025-09-30 23:59:59",
    "exclude_2026_before_indicator_calc": True,
    "fulltrain_csv_count": 597,
}

EXECUTION_ENV = {
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "leverage": 1.0,
    "fee_per_side": 0.0004,
    "round_trip_fee": 0.0008,
}

ENTRY_PARAMS = {
    "entry_family": "short_max2_v1_overheat_reversion",
    "side": "short",
    "short_dev": 0.032,
    "short_wick_mult": 1.30,
    "score_min_short": 2.35,
    "use_rsi_gate": False,
}

EXIT_RISK_PARAMS = {
    "atr_stop_mult": 2.50,
    "rr_mult": 5.00,
    "timeout_bars": 320,
    "time_reduce_bars": 3,
    "time_reduce_to_risk_frac": 0.00,
    "fail_fast_bars": 12,
    "dd_brake_trigger_pct": 0.035,
    "dd_brake_freeze_steps": 4,
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

FULLTRAIN_GATE = {
    "period": "full_train_to_2025_12_31",
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
    "period": "pre_q4_to_2025_09_30",
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
    "load_errors": 45,
}

V1_COMPARISON = {
    "pre_q4_delta_max_return_pct": 87.84523187756795,
    "pre_q4_delta_mdd_pct": -0.1004936676990419,
    "pre_q4_delta_official_cd_value": 89.5169710444647,
    "pre_q4_delta_profit_factor": 0.0311691291572657,
    "pre_q4_delta_avg_month_pnl": 1.237256787008306,
    "fulltrain_delta_max_return_pct": 685.635291072757,
    "fulltrain_delta_mdd_pct": -0.0034407283908688,
    "fulltrain_delta_official_cd_value": 670.5600864816588,
    "fulltrain_delta_profit_factor": 0.0464704879386053,
}

def official_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)

def selected_params() -> dict:
    return {
        **ENTRY_PARAMS,
        **EXIT_RISK_PARAMS,
        **EXECUTION_ENV,
    }

if __name__ == "__main__":
    print(STRATEGY_NAME)
    print(selected_params())
    print(FULLTRAIN_GATE)
    print(PRE_Q4_REFERENCE)
