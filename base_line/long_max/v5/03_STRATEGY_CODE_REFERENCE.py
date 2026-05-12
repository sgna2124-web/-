# -*- coding: utf-8 -*-
"""
long_max v5 기준선 코드 레퍼런스

공식 기준선 전략:
8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350

전체 백테스트 실행용 본체는 V17 단독 리테스트 runner를 사용한다.
이 파일은 기준선 스펙, 기대 결과값, cd_value 계산식, TP03 계산식, 재현 판정 기준을 코드로 확인하기 위한 레퍼런스다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategySpec:
    name: str = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350"
    side: str = "long"
    parent_strategy: str = "8V4_V09_V054_extreme_vol18"
    parent_entry_key: str = "orig_V09_extreme_vol18"
    entry_key: str = "child::orig_V09_extreme_vol18::tp03"
    atr_stop: float = 1.10
    rr_target: float = 3.50
    max_hold_bars: int = 21
    cooldown_bars: int = 31
    tp_min_pct: float = 0.30


SPEC = StrategySpec()

EXPECTED_RESULT = {
    "trades": 57035,
    "wins": 20451,
    "losses": 36584,
    "win_rate_pct": 35.8569299553,
    "final_return_pct": 305.0347181084,
    "max_return_pct": 305.8775211164,
    "max_drawdown_pct": 1.2432451599,
    "official_cd_value": 400.8314684802,
    "max_conc": 441,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def is_long_max_eligible(_max_drawdown_pct):
    return True


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
    print("long_max_eligible", is_long_max_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
    print(conceptual_entry_formula())
