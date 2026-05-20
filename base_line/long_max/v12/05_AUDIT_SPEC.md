# LONG MAX v12 감사 사양

## 공식 기준선

LONG_MAX_V12_LM26_S128_RR505_B360_H17_CD32

## 공식 expected

trades = 55821
wins = 22425
losses = 33396
win_rate_pct = 40.17305315203956
final_return_pct = 508.8757953955824
max_return_pct = 510.01650319972197
max_drawdown_pct = 1.0930827574126778
official_cd_value = 603.3485179858741
symbol_files = 597
errors = 0
ruined = false

max_conc = diagnostic only
observed max_conc = 436 in standalone retest

## 공식 게이트

포함:
trades, wins, losses, win_rate_pct, final_return_pct, max_return_pct, max_drawdown_pct, official_cd_value, symbol_files, errors, ruined

제외:
max_conc

허용 오차:
정수 항목은 exact
pct 및 cd 항목은 1e-6 이하 차이 허용

## equity 누적

공식 equity는 symbol 정렬 순서와 각 symbol 내부 signal index 오름차순으로 생성된 pnl append 순서를 그대로 누적한다.
전체 trade를 timestamp로 재정렬하지 않는다.

## 수수료 및 자산분할

round_trip_cost_bps = 8.0
position_fraction = 0.01
