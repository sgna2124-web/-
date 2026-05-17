# -*- coding: utf-8 -*-
"""long_main v13 기준선 코드 레퍼런스."""

STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18"
SOURCE_SEARCH_BATCH = "LONG_MAX_V7_2025_COMBO_ENTRY_DEV_V24"
SOURCE_RETEST_BATCH = "LONG_MAX_V8_2025_SINGLE_RETEST_DEV_V25"
SOURCE_CANDIDATE = "DEV24_near_stop112_rr470_hold18"
RESULT_SCOPE = "2025년까지의 데이터 기준"
TRAIN_END_EXCLUSIVE_UTC = "2026-01-01 00:00:00"
ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
ATR_STOP = 1.12
RR_TARGET = 4.70
MAX_HOLD_BARS = 18
COOLDOWN_BARS = 31
POSITION_FRACTION = 0.01
ROUND_TRIP_COST_BPS = 8.0

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


def long_main_eligible(max_drawdown_pct):
    return max_drawdown_pct < 5.0


if __name__ == "__main__":
    print(RESULT_SCOPE)
    print(TRAIN_END_EXCLUSIVE_UTC)
    print(STRATEGY_NAME)
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
    print("long_main_eligible", long_main_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
