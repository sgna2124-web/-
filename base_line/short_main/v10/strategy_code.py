"""
short_main v10 strategy constants

주의: 이 파일은 전략 조건/파라미터 정의용이다.
공식 재현은 frozen_reproduce_runner.py 또는 동일한 actual bar engine으로 해야 한다.
"""

STRATEGY = {
    "strategy": "smv8_mix2_02_prev_mix18_top2_top3_timereduce6",
    "retest_strategy": "smv8_mix2_02_prev_mix18_top2_top3_timereduce6__short_main_formula_top1_RETEST",
    "axis": "short_main",
    "baseline_version": "short_main/v10",
    "origin": "short_max v8 derived mix2 candidate",
    "selection_rule": "short_main formula, MDD under 5%, highest official_cd_value after retest",
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
    "score_dev_weight": 1.3,
    "score_rsi_weight": 0.8,
    "score_wick_weight": 0.7,
    "score_dev_cap": 2.0,
    "score_rsi_cap": 2.0,
    "score_wick_cap": 2.5,
    "wick_atr_floor_mult": 0.2,
    "atr_stop_mult": 2.0,
    "rr_mult": 5.5,
    "min_expected_tp": 0.003,
    "timeout_bars": 200,
    "time_reduce_bars": 6,
    "time_reduce_to_risk_frac": 0.05,
    "fail_fast_bars": 10,
    "fail_fast_min_progress_r": 0.1,
    "atr_pct_min": 0.0,
    "atr_pct_max": 999.0,
    "close_position_min": -999.0,
    "dd_brake_trigger_pct": 0.03,
    "dd_brake_freeze_steps": 5,
    "dd_brake_mode": "edge_current",
}

OFFICIAL_RESULT = {
    "trades": 50501,
    "wins": 6382,
    "losses": 44119,
    "win_rate_pct": 12.637373517356092,
    "final_return_pct": 1973.4390960274047,
    "max_return_pct": 1973.4472303933733,
    "max_drawdown_pct": 4.814092666588577,
    "official_cd_value": 1973.629559329422,
    "profit_factor": 1.5675065791005796,
    "max_conc": 302,
    "same_bar_trades": 3533,
    "active_leftover": 0,
    "pending_leftover": 0,
    "load_errors": 0,
}

PREVIOUS_SHORT_MAIN_V9 = {
    "strategy": "short_main_v9_wick120_dev03475_timeout215_actual_bar_engine",
    "trades": 36791,
    "max_drawdown_pct": 4.770262221769094,
    "official_cd_value": 1233.487844954492,
}


def short_score(close, ema20, rsi14, upper_wick, body, atr14, cfg=STRATEGY):
    import math
    raw_dev = max(0.0, close / max(ema20, 1e-12) - 1.0)
    raw_rsi = max(0.0, rsi14 - cfg["short_rsi_min"])
    dev_score = max(0.0, min(raw_dev / max(cfg["short_dev"], 1e-12), cfg["score_dev_cap"]))
    rsi_score = max(0.0, min(raw_rsi / 10.0, cfg["score_rsi_cap"]))
    floor = max(abs(body), atr14 * cfg["wick_atr_floor_mult"], 1e-12)
    wick_score = max(0.0, min(math.log1p(max(0.0, upper_wick / floor)), cfg["score_wick_cap"]))
    return cfg["score_dev_weight"] * dev_score + cfg["score_rsi_weight"] * rsi_score + cfg["score_wick_weight"] * wick_score


def entry_condition(open_, high, close, ema20, rsi14, atr14, next_open, cfg=STRATEGY):
    body = abs(close - open_)
    upper_wick = high - max(open_, close)
    sc = short_score(close, ema20, rsi14, upper_wick, body, atr14, cfg)
    dev_ok = close / max(ema20, 1e-12) - 1.0 >= cfg["short_dev"]
    wick_ok = upper_wick >= cfg["short_wick_mult"] * body
    score_ok = sc >= cfg["score_min_short"]
    entry = float(next_open)
    stop = entry + atr14 * cfg["atr_stop_mult"]
    target = entry - cfg["rr_mult"] * (stop - entry)
    expected_tp = (entry - target) / max(entry, 1e-12)
    tp_ok = expected_tp >= cfg["min_expected_tp"]
    return dev_ok and wick_ok and score_ok and tp_ok
