from __future__ import annotations

"""
long_main v4 official baseline strategy
=======================================

Official strategy name:
    LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220

Source development variant:
    LM8_021_LOOSER_BODY_GUARD_220

Parent baseline:
    LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08

Original core:
    6V2_L01_doubleflush_core

Core rule:
    The original long_main entry structure is preserved:
        raw_l01_cap_reclaim AND double_flush_ok

    v4 keeps the v3 volume and pullback filters:
        vol_ratio >= 1.45
        ret20 <= -0.08

    v4 relaxes the body upper guard:
        body_atr <= 1.60  ->  body_atr <= 2.20

    v4 does NOT use the v2 close_pos reinforcement:
        close_pos >= 0.77 is NOT used.

    Important:
        close_pos is not fully removed. The original v1 raw gate still requires
        close_pos > 0.70 inside raw_l01_cap_reclaim.

Execution assumptions:
    fee_per_side = 0.0004
    round_trip_fee = 0.0008
    round_trip_cost_bps = 8.0
    position_fraction = 0.01

Exact reproduction target:
    trades ~= 479
    max_return_pct ~= 25.2063735035
    max_drawdown_pct ~= 1.0904624350
    official_cd_value ~= 123.5780610685
"""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class LongMainV4Params:
    # Exit model inherited from long_main v1/v2/v3 baseline
    atr_stop: float = 1.05
    rr_target: float = 2.50
    max_hold_bars: int = 18
    cooldown_bars: int = 18

    # Fee / sizing model
    fee_per_side: float = 0.0004
    round_trip_fee: float = 0.0008
    round_trip_cost_bps: float = 8.0
    position_fraction: float = 0.01

    # Original v1 raw_l01_cap_reclaim thresholds
    atrp_min: float = 0.003
    atrp_max: float = 0.070
    range20p_max: float = 0.180
    vol_ratio_min_v1: float = 1.35
    body_atr_min: float = 0.34
    close_pos_min_v1: float = 0.70
    low_reclaim_buffer: float = 1.003
    ret5_max: float = 0.025
    ret10_max: float = 0.040
    ret20_max_v1: float = 0.075
    double_flush_lookback: int = 10

    # v3/v4 retained filters
    vol_ratio_min_v4: float = 1.45
    ret20_pullback_max_v4: float = -0.08

    # v4 relaxed body upper guard
    body_atr_max_v4: float = 2.20

    # TP rule
    min_expected_tp: float = 0.003


PARAMS = LongMainV4Params()


def safe_get(values: Sequence[float], i: int, default: float = 0.0) -> float:
    try:
        return float(values[i])
    except Exception:
        return default


def ema_guard_soft(close: Sequence[float], ema20: Sequence[float], ema50: Sequence[float], i: int) -> bool:
    """Soft EMA guard used by the restored long_main family.

    long_main is a flush/reclaim reversal strategy, not a trend-following
    strategy. Therefore this guard must remain soft and must not be replaced
    with EMA50 gap/slope, trend floor, or quiet-ratio hard filters.
    """
    c = safe_get(close, i)
    e20 = safe_get(ema20, i)
    e50 = safe_get(ema50, i)
    if c <= 0 or e20 <= 0 or e50 <= 0:
        return True
    return bool((c >= e20 * 0.965) or (c >= e50 * 0.940))


def double_flush_ok(
    shock_down: Sequence[bool],
    i: int,
    lookback: int = PARAMS.double_flush_lookback,
) -> bool:
    """Require at least one prior shock_down/flush in the recent window."""
    start = max(0, i - lookback)
    end = max(start, i)
    for j in range(start, end):
        if bool(shock_down[j]):
            return True
    return False


def raw_l01_cap_reclaim(
    *,
    open_: Sequence[float],
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    ll20: Sequence[float],
    ema20: Sequence[float],
    ema50: Sequence[float],
    atrp: Sequence[float],
    range20p: Sequence[float],
    vol_ratio: Sequence[float],
    body_atr: Sequence[float],
    close_pos: Sequence[float],
    ret5: Sequence[float],
    ret10: Sequence[float],
    ret20: Sequence[float],
    i: int,
    p: LongMainV4Params = PARAMS,
) -> bool:
    """Original long_main raw cap reclaim gate.

    This gate still contains close_pos > 0.70. v4 does not use the extra v2
    close_pos >= 0.77 reinforcement.
    """
    if i <= 0:
        return False

    o = safe_get(open_, i)
    c = safe_get(close, i)
    l = safe_get(low, i)
    ll20_prev = safe_get(ll20, i - 1)

    if c <= 0 or ll20_prev <= 0:
        return False

    return bool(
        safe_get(atrp, i) >= p.atrp_min
        and safe_get(atrp, i) <= p.atrp_max
        and safe_get(range20p, i) <= p.range20p_max
        and safe_get(vol_ratio, i) >= p.vol_ratio_min_v1
        and safe_get(body_atr, i) >= p.body_atr_min
        and c > o
        and safe_get(close_pos, i) > p.close_pos_min_v1
        and l <= ll20_prev * p.low_reclaim_buffer
        and c >= ll20_prev
        and safe_get(ret5, i) <= p.ret5_max
        and safe_get(ret10, i) <= p.ret10_max
        and safe_get(ret20, i) <= p.ret20_max_v1
        and ema_guard_soft(close, ema20, ema50, i)
    )


def expected_tp_ok(atrp: Sequence[float], i: int, p: LongMainV4Params = PARAMS) -> bool:
    expected_tp = p.atr_stop * p.rr_target * safe_get(atrp, i)
    return bool(expected_tp >= p.min_expected_tp)


def long_main_v4_entry(
    *,
    open_: Sequence[float],
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    ll20: Sequence[float],
    ema20: Sequence[float],
    ema50: Sequence[float],
    atrp: Sequence[float],
    range20p: Sequence[float],
    vol_ratio: Sequence[float],
    body_atr: Sequence[float],
    close_pos: Sequence[float],
    ret5: Sequence[float],
    ret10: Sequence[float],
    ret20: Sequence[float],
    shock_down: Sequence[bool],
    i: int,
    p: LongMainV4Params = PARAMS,
) -> bool:
    """Official long_main v4 baseline entry."""
    base_ok = raw_l01_cap_reclaim(
        open_=open_,
        high=high,
        low=low,
        close=close,
        ll20=ll20,
        ema20=ema20,
        ema50=ema50,
        atrp=atrp,
        range20p=range20p,
        vol_ratio=vol_ratio,
        body_atr=body_atr,
        close_pos=close_pos,
        ret5=ret5,
        ret10=ret10,
        ret20=ret20,
        i=i,
        p=p,
    ) and double_flush_ok(shock_down, i, p.double_flush_lookback)

    if not base_ok:
        return False

    return bool(
        safe_get(vol_ratio, i) >= p.vol_ratio_min_v4
        and safe_get(body_atr, i) <= p.body_atr_max_v4
        and safe_get(ret20, i) <= p.ret20_pullback_max_v4
        and expected_tp_ok(atrp, i, p)
    )


LONG_MAIN_V4_RESULT = {
    "strategy": "LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220",
    "source_variant": "LM8_021_LOOSER_BODY_GUARD_220",
    "trades": 479,
    "wins": 310,
    "losses": 169,
    "win_rate_pct": 64.7181628392,
    "final_return_pct": 24.9404780954,
    "max_return_pct": 25.2063735035,
    "max_drawdown_pct": 1.0904624350,
    "official_cd_value": 123.5780610685,
    "profit_factor": 4.5655373148,
}


if __name__ == "__main__":
    import json

    print(json.dumps({
        "params": PARAMS.__dict__,
        "result": LONG_MAIN_V4_RESULT,
    }, indent=2, ensure_ascii=False))
