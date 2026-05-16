# long_main v13 결과 요약

## 공식 결과 범위

- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 공식 기준선 전략

`8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__DEV24_near_stop112_rr470_hold18`

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

## v12 대비 변화

| 항목 | v12 | v13 | 변화 |
|---|---:|---:|---:|
| trades | 56428 | 56697 | +269 |
| wins | 20531 | 20962 | +431 |
| losses | 35897 | 35735 | -162 |
| win_rate_pct | 36.38441908272489 | 36.97197382577562 | +0.58755474305073 |
| final_return_pct | 397.7275034318756 | 405.1480528315248 | +7.4205493996492 |
| max_return_pct | 398.29373996834414 | 405.8734002703171 | +7.57966030197296 |
| max_drawdown_pct | 1.4367182391297861 | 1.228290350505734 | -0.208427888624052 |
| official_cd_value | 491.134662921777 | 499.6598061090216 | +8.525143187244566 |
| max_conc | 443 | 444 | +1 |

## long_main 기준 충족 여부

- MDD: `1.228290350505734 < 5`
- 기준: `MDD 5% 미만 전략 중 official_cd_value 최대`

## 다음 개선 기준

앞으로 long_main 개선은 v13을 기준으로 한다.

- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.12`, `rr_target 4.70`, `max_hold 18`, `cooldown 31`
- 목표: `max_drawdown_pct < 5` 유지 + `official_cd_value > 499.6598061090216`
