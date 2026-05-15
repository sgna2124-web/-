# long_main v10 진입 조건 및 청산 조건

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380`

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 검증용으로 제외한다.

## 핵심 변경점

v10은 v9의 진입 조건을 그대로 사용한다. 개선된 부분은 청산/리스크 파라미터다.

- v9 rr_target: `3.50`
- v10 rr_target: `3.80`
- atr_stop: `1.10`, 유지
- max_hold_bars: `21`, 유지
- cooldown_bars: `31`, 유지
- entry_key: `child::orig_V09_extreme_vol18::tp03`, 유지

## 공식 재현값: 2025년까지의 기록

- trades: `56673`
- wins: `20255`
- losses: `36418`
- win_rate_pct: `35.740123162705345`
- final_return_pct: `332.2800895520915`
- max_return_pct: `332.5601665725121`
- max_drawdown_pct: `1.2943172013524573`
- official_cd_value: `426.96146593036525`
- max_conc: `442`
- symbol_files: `597`
- errors: `0`
- ruined: `false`

## 진입 구조

parent 전략:

`8V4_V09_V054_extreme_vol18`

parent entry_key:

`orig_V09_extreme_vol18`

개념식:

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

구성:

- `family_signal_V09 = raw_shock_down_at OR raw_l01_signal_at OR raw_shock_reversal_balance_at`
- `anchor_extreme = raw_extreme_reclaim_at OR rsi14 <= 34.0`
- `guard_vol18 = vol_ratio >= 1.18`

최종 entry:

`final_entry = parent_entry AND tp03_gate`

TP03 게이트:

`target_pct = (atr_stop * atr14 * rr_target / close) * 100.0`

`tp03_gate = target_pct >= 0.30`

v10에서는 `atr_stop = 1.10`, `rr_target = 3.80`이므로 TP03 계산도 이 값을 기준으로 한다.

## 청산 조건

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.80 |
| max_hold_bars | 21 |
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
