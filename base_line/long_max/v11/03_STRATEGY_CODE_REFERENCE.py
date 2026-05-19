# -*- coding: utf-8 -*-
"""long_max v11 기준선 코드 레퍼런스."""

STRATEGY_NAME = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18__LM21_stop115_rr480_body020_hold17__LM22_stop120_rr500_body020_hold17__LM23_stop121_rr505_body022_hold17"
SOURCE_BATCH = "LONG_MAIN_LM23_RANK1_RETEST_20260519_213610"
SOURCE_CANDIDATE = "LM23R_001_RETEST_S121_RR505_B022_H17"
AXIS = "long_max"
VERSION = "v11"
SIDE = "long"
RESULT_SCOPE = "2025년까지의 데이터 기준"
TRAIN_END_EXCLUSIVE_UTC = "2026-01-01 00:00:00"

ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
ENTRY_SOURCE_ATR_STOP = 1.10
ENTRY_SOURCE_RR_TARGET = 3.80
TP03_MIN_TARGET_PCT = 0.30
BODY_ATR_MIN = 0.22

ATR_STOP = 1.21
RR_TARGET = 5.05
MAX_HOLD_BARS = 17
COOLDOWN_BARS = 31
ROUND_TRIP_COST_BPS = 8.0
POSITION_FRACTION = 0.01

EXPECTED_RESULT = {
    "trades": 56551,
    "wins": 21969,
    "losses": 34582,
    "win_rate_pct": 38.84811939665081,
    "final_return_pct": 454.0898854634718,
    "max_return_pct": 455.0171719748199,
    "max_drawdown_pct": 1.3974597812998368,
    "official_cd_value": 547.2610302171641,
    "max_conc": 445,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}


def tp03_target_pct(close, atr14):
    return (ENTRY_SOURCE_ATR_STOP * atr14 * ENTRY_SOURCE_RR_TARGET / max(close, 1e-12)) * 100.0


def apply_final_entry_filter(entry_source, body_atr):
    return bool(entry_source) and float(body_atr) >= BODY_ATR_MIN


def long_exit_prices(entry_price, signal_atr14):
    risk = ATR_STOP * signal_atr14
    return entry_price - risk, entry_price + risk * RR_TARGET


def trade_pnl_pct(entry_price, exit_price):
    return (exit_price / entry_price - 1.0) * 100.0 - (ROUND_TRIP_COST_BPS * 0.01)


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


if __name__ == "__main__":
    print(AXIS, VERSION)
    print(STRATEGY_NAME)
    print(EXPECTED_RESULT)
