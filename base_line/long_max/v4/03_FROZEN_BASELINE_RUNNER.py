# -*- coding: utf-8 -*-
"""
long_max v4 frozen baseline runner 안내

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

이 파일은 기준선 폴더 안에서 v4 공식값과 실행 규칙을 고정해두는 안내 파일이다.
전체 runner 본체를 기준선 폴더에 통째로 넣어야 하는 경우, V15 파일 내용을 이 파일 위치로 복사하되 아래 항목만 v4 기준으로 유지한다.

RUN_LABEL = LONG_MAX_V4_FROZEN_BASELINE
strategy = 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320
rr_target = 3.20
EXPECTED_RESULT = 위 공식 값

재현 판정:
trades, wins, losses가 모두 같아야 한다.
cd_value는 max_return_pct와 max_drawdown_pct로 계산한다.
long_max는 MDD 제한 없이 cd_value 최대 기준이다.
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


def reproduction_gate(actual, tol=1e-3):
    for key in ["trades", "wins", "losses", "max_conc", "errors"]:
        if int(actual.get(key, -1)) != EXPECTED_RESULT[key]:
            return False
    for key in ["max_return_pct", "max_drawdown_pct", "official_cd_value"]:
        if abs(float(actual.get(key, 1e99)) - EXPECTED_RESULT[key]) > tol:
            return False
    return True


if __name__ == "__main__":
    print("이 파일은 v4 공식 기준선 고정 안내 및 재현 판정 레퍼런스다.")
    print("V15 단독 리테스트 runner를 사용해 전체 재현을 수행한다.")
    print(EXPECTED_RESULT)
    print("cd", official_cd_value(EXPECTED_RESULT["max_return_pct"], EXPECTED_RESULT["max_drawdown_pct"]))
