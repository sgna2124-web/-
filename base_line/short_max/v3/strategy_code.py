from __future__ import annotations

"""
short_max v3 baseline strategy code

Official baseline:
    short_max_v3_combo_dev033_timeout240

Origin:
    Promoted from short_max v2 development result `combo_dev033_timeout240`.

Core change from short_max v2:
    short_dev: 0.032 -> 0.033
    timeout_bars: 200 -> 240

Important engine rule:
    score_min_short is applied at portfolio evaluation stage, not inside the per-symbol
    entry mask. Same-bar trades must be closed immediately after entry in the same
    timestamp.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ShortMaxV3Config:
    name: str = "short_max_v3_combo_dev033_timeout240"
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

    short_dev: float = 0.033
    short_rsi_min: float = 76.0
    short_wick_mult: float = 1.3
    score_min_short: float = 2.0

    atr_stop_mult: float = 1.8975
    rr_mult: float = 6.0
    min_expected_tp: float = 0.003
    timeout_bars: int = 240

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

    cooldown_bars_same_symbol_same_side: int = 0

    current_597_trades: int = 34782
    current_597_final_return_pct: float = 451.45526435735064
    current_597_max_return_pct: float = 451.8246548170149
    current_597_max_drawdown_pct: float = 7.484506060174601
    current_597_official_cd_value: float = 510.52330508569787
    current_597_win_rate_pct: float = 14.070496233684091
    current_597_profit_factor: float = 1.4377856344586135
    current_597_max_conc: int = 292
    current_597_max_conc_unique_symbols: int = 292
    current_597_same_bar_trades: int = 3585
    current_597_active_leftover: int = 0


DEFAULT_CONFIG = ShortMaxV3Config()


def config_dict(cfg: ShortMaxV3Config = DEFAULT_CONFIG) -> Dict[str, Any]:
    return asdict(cfg)


def add_indicators(df: pd.DataFrame, cfg: ShortMaxV3Config = DEFAULT_CONFIG) -> pd.DataFrame:
    """Add indicators required by short_max v3.

    Input columns required:
        date, open, high, low, close, volume
    """
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
    out["rsi14"] = out["rsi14"].fillna(50.0)

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


def short_signal_mask(df: pd.DataFrame, cfg: ShortMaxV3Config = DEFAULT_CONFIG) -> pd.Series:
    """Per-symbol short signal mask.

    This mask intentionally does not include `short_score >= score_min_short`.
    The official strict time-axis engine applies score_min_short during portfolio
    timestamp evaluation. Moving score filtering into this mask can change per-symbol
    occupancy order and break baseline reproduction.
    """
    required = {"open", "high", "low", "close", "ema20", "rsi14", "atr14", "body", "upper_wick", "short_score"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing indicator columns: {missing}")

    dev_ok = (df["close"] / df["ema20"] - 1.0) >= cfg.short_dev
    rsi_ok = df["rsi14"] > cfg.short_rsi_min
    wick_ok = df["upper_wick"] >= cfg.short_wick_mult * df["body"]

    return dev_ok & rsi_ok & wick_ok


def build_short_trade_from_signal(
    df: pd.DataFrame,
    signal_index: int,
    cfg: ShortMaxV3Config = DEFAULT_CONFIG,
) -> Optional[Dict[str, Any]]:
    """Create a short trade plan from one signal candle.

    Entry is next bar open.
    TP expectation must be at least 0.3%.
    """
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
        "timeout_bars": cfg.timeout_bars,
    }


def should_select_trade_at_portfolio_stage(trade: Dict[str, Any], cfg: ShortMaxV3Config = DEFAULT_CONFIG) -> bool:
    """Official portfolio-stage score filter."""
    return float(trade.get("score", 0.0)) >= cfg.score_min_short


def trade_return_short(entry: float, exit_price: float, cfg: ShortMaxV3Config = DEFAULT_CONFIG) -> float:
    """Net short return after round-trip fee."""
    return entry / max(exit_price, 1e-12) - 1.0 - 2.0 * cfg.fee_per_side


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
    cfg: ShortMaxV3Config = DEFAULT_CONFIG,
) -> tuple[Optional[float], Optional[str], float]:
    """Evaluate one candle after entry for a short position.

    Return:
        exit_price, exit_reason, updated_stop_price
    """
    updated_stop = stop_price

    if bars_since_entry >= cfg.time_reduce_bars and mfe_r > 0:
        updated_stop = min(updated_stop, entry_price + risk_value * cfg.time_reduce_to_risk_frac)

    if high >= updated_stop:
        return float(updated_stop), "stop", updated_stop
    if low <= target_price:
        return float(target_price), "target", updated_stop
    if bars_since_entry >= cfg.fail_fast_bars and mfe_r < cfg.fail_fast_min_progress_r and close > entry_price:
        return float(close), "fail_fast", updated_stop
    if bars_since_entry >= cfg.timeout_bars:
        return float(close), "timeout", updated_stop

    return None, None, updated_stop


BASELINE_NOTES = {
    "strategy": DEFAULT_CONFIG.name,
    "v2_parent": "short_only_reference_1x",
    "promotion_source": "local_results/short_max/short_max_v2_dev_strict_time_axis_v5_results/improved_candidates.csv",
    "selected_candidate": "combo_dev033_timeout240",
    "core_change": {
        "short_dev": "0.032 -> 0.033",
        "timeout_bars": "200 -> 240",
    },
    "official_597_result": {
        "trades": DEFAULT_CONFIG.current_597_trades,
        "final_return_pct": DEFAULT_CONFIG.current_597_final_return_pct,
        "max_return_pct": DEFAULT_CONFIG.current_597_max_return_pct,
        "max_drawdown_pct": DEFAULT_CONFIG.current_597_max_drawdown_pct,
        "official_cd_value": DEFAULT_CONFIG.current_597_official_cd_value,
        "profit_factor": DEFAULT_CONFIG.current_597_profit_factor,
        "max_conc": DEFAULT_CONFIG.current_597_max_conc,
        "same_bar_trades": DEFAULT_CONFIG.current_597_same_bar_trades,
        "active_leftover": DEFAULT_CONFIG.current_597_active_leftover,
    },
    "critical_rules": [
        "score_min_short is applied at portfolio evaluation stage, not inside short_signal_mask.",
        "entry is next candle open.",
        "same-bar trades must be closed immediately in the same timestamp.",
        "fee_per_side is 0.0004 and position_fraction is 0.01.",
        "expected_tp must be at least 0.003.",
    ],
}
