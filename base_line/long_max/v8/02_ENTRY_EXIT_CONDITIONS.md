# long_max v8 진입/청산 조건

## 전략 식별

- source candidate: `LM18_041_STOP115_RR520_BODY025`
- final strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__LM18_stop115_rr520_body025`

## 진입 구조

```text
entry_source = long_max v7 frozen entry
final_entry = entry_source AND body_atr >= 0.25
```

entry_source는 v7 기준선의 entry다. long_main v12와 같은 진입 구조를 사용한다.

## TP03 gate 주의사항

- entry source TP03 계산: `atr_stop=1.10`, `rr_target=3.80`
- 최종 청산 계산: `atr_stop=1.15`, `rr_target=5.20`

최종 rr_target 5.20으로 TP03 gate를 다시 계산하지 않는다.

## 추가 필터

```text
body_atr = abs(close - open) / atr14
body_atr >= 0.25
```

## 청산 조건

| parameter | value |
|---|---:|
| atr_stop | 1.15 |
| rr_target | 5.20 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |

청산 우선순위:

1. stop/target을 각 캔들의 low/high로 확인한다.
2. 같은 캔들에서 stop과 target이 모두 닿으면 stop-first 처리한다.
3. max_hold_bars까지 미청산이면 time exit 처리한다.

## 수수료와 자산분할

| parameter | value |
|---|---:|
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 공식 cd 계산식

```text
official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)
```
