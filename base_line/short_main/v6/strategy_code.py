from __future__ import annotations

"""
short_main v6 baseline strategy

Official strategy:
    short_main_v6_timeout210

Parent:
    short_main v5 / SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge

Core change:
    timeout_bars: 200 -> 210

Critical rules:
    - short_main stable baseline. MDD is 4.5067%, so it satisfies MDD < 5%.
    - RSI direct gate is disabled.
    - RSI remains inside short_score.
    - score_min_short is included in entry mask.
    - dd_brake is portfolio-level edge_current.
    - entry is next bar open.
    - fee_per_side=0.0004 and position_fraction=0.01.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ShortMainV6Config:
    strategy_name: str = "short_main_v6_timeout210"
    candidate_name: str = "timeout210"
    parent_name: str = "SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge"
    axis: str = "short_main"
    side: str = "short"

    initial_asset: float = 100.0
    position_fraction: float = 0.01
    fee_per_side: float = 0.0004
    min_bars: int = 120

    ema_period: int = 20
    rsi_period: int = 14
    atr_period: int = 14

    short_dev: float = 0.035
    short_rsi_min: float = 77.0
    use_rsi_gate: bool = False
    short_wick_mult: float = 1.3
    score_min_short: float = 2.35

    score_dev_weight: float = 1.0
    score_rsi_weight: float = 0.8
    score_wick_weight: float = 0.7
    score_dev_cap: float = 2.0
    score_rsi_cap: float = 2.0
    score_wick_cap: float = 2.5
    wick_atr_floor_mult: float = 0.2

    atr_stop_mult: float = 1.8975
    rr_mult: float = 5.75
    min_expected_tp: float = 0.003
    timeout_bars: int = 210
    time_reduce_bars: int = 8
    time_reduce_to_risk_frac: float = 0.05
    fail_fast_bars: int = 10
    fail_fast_min_progress_r: float = 0.1

    dd_brake_trigger_pct: float = 0.03
    dd_brake_freeze_steps: int = 5
    dd_brake_mode: str = "edge_current"

    current_597_trades: int = 33989
    current_597_win_rate_pct: float = 14.213421989467182
    current_597_final_return_pct: float = 931.1433546380067
    current_597_max_return_pct: float = 931.6464095007982
    current_597_max_drawdown_pct: float = 4.506694290977831
    current_597_official_cd_value: float = 985.153259660748
    current_597_profit_factor: float = 1.5653897913886468
    current_597_max_conc: int = 277
    current_597_max_conc_unique_symbols: int = 277
    current_597_same_bar_trades: int = 3112
    current_597_active_leftover: int = 0
    current_597_blocked_by_guard: int = 30
    current_597_generated_trades_before_score_filter: int = 34019
    current_597_errors: int = 0


CFG = ShortMainV6Config()


def config_dict(cfg: ShortMainV6Config = CFG) -> Dict[str, Any]:
    return asdict(cfg)


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(close: pd.Series, period: int) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    return 100.0 - 100.0 / (1.0 + rs)


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([(high - low).abs(), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, adjust=False).mean()


def add_indicators(df: pd.DataFrame, cfg: ShortMainV6Config = CFG) -> pd.DataFrame:
    out = df.copy()
    for col in ["open", "high", "low", "close"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out["ema20"] = ema(out["close"], cfg.ema_period)
    out["rsi14"] = rsi(out["close"], cfg.rsi_period)
    out["atr14"] = atr(out["high"], out["low"], out["close"], cfg.atr_period)
    out["body"] = (out["close"] - out["open"]).abs()
    out["upper_wick"] = out["high"] - pd.concat([out["open"], out["close"]], axis=1).max(axis=1)
    raw_dev = (out["close"] / out["ema20"] - 1.0).clip(lower=0.0)
    raw_rsi = (out["rsi14"] - cfg.short_rsi_min).clip(lower=0.0)
    dev_score = (raw_dev / cfg.short_dev).clip(lower=0.0, upper=cfg.score_dev_cap)
    rsi_score = (raw_rsi / 10.0).clip(lower=0.0, upper=cfg.score_rsi_cap)
    wick_floor = pd.concat([out["body"].abs(), out["atr14"] * cfg.wick_atr_floor_mult, pd.Series(1e-12, index=out.index)], axis=1).max(axis=1)
    wick_score = np.log1p(out["upper_wick"] / wick_floor).clip(lower=0.0, upper=cfg.score_wick_cap)
    out["short_score"] = cfg.score_dev_weight * dev_score + cfg.score_rsi_weight * rsi_score + cfg.score_wick_weight * wick_score
    return out


def entry_mask(df: pd.DataFrame, cfg: ShortMainV6Config = CFG) -> pd.Series:
    dev_ok = (df["close"] / df["ema20"] - 1.0) >= cfg.short_dev
    rsi_ok = (df["rsi14"] > cfg.short_rsi_min) if cfg.use_rsi_gate else pd.Series(True, index=df.index)
    wick_ok = df["upper_wick"] >= cfg.short_wick_mult * df["body"]
    score_ok = df["short_score"] >= cfg.score_min_short
    return dev_ok & rsi_ok & wick_ok & score_ok


def build_trade(df: pd.DataFrame, signal_index: int, symbol: str = "", cfg: ShortMainV6Config = CFG) -> Optional[Dict[str, Any]]:
    entry_index = signal_index + 1
    if entry_index >= len(df):
        return None
    sig = df.iloc[signal_index]
    ent = df.iloc[entry_index]
    entry = float(ent["open"])
    atr_value = float(sig["atr14"])
    if not np.isfinite(entry) or not np.isfinite(atr_value) or entry <= 0 or atr_value <= 0:
        return None
    risk = atr_value * cfg.atr_stop_mult
    stop = entry + risk
    target = entry - cfg.rr_mult * risk
    expected_tp = (entry - target) / entry
    if stop <= entry or target <= 0 or expected_tp < cfg.min_expected_tp:
        return None
    return {"strategy": cfg.strategy_name, "symbol": symbol, "side": "short", "signal_index": signal_index, "entry_index": entry_index, "entry": entry, "risk": risk, "stop": stop, "target": target, "expected_tp": expected_tp, "score": float(sig["short_score"])}


def apply_time_reduce(entry: float, risk: float, current_stop: float, bars_held: int, mfe_r: float, cfg: ShortMainV6Config = CFG) -> float:
    if bars_held >= cfg.time_reduce_bars and mfe_r > 0:
        return min(current_stop, entry + risk * cfg.time_reduce_to_risk_frac)
    return current_stop


def exit_short(entry: float, stop: float, target: float, risk: float, mfe_r: float, bars_held: int, high: float, low: float, close: float, cfg: ShortMainV6Config = CFG):
    stop = apply_time_reduce(entry, risk, stop, bars_held, mfe_r, cfg)
    if high >= stop:
        return stop, "stop", stop
    if low <= target:
        return target, "target", stop
    if bars_held >= cfg.fail_fast_bars and mfe_r < cfg.fail_fast_min_progress_r and close > entry:
        return close, "fail_fast", stop
    if bars_held >= cfg.timeout_bars:
        return close, "timeout", stop
    return None, None, stop


def net_short_return(entry: float, exit_price: float, cfg: ShortMainV6Config = CFG) -> float:
    return entry / max(exit_price, 1e-12) - 1.0 - 2.0 * cfg.fee_per_side


BASELINE_NOTES = {
    "official_name": CFG.strategy_name,
    "axis": CFG.axis,
    "candidate": CFG.candidate_name,
    "retest_source": "local_results/short_max/short_max_v6_top_candidates_retest_v1_results",
    "official_result": {
        "trades": CFG.current_597_trades,
        "max_return_pct": CFG.current_597_max_return_pct,
        "max_drawdown_pct": CFG.current_597_max_drawdown_pct,
        "official_cd_value": CFG.current_597_official_cd_value,
        "generated_trades_before_score_filter": CFG.current_597_generated_trades_before_score_filter,
        "active_leftover": CFG.current_597_active_leftover,
        "errors": CFG.current_597_errors,
    },
    "critical_rules": [
        "short_main stable baseline; MDD below 5%.",
        "RSI direct gate disabled.",
        "RSI remains inside short_score.",
        "score_min_short in entry mask.",
        "dd_brake edge_current at portfolio level.",
        "entry next bar open.",
        "same-bar trades close immediately.",
        "fee_per_side=0.0004 and position_fraction=0.01.",
    ],
}
