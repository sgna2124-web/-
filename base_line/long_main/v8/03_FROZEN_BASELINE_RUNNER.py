# -*- coding: utf-8 -*-
"""
long_main v8 frozen baseline runner 안내

공식 기준선:
8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320

공식 값:
trades=57065
wins=20612
losses=36453
win_rate_pct=36.1202137913
final_return_pct=267.6967217810
max_return_pct=268.4930973199
max_drawdown_pct=1.3412321126
official_cd_value=363.5507495661
max_conc=439
errors=0
ruined=False

전략 스펙:
entry_key=child::orig_V09_extreme_vol18::tp03
atr_stop=1.10
rr_target=3.20
max_hold_bars=21
cooldown_bars=31
position_fraction=0.01
round_trip_cost_bps=8.0

실제 단독 검증에 사용한 전체 실행 파일은 개발 산출물 V15다.
다음 파일명을 기준선 재현용으로 사용한다.

run_long_max_v3_single_top_retest_dev_v15.py

실행 시 결과 폴더는 코드 실행 위치 기준으로 생성된다.
./local_result/long_max/LONG_MAX_V3_SINGLE_TOP_RETEST_DEV_V15/

long_main v8과 long_max v4는 같은 전략을 기준선으로 사용한다.
차이는 선별 기준뿐이다.
long_main은 MDD 5% 미만 조건 안에서 cd_value 최대를 본다.
현재 MDD는 1.3412321126%로 long_main 조건을 통과한다.

재현 판정:
trades, wins, losses가 모두 같아야 한다.
cd_value는 max_return_pct와 max_drawdown_pct로 계산한다.
"""

EXPECTED_RESULT = {
    "strategy": "8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320",
    "trades": 57065,
    "wins": 20612,
    "losses": 36453,
    "win_rate_pct": 36.1202137913,
    "final_return_pct": 267.6967217810,
    "max_return_pct": 268.4930973199,
    "max_drawdown_pct": 1.3412321126,
    "official_cd_value": 363.5507495661,
    "max_conc": 439,
    "errors": 0,
    "ruined": False,
}


def official_cd_value(max_return_pct, max_drawdown_pct):
    return 100.0 * (1.0 - abs(max_drawdown_pct) / 100.0) * (1.0 + max_return_pct / 100.0)


def long_main_eligible(max_drawdown_pct):
    return max_drawdown_pct < 5.0


def reproduction_gate(actual, tol=1e-3):
    for key in ["trades", "wins", "losses", "max_conc", "errors"]:
        if int(actual.get(key, -1)) != EXPECTED_RESULT[key]:
            return False
    for key in ["max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    return True


if __name__ == "__main__":
    print("이 파일은 v8 공식 기준선 고정 안내 및 재현 판정 레퍼런스다.")
    print("V15 단독 리테스트 runner를 사용해 전체 재현을 수행한다.")
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
    print("long_main_eligible", long_main_eligible(EXPECTED_RESULT["max_drawdown_pct"]))
