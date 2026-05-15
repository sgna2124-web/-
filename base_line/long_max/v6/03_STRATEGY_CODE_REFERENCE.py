# -*- coding: utf-8 -*-
"""long_max v6 기준선 코드 레퍼런스. 결과값은 2025년까지의 데이터 기준이다."""

STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380"
PARENT_STRATEGY = "8V4_V09_V054_extreme_vol18"
PARENT_ENTRY_KEY = "orig_V09_extreme_vol18"
ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
SIDE = "long"
RESULT_SCOPE = "2025년까지의 데이터 기준"
TRAIN_END_EXCLUSIVE_UTC = "2026-01-01 00:00:00"
ATR_STOP = 1.10
RR_TARGET = 3.80
MAX_HOLD_BARS = 21
COOLDOWN_BARS = 31
POSITION_FRACTION = 0.01
ROUND_TRIP_COST_BPS = 8.0
TP_MIN_PCT = 0.30

EXPECTED_RESULT = {
    "trades": 56673,
    "wins": 20255,
    "losses": 36418,
    "win_rate_pct": 35.740123162705345,
    "final_return_pct": 332.2800895520915,
    "max_return_pct": 332.5601665725121,
    "max_drawdown_pct": 1.2943172013524573,
    "official_cd_value": 426.96146593036525,
    "max_conc": 442,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def is_long_max_eligible(_max_drawdown_pct):
    return True


def tp03_gate(close, atr14):
    target_pct = (ATR_STOP * atr14 * RR_TARGET / close) * 100.0
    return target_pct >= TP_MIN_PCT


def reproduction_gate(actual, tol=1e-3):
    for key in ["trades", "wins", "losses"]:
        if int(actual.get(key, -1)) != EXPECTED_RESULT[key]:
            return False
    for key in ["max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    return True


ENTRY_FORMULA = "final_entry = ((shock_down OR l01 OR shock_balance) AND (raw_extreme_reclaim OR rsi14 <= 34.0) AND vol_ratio >= 1.18) AND TP03"

if __name__ == "__main__":
    print(RESULT_SCOPE)
    print(TRAIN_END_EXCLUSIVE_UTC)
    print(STRATEGY_NAME)
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
    print("long_max_eligible", is_long_max_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
