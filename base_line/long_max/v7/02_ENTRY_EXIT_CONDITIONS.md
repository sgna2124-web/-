# long_max v7 진입/청산 조건

## 핵심 원칙

이 문서는 사람이 이해하기 위한 설명이다. 실제 재현은 반드시 `03_FROZEN_BASELINE_RUNNER.py`의 상수와 v15에서 exact 통과한 엔진 구조를 따른다.

전략명을 보고 조건을 재해석하지 않는다. `V09`, `extreme`, `vol18`, `tp03`이라는 이름만으로 유사 조건을 만들면 안 된다.

## 전략명

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420`

## 축

- axis: long_max
- side: long
- result_scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`

## 기준 진입 구조

- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`

개념 구조:

```text
family_signal_V09
AND anchor_extreme
AND guard_vol18
AND tp03_gate
```

단, 위 개념 구조는 설명용이다. 정확한 Boolean 구현은 기존 frozen runner의 `compute_entry_masks()`와 그 하위 raw signal 함수들을 그대로 따른다.

## 청산 조건

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 4.20 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |

청산 가격:

```text
stop_price = entry_price - atr_stop * atr14[signal_i]
target_price = entry_price + atr_stop * atr14[signal_i] * rr_target
```

청산 우선순위:

1. stop/target을 각 캔들의 low/high로 확인한다.
2. 같은 캔들에서 stop과 target이 모두 닿으면 stop-first 처리한다.
3. max_hold_bars까지 미청산이면 time exit 처리한다.

## 수수료와 자산분할

| 항목 | 값 |
|---|---:|
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 다음 진입 가능 시점

현재 frozen 기준선은 기존 계열과 동일하게 다음 규칙을 따른다.

```text
next_allowed_signal_i = exit_i + cooldown_bars
```

cooldown_bars가 31이므로 같은 캔들 재진입 문제는 실질적으로 발생하지 않는다. 시간 규칙을 바꿀 경우 모든 기준선을 동일 규칙으로 재산출해야 한다.
