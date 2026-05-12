# long_max v4 기준선 재현 시작 문서

이 폴더는 long_max v4 공식 기준선을 처음 보는 작업자도 같은 값으로 재현하고, 그 기준선에서 다음 개선을 시작하게 만들기 위한 기준선 폴더다.

## 1. 현재 공식 기준선

- axis: long_max
- version: v4
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- family: `V09`
- anchor: `extreme`
- guard: `vol18`
- child filter: `TP expected >= 0.3%`
- exit profile: `DEV13 atr_stop 1.10 + DEV14 rr_target 3.20`

## 2. 공식 결과값

아래 값이 재현 기준이다. 이 값과 다르면 기준선 재현 실패다.

| 항목 | 값 |
|---|---:|
| trades | 57065 |
| wins | 20612 |
| losses | 36453 |
| win_rate_pct | 36.1202137913 |
| final_return_pct | 267.6967217810 |
| max_return_pct | 268.4930973199 |
| max_drawdown_pct | 1.3412321126 |
| official_cd_value | 363.5507495661 |
| max_conc | 439 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 3. 갱신 이유

이전 long_max v3 기준선:

- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`
- cd_value: `336.7657621418`
- MDD: `1.3408670828%`

새 v4 기준선:

- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`
- cd_value: `363.5507495661`
- MDD: `1.3412321126%`

long_max 기준은 `MDD 제한 없이 official_cd_value 최대`다. v4는 v3보다 cd_value가 높다. V15 단독 리테스트에서 V14 탐색 결과와 동일하게 재현되었으므로 v4로 갱신한다.

## 4. 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

주의:

- cd_value 계산에는 `final_return_pct`가 아니라 `max_return_pct`를 사용한다.
- long_max는 MDD 제한 없이 cd_value 최대를 본다.

## 5. 재현에 필요한 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.20 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |
| warmup_bars | 120 |
| min_bars | 250 |
| timeframe | 5m |
| max_bars | 0, 전체 캔들 사용 |

## 6. 정확한 진입 구조

이 전략의 진입 조건은 v3과 동일하다. 바뀐 것은 청산/리스크 파라미터 중 `rr_target`뿐이다.

개념식:

`family_signal_V09 = shock_down OR l01 OR shock_balance`

`anchor_extreme = raw_extreme_reclaim OR rsi14 <= 34.0`

`guard_vol18 = vol_ratio >= 1.18`

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

`tp03_gate = ((atr_stop * atr14 * rr_target / close) * 100.0) >= 0.30`

`final_entry = parent_entry AND tp03_gate`

v4에서는 `atr_stop = 1.10`, `rr_target = 3.20`이므로 TP03 계산도 이 값을 기준으로 한다.

## 7. 절대 하면 안 되는 재현 방식

1. `V09`, `extreme`, `vol18`이라는 이름만 보고 조건을 새로 추측하지 않는다.
2. v3의 `rr_target = 2.90`을 그대로 쓰지 않는다. v4는 `rr_target = 3.20`이다.
3. `final_return_pct`로 cd_value를 계산하지 않는다.
4. 기준선 재현값이 다르게 나오는데도 그 결과를 기준으로 개선하지 않는다.
5. trades/wins/losses가 다르면 결과가 비슷해도 재현 실패로 본다.

## 8. 재현 성공 판정

다음 조건을 모두 만족해야 한다.

1. trades == 57065
2. wins == 20612
3. losses == 36453
4. errors == 0
5. ruined == false
6. official_cd_value가 363.5507495661 근처일 것
7. max_drawdown_pct가 1.3412321126 근처일 것
8. max_return_pct가 268.4930973199 근처일 것

## 9. 다음 개발 기준

long_max 다음 개선 목표:

- `official_cd_value > 363.5507495661` 달성

허용되는 개선:

1. `baseline_entry AND 추가 필터`
2. `baseline_entry OR 근접 parent 신호`
3. `baseline_entry` 유지 + 청산 파라미터 조정
4. `baseline_entry` 유지 + cooldown/max_hold 조정
5. TP03 게이트 강화 또는 완화

인수인계 문장:

`long_max 현재 기준선은 v4 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320이다. 기준선 재현값은 trades 57065, wins 20612, losses 36453, MDD 1.3412321126, cd_value 363.5507495661이다. 진입 조건은 V09/extreme/vol18/TP03이고, v3에서 rr_target만 2.90에서 3.20으로 바뀐 전략이다.`
