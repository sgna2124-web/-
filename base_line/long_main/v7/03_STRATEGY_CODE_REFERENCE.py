# -*- coding: utf-8 -*-
"""
long_main v7 기준선 코드 레퍼런스

공식 기준선 전략:
    8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110

이 파일은 다음 개발자가 기준선 스펙, 공식 결과값, cd_value 계산식,
재현 판정 기준을 코드로 바로 확인하기 위한 기준선 레퍼런스다.

주의:
    이 파일만으로 전체 OHLCV 백테스트가 실행되는 frozen runner는 아니다.
    전체 재현 runner는 V13 엔진의 entry mask, feature 계산, 청산 루프를 그대로 사용해야 한다.
    단, 이 파일의 StrategySpec과 EXPECTED_RESULT 값은 v7 공식 기준선으로 고정한다.
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class StrategySpec:
    name: str
    side: str
    parent_strategy: str
    parent_entry_key: str
    entry_key: str
    family: str
    anchor: str
    guard: str
    atr_stop: float
    rr_target: float
    max_hold_bars: int
    cooldown_bars: int
    use_tp03_gate: bool
    tp_min_pct: float


STRATEGY_SPEC = StrategySpec(
    name="8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110",
    side="long",
    parent_strategy="8V4_V09_V054_extreme_vol18",
    parent_entry_key="orig_V09_extreme_vol18",
    entry_key="child::orig_V09_extreme_vol18::tp03",
    family="V09",
    anchor="extreme",
    guard="vol18",
    atr_stop=1.10,
    rr_target=2.90,
    max_hold_bars=21,
    cooldown_bars=31,
    use_tp03_gate=True,
    tp_min_pct=0.30,
)

EXPECTED_RESULT: Dict[str, Any] = {
    "strategy": STRATEGY_SPEC.name,
    "trades": 57114,
    "wins": 20911,
    "losses": 36203,
    "win_rate_pct": 36.6127394334,
    "final_return_pct": 240.7307747654,
    "max_return_pct": 241.3427142366,
    "max_drawdown_pct": 1.3408670828,
    "official_cd_value": 336.7657621418,
    "max_conc": 435,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
    "position_fraction": 0.01,
    "round_trip_cost_bps": 8.0,
}


def official_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def is_long_main_eligible(max_drawdown_pct: float) -> bool:
    return max_drawdown_pct < 5.0


def tp03_gate(close: float, atr14: float, spec: StrategySpec = STRATEGY_SPEC) -> bool:
    target_pct = (spec.atr_stop * atr14 * spec.rr_target / close) * 100.0
    return target_pct >= spec.tp_min_pct


def conceptual_entry_formula() -> str:
    return (
        "family_signal_V09 = shock_down OR l01 OR shock_balance\n"
        "anchor_extreme = raw_extreme_reclaim OR rsi14 <= 34.0\n"
        "guard_vol18 = vol_ratio >= 1.18\n"
        "parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18\n"
        "final_entry = parent_entry AND tp03_gate"
    )


def reproduction_gate(actual: Dict[str, Any], tol: float = 1e-3) -> bool:
    if int(actual.get("trades", -1)) != EXPECTED_RESULT["trades"]:
        return False
    if int(actual.get("wins", -1)) != EXPECTED_RESULT["wins"]:
        return False
    if int(actual.get("losses", -1)) != EXPECTED_RESULT["losses"]:
        return False
    for key in ["final_return_pct", "max_return_pct", "max_drawdown_pct"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    actual_cd = float(actual.get("official_cd_value", actual.get("cd_value", 1e99)))
    if abs(actual_cd - EXPECTED_RESULT["official_cd_value"]) > tol:
        return False
    return True


if __name__ == "__main__":
    print(STRATEGY_SPEC)
    print("official_cd_value", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
    print("long_main_eligible", is_long_main_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
    print(conceptual_entry_formula())
