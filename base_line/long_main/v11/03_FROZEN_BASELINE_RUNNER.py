# -*- coding: utf-8 -*-
"""
Frozen baseline reference for long_main v11 / long_max v7.
This file is intentionally small enough to review. For actual batch backtest, use the
same engine structure as run_long_main_dev_v15.py and keep the constants below unchanged.
"""
from dataclasses import dataclass, asdict

STRATEGY = "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420"
SOURCE_CANDIDATE = "LM15_031_V10_RR420"
PARENT_STRATEGY = "8V4_V09_V054_extreme_vol18"
PARENT_ENTRY_KEY = "orig_V09_extreme_vol18"
FINAL_ENTRY_KEY = "child::orig_V09_extreme_vol18::tp03"
RESULT_SCOPE = "2025년까지의 데이터 기준; 2026년 데이터 제외"
TRAIN_END_EXCLUSIVE_UTC = "2026-01-01 00:00:00"

@dataclass(frozen=True)
class StrategySpec:
    name: str = SOURCE_CANDIDATE
    side: str = "long"
    entry_key: str = FINAL_ENTRY_KEY
    atr_stop: float = 1.10
    rr_target: float = 4.20
    max_hold_bars: int = 21
    cooldown_bars: int = 31
    position_fraction: float = 0.01
    round_trip_cost_bps: float = 8.0
    use_tp03_gate: bool = True

EXPECTED_RESULT = {
    "trades": 56651,
    "wins": 20168,
    "losses": 36483,
    "win_rate_pct": 35.600430707313194,
    "final_return_pct": 358.93258386772163,
    "max_return_pct": 359.3568623293992,
    "max_drawdown_pct": 1.2516306589841375,
    "official_cd_value": 453.60741100633686,
    "max_conc": 442,
    "symbol_files": 597,
    "errors": 0,
    "ruined": False,
}

def official_cd_value(max_return_pct: float, max_drawdown_pct: float) -> float:
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)

def pass_reproduction(row: dict, tol: float = 1e-6) -> bool:
    required_ints = ["trades", "wins", "losses", "max_conc", "errors"]
    for k in required_ints:
        if int(row.get(k, -999999)) != int(EXPECTED_RESULT[k]):
            return False
    if bool(row.get("ruined", True)) != bool(EXPECTED_RESULT["ruined"]):
        return False
    for k in ["max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(row.get(k, float("nan"))) - float(EXPECTED_RESULT[k])) > tol:
            return False
    return True

if __name__ == "__main__":
    print("strategy=", STRATEGY)
    print("source_candidate=", SOURCE_CANDIDATE)
    print("spec=", asdict(StrategySpec()))
    print("expected=", EXPECTED_RESULT)
    print("cd_check=", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
