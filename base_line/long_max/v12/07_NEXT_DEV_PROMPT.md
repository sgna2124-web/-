# LONG MAX v12 다음 개발 시작 지시문

다음 long_max 개선은 아래 기준선을 0번 exact 후보로 넣고 시작한다.

기준선:
LONG_MAX_V12_LM26_S128_RR505_B360_H17_CD32

필수 고정:
entry_source = child::orig_V09_extreme_vol18::tp03
entry_source_atr_stop = 1.10
entry_source_rr_target = 3.80
tp03_min_target_pct = 0.30
final_atr_stop = 1.28
final_rr_target = 5.05
body_atr_min = 0.36
max_hold_bars = 17
cooldown_bars = 32
round_trip_cost_bps = 8.0
position_fraction = 0.01
2025년까지 데이터만 사용

공식 expected:
trades 55821
wins 22425
losses 33396
win_rate_pct 40.17305315203956
final_return_pct 508.8757953955824
max_return_pct 510.01650319972197
max_drawdown_pct 1.0930827574126778
official_cd_value 603.3485179858741
symbol_files 597
errors 0
ruined false

max_conc는 진단값으로만 사용한다.

개선 방향:
body_atr 0.34~0.44
cooldown 32~34
stop 1.27~1.31
rr 5.00~5.15
hold 17~19

상위 후보가 나오면 단독 리테스트 후 기준선 갱신한다.
