# LONG MAIN v18 START HERE

이 폴더가 현재 long_main 공식 기준선이다.

공식 전략명:
`LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`

공식 결과 소스:
`local_results/long_max/LONG_MAX_V16_2025_V34_TOP1_RETEST_V35_STANDALONE`

공식 판정:
- 2025년까지 데이터 기준
- 597개 심볼
- round_trip_cost_bps 8.0
- position_fraction 0.01
- errors 0
- ruined false
- V35 단독 리테스트에서 동일 후보 재현 성공
- long_main v18 기준선으로 채택

중요:
이 기준선의 공식 expected 값은 V35 리테스트 1위 후보값이다.
이전 long_main v17 기준선 expected CD/MDD와 비교해 baseline_reproduction_ok를 판단하지 않는다.
이전 LM26 기준값 603.3485179858741은 과거 기준선 검증값이며, v18 기준선 검증에는 사용 금지다.

처음 재현하는 사람은 다음만 확인한다.

1. `08_STANDALONE_FROZEN_RUNNER.py`를 실행한다.
2. 데이터 폴더는 자동 탐색되며, 필요하면 `--data-root`로 지정한다.
3. 아래 전략 행을 확인한다.
   `LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`
4. 공식 기준값과 비교한다.
   - trades 55597
   - wins 22513
   - losses 33084
   - final_return_pct 525.6012732388051
   - max_drawdown_pct 1.3626489750456883
   - official_cd_value 618.2592886468248

재현 실패 판단 기준:
- errors가 0이 아니면 실패
- symbol_files가 597이 아니면 실패
- trades가 55597과 다르면 실패
- wins/losses가 22513/33084와 다르면 실패
- official_cd_value가 618.2592886468248과 다르면 실패
- max_drawdown_pct가 1.3626489750456883과 다르면 실패
