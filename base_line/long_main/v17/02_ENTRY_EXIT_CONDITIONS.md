# LONG MAIN v17 진입 및 청산 조건

## 기본 방향

이 전략은 기존 long_main 계열을 완전히 교체한 신규 전략이 아니다. 기존 entry_source를 그대로 사용하고, final 필터와 청산 파라미터만 변경한 개발형 기준선이다.

## 데이터 조건

- 5분봉 OHLCV 사용
- 2025년까지의 데이터만 사용
- 2026년 데이터 제외
- symbol_files 기준 597

## Entry source

entry_source는 아래 원천 신호를 그대로 사용한다.

child::orig_V09_extreme_vol18::tp03

TP03 source 파라미터:

- entry_source_atr_stop = 1.10
- entry_source_rr_target = 3.80
- tp03_min_target_pct = 0.30

주의:
TP03 source는 source 단계에서 1.10 / 3.80 / min target 0.30으로 계산한다. final exit 파라미터인 1.28 / 5.05로 TP03 source를 다시 만들면 안 된다.

## Final entry filter

최종 진입은 entry_source에 body_atr 필터를 추가한다.

final_entry = entry_source AND body_atr >= 0.36

body_atr 계산:

body_atr = abs(close - open) / atr14

## 실제 진입 시점

signal_i 캔들에서 조건이 확정되면 실제 진입은 다음 캔들 open이다.

entry_i = signal_i + 1
entry_price = open[entry_i]

signal_i에서 바로 진입하지 않는다.

## 청산 조건

final_atr_stop = 1.28
final_rr_target = 5.05
max_hold_bars = 17
cooldown_bars = 32

Long 기준:

risk = final_atr_stop * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * final_rr_target

exit 탐색 범위:

entry_i부터 min(n - 1, entry_i + max_hold_bars)까지 확인한다.

같은 캔들에서 stop과 target이 동시에 닿으면 stop 우선이다.

max_hold까지 stop/target이 닿지 않으면 마지막 캔들의 close로 시간 청산한다.

## Cooldown

청산 후 다음 진입 가능 signal index:

next_allowed_signal_i = exit_i + cooldown_bars

v17에서는 cooldown_bars = 32다.

## 수수료 및 자산분할

round_trip_cost_bps = 8.0
position_fraction = 0.01

수수료는 왕복 8bps를 pnl_pct에서 차감한다.
자산 반영은 거래당 총자산의 1%만 사용한다.
