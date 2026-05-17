# long_main v13 진입 조건 및 청산 조건

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18`

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 핵심 변경점

v13은 v12의 `body_atr >= 0.25` 필터 계승형이 아니다. V24에서 발견된 `long_max v7` entry 기반 조합을 V25에서 새 기준선 v8/v12와 단독 비교해 승격한 전략이다.

v12 대비:

- v12 final_entry: `long_max_v7_frozen_entry AND body_atr >= 0.25`
- v13 final_entry: `child::orig_V09_extreme_vol18::tp03`
- v12 청산: `atr_stop 1.15`, `rr_target 5.20`, `max_hold 21`, `cooldown 31`
- v13 청산: `atr_stop 1.12`, `rr_target 4.70`, `max_hold 18`, `cooldown 31`

## 공식 재현값: 2025년까지의 기록

- trades: `56697`
- wins: `20962`
- losses: `35735`
- win_rate_pct: `36.97197382577562`
- final_return_pct: `405.1480528315248`
- max_return_pct: `405.8734002703171`
- max_drawdown_pct: `1.228290350505734`
- official_cd_value: `499.6598061090216`
- max_conc: `444`
- symbol_files: `597`
- errors: `0`
- ruined: `false`

## 진입 구조

최종 entry:

`final_entry = child::orig_V09_extreme_vol18::tp03`

parent 전략 계열:

`8V4_V09_V054_extreme_vol18`

개념식:

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

구성:

- `family_signal_V09 = raw_shock_down_at OR raw_l01_signal_at OR raw_shock_reversal_balance_at`
- `anchor_extreme = raw_extreme_reclaim_at OR rsi14 <= 34.0`
- `guard_vol18 = vol_ratio >= 1.18`

TP03 게이트:

`target_pct = (entry_atr_stop * atr14 * entry_rr_target / close) * 100.0`

`tp03_gate = target_pct >= 0.30`

주의: 이 전략의 entry_key는 `child::orig_V09_extreme_vol18::tp03`이다. V25 단독 리테스트에서는 후보 조건 그대로 비교했다. 새 v8/v12 기준선의 `body_atr >= 0.25` 필터를 후보에 강제로 추가하지 않았다.

## 청산 조건

| 항목 | 값 |
|---|---:|
| atr_stop | 1.12 |
| rr_target | 4.70 |
| max_hold_bars | 18 |
| cooldown_bars | 31 |
| round_trip_cost_bps | 8.0 |
| position_fraction | 0.01 |

청산 구조:

1. 진입 시점의 ATR14를 사용한다.
2. `stop_dist = atr_stop * atr14`
3. `stop_price = entry_price - stop_dist`
4. `target_price = entry_price + stop_dist * rr_target`
5. 같은 봉에서 stop과 target이 동시에 발생하면 stop 우선 처리한다.
6. target hit면 목표가 청산한다.
7. stop hit면 손절 청산한다.
8. max_hold_bars 도달 시 시간 청산한다.
9. 청산 후 cooldown_bars 동안 같은 심볼 재진입 금지.
10. 수익률 계산 시 왕복 수수료 8bps를 차감한다.
11. 포지션 비중 0.01로 equity curve를 계산한다.

## 신호/진입/청산 타이밍 주의사항

- 신호 봉 `signal_i`에서 조건을 계산한다.
- 실제 진입은 반드시 `entry_i = signal_i + 1`에서 수행한다.
- 5분봉 12:00 신호는 12:00~12:04:59 데이터가 확정된 뒤 12:05 open에서만 진입 가능하다.
- 청산 봉 `exit_i` 이후 `next_allowed_signal_i = exit_i + cooldown_bars`로 다음 허용 신호를 제한한다.
- 청산이 발생한 봉 내부에서 같은 봉 재진입은 허용하지 않는다.
