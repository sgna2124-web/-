# LONG MAIN v18 FROZEN RUNNER

공식 frozen runner:
`run_long_max_v35_v34_top1_retest_standalone.py`

공식 전략:
`LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`

공식 expected:
- official_cd_value 618.2592886468248
- max_drawdown_pct 1.3626489750456883
- trades 55597
- wins 22513
- losses 33084

공식 검증 파일:
- official_expected.json
- official_baseline_snapshot.csv

재현 절차:
1. frozen runner 실행
2. 결과 csv 생성 확인
3. 전략 행이 official_baseline_snapshot.csv와 완전히 일치하는지 비교
4. 값 하나라도 다르면 재현 실패

금지:
- 이전 long_main v17 expected 값 사용 금지
- official_cd_value 대신 cd_value 비교 금지
- body_atr_min 0.36 사용 금지
- rr_target 5.05 사용 금지
