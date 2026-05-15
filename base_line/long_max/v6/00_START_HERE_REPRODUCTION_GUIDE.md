# long_max v6 기준선 재현 시작 문서

## 공식 기준선

- axis: long_max
- version: v6
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 공식 결과값: 2025년까지의 기록

| 항목 | 값 |
|---|---:|
| trades | 56673 |
| wins | 20255 |
| losses | 36418 |
| win_rate_pct | 35.740123162705345 |
| final_return_pct | 332.2800895520915 |
| max_return_pct | 332.5601665725121 |
| max_drawdown_pct | 1.2943172013524573 |
| official_cd_value | 426.96146593036525 |
| max_conc | 442 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 갱신 근거

- 탐색 배치: `LONG_MAX_V5_2025_BASELINE_ENTRY_DEV_V19`
- 단독 리테스트 배치: `LONG_MAX_V5_2025_SINGLE_TOP_RETEST_DEV_V20`
- 단독 재현 판정: `pass_single_retest_gate = true`
- long_max 갱신 판정: `long_max_update_candidate = true`

v6는 v5 대비 진입 조건은 유지하고 `rr_target`만 3.50에서 3.80으로 상향한 전략이다. V19 탐색 1위가 V20 단독 리테스트에서 trades, wins, losses, cd_value까지 완전 일치했다.

## 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 3.80 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

cd_value 계산에는 final_return_pct가 아니라 max_return_pct를 사용한다.

## 재현 성공 판정

1. trades == 56673
2. wins == 20255
3. losses == 36418
4. errors == 0
5. ruined == false
6. official_cd_value가 426.96146593036525 근처일 것
7. max_drawdown_pct가 1.2943172013524573 근처일 것
8. max_return_pct가 332.5601665725121 근처일 것

## 다음 개발 기준

long_max 다음 개선 목표는 2025년까지의 데이터 기준 `official_cd_value > 426.96146593036525` 달성이다.
