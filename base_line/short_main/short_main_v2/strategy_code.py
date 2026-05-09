"""
short_main baseline strategy code

Strategy: short_beh_dd_brake
Axis: short_main
Purpose: baseline strategy definition for future short_main development.

This file intentionally contains only the strategy-side logic and parameters.
It does not import any external runner, json config, or repository-specific path.
Use it as the source of truth when embedding the short_main baseline into a backtest script.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ShortMainBaselineConfig:
    name: str = "short_beh_dd_brake"
    axis: str = "short_main"
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

    short_dev: float = 0.033
    short_rsi_min: float = 77.0
    short_wick_mult: float = 1.3
    score_min_short: float = 2.2

    atr_stop_mult: float = 1.8975
    rr_mult: float = 6.0
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
    time_reduce_bars: int = 10
    time_reduce_to_risk_frac: float = 0.05
    fail_fast_bars: int = 10
    fail_fast_min_progress_r: float = 0.1

    dd_brake_trigger_pct: float = 0.03
    dd_brake_freeze_steps: int = 5

    cooldown_bars_same_symbol_same_side: int = 0

    current_597_trades: int = 28308
    current_597_max_return_pct: float = 322.7577232826396
    current_597_max_drawdown_pct: float = 4.4066222161057595
    current_597_official_cd_value: float = 404.12838752816384


def config_dict() -> Dict[str, Any]:
    return asdict(ShortMainBaselineConfig())


def add_indicators(df: pd.DataFrame, cfg: ShortMainBaselineConfig = ShortMainBaselineConfig()) -> pd.DataFrame:
    """Add EMA20, RSI14, ATR14, body, upper_wick, and baseline score columns."""
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


def short_main_entry_mask(df: pd.DataFrame, cfg: ShortMainBaselineConfig = ShortMainBaselineConfig()) -> pd.Series:
    """Return boolean mask for signal candles. Entry itself is next bar open."""
    required = {"open", "high", "low", "close", "ema20", "rsi14", "atr14", "body", "upper_wick", "short_score"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing indicator columns: {missing}")

    dev_ok = (df["close"] / df["ema20"] - 1.0) >= cfg.short_dev
    rsi_ok = df["rsi14"] > cfg.short_rsi_min
    wick_ok = df["upper_wick"] >= cfg.short_wick_mult * df["body"]
    score_ok = df["short_score"] >= cfg.score_min_short

    return dev_ok & rsi_ok & wick_ok & score_ok


def build_short_trade_from_signal(
    df: pd.DataFrame,
    signal_index: int,
    cfg: ShortMainBaselineConfig = ShortMainBaselineConfig(),
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

    if expected_tp < cfg.min_expected_tp:
        return None

    return {
        "strategy": cfg.name,
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
        "atr": atr,
        "rr_mult": cfg.rr_mult,
        "atr_stop_mult": cfg.atr_stop_mult,
    }


def apply_dd_brake_state(current_drawdown_pct: float, freeze_left: int, cfg: ShortMainBaselineConfig = ShortMainBaselineConfig()) -> int:
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


BASELINE_CONFIG = ShortMainBaselineConfig()
