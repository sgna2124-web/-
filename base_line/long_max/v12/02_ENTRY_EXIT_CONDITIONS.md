# LONG MAX v12 진입 및 청산 조건

## 기본 방향

long_max v12는 long_main v17과 동일한 LM26 리테스트 성공 조건을 사용한다. long_max 개발에서는 이 조건을 기준으로 CD 랭킹과 최대 성과를 더 공격적으로 개선한다.

## Entry source

entry_source:
child::orig_V09_extreme_vol18::tp03

TP03 source 파라미터:
entry_source_atr_stop = 1.10
entry_source_rr_target = 3.80
tp03_min_target_pct = 0.30

TP03 source는 반드시 위 값으로 만든다. final exit 값으로 source를 다시 만들면 안 된다.

## Final entry

final_entry = entry_source AND body_atr >= 0.36

body_atr = abs(close - open) / atr14

## 실제 진입

signal_i 조건 확정 후 다음 캔들 open에서 진입한다.

entry_i = signal_i + 1
entry_price = open[entry_i]

## 청산 조건

final_atr_stop = 1.28
final_rr_target = 5.05
max_hold_bars = 17
cooldown_bars = 32

risk = final_atr_stop * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * final_rr_target

같은 캔들에서 stop과 target이 동시에 닿으면 stop 우선이다.

## Cooldown

next_allowed_signal_i = exit_i + cooldown_bars

v12에서는 cooldown_bars = 32다.

## 수수료 및 자산분할

round_trip_cost_bps = 8.0
position_fraction = 0.01

## 데이터 범위

2025년까지 사용한다. 2026년 데이터는 제외한다.
