"""
short_main2 v2 strategy core specification

Official baseline:
- strategy: SM60_C03_stop240_score270_timeout315
- candidate_key: C03_stop240_score270_timeout315
- previous baseline: short_main2/v1 SM52_B04_stop230_score270_single_retest
- official_cd_value: 69498.03075622236
- max_drawdown_pct: 5.888592725709996
- mtm_close_max_drawdown_pct: 15.017466599306728
- mtm_worstbar_max_drawdown_pct: 14.23277215250176
- source result: local_results/short_main/SHORT_MAIN2_V2_C03_SINGLE_RETEST_V1_3_ENVLOCKED/single_retest_summary_compact.csv

This file is a compact strategy specification, not a full backtest runner.
Use short_main2_v2_C03_single_retest_v1_3_envlocked.py as the official executable runner.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ShortMain2V2Config:
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

    atr_stop_mult: float = 2.40
    rr_mult: float = 6.20
    time_reduce_bars: int = 3
    time_reduce_to_risk_frac: float = 0.00
    fail_fast_bars: int = 12
    fail_fast_min_progress_r: float = 0.1
    timeout_bars: int = 315
    dd_brake_trigger_pct: float = 0.080
    dd_brake_freeze_steps: int = 3

    initial_asset: float = 100.0
    position_fraction: float = 0.01
    leverage: float = 1.0
    fee_per_side: float = 0.0004


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def climax_score(features: Dict[str, float], cfg: ShortMain2V2Config = ShortMain2V2Config()) -> float:
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


def should_enter_short(features: Dict[str, float], cfg: ShortMain2V2Config = ShortMain2V2Config()) -> bool:
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


def make_exit_levels(entry_price: float, atr14: float, cfg: ShortMain2V2Config = ShortMain2V2Config()) -> Dict[str, float]:
    risk = atr14 * cfg.atr_stop_mult
    return {
        "risk": risk,
        "stop": entry_price + risk,
        "target": entry_price - cfg.rr_mult * risk,
    }


OFFICIAL_RESULT = {
    "strategy": "SM60_C03_stop240_score270_timeout315",
    "trades": 152030,
    "wins": 11364,
    "losses": 140666,
    "win_rate_pct": 7.4748404920081555,
    "max_return_pct": 73746.55353592646,
    "max_drawdown_pct": 5.888592725709996,
    "official_cd_value": 69498.03075622236,
    "profit_factor": 1.8286053579584032,
    "mtm_close_max_drawdown_pct": 15.017466599306728,
    "mtm_worstbar_max_drawdown_pct": 14.23277215250176,
    "mtm_worstbar_cd_value": 63347.67993125091,
    "generated_signals": 267412,
    "executed_entries": 152030,
    "blocked_entries": 0,
    "same_bar_trades": 8883,
    "max_conc": 364,
    "max_conc_unique_symbols": 364,
    "active_leftover": 0,
    "pending_leftover": 0,
}

Q4_REALISM_CHECK = {
    "q4_dependency_flag": "GENERAL_EDGE_CONFIRMED",
    "full_train_official_cd_value": 69498.03075622236,
    "excl_2025_q4_official_cd_value": 16979.64262769056,
    "q4_only_official_cd_value": 390.894405739309,
    "exq4_to_full_cd_ratio": 0.24431832733865372,
    "q4_to_full_cd_ratio": 0.005624539306882607,
    "slip005_full_official_cd_value": 15177.194065003236,
    "slip005_excl_2025_q4_official_cd_value": 4617.4606705665265,
    "slip005_q4_only_official_cd_value": 310.33515316809167,
}
