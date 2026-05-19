# LONG_MAIN_V22_RAW_TOP_RETEST 결과 해석 가이드

## 기준선
- strategy: 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18
- entry_key: child::orig_V09_extreme_vol18::tp03
- source of truth: long_main v21 rank1 retest exact logic embedded; v13 entry source remains frozen
- 외부 경로 참조 없음
- 결과 폴더는 실행 위치 기준 local_results/long_main 안에 생성

## 기준선 exact audit
- pass_frozen_reproduction_gate: True

## 판정
기준선 exact 재현 통과. summary_long_main_mdd_lt5.csv와 summary_long_max_cd_rank.csv에서 리테스트 후보를 비교한다.

## long_main 기준 1위
- strategy: LM22R_068_RETEST_STOP120_RR500_BODY020_HOLD17
- cd: 539.1375335808302
- mdd: 1.4424051244910419

## long_max식 cd 기준 1위
- strategy: LM22R_068_RETEST_STOP120_RR500_BODY020_HOLD17
- cd: 539.1375335808302
- mdd: 1.4424051244910419
