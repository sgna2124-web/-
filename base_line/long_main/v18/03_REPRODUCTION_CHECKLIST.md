# LONG MAIN v18 재현 체크리스트

실행 파일:
`08_STANDALONE_FROZEN_RUNNER.py`

공식 전략명:
`LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`

필수 파라미터:
- body_atr_min 0.40
- atr_stop 1.30
- rr_target 6.25
- max_hold_bars 17
- cooldown_bars 32
- round_trip_cost_bps 8.0
- position_fraction 0.01

공식 검증값:
- trades 55597
- wins 22513
- losses 33084
- final_return_pct 525.6012732388051
- max_drawdown_pct 1.3626489750456883
- official_cd_value 618.2592886468248
- symbol_files 597
- errors 0

다음 중 하나라도 다르면 재현 실패:
- trades 불일치
- wins/losses 불일치
- official_cd_value 불일치
- max_drawdown_pct 불일치
- symbol_files != 597
- errors != 0
