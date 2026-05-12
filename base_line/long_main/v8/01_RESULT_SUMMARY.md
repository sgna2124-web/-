# long_main v8 결과 요약

## 1. 갱신 판정

long_main 기준선을 v7 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`에서 v8 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`으로 갱신한다.

갱신 이유:

- long_main 기준은 `MDD 5% 미만 전략 중 official_cd_value 최대`다.
- v8의 MDD는 `1.3412321126%`로 5% 미만이다.
- v8의 cd_value는 `363.5507495661`로 v7의 `336.7657621418`보다 높다.
- V14 탐색 결과의 1위 전략을 V15 단독 리테스트에서 동일하게 재현했다.
- 진입 조건은 그대로 유지하고, `rr_target`만 2.90에서 3.20으로 조정한 직접 개선이다.

## 2. 개발 및 검증 원천

- 탐색 배치: `LONG_MAX_V3_BASELINE_ENTRY_DEV_V14`
- 단독 리테스트 배치: `LONG_MAX_V3_SINGLE_TOP_RETEST_DEV_V15`
- 기준선 재현 상태: `pass_single_retest_gate = True`
- V15 단독 리테스트 전략: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`

## 3. v7 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110 |
| trades | 57114 |
| wins | 20911 |
| losses | 36203 |
| win_rate_pct | 36.6127394334 |
| final_return_pct | 240.7307747654 |
| max_return_pct | 241.3427142366 |
| max_drawdown_pct | 1.3408670828 |
| official_cd_value | 336.7657621418 |
| max_conc | 435 |

## 4. v8 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320 |
| parent_strategy | 8V4_V09_V054_extreme_vol18 |
| side | long |
| entry_key | child::orig_V09_extreme_vol18::tp03 |
| atr_stop | 1.10 |
| rr_target | 3.20 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| use_tp03_gate | true |
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

## 5. v7 대비 변화

| 항목 | v7 | v8 | 변화 |
|---|---:|---:|---:|
| trades | 57114 | 57065 | -49 |
| wins | 20911 | 20612 | -299 |
| losses | 36203 | 36453 | +250 |
| win_rate_pct | 36.6127394334 | 36.1202137913 | -0.4925256421 |
| final_return_pct | 240.7307747654 | 267.6967217810 | +26.9659470156 |
| max_return_pct | 241.3427142366 | 268.4930973199 | +27.1503830833 |
| max_drawdown_pct | 1.3408670828 | 1.3412321126 | +0.0003650298 |
| official_cd_value | 336.7657621418 | 363.5507495661 | +26.7849874243 |
| max_conc | 435 | 439 | +4 |

cd_value 개선율: 약 `+7.9536%`

## 6. long_main 기준 충족 여부

long_main 기준:

`max_drawdown_pct < 5` 조건을 만족하는 전략 중 `official_cd_value` 최대

v8은 다음을 만족한다.

- MDD: `1.3412321126 < 5`
- cd_value: `363.5507495661 > 336.7657621418`

따라서 long_main 공식 기준선으로 갱신한다.

## 7. 다음 개선 기준

앞으로 long_main 개선은 v8을 기준으로 한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.10`, `rr_target 3.20`, `max_hold 21`, `cooldown 31`
- 목표: `MDD < 5` 유지 + `official_cd_value > 363.5507495661`
