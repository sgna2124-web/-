"""
short_max v5 baseline strategy code

Strategy: SM16_C05_remove_no_rsi_dev035
Short max record name: short_max_v5_SM16_C05_remove_no_rsi_dev035
Origin: promoted from short_main v4 because short_max criterion is official_cd_value rank #1.

Parent context:
    short_main parent: SM15_B10_rr575_tr8_f005
    previous short_max baseline: short_max_v4_combo_rsi755_timeout280

Purpose:
    Source-of-truth strategy definition for embedding short_max v5 baseline into
    future development backtest scripts.

Critical notes:
    - RSI direct gate is disabled.
    - RSI remains inside score calculation.
    - DD brake is portfolio-level, not per-symbol trade generation.
    - Entry is next bar open.
    - fee_per_side=0.0004 and position_fraction=0.01.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ShortMaxV5BaselineConfig:
    name: str = "SM16_C05_remove_no_rsi_dev035"
    short_max_record_name: str = "short_max_v5_SM16_C05_remove_no_rsi_dev035"
    parent_short_main: str = "SM15_B10_rr575_tr8_f005"
    previous_short_max: str = "short_max_v4_combo_rsi755_timeout280"
    axis: str = "short_max"
    side: str = "short"

    initial_asset: float = 100.0
    position_fraction: float = 0.01
    fee_per_side: float = 0.0004

    min_bars: int = 120
    entry_on_next_bar_open: bool = True
    allow_long: bool = False
    allow_short: bool = True

    ema_period: int = 20
    rsi_period: int = 14
    atr_period: int = 14

    short_dev: float = 0.035
    short_rsi_min: float = 77.0
    use_rsi_gate: bool = False
    short_wick_mult: float = 1.3
    score_min_short: float = 2.35

    atr_stop_mult: float = 1.8975
    rr_mult: float = 5.75
    min_expected_tp: float = 0.003
    timeout_bars: int = 200

    score_dev_weight: float = 1.0
    score_rsi_weight: float = 0.8
    score_wick_weight: float = 0.7
    score_dev_cap: float = 2.0
    score_rsi_cap: float = 2.0
    score_wick_cap: float = 2.5
    wick_atr_floor_mult: float = 0.2

    protect_mode: str = "time_reduce"
    time_reduce_bars: int = 8
    time_reduce_to_risk_frac: float = 0.05
    fail_fast_bars: int = 10
    fail_fast_min_progress_r: float = 0.1

    dd_brake_trigger_pct: float = 0.03
    dd_brake_freeze_steps: int = 5

    cooldown_bars_same_symbol_same_side: int = 0

    current_597_trades: int = 31798
    current_597_wins: int = 4638
    current_597_losses: int = 27160
    current_597_win_rate_pct: float = 14.585823007736334
    current_597_final_asset: float = 921.5165864710646
    current_597_final_return_pct: float = 821.5165864710646
    current_597_peak_asset: float = 921.9869251730971
    current_597_max_return_pct: float = 821.9869251730971
    current_597_max_drawdown_pct: float = 4.6783483625391975
    current_597_official_cd_value: float = 878.8531649564361
    current_597_pf: float = 1.5778442611030818
    current_597_max_conc: int = 275
    current_597_max_conc_unique_symbols: int = 275
    current_597_same_bar_trades: int = 4559
    current_597_active_leftover: int = 0
    current_597_raw_trades_generated: int = 61818
    current_597_errors: int = 0


def config_dict() -> Dict[str, Any]:
    return asdict(ShortMaxV5BaselineConfig())


def add_indicators(df: pd.DataFrame, cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig()) -> pd.DataFrame:
    """Add EMA20, RSI14, ATR14, body, upper_wick, and v5 score columns."""
    out = df.copy()

    for col in ["open", "high", "low", "close"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    close = out["close"]
    high = out["high"]
    low = out["low"]
    open_ = out["open"]

    out["ema20"] = close.ewm(span=cfg.ema_period, adjust=False).mean()

    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1.0 / cfg.rsi_period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / cfg.rsi_period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    out["rsi14"] = 100.0 - (100.0 / (1.0 + rs))

    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low).abs(),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    out["atr14"] = tr.ewm(alpha=1.0 / cfg.atr_period, adjust=False).mean()

    out["body"] = (close - open_).abs()
    out["upper_wick"] = high - pd.concat([open_, close], axis=1).max(axis=1)

    raw_dev = (close / out["ema20"] - 1.0).clip(lower=0.0)
    raw_rsi = (out["rsi14"] - cfg.short_rsi_min).clip(lower=0.0)

    dev_score = (raw_dev / cfg.short_dev).clip(lower=0.0, upper=cfg.score_dev_cap)
    rsi_score = (raw_rsi / 10.0).clip(lower=0.0, upper=cfg.score_rsi_cap)

    wick_floor = pd.concat(
        [
            out["body"].abs(),
            out["atr14"] * cfg.wick_atr_floor_mult,
            pd.Series(1e-12, index=out.index),
        ],
        axis=1,
    ).max(axis=1)
    wick_ratio = out["upper_wick"] / wick_floor
    wick_score = np.log1p(wick_ratio).clip(lower=0.0, upper=cfg.score_wick_cap)

    out["short_score"] = (
        cfg.score_dev_weight * dev_score
        + cfg.score_rsi_weight * rsi_score
        + cfg.score_wick_weight * wick_score
    )

    return out


def short_max_v5_entry_mask(df: pd.DataFrame, cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig()) -> pd.Series:
    """
    Return boolean mask for v5 signal candles. Entry itself is next bar open.

    v5 intentionally does not require rsi14 > 77 as a direct gate.
    RSI is still used inside short_score.
    """
    required = {"open", "high", "low", "close", "ema20", "rsi14", "atr14", "body", "upper_wick", "short_score"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing indicator columns: {missing}")

    dev_ok = (df["close"] / df["ema20"] - 1.0) >= cfg.short_dev
    if cfg.use_rsi_gate:
        rsi_ok = df["rsi14"] > cfg.short_rsi_min
    else:
        rsi_ok = pd.Series(True, index=df.index)
    wick_ok = df["upper_wick"] >= cfg.short_wick_mult * df["body"]
    score_ok = df["short_score"] >= cfg.score_min_short

    return dev_ok & rsi_ok & wick_ok & score_ok


def build_short_trade_from_signal(
    df: pd.DataFrame,
    signal_index: int,
    cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig(),
) -> Optional[Dict[str, Any]]:
    """Create a trade plan from one signal candle. Returns None if entry cannot be made."""
    entry_index = signal_index + 1
    if entry_index >= len(df):
        return None

    signal_row = df.iloc[signal_index]
    entry_row = df.iloc[entry_index]

    entry = float(entry_row["open"])
    atr = float(signal_row["atr14"])
    if not np.isfinite(entry) or not np.isfinite(atr) or entry <= 0.0 or atr <= 0.0:
        return None

    risk = atr * cfg.atr_stop_mult
    stop = entry + risk
    target = entry - cfg.rr_mult * risk
    expected_tp = (entry - target) / entry

    if stop <= entry:
        return None
    if target <= 0.0:
        return None
    if expected_tp < cfg.min_expected_tp:
        return None

    return {
        "strategy": cfg.name,
        "record_name": cfg.short_max_record_name,
        "axis": cfg.axis,
        "side": "short",
        "signal_index": int(signal_index),
        "entry_index": int(entry_index),
        "entry": entry,
        "risk": risk,
        "stop": stop,
        "target": target,
        "expected_tp": expected_tp,
        "score": float(signal_row["short_score"]),
        "rsi14": float(signal_row["rsi14"]),
        "atr": atr,
        "rr_mult": cfg.rr_mult,
        "atr_stop_mult": cfg.atr_stop_mult,
        "time_reduce_bars": cfg.time_reduce_bars,
        "time_reduce_to_risk_frac": cfg.time_reduce_to_risk_frac,
        "use_rsi_gate": cfg.use_rsi_gate,
    }


def trade_return_short(entry: float, exit_price: float, cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig()) -> float:
    """Net short return after round-trip fee."""
    return entry / max(exit_price, 1e-12) - 1.0 - 2.0 * cfg.fee_per_side


def apply_time_reduce_stop(
    entry: float,
    risk: float,
    current_stop: float,
    bars_held: int,
    mfe_r: float,
    cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig(),
) -> float:
    """Short-side time_reduce protection."""
    if bars_held >= cfg.time_reduce_bars and mfe_r > 0.0:
        reduced_stop = entry + risk * cfg.time_reduce_to_risk_frac
        return min(current_stop, reduced_stop)
    return current_stop


def exit_short_trade(
    entry_price: float,
    stop_price: float,
    target_price: float,
    risk_value: float,
    mfe_r: float,
    bars_since_entry: int,
    high: float,
    low: float,
    close: float,
    cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig(),
) -> tuple[Optional[float], Optional[str], float]:
    """Evaluate one candle after entry for a short position."""
    updated_stop = apply_time_reduce_stop(entry_price, risk_value, stop_price, bars_since_entry, mfe_r, cfg)

    if high >= updated_stop:
        return float(updated_stop), "stop", updated_stop
    if low <= target_price:
        return float(target_price), "target", updated_stop
    if bars_since_entry >= cfg.fail_fast_bars and mfe_r < cfg.fail_fast_min_progress_r and close > entry_price:
        return float(close), "fail_fast", updated_stop
    if bars_since_entry >= cfg.timeout_bars:
        return float(close), "timeout", updated_stop
    return None, None, updated_stop


def apply_dd_brake_state(current_drawdown_pct: float, freeze_left: int, cfg: ShortMaxV5BaselineConfig = ShortMaxV5BaselineConfig()) -> int:
    """
    Portfolio-level dd_brake helper.

    This does not belong to individual trade generation.
    When current drawdown is at or below -3%, freeze new entries for 5 timestamps.
    """
    if freeze_left > 0:
        return freeze_left - 1
    if current_drawdown_pct <= -100.0 * cfg.dd_brake_trigger_pct:
        return int(cfg.dd_brake_freeze_steps)
    return 0


BASELINE_CONFIG = ShortMaxV5BaselineConfig()
BASELINE_NOTES = {
    "strategy": BASELINE_CONFIG.name,
    "record_name": BASELINE_CONFIG.short_max_record_name,
    "axis": BASELINE_CONFIG.axis,
    "previous_short_max": BASELINE_CONFIG.previous_short_max,
    "reason_for_promotion": "short_max criterion is official_cd_value rank #1; this strategy exceeded previous short_max v4.",
    "official_597_result": {
        "trades": BASELINE_CONFIG.current_597_trades,
        "wins": BASELINE_CONFIG.current_597_wins,
        "losses": BASELINE_CONFIG.current_597_losses,
        "win_rate_pct": BASELINE_CONFIG.current_597_win_rate_pct,
        "final_return_pct": BASELINE_CONFIG.current_597_final_return_pct,
        "max_return_pct": BASELINE_CONFIG.current_597_max_return_pct,
        "max_drawdown_pct": BASELINE_CONFIG.current_597_max_drawdown_pct,
        "official_cd_value": BASELINE_CONFIG.current_597_official_cd_value,
        "pf": BASELINE_CONFIG.current_597_pf,
        "max_conc": BASELINE_CONFIG.current_597_max_conc,
        "same_bar_trades": BASELINE_CONFIG.current_597_same_bar_trades,
        "active_leftover": BASELINE_CONFIG.current_597_active_leftover,
        "raw_trades_generated": BASELINE_CONFIG.current_597_raw_trades_generated,
        "errors": BASELINE_CONFIG.current_597_errors,
    },
    "critical_rules": [
        "RSI direct gate is disabled.",
        "RSI remains inside short_score calculation.",
        "DD brake is portfolio-level, not per-symbol trade generation.",
        "Entry is next candle open.",
        "Same-bar trades must be closed immediately in the same timestamp.",
        "fee_per_side is 0.0004 and position_fraction is 0.01.",
        "expected_tp must be at least 0.003.",
    ],
}
