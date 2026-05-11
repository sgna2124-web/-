from __future__ import annotations

"""
long_main v5 official baseline strategy
=======================================

Official strategy name:
    LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3

Source development variant:
    LM9_012_V4_SHOCK_RECENCY_3

Parent baseline:
    LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220

Original core:
    6V2_L01_doubleflush_core

Core rule:
    raw_l01_cap_reclaim AND double_flush_ok

v5 keeps the v4 filters:
    vol_ratio >= 1.45
    body_atr <= 2.20
    ret20 <= -0.08
    expected_tp >= 0.003

v5 adds:
    shock_recency <= 3

Important:
    close_pos >= 0.77 is NOT used.
    raw_l01_cap_reclaim still requires close_pos > 0.70.

Execution assumptions:
    fee_per_side = 0.0004
    round_trip_fee = 0.0008
    round_trip_cost_bps = 8.0
    position_fraction = 0.01

Exact reproduction target:
    trades ~= 447
    max_return_pct ~= 25.0899569668
    max_drawdown_pct ~= 0.9930660871
    official_cd_value ~= 123.6093482796
"""

from dataclasses import dataclass
from typing import Sequence, List


@dataclass(frozen=True)
class LongMainV5Params:
    # Exit model inherited from long_main v1/v2/v3/v4 baseline
    atr_stop: float = 1.05
    rr_target: float = 2.50
    max_hold_bars: int = 18
    cooldown_bars: int = 18

    # Fee / sizing model
    fee_per_side: float = 0.0004
    round_trip_fee: float = 0.0008
    round_trip_cost_bps: float = 8.0
    position_fraction: float = 0.01

    # raw_l01_signal_at v1 restored thresholds used by v9 implementation
    raw_ret3_max: float = -0.040
    raw_ret5_max: float = -0.060
    raw_close_pos_min: float = 0.70
    raw_vol_min: float = 1.40
    raw_body_atr_min: float = 0.35
    raw_atrp_min: float = 0.003
    reclaim_buffer: float = 0.0

    # raw_shock_down_at restored thresholds
    shock_ret3_max: float = -0.035
    shock_ret5_max: float = -0.050
    shock_vol_min: float = 1.10
    shock_body_atr_min: float = 0.25

    # double_flush_ok thresholds
    df_lookback: int = 10
    df_low_mult: float = 1.003
    df_close_pos_min: float = 0.75
    df_wick_ratio_min: float = 1.30

    # v4 retained filters
    vol_ratio_min_v5: float = 1.45
    body_atr_max_v5: float = 2.20
    ret20_pullback_max_v5: float = -0.08

    # v5 shock freshness filter
    shock_recency_max_v5: int = 3

    # TP rule
    min_expected_tp: float = 0.003


PARAMS = LongMainV5Params()


def safe_get(values: Sequence[float], i: int, default: float = 0.0) -> float:
    try:
        return float(values[i])
    except Exception:
        return default


def raw_l01_cap_reclaim(
    *,
    open_: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    ll20: Sequence[float],
    atrp: Sequence[float],
    vol_ratio: Sequence[float],
    body_atr: Sequence[float],
    close_pos: Sequence[float],
    ret3: Sequence[float],
    ret5: Sequence[float],
    i: int,
    p: LongMainV5Params = PARAMS,
) -> bool:
    """Restored raw_l01_cap_reclaim gate used by v9 long_main development.

    This gate includes close_pos > 0.70. v5 does not add close_pos >= 0.77.
    """
    if i < 21:
        return False

    ll20_prev = safe_get(ll20, i - 1)
    if ll20_prev <= 0:
        return False

    bull_reclaim = (
        safe_get(low, i) < ll20_prev
        and safe_get(close, i) > ll20_prev * (1.0 + p.reclaim_buffer)
        and safe_get(close, i) > safe_get(open_, i)
        and safe_get(close_pos, i) > p.raw_close_pos_min
    )

    return bool(
        (safe_get(ret3, i) < p.raw_ret3_max or safe_get(ret5, i) < p.raw_ret5_max)
        and bull_reclaim
        and safe_get(vol_ratio, i) > p.raw_vol_min
        and safe_get(body_atr, i) > p.raw_body_atr_min
        and safe_get(atrp, i) > p.raw_atrp_min
    )


def raw_shock_down(
    *,
    vol_ratio: Sequence[float],
    body_atr: Sequence[float],
    ret3: Sequence[float],
    ret5: Sequence[float],
    i: int,
    p: LongMainV5Params = PARAMS,
) -> bool:
    """Restored shock_down definition used by double_flush context."""
    return bool(
        (safe_get(ret3, i) <= p.shock_ret3_max or safe_get(ret5, i) <= p.shock_ret5_max)
        and safe_get(vol_ratio, i) >= p.shock_vol_min
        and safe_get(body_atr, i) >= p.shock_body_atr_min
    )


def recent_shock_indices(
    *,
    shock_down_flags: Sequence[bool],
    i: int,
    lookback: int = PARAMS.df_lookback,
) -> List[int]:
    """Past-only shock indices in [i-lookback, i-1]."""
    start = max(0, i - lookback)
    end = max(start, i)
    return [j for j in range(start, end) if bool(shock_down_flags[j])]


def reclaim_quality_ok(
    *,
    open_: Sequence[float],
    close: Sequence[float],
    close_pos: Sequence[float],
    lower_wick_body_ratio: Sequence[float],
    i: int,
    p: LongMainV5Params = PARAMS,
) -> bool:
    return bool(
        safe_get(close_pos, i) >= p.df_close_pos_min
        and safe_get(lower_wick_body_ratio, i) >= p.df_wick_ratio_min
        and safe_get(close, i) > safe_get(open_, i)
    )


def double_flush_ok(
    *,
    open_: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    close_pos: Sequence[float],
    lower_wick_body_ratio: Sequence[float],
    shock_down_flags: Sequence[bool],
    i: int,
    p: LongMainV5Params = PARAMS,
) -> bool:
    """Recent shock_down exists and current candle retests/reclaims that shock low."""
    idxs = recent_shock_indices(shock_down_flags=shock_down_flags, i=i, lookback=p.df_lookback)
    if not idxs:
        return False

    ref_low = min(safe_get(low, j) for j in idxs)
    return bool(
        safe_get(low, i) <= ref_low * p.df_low_mult
        and reclaim_quality_ok(
            open_=open_,
            close=close,
            close_pos=close_pos,
            lower_wick_body_ratio=lower_wick_body_ratio,
            i=i,
            p=p,
        )
    )


def shock_recency_ok(
    *,
    shock_down_flags: Sequence[bool],
    i: int,
    p: LongMainV5Params = PARAMS,
) -> bool:
    """Require the latest shock_down in the double-flush window to be fresh."""
    idxs = recent_shock_indices(shock_down_flags=shock_down_flags, i=i, lookback=p.df_lookback)
    if not idxs:
        return False
    latest = max(idxs)
    return bool((i - latest) <= p.shock_recency_max_v5)


def expected_tp_ok(atrp: Sequence[float], i: int, p: LongMainV5Params = PARAMS) -> bool:
    expected_tp = p.atr_stop * p.rr_target * safe_get(atrp, i)
    return bool(expected_tp >= p.min_expected_tp)


def long_main_v5_entry(
    *,
    open_: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    ll20: Sequence[float],
    atrp: Sequence[float],
    vol_ratio: Sequence[float],
    body_atr: Sequence[float],
    close_pos: Sequence[float],
    lower_wick_body_ratio: Sequence[float],
    ret3: Sequence[float],
    ret5: Sequence[float],
    ret20: Sequence[float],
    shock_down_flags: Sequence[bool],
    i: int,
    p: LongMainV5Params = PARAMS,
) -> bool:
    """Official long_main v5 baseline entry.

    `shock_down_flags` must be precomputed with `raw_shock_down` for every bar.
    """
    base_ok = raw_l01_cap_reclaim(
        open_=open_,
        low=low,
        close=close,
        ll20=ll20,
        atrp=atrp,
        vol_ratio=vol_ratio,
        body_atr=body_atr,
        close_pos=close_pos,
        ret3=ret3,
        ret5=ret5,
        i=i,
        p=p,
    ) and double_flush_ok(
        open_=open_,
        low=low,
        close=close,
        close_pos=close_pos,
        lower_wick_body_ratio=lower_wick_body_ratio,
        shock_down_flags=shock_down_flags,
        i=i,
        p=p,
    )

    if not base_ok:
        return False

    return bool(
        safe_get(vol_ratio, i) >= p.vol_ratio_min_v5
        and safe_get(body_atr, i) <= p.body_atr_max_v5
        and safe_get(ret20, i) <= p.ret20_pullback_max_v5
        and shock_recency_ok(shock_down_flags=shock_down_flags, i=i, p=p)
        and expected_tp_ok(atrp, i, p)
    )


LONG_MAIN_V5_RESULT = {
    "strategy": "LONG_MAIN_V5_LM9_012_V4_SHOCK_RECENCY_3",
    "source_variant": "LM9_012_V4_SHOCK_RECENCY_3",
    "trades": 447,
    "wins": 297,
    "losses": 150,
    "win_rate_pct": 66.4429530201,
    "final_return_pct": 24.8492730067,
    "max_return_pct": 25.0899569668,
    "max_drawdown_pct": 0.9930660871,
    "official_cd_value": 123.6093482796,
    "profit_factor": 4.9302639666,
}


if __name__ == "__main__":
    import json

    print(json.dumps({
        "params": PARAMS.__dict__,
        "result": LONG_MAIN_V5_RESULT,
    }, indent=2, ensure_ascii=False))
