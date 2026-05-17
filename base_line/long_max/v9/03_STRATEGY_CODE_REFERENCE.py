# -*- coding: utf-8 -*-
"""long_max v9 기준선 코드 레퍼런스.

공식 결과는 2025년까지의 데이터 기준이다.
전체 재현은 V25 단독 리테스트 엔진 구조를 사용한다.
"""

STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18"
SOURCE_SEARCH_BATCH = "LONG_MAX_V7_2025_COMBO_ENTRY_DEV_V24"
SOURCE_RETEST_BATCH = "LONG_MAX_V8_2025_SINGLE_RETEST_DEV_V25"
SOURCE_CANDIDATE = "DEV24_near_stop112_rr470_hold18"
SIDE = "long"
RESULT_SCOPE = "2025년까지의 데이터 기준"
TRAIN_END_EXCLUSIVE_UTC = "2026-01-01 00:00:00"

ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
ENTRY_FORMULA = "final_entry = child::orig_V09_extreme_vol18::tp03"

ATR_STOP = 1.12
RR_TARGET = 4.70
MAX_HOLD_BARS = 18
COOLDOWN_BARS = 31
POSITION_FRACTION = 0.01
ROUND_TRIP_COST_BPS = 8.0
TP_MIN_PCT = 0.30

EXPECTED_RESULT = {
    "trades": 56697,
    "wins": 20962,
    "losses": 35735,
    "win_rate_pct": 36.97197382577562,
    "final_return_pct": 405.1480528315248,
    "max_return_pct": 405.8734002703171,
    "max_drawdown_pct": 1.228290350505734,
    "official_cd_value": 499.6598061090216,
    "max_conc": 444,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def reproduction_check(actual, tol=1e-3):
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
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
