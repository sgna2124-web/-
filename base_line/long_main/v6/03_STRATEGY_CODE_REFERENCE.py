# -*- coding: utf-8 -*-
"""
long_main v6 / long_max v2 기준선 코드 레퍼런스

공식 기준선 전략:
    8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20

이 파일은 다음 개선 작업에서 기준으로 삼을 전략 식별자, entry_key, 리스크 파라미터,
성과 계산식, 재현 체크값을 고정 기록하기 위한 코드 레퍼런스다.

실제 단독 재현 전체 runner는 대화창에서 생성된
    run_long_max_single_top_retest_dev_v12.py
와 동일한 로직을 기준으로 한다.

다음 개발자는 이 파일의 STRATEGY_SPEC, EXPECTED_RESULT, cd_value 계산식을
기준으로 개선안을 붙인다.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class StrategySpec:
    name: str
    side: str
    description: str
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


STRATEGY_SPEC = StrategySpec(
    name="8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20",
    side="long",
    description="V09 extreme vol18 parent + TP03 expectation gate + risk_rr_plus20 exit profile",
    parent_strategy="8V4_V09_V054_extreme_vol18",
    parent_entry_key="orig_V09_extreme_vol18",
    entry_key="child::orig_V09_extreme_vol18::tp03",
    family="V09",
    anchor="extreme",
    guard="vol18",
    atr_stop=1.01,
    rr_target=2.90,
    max_hold_bars=21,
    cooldown_bars=31,
    use_tp03_gate=True,
)

EXPECTED_RESULT: Dict[str, Any] = {
    "run_label": "LONG_MAX_SINGLE_TOP_RETEST_DEV_V12",
    "strategy": "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20",
    "trades": 57243,
    "wins": 20312,
    "losses": 36931,
    "win_rate_pct": 35.48381461488741,
    "final_return_pct": 214.71444608282576,
    "max_return_pct": 215.22710202673295,
    "max_drawdown_pct": 1.221987075736386,
    "official_cd_value": 311.37506758074795,
    "max_conc": 429,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
    "position_fraction": 0.01,
    "round_trip_cost_bps": 8.0,
}


def official_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    """프로젝트 공식 cd_value 계산식."""
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def is_long_main_eligible(max_drawdown_pct: float) -> bool:
    """long_main 선별 조건: MDD 5% 미만."""
    return max_drawdown_pct < 5.0


def is_long_max_eligible(_: float) -> bool:
    """long_max 선별 조건: MDD 제한 없음."""
    return True


def build_single_target_strategy() -> StrategySpec:
    """다음 개선 코드가 불러 써야 할 frozen 기준선 스펙."""
    return STRATEGY_SPEC


# ---------------------------------------------------------------------------
# 진입 조건 구현 계약
# ---------------------------------------------------------------------------
# 최종 진입 신호는 아래 개념식을 따른다.
#
#   parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18
#   child_entry  = parent_entry AND tp03_gate
#
# parent_entry는 8V4 계열의 V09/extreme/vol18 조합 신호다.
# child_entry는 parent_entry에 TP 기대값 0.3% 이상 조건을 추가한 신호다.
#
# 정확한 Boolean 구현은 V12 runner의 compute_entry_masks() 흐름을 따른다.
# 다음 개선에서는 전략명만 보고 V09/extreme/vol18을 임의 재해석하지 않는다.
#
# 개선 후보는 기본적으로 아래 중 하나여야 한다.
#   1. child_entry AND 추가 필터
#   2. child_entry OR parent 근접 신호
#   3. child_entry 유지 + 청산 파라미터 변경
#   4. child_entry 유지 + cooldown/max_hold 변경
# ---------------------------------------------------------------------------


def reproduction_gate(actual: Dict[str, Any], tol: float = 1e-3) -> bool:
    """
    기준선 단독 재현 최소 판정.

    반드시 일치해야 하는 항목:
        trades, wins, losses

    허용 오차로 비교하는 항목:
        final_return_pct, max_return_pct, max_drawdown_pct, official_cd_value/cd_value
    """
    if int(actual.get("trades", -1)) != EXPECTED_RESULT["trades"]:
        return False
    if int(actual.get("wins", -1)) != EXPECTED_RESULT["wins"]:
        return False
    if int(actual.get("losses", -1)) != EXPECTED_RESULT["losses"]:
        return False

    checks = [
        ("final_return_pct", EXPECTED_RESULT["final_return_pct"]),
        ("max_return_pct", EXPECTED_RESULT["max_return_pct"]),
        ("max_drawdown_pct", EXPECTED_RESULT["max_drawdown_pct"]),
    ]
    for key, expected in checks:
        if abs(float(actual.get(key, 1e99)) - expected) > tol:
            return False

    actual_cd = float(actual.get("official_cd_value", actual.get("cd_value", 1e99)))
    if abs(actual_cd - EXPECTED_RESULT["official_cd_value"]) > tol:
        return False
    return True


if __name__ == "__main__":
    cd = official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"])
    print("strategy", STRATEGY_SPEC.name)
    print("official_cd_value", cd)
    print("expected_official_cd_value", EXPECTED_RESULT["official_cd_value"])
    print("long_main_eligible", is_long_main_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
    print("long_max_eligible", is_long_max_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
