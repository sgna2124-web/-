"""
short_main2 v1 strategy core specification

Official baseline:
- strategy: SM52_B04_stop230_score270_single_retest
- source strategy: SM50_B04_stop230_score270
- official_cd_value: 50591.202383140204
- max_drawdown_pct: 5.923149464550481
- source result: local_results/short_main/SHORT_MAIN_V15_B04_SINGLE_RETEST_V5_2_ENVLOCKED/summary_compact.csv

This file is a compact strategy specification, not a full backtest runner.
Use short_main_v15_B04_single_retest_v5_2_envlocked.py as the official executable runner.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ShortMain2V1Config:
    entry_mode: str = "climax_exhaustion"
    precompute_signals: bool = True

    short_dev: float = 0.025
    ret12_min: float = 0.030
    ret3_min: float = 0.004
    volume_spike_min: float = 0.75
    upper_range_ratio_min: float = 0.16
    close_position_max: float = 0.94
    green_streak_min: int = 0
    ema20_slope12_min: float = -0.025
    ema20_slope12_max: float = 0.095
    atr_pct_min: float = 0.0008
    atr_pct_max: float = 0.135
    range_spike_min: float = 0.0
    dist_roll_high20_min: float = -0.08
    climax_score_min: float = 2.7

    climax_dev_weight: float = 1.05
    climax_ret_weight: float = 0.75
    climax_vol_weight: float = 0.15
    climax_wick_weight: float = 0.55
    climax_streak_weight: float = 0.10
    ret12_ref: float = 0.070
    volume_spike_ref: float = 2.0
    upper_range_ratio_ref: float = 0.38

    atr_stop_mult: float = 2.30
    rr_mult: float = 6.20
    time_reduce_bars: int = 3
    time_reduce_to_risk_frac: float = 0.00
    fail_fast_bars: int = 12
    fail_fast_min_progress_r: float = 0.1
    timeout_bars: int = 285
    dd_brake_trigger_pct: float = 0.075
    dd_brake_freeze_steps: int = 3

    initial_asset: float = 100.0
    position_fraction: float = 0.01
    leverage: float = 1.0
    fee_per_side: float = 0.0004


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def climax_score(features: Dict[str, float], cfg: ShortMain2V1Config = ShortMain2V1Config()) -> float:
    dev = features["close"] / features["ema20"] - 1.0
    ret12 = features["ret12"]
    volume_spike = features["volume_spike"]
    upper_range_ratio = features["upper_range_ratio"]
    green_streak = features.get("green_streak", 0.0)

    dev_component = clamp(dev / cfg.short_dev, 0.0, 2.0)
    ret_component = clamp(ret12 / cfg.ret12_ref, 0.0, 2.5)
    volume_component = clamp(volume_spike / cfg.volume_spike_ref, 0.0, 2.0)
    wick_component = clamp(upper_range_ratio / cfg.upper_range_ratio_ref, 0.0, 2.5)
    streak_component = clamp(green_streak / 4.0, 0.0, 1.5)

    return (
        cfg.climax_dev_weight * dev_component
        + cfg.climax_ret_weight * ret_component
        + cfg.climax_vol_weight * volume_component
        + cfg.climax_wick_weight * wick_component
        + cfg.climax_streak_weight * streak_component
    )


def should_enter_short(features: Dict[str, float], cfg: ShortMain2V1Config = ShortMain2V1Config()) -> bool:
    if features["close"] / features["ema20"] - 1.0 < cfg.short_dev:
        return False
    if features["ret12"] < cfg.ret12_min:
        return False
    if features["ret3"] < cfg.ret3_min:
        return False
    if features["volume_spike"] < cfg.volume_spike_min:
        return False
    if features["upper_range_ratio"] < cfg.upper_range_ratio_min:
        return False
    if features["close_position"] > cfg.close_position_max:
        return False
    if features.get("green_streak", 0) < cfg.green_streak_min:
        return False
    if features["ema20_slope12"] < cfg.ema20_slope12_min:
        return False
    if features["ema20_slope12"] > cfg.ema20_slope12_max:
        return False
    if features["atr_pct"] < cfg.atr_pct_min:
        return False
    if features["atr_pct"] > cfg.atr_pct_max:
        return False
    if features.get("range_spike", 0.0) < cfg.range_spike_min:
        return False
    if features["dist_roll_high20"] < cfg.dist_roll_high20_min:
        return False
    if climax_score(features, cfg) < cfg.climax_score_min:
        return False
    return True


def make_exit_levels(entry_price: float, atr14: float, cfg: ShortMain2V1Config = ShortMain2V1Config()) -> Dict[str, float]:
    risk = atr14 * cfg.atr_stop_mult
    return {
        "risk": risk,
        "stop": entry_price + risk,
        "target": entry_price - cfg.rr_mult * risk,
    }


OFFICIAL_RESULT = {
    "strategy": "SM52_B04_stop230_score270_single_retest",
    "trades": 154015,
    "wins": 11824,
    "losses": 142191,
    "max_return_pct": 53676.46264218497,
    "max_drawdown_pct": 5.923149464550481,
    "official_cd_value": 50591.202383140204,
    "profit_factor": 1.7648350795085153,
    "generated_signals": 267412,
    "executed_entries": 154015,
    "blocked_entries": 0,
    "same_bar_trades": 9995,
    "max_conc": 364,
    "active_leftover": 0,
    "pending_leftover": 0,
}
