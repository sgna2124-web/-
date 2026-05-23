# LONG MAX v13 START HERE

이 폴더가 현재 long_max 공식 기준선이다.

공식 전략명:
`LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`

공식 결과 소스:
`local_results/long_max/LONG_MAX_V16_2025_V34_TOP1_RETEST_V35_STANDALONE`

long_max v13은 long_main v18과 동일한 진입 및 청산 조건을 사용한다.
두 축은 같은 frozen runner, 같은 expected json, 같은 snapshot csv로 검증한다.

공식 판정:
- 2025년까지 데이터 기준
- 597개 심볼
- round_trip_cost_bps 8.0
- position_fraction 0.01
- errors 0
- ruined false
- V35 단독 리테스트에서 동일 후보 재현 성공
- long_max v13 기준선으로 채택

공식 기준값:
- trades 55597
- wins 22513
- losses 33084
- final_return_pct 525.6012732388051
- max_return_pct 526.8003775673284
- max_drawdown_pct 1.3626489750456883
- official_cd_value 618.2592886468248
- max_conc 446

중요:
이전 long_max v12 / long_main v17 expected 값은 v13 검증에 사용하지 않는다.
이전 LM26 기준 CD 603.3485179858741은 과거 기준선 값이며, v13에서는 공식 expected가 아니다.

재현 순서:
1. `08_STANDALONE_FROZEN_RUNNER.py` 실행
2. 결과 CSV 생성 확인
3. `official_baseline_snapshot.csv`와 공식 전략 행 비교
4. 값 하나라도 다르면 재현 실패
