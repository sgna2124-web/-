# LONG MAIN v17 감사 사양

## 공식 기준선

LONG_MAIN_V17_LM26_S128_RR505_B360_H17_CD32

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

다음 항목은 exact 또는 허용 오차 내 일치해야 한다.

- trades
- wins
- losses
- win_rate_pct
- final_return_pct
- max_return_pct
- max_drawdown_pct
- official_cd_value
- symbol_files
- errors
- ruined

허용 오차:

- 정수 항목은 exact
- pct 및 cd 항목은 1e-6 이하 차이 허용

## max_conc 처리

max_conc는 공식 기준선 성과 판정에서 제외한다.
이 값은 동시 보유 진단 목적의 참고값이다.

## equity 누적

공식 equity는 symbol 정렬 순서와 각 symbol 내부 signal index 오름차순으로 생성된 pnl append 순서를 그대로 누적한다.
전체 trade를 timestamp로 다시 정렬해서 equity를 계산하지 않는다.

## max_drawdown 계산

위 equity 누적 경로에서 peak 대비 drawdown을 계산한다.
max_drawdown_pct는 1.0930827574126778이어야 한다.

## 수수료 및 포지션 반영

round_trip_cost_bps = 8.0
position_fraction = 0.01

pnl_pct는 trade 단위 수익률에서 왕복 수수료를 차감한 값이다.
equity 누적은 position_fraction 0.01을 반영한다.
