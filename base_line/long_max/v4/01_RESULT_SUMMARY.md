# long_max v4 결과 요약

## 1. 갱신 판정

long_max 기준선을 v3 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110`에서 v4 `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`으로 갱신한다.

갱신 이유:

- long_max 기준은 `MDD 제한 없이 official_cd_value 최대`다.
- v4의 cd_value는 `363.5507495661`로 v3의 `336.7657621418`보다 높다.
- V14 탐색 결과의 1위 전략을 V15 단독 리테스트에서 동일하게 재현했다.
- 진입 조건은 그대로 유지하고, `rr_target`만 2.90에서 3.20으로 조정한 직접 개선이다.

## 2. 개발 및 검증 원천

- 탐색 배치: `LONG_MAX_V3_BASELINE_ENTRY_DEV_V14`
- 단독 리테스트 배치: `LONG_MAX_V3_SINGLE_TOP_RETEST_DEV_V15`
- 기준선 재현 상태: `pass_single_retest_gate = True`
- V15 단독 리테스트 전략: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320`

## 3. v3 기준선 결과

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

## 4. v4 갱신 기준선 결과

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

## 5. v3 대비 변화

| 항목 | v3 | v4 | 변화 |
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

## 6. 해석

v4는 승률이 약간 낮아졌지만 rr_target을 3.20으로 높이면서 이익 거래의 보상이 커졌다. MDD 증가는 `+0.0003650298%p`로 사실상 미미하고, max_return이 크게 증가해 cd_value가 상승했다.

## 7. 다음 개선 기준

앞으로 long_max 개선은 v4를 기준으로 한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.10`, `rr_target 3.20`, `max_hold 21`, `cooldown 31`
- 목표: `official_cd_value > 363.5507495661`
