# long_main v9 결과 요약

## 1. 갱신 판정

long_main 기준선을 v8에서 v9로 갱신한다.

새 기준선:

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350`

갱신 이유:

- long_main 기준은 `MDD 5% 미만 전략 중 official_cd_value 최대`다.
- v9의 MDD는 `1.2432451599%`로 5% 미만이다.
- v9의 cd_value는 `400.8314684802`로 v8의 `363.5507495661`보다 높다.
- V16 탐색 결과의 1위 전략을 V17 단독 리테스트에서 동일하게 재현했다.
- 진입 조건은 그대로 유지하고, `rr_target`만 3.20에서 3.50으로 조정한 직접 개선이다.

## 2. 개발 및 검증 원천

- 탐색 배치: `LONG_MAX_V4_BASELINE_ENTRY_DEV_V16`
- 단독 리테스트 배치: `LONG_MAX_V4_SINGLE_TOP_RETEST_DEV_V17`
- 기준선 재현 상태: `pass_single_retest_gate = True`

## 3. v8 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320 |
| trades | 57065 |
| wins | 20612 |
| losses | 36453 |
| win_rate_pct | 36.1202137913 |
| final_return_pct | 267.6967217810 |
| max_return_pct | 268.4930973199 |
| max_drawdown_pct | 1.3412321126 |
| official_cd_value | 363.5507495661 |
| max_conc | 439 |

## 4. v9 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350 |
| parent_strategy | 8V4_V09_V054_extreme_vol18 |
| side | long |
| entry_key | child::orig_V09_extreme_vol18::tp03 |
| atr_stop | 1.10 |
| rr_target | 3.50 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| use_tp03_gate | true |
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

## 5. v8 대비 변화

| 항목 | v8 | v9 | 변화 |
|---|---:|---:|---:|
| trades | 57065 | 57035 | -30 |
| wins | 20612 | 20451 | -161 |
| losses | 36453 | 36584 | +131 |
| win_rate_pct | 36.1202137913 | 35.8569299553 | -0.2632838360 |
| final_return_pct | 267.6967217810 | 305.0347181084 | +37.3379963274 |
| max_return_pct | 268.4930973199 | 305.8775211164 | +37.3844237965 |
| max_drawdown_pct | 1.3412321126 | 1.2432451599 | -0.0979869527 |
| official_cd_value | 363.5507495661 | 400.8314684802 | +37.2807189141 |
| max_conc | 439 | 441 | +2 |

cd_value 개선율: 약 `+10.25%`

## 6. long_main 기준 충족 여부

- MDD: `1.2432451599 < 5`
- cd_value: `400.8314684802 > 363.5507495661`

따라서 long_main 공식 기준선으로 갱신한다.

## 7. 다음 개선 기준

앞으로 long_main 개선은 v9를 기준으로 한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.10`, `rr_target 3.50`, `max_hold 21`, `cooldown 31`
- 목표: `MDD < 5` 유지 + `official_cd_value > 400.8314684802`
