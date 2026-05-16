# -*- coding: utf-8 -*-
"""long_max v8 기준선 코드 레퍼런스.

전체 배치 백테스트 엔진은 LONG_MAIN_DEV_V18에서 기준선 exact가 통과한 엔진 구조를 사용한다.
다음 long_max 개발 파일에서는 첫 후보를 반드시 LMAX##_000_LONG_MAX_V8_EXACT_FROZEN으로 두고 이 상수와 같은 결과를 재현해야 한다.
"""

STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__LM18_stop115_rr520_body025"
SOURCE_BATCH = "LONG_MAIN_DEV_V18_20260516_213239"
SOURCE_CANDIDATE = "LM18_041_STOP115_RR520_BODY025"
PARENT_VERSION = "long_max/v7"
SIDE = "long"
RESULT_SCOPE = "2025년까지의 데이터 기준"
TRAIN_END_EXCLUSIVE_UTC = "2026-01-01 00:00:00"

ENTRY_SOURCE_ATR_STOP = 1.10
ENTRY_SOURCE_RR_TARGET = 3.80
ENTRY_SOURCE_KEY = "child::orig_V09_extreme_vol18::tp03"
EXTRA_FILTER = "body_atr >= 0.25"

ATR_STOP = 1.15
RR_TARGET = 5.20
MAX_HOLD_BARS = 21
COOLDOWN_BARS = 31
POSITION_FRACTION = 0.01
ROUND_TRIP_COST_BPS = 8.0

EXPECTED_RESULT = {
    "trades": 56428,
    "wins": 20531,
    "losses": 35897,
    "win_rate_pct": 36.38441908272489,
    "final_return_pct": 397.7275034318756,
    "max_return_pct": 398.29373996834414,
    "max_drawdown_pct": 1.4367182391297861,
    "official_cd_value": 491.134662921777,
    "max_conc": 443,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}

ENTRY_FORMULA = "final_entry = long_max_v7_frozen_entry AND body_atr >= 0.25"
EXIT_FORMULA = "long exit: atr_stop=1.15, rr_target=5.20, max_hold_bars=21, cooldown_bars=31, stop_first_when_same_bar"


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def reproduction_gate(actual, tol=1e-3):
    for key in ["trades", "wins", "losses", "max_conc", "errors"]:
        if int(actual.get(key, -1)) != EXPECTED_RESULT[key]:
            return False
    for key in ["max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    if bool(actual.get("ruined", True)) != EXPECTED_RESULT["ruined"]:
        return False
    return True


if __name__ == "__main__":
    print(RESULT_SCOPE)
    print(TRAIN_END_EXCLUSIVE_UTC)
    print(STRATEGY_NAME)
    print(SOURCE_CANDIDATE)
    print(ENTRY_FORMULA)
    print(EXIT_FORMULA)
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
