# long_main v9 기준선 재현 시작 문서

## 공식 기준선

- axis: long_main
- version: v9
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`

## 공식 결과값

| 항목 | 값 |
|---|---:|
| trades | 57035 |
| wins | 20451 |
| losses | 36584 |
| win_rate_pct | 35.8569299553 |
| final_return_pct | 305.0347181084 |
| max_return_pct | 305.8775211164 |
| max_drawdown_pct | 1.2432451599 |
| official_cd_value | 400.8314684802 |
| max_conc | 441 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 갱신 이유

long_main 기준은 `MDD 5% 미만 전략 중 official_cd_value 최대`다. v9는 MDD가 `1.2432451599%`로 5% 미만이고, cd_value가 v8 `363.5507495661`보다 높다. V17 단독 리테스트에서 V16 탐색 1위 결과와 동일하게 재현되었으므로 v9로 갱신한다.

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

cd_value 계산에는 final_return_pct가 아니라 max_return_pct를 사용한다.

## 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.50 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |
| warmup_bars | 120 |
| min_bars | 250 |
| max_bars | 0, 전체 캔들 사용 |

## 진입 구조

이 전략의 진입 조건은 v8과 동일하다. 바뀐 것은 `rr_target 3.20 → 3.50`이다.

`family_signal_V09 = shock_down OR l01 OR shock_balance`

`anchor_extreme = raw_extreme_reclaim OR rsi14 <= 34.0`

`guard_vol18 = vol_ratio >= 1.18`

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

`tp03_gate = ((atr_stop * atr14 * rr_target / close) * 100.0) >= 0.30`

`final_entry = parent_entry AND tp03_gate`

v9에서는 `atr_stop = 1.10`, `rr_target = 3.50`이므로 TP03 계산도 이 값을 기준으로 한다.

## 재현 성공 판정

1. trades == 57035
2. wins == 20451
3. losses == 36584
4. errors == 0
5. ruined == false
6. official_cd_value가 400.8314684802 근처일 것
7. max_drawdown_pct가 1.2432451599 근처일 것
8. max_return_pct가 305.8775211164 근처일 것

## 다음 개발 기준

long_main 다음 개선 목표는 `max_drawdown_pct < 5` 유지와 `official_cd_value > 400.8314684802` 달성이다.

인수인계 문장:

`long_main 현재 기준선은 v9 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350이다. 기준선 재현값은 trades 57035, wins 20451, losses 36584, MDD 1.2432451599, cd_value 400.8314684802이다. 진입 조건은 V09/extreme/vol18/TP03이고, v8에서 rr_target만 3.20에서 3.50으로 바뀐 전략이다.`
