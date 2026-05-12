# long_main v9 진입 조건 및 청산 조건

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`

## 1. 핵심 변경점

v9는 v8의 진입 조건을 그대로 사용한다. 개선된 부분은 청산/리스크 파라미터다.

- v8 rr_target: `3.20`
- v9 rr_target: `3.50`
- atr_stop: `1.10`, 유지
- max_hold_bars: `21`, 유지
- cooldown_bars: `31`, 유지
- entry_key: `child::orig_V09_extreme_vol18::tp03`, 유지

따라서 v9는 신규 진입 조건 전략이 아니라, 기준선 진입 조건을 유지한 수익 목표 배율 개선 전략이다.

## 2. parent entry

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

## 3. child entry

최종 entry:

`final_entry = parent_entry AND tp03_gate`

TP03 게이트:

`target_pct = (atr_stop * atr14 * rr_target / close) * 100.0`

`tp03_gate = target_pct >= 0.30`

v9에서는 다음 값을 사용한다.

- `atr_stop = 1.10`
- `rr_target = 3.50`

따라서 entry_key 이름은 같아도 TP03 계산에 들어가는 rr_target이 3.50으로 바뀌므로 실제 진입 수는 v8과 달라질 수 있다.

## 4. 청산 조건

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.50 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| round_trip_cost_bps | 8.0 |
| position_fraction | 0.01 |

청산 구조:

1. 진입 시점의 ATR14를 사용한다.
2. `stop_dist = atr_stop * atr14`
3. `stop_price = entry_price - stop_dist`
4. `target_price = entry_price + stop_dist * rr_target`
5. 이후 봉에서 stop/target hit 여부를 확인한다.
6. 같은 봉에서 stop과 target이 동시에 발생하면 stop 우선 처리한다.
7. target hit면 목표가 청산한다.
8. stop hit면 손절 청산한다.
9. max_hold_bars 도달 시 시간 청산한다.
10. 청산 후 cooldown_bars 동안 같은 심볼 재진입 금지.
11. 수익률 계산 시 왕복 수수료 8bps를 차감한다.
12. 포지션 비중 0.01로 equity curve를 계산한다.

## 5. 재현 주의사항

- v8의 `rr_target = 3.20`을 쓰면 안 된다.
- v9는 `rr_target = 3.50`이다.
- entry_key는 같아도 TP03 계산에 rr_target이 들어가므로 v8과 진입 수가 달라진다.
- `vol_ratio`, `rsi14`, `atr14` 계산 방식이 다르면 재현에 실패한다.
- 마지막 봉 진입 여부, warmup 처리, cooldown 처리, 동일봉 stop/target 우선순위가 달라도 재현에 실패한다.

## 6. 공식 재현값

- trades: `57035`
- wins: `20451`
- losses: `36584`
- MDD: `1.2432451599`
- cd_value: `400.8314684802`
