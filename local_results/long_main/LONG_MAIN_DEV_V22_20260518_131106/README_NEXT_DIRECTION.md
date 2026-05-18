# LONG_MAIN_DEV_V22 결과 해석 가이드

## 기준선
- strategy: 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18
- entry_key: child::orig_V09_extreme_vol18::tp03
- source of truth: long_main v21 rank1 retest exact logic embedded; v13 entry source remains frozen
- 외부 경로 참조 없음
- 결과 폴더는 실행 위치 기준 local_results/long_main 안에 생성

## 기준선 exact audit
- pass_frozen_reproduction_gate: False

## 판정
기준선 exact 재현 실패. 개선 후보 평가는 전부 무효 처리한다.
summary_all.csv는 원인 추적용으로만 본다.
