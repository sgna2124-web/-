# long_main v11 진입/청산 조건

## 핵심 원칙

이 문서는 사람이 이해하기 위한 설명이다. 실제 재현은 반드시 `03_FROZEN_BASELINE_RUNNER.py`의 구현을 따른다.

전략명을 보고 조건을 재해석하지 않는다. `V09`, `extreme`, `vol18`, `tp03`이라는 이름만으로 유사 조건을 만들면 안 된다.

## 전략명

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420`

## 축

- axis: long_main
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

단, 위 개념 구조는 설명용이다. 정확한 Boolean 구현은 frozen runner의 `compute_entry_masks()`와 그 하위 raw signal 함수들을 그대로 따른다.

## 진입 실행 타이밍

- signal_i 캔들에서 조건을 계산한다.
- 실제 진입은 `entry_i = signal_i + 1` 캔들의 open 가격으로 처리한다.
- 캔들 시간 기준으로 12:00 5분봉 조건은 12:00~12:04:59까지 완성된 캔들을 뜻하므로, 실제 진입은 12:05 캔들 open이다.

## 청산 조건

고정 파라미터:

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

1. 진입 후 각 캔들에서 low <= stop_price, high >= target_price 여부를 확인한다.
2. 같은 캔들에서 stop과 target이 모두 닿으면 보수적으로 stop-first 처리한다.
3. max_hold_bars까지 stop/target이 없으면 time exit 처리한다.

## 청산 후 다음 진입 가능 조건

현재 frozen 기준선의 재현 규칙은 기존 기준선 계열과 동일한 청산 후 cooldown 처리 방식을 따른다.

```text
next_allowed_signal_i = exit_i + cooldown_bars
```

현재 cooldown_bars가 31이므로 같은 캔들 재진입 문제는 실질적으로 발생하지 않는다. 만약 향후 시간 규칙을 `exit_i + 1 + cooldown_bars`로 변경한다면 기존 기준선과 다른 백테스트 규칙이 되므로, 모든 기준선과 후보를 같은 새 규칙으로 다시 리테스트해야 한다.

## 수수료와 자산분할

| 항목 | 값 |
|---|---:|
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

수익률 계산 시 왕복 수수료는 0.08%로 차감한다.

## TP03 gate

최종 entry는 TP03 gate를 포함한다. 이 gate는 기준선 후보의 손익비 구조에서 기대 target_pct가 0.30% 이상인 경우만 통과시키는 역할이다.

정확한 계산은 frozen runner의 `compute_entry_masks()` 구현을 따른다.
