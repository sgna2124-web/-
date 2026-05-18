"""
short_main v9 strategy constants

주의:
- 이 파일은 전략 조건/파라미터 정의용이다.
- 공식 재현은 동일한 actual bar engine으로 해야 한다.
- 재현용 코드는 frozen_reproduce_runner.py를 사용한다.
"""

STRATEGY = {
    "strategy": "short_main_v9_wick120_dev03475_timeout215_actual_bar_engine",
    "axis": "short_main",
    "baseline_version": "short_main/v9",
    "source_candidate": "SM23_D02_wick120_dev03475_timeout215",
    "parent_strategy": "short_main_v8_wick125_actual_bar_engine",
    "previous_baseline": "short_main/v8",
    "engine": "actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231",
    "data_scope": "train_only_until_2025_12_31_end",
    "train_end": "2025-12-31 23:59:59",
    "holdout_start": "2026-01-01 00:00:00",
    "initial_asset": 100.0,
    "position_fraction": 0.01,
    "fee_per_side": 0.0004,
    "min_bars": 120,
    "ema_period": 20,
    "rsi_period": 14,
    "atr_period": 14,
    "short_dev": 0.03475,
    "short_rsi_min": 77.0,
    "use_rsi_gate": False,
    "short_wick_mult": 1.20,
    "score_min_short": 2.35,
    "score_dev_weight": 1.0,
    "score_rsi_weight": 0.8,
    "score_wick_weight": 0.7,
    "score_dev_cap": 2.0,
    "score_rsi_cap": 2.0,
    "score_wick_cap": 2.5,
    "wick_atr_floor_mult": 0.2,
    "atr_stop_mult": 1.8975,
    "rr_mult": 5.75,
    "min_expected_tp": 0.003,
    "timeout_bars": 215,
    "time_reduce_bars": 8,
    "time_reduce_to_risk_frac": 0.05,
    "fail_fast_bars": 10,
    "fail_fast_min_progress_r": 0.1,
    "dd_brake_trigger_pct": 0.03,
    "dd_brake_freeze_steps": 5,
    "dd_brake_mode": "edge_current",
}

OFFICIAL_RESULT = {
    "trades": 36791,
    "wins": 5171,
    "losses": 31620,
    "win_rate_pct": 14.055067815498356,
    "final_asset": 1294.9206565723089,
    "final_return_pct": 1194.9206565723089,
    "peak_asset": 1295.2759019740386,
    "max_return_pct": 1195.2759019740386,
    "max_drawdown_pct": 4.770262221769094,
    "official_cd_value": 1233.487844954492,
    "profit_factor": 1.5698636647889879,
    "max_conc": 287,
    "max_conc_unique_symbols": 287,
    "same_bar_trades": 3354,
    "active_leftover": 0,
    "pending_leftover": 0,
    "blocked_by_guard": 56,
    "generated_entry_candidates": 36847,
    "executed_entries": 36791,
    "load_errors": 0,
}

PARENT_RESULT = {
    "strategy": "short_main_v8_wick125_actual_bar_engine",
    "baseline_version": "short_main/v8",
    "trades": 35803,
    "wins": 5070,
    "losses": 30733,
    "max_return_pct": 1156.1081244457819,
    "max_drawdown_pct": 4.612307655489422,
    "official_cd_value": 1198.1725532607445,
    "profit_factor": 1.5763819188582828,
    "max_conc": 285,
    "same_bar_trades": 3246,
}

DELTA_VS_PARENT = {
    "delta_trades": 988,
    "delta_max_return_pct": 39.16777752825669,
    "delta_max_drawdown_pct": 0.1579545662796722,
    "delta_official_cd_value": 35.31529169374744,
    "delta_same_bar_trades": 108,
    "delta_max_conc": 2,
}

REPRODUCTION_REQUIRED = {
    "csv_files": 597,
    "loaded_symbols": 597,
    "train_end": "2025-12-31 23:59:59",
    "holdout_start": "2026-01-01 00:00:00",
    "exclude_holdout_before_indicator_calculation": True,
    "actual_bar_engine": True,
    "same_timestamp_reentry": False,
    "force_final_close": True,
}
