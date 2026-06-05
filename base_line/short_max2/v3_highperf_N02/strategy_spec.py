from __future__ import annotations

STRATEGY_NAME = "SMX2V2_C08_EX20_02_N02_stop257_rr5075"
AXIS = "short_max2"
BRANCH = "v3_highperf_N02"
ENGINE_NAME = "actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231_FAST_SIGNAL_PRECOMPUTE_CHUNKED_MEMSAFE"

PARAMS = {
    "short_dev": 0.032,
    "short_rsi_min": 76.0,
    "short_wick_mult": 1.30,
    "score_min_short": 2.35,
    "score_dev_weight": 1.30,
    "score_rsi_weight": 0.80,
    "score_wick_weight": 0.70,
    "score_dev_cap": 2.0,
    "score_rsi_cap": 2.0,
    "score_wick_cap": 2.5,
    "atr_stop_mult": 2.57,
    "rr_mult": 5.075,
    "timeout_bars": 320,
    "time_reduce_bars": 3,
    "time_reduce_to_risk_frac": 0.0,
    "fail_fast_bars": 12,
    "fail_fast_min_progress_r": 0.10,
    "dd_brake_trigger_pct": 0.035,
    "dd_brake_freeze_steps": 4,
    "atr_pct_min": 0.0,
    "atr_pct_max": 999.0,
    "close_position_min": -999.0,
    "close_position_max": 999.0,
    "upper_body_ratio_min": 0.0,
    "upper_body_ratio_max": 999.0,
    "range20_pct_max": 999.0,
    "ret3_ceil": 999.0,
    "ret5_ceil": 999.0,
    "ret10_ceil": 999.0,
    "ret20_ceil": 999.0,
    "require_upper_sweep": False,
    "require_ema_reject": False,
}

RUN_CONFIG = {
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "fee_per_side": 0.0004,
    "csv_files": 597,
    "preq4_end": "2025-09-30 23:59:59",
    "full_2025_end": "2025-12-31 23:59:59",
    "all_end": "2026-12-31 23:59:59",
    "recommended_workers": 4,
    "recommended_period_workers": 1,
}

FROZEN_GATE_2025 = {
    "preq4": {
        "trades": 88892,
        "final_return_pct": 5636.697084804827,
        "max_drawdown_pct": 5.655961392725716,
        "official_cd_value": 5412.231712470644,
        "profit_factor": 1.9410396856986845,
    },
    "full2025": {
        "trades": 104753,
        "final_return_pct": 19461.28974837902,
        "max_drawdown_pct": 5.655961392725716,
        "official_cd_value": 18454.91075229149,
        "profit_factor": 2.0040638913290496,
    },
}

ALL_THROUGH_2026 = {
    "trades": 106337,
    "final_return_pct": 20964.787242703645,
    "max_drawdown_pct": 5.655961392725716,
    "official_cd_value": 19873.371008796516,
    "profit_factor": 2.0010696725618833,
}

YEAR_SUMMARY = {
    "2023": {"trades": 11172, "final_return_pct": 58.13785276936261, "max_drawdown_pct": 1.9196538272639008, "official_cd_value": 155.1021534263226, "profit_factor": 1.8189380113743816},
    "2024": {"trades": 21615, "final_return_pct": 134.59296305171026, "max_drawdown_pct": 1.822985917841291, "official_cd_value": 230.31636637103094, "profit_factor": 1.9135547532977255},
    "2025": {"trades": 43771, "final_return_pct": 1529.7313609927087, "max_drawdown_pct": 5.655961392725628, "official_cd_value": 1537.5543844098192, "profit_factor": 2.098346033746182},
    "2026": {"trades": 1483, "final_return_pct": 7.8345965695261865, "max_drawdown_pct": 1.1085064239765963, "official_cd_value": 106.63924313928375, "profit_factor": 2.024525285956021},
}

ACCEPTANCE_RULE = "retest_gate_2025.json must have gate_ok=true and gate_misses=[]"
