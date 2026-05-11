# LONG_MAIN_DEV_V12 결과 해석 가이드

## 기준선
- strategy: 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110
- entry_key: child::orig_V09_extreme_vol18::tp03
- source of truth: base_line/long_max/v3/03_FROZEN_BASELINE_RUNNER.py 핵심 로직 내장
- 외부 경로 참조 없음
- 결과 폴더는 실행 위치 기준 local_results/long_main 안에 생성

## 기준선 exact audit
- pass_frozen_reproduction_gate: True

## 판정
기준선 exact 재현 통과. summary_long_main_mdd_lt5.csv와 summary_long_max_cd_rank.csv에서 기준선 초과 후보를 비교한다.

## long_main 기준 1위
- strategy: LM12_050_V7_BODY025
- cd: 338.45478478360224
- mdd: 1.3408670828357394

## long_max식 cd 기준 1위
- strategy: LM12_050_V7_BODY025
- cd: 338.45478478360224
- mdd: 1.3408670828357394
