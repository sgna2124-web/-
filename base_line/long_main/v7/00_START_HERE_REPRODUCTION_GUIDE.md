# long_main v7 기준선 재현 시작 문서

이 폴더는 long_main v7 기준선을 처음 보는 작업자도 같은 값으로 재현하고, 그 기준선에서 다음 개선을 시작하게 만들기 위한 공식 기준선 폴더다.

## 1. 현재 공식 기준선

- axis: long_main
- version: v7
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- family: `V09`
- anchor: `extreme`
- guard: `vol18`
- child filter: `TP expected >= 0.3%`
- exit profile: `risk_rr_plus20 + DEV13 atr_stop 1.10`

## 2. 공식 결과값

아래 값이 재현 기준이다. 이 값과 다르면 기준선 재현 실패다.

| 항목 | 값 |
|---|---:|
| trades | 57114 |
| wins | 20911 |
| losses | 36203 |
| win_rate_pct | 36.6127394334 |
| final_return_pct | 240.7307747654 |
| max_return_pct | 241.3427142366 |
| max_drawdown_pct | 1.3408670828 |
| official_cd_value | 336.7657621418 |
| max_conc | 435 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 3. 이전 기준선 대비 갱신 이유

이전 long_main v6 기준선:

- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`
- cd_value: `311.3750675807`
- MDD: `1.2219870757%`

새 v7 기준선:

- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`
- cd_value: `336.7657621418`
- MDD: `1.3408670828%`

long_main 기준은 `MDD 5% 미만 전략 중 cd_value 최대`다. v7은 MDD가 1.3408670828%로 5% 미만이고, cd_value가 v6보다 +25.3906945610 높다. 따라서 long_main v7로 갱신한다.

## 4. 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

주의:

- cd_value 계산에는 `final_return_pct`가 아니라 `max_return_pct`를 사용한다.
- long_main 후보는 반드시 `max_drawdown_pct < 5`를 통과해야 한다.

## 5. 재현에 필요한 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 2.90 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |
| warmup_bars | 120 |
| min_bars | 250 |
| timeframe | 5m |
| max_bars | 0, 전체 캔들 사용 |

## 6. 정확한 진입 구조

이 전략의 진입 조건은 v6/v2 기준선과 동일하다. 바뀐 것은 청산/리스크 파라미터 중 `atr_stop`뿐이다.

개념식:

`family_signal_V09 = shock_down OR l01 OR shock_balance`

`anchor_extreme = raw_extreme_reclaim OR rsi14 <= 34.0`

`guard_vol18 = vol_ratio >= 1.18`

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

`tp03_gate = ((atr_stop * atr14 * rr_target / close) * 100.0) >= 0.30`

`final_entry = parent_entry AND tp03_gate`

v7에서는 `atr_stop = 1.10`, `rr_target = 2.90`이므로 TP03 계산도 이 값을 기준으로 한다.

## 7. 절대 하면 안 되는 재현 방식

1. `V09`, `extreme`, `vol18`이라는 이름만 보고 조건을 새로 추측하지 않는다.
2. v6의 `atr_stop = 1.01`을 그대로 쓰지 않는다. v7은 `atr_stop = 1.10`이다.
3. `final_return_pct`로 cd_value를 계산하지 않는다.
4. 기준선 재현값이 다르게 나오는데도 그 결과를 기준으로 개선하지 않는다.
5. trades/wins/losses가 다르면 결과가 비슷해도 재현 실패로 본다.

## 8. 청산 구조

1. 진입 시 entry_price를 정한다.
2. stop_dist = atr_stop * atr14
3. stop_price = entry_price - stop_dist
4. target_price = entry_price + stop_dist * rr_target
5. 이후 봉에서 stop 또는 target 도달 여부를 확인한다.
6. 같은 봉에서 stop과 target이 동시에 맞으면 stop을 우선 처리한다.
7. target 도달 시 target 청산한다.
8. stop 도달 시 stop 청산한다.
9. max_hold_bars 초과 시 시간 청산한다.
10. 청산 후 cooldown_bars 동안 같은 심볼 재진입을 막는다.
11. 왕복 수수료 8bps를 반영한다.
12. position_fraction 0.01로 equity curve를 계산한다.

## 9. 재현 성공 판정

다음 조건을 모두 만족해야 한다.

1. trades == 57114
2. wins == 20911
3. losses == 36203
4. errors == 0
5. ruined == false
6. official_cd_value가 336.7657621418 근처일 것
7. max_drawdown_pct가 1.3408670828 근처일 것
8. max_return_pct가 241.3427142366 근처일 것

## 10. 다음 개발 기준

long_main 다음 개선 목표:

- `max_drawdown_pct < 5` 유지
- `official_cd_value > 336.7657621418` 달성

허용되는 개선:

1. `baseline_entry AND 추가 방어 필터`
2. `baseline_entry AND 과열 회피 필터`
3. `baseline_entry AND max_conc 감소 필터`
4. `baseline_entry` 유지 + 청산 파라미터 조정
5. `baseline_entry` 유지 + cooldown/max_hold 조정

인수인계 문장:

`long_main 현재 기준선은 v7 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110이다. 기준선 재현값은 trades 57114, wins 20911, losses 36203, MDD 1.3408670828, cd_value 336.7657621418이다. 진입 조건은 V09/extreme/vol18/TP03이고, v6에서 atr_stop만 1.01에서 1.10으로 바뀐 전략이다.`
