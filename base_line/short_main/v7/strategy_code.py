"""
short_main v7 strategy constants

주의: 이 파일은 전략 조건/파라미터 정의용이다.
공식 재현은 동일한 actual bar engine으로 해야 한다.
"""

STRATEGY = {
    "strategy": "short_main_v6_timeout210_actual_bar_engine",
    "axis": "short_main",
    "baseline_version": "short_main/v7",
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
    "short_dev": 0.035,
    "short_rsi_min": 77.0,
    "use_rsi_gate": False,
    "short_wick_mult": 1.3,
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
    "timeout_bars": 210,
    "time_reduce_bars": 8,
    "time_reduce_to_risk_frac": 0.05,
    "fail_fast_bars": 10,
    "fail_fast_min_progress_r": 0.1,
    "dd_brake_trigger_pct": 0.03,
    "dd_brake_freeze_steps": 5,
    "dd_brake_mode": "edge_current",
}

OFFICIAL_RESULT = {
    "trades": 35330,
    "wins": 4997,
    "losses": 30333,
    "win_rate_pct": 14.143787149731107,
    "final_return_pct": 1114.6701489565148,
    "max_return_pct": 1115.0033786152128,
    "max_drawdown_pct": 4.607649926423363,
    "official_cd_value": 1159.0202763344078,
    "profit_factor": 1.5743323511471792,
    "max_conc": 284,
    "same_bar_trades": 3187,
    "active_leftover": 0,
    "pending_leftover": 0,
    "load_errors": 0,
}
