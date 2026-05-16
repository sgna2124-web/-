# long_main v12 진입/청산 조건

## 전략 식별

- source candidate: `LM18_041_STOP115_RR520_BODY025`
- final strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__LM18_stop115_rr520_body025`

## 진입 구조

최종 entry는 다음 구조다.

```text
entry_source = long_main v11 frozen entry
final_entry = entry_source AND body_atr >= 0.25
```

여기서 `entry_source`는 v11 기준선의 entry이며, 다시 풀면 다음 개념 구조다.

```text
family_signal_V09
AND anchor_extreme
AND guard_vol18
AND tp03_gate
```

단, 위 식은 설명용이다. 실제 Boolean 구현은 v18에서 기준선 exact가 통과한 `compute_core_masks()` 계열 구현을 따른다.

## TP03 gate 주의사항

v12의 가장 중요한 재현 포인트는 TP03 계산 기준이다.

- entry source TP03 계산: `atr_stop=1.10`, `rr_target=3.80`
- 최종 청산 계산: `atr_stop=1.15`, `rr_target=5.20`

즉, 최종 전략의 rr_target 5.20으로 TP03 gate를 다시 계산하면 안 된다. 그렇게 하면 공식 v12와 다른 전략이 된다.

## 추가 필터

```text
body_atr = abs(close - open) / atr14
body_atr >= 0.25
```

이 필터는 LM18_041에서 손실 거래를 줄이고 cd_value를 끌어올린 핵심 조건이다.

## 청산 조건

| parameter | value |
|---|---:|
| atr_stop | 1.15 |
| rr_target | 5.20 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |

롱 포지션 청산 가격:

```text
risk = atr_stop * atr14[signal_i]
stop_price = entry_price - risk
target_price = entry_price + risk * rr_target
```

청산 우선순위:

1. 진입 후 각 캔들에서 low <= stop_price 여부를 확인한다.
2. 같은 캔들에서 stop과 target이 동시에 닿으면 stop-first로 처리한다.
3. target만 닿으면 target exit 처리한다.
4. max_hold_bars까지 stop/target이 없으면 time exit 처리한다.

## 진입 타이밍

- signal_i 캔들에서 entry 조건을 계산한다.
- 실제 진입은 `entry_i = signal_i + 1` 캔들의 open 가격으로 처리한다.
- 5분봉에서 12:00 캔들의 조건은 12:00~12:04:59 완성 캔들이므로 실제 진입은 12:05 open이다.

## 수수료와 자산분할

| parameter | value |
|---|---:|
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 공식 cd 계산식

```text
official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)
```

final_return_pct가 아니라 max_return_pct를 사용한다.
