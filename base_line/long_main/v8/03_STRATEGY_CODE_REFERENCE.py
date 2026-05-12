# -*- coding: utf-8 -*-
"""
long_main v8 기준선 코드 레퍼런스.
전체 백테스트 실행용 본체는 03_FROZEN_BASELINE_RUNNER.py를 사용한다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategySpec:
    name: str = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320"
    side: str = "long"
    parent_strategy: str = "8V4_V09_V054_extreme_vol18"
    parent_entry_key: str = "orig_V09_extreme_vol18"
    entry_key: str = "child::orig_V09_extreme_vol18::tp03"
    atr_stop: float = 1.10
    rr_target: float = 3.20
    max_hold_bars: int = 21
    cooldown_bars: int = 31
    tp_min_pct: float = 0.30


SPEC = StrategySpec()

EXPECTED_RESULT = {
    "trades": 57065,
    "wins": 20612,
    "losses": 36453,
    "win_rate_pct": 36.1202137913,
    "final_return_pct": 267.6967217810,
    "max_return_pct": 268.4930973199,
    "max_drawdown_pct": 1.3412321126,
    "official_cd_value": 363.5507495661,
    "max_conc": 439,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def is_long_main_eligible(max_drawdown_pct):
    return max_drawdown_pct < 5.0


def tp03_gate(close, atr14, spec=SPEC):
    target_pct = (spec.atr_stop * atr14 * spec.rr_target / close) * 100.0
    return target_pct >= spec.tp_min_pct


def reproduction_gate(actual, tol=1e-3):
    for key in ["trades", "wins", "losses"]:
        if int(actual.get(key, -1)) != EXPECTED_RESULT[key]:
            return False
    for key in ["final_return_pct", "max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    return True


def conceptual_entry_formula():
    return "parent_entry = (shock_down OR l01 OR shock_balance) AND (raw_extreme_reclaim OR rsi14 <= 34.0) AND vol_ratio >= 1.18; final_entry = parent_entry AND TP03"


if __name__ == "__main__":
    print(SPEC)
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
    print("eligible", is_long_main_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
    print(conceptual_entry_formula())
