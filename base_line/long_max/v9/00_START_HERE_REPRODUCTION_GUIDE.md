# long_max v9 기준선 재현 시작 문서

## 공식 기준선

- axis: `long_max`
- version: `v9`
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18`
- side: `long`
- source_search_batch: `LONG_MAX_V7_2025_COMBO_ENTRY_DEV_V24`
- source_retest_batch: `LONG_MAX_V8_2025_SINGLE_RETEST_DEV_V25`
- source_candidate: `DEV24_near_stop112_rr470_hold18`
- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 공식 결과값: 2025년까지의 기록

| 항목 | 값 |
|---|---:|
| trades | 56697 |
| wins | 20962 |
| losses | 35735 |
| win_rate_pct | 36.97197382577562 |
| final_return_pct | 405.1480528315248 |
| max_return_pct | 405.8734002703171 |
| max_drawdown_pct | 1.228290350505734 |
| official_cd_value | 499.6598061090216 |
| max_conc | 444 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 갱신 근거

- 새 기준선 `long_max v8 / long_main v12`를 V25에서 먼저 exact 재현했다.
- v8/v12 기준선 cd_value: `491.134662921777`
- V25 단독 리테스트 후보 cd_value: `499.6598061090216`
- 개선폭: `+8.525143187244566`
- V25 판정: `baseline_reproduction_ok = true`, `top_is_update_candidate = true`, `long_max_update_candidate = true`, `long_main_update_candidate = true`

## 핵심 주의사항

이 v9 전략은 v8의 `body_atr >= 0.25` 필터를 계승한 전략이 아니다. V24에서 발견된 기존 `long_max v7` 계열 entry 기반 조합이며, V25에서 새 v8/v12 기준선을 먼저 재현한 뒤 동일 조건에서 비교해 더 우수함을 확인했다.

## 공식 진입/청산 파라미터

| 항목 | 값 |
|---|---:|
| entry_key | `child::orig_V09_extreme_vol18::tp03` |
| atr_stop | 1.12 |
| rr_target | 4.70 |
| max_hold_bars | 18 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

cd_value 계산에는 final_return_pct가 아니라 max_return_pct를 사용한다.

## 재현 성공 판정

1. trades == 56697
2. wins == 20962
3. losses == 35735
4. max_conc == 444
5. errors == 0
6. ruined == false
7. official_cd_value가 499.6598061090216 근처일 것
8. max_drawdown_pct가 1.228290350505734 근처일 것
9. max_return_pct가 405.8734002703171 근처일 것

## 다음 개발 기준

long_max 다음 개선 목표는 2025년까지의 데이터 기준 `official_cd_value > 499.6598061090216` 달성이다.
