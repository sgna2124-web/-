# -*- coding: utf-8 -*-
"""long_main v9 기준선 코드 레퍼런스."""

STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350"
PARENT_STRATEGY = "8V4_V09_V054_extreme_vol18"
PARENT_ENTRY_KEY = "orig_V09_extreme_vol18"
ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
SIDE = "long"
ATR_STOP = 1.10
RR_TARGET = 3.50
MAX_HOLD_BARS = 21
COOLDOWN_BARS = 31
TP_MIN_PCT = 0.30

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


def is_long_main_eligible(max_drawdown_pct):
    return max_drawdown_pct < 5.0


def tp03_gate(close, atr14):
    target_pct = (ATR_STOP * atr14 * RR_TARGET / close) * 100.0
    return target_pct >= TP_MIN_PCT


def reproduction_gate(actual, tol=1e-3):
    for key in ["trades", "wins", "losses"]:
        if int(actual.get(key, -1)) != EXPECTED_RESULT[key]:
            return False
    for key in ["final_return_pct", "max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    return True


ENTRY_FORMULA = "parent_entry = (shock_down OR l01 OR shock_balance) AND (raw_extreme_reclaim OR rsi14 <= 34.0) AND vol_ratio >= 1.18; final_entry = parent_entry AND TP03"

if __name__ == "__main__":
    print(STRATEGY_NAME)
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
    print("long_main_eligible", is_long_main_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
    print(ENTRY_FORMULA)
