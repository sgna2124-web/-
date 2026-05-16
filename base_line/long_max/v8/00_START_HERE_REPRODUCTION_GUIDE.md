# long_max v8 기준선 재현 시작 문서

## 공식 기준선

- axis: long_max
- version: v8
- source batch: `LONG_MAIN_DEV_V18_20260516_213239`
- source candidate: `LM18_041_STOP115_RR520_BODY025`
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__LM18_stop115_rr520_body025`
- side: long
- parent baseline: long_max v7
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 재현 핵심

long_max v8은 long_main v12와 같은 후보다. long_max식 기준으로도 official_cd_value 491.134662921777이 1위였으므로 기준선 갱신이 가능하다.

중요한 점:

- TP03 진입 마스크는 v10/v11 frozen entry 기준으로 계산한다.
- entry source TP03 계산에는 `atr_stop=1.10`, `rr_target=3.80`을 사용한다.
- 최종 진입에는 `body_atr >= 0.25`를 추가한다.
- 최종 청산에는 `atr_stop=1.15`, `rr_target=5.20`을 사용한다.
- entry를 rr_target 5.20으로 다시 계산하면 공식 기준선과 다른 전략이 된다.

## 공식 결과값

| metric | expected |
|---|---:|
| trades | 56428 |
| wins | 20531 |
| losses | 35897 |
| win_rate_pct | 36.38441908272489 |
| final_return_pct | 397.7275034318756 |
| max_return_pct | 398.29373996834414 |
| max_drawdown_pct | 1.4367182391297861 |
| official_cd_value | 491.134662921777 |
| max_conc | 443 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 다음 개발 기준

다음 long_max 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LMAX##_000_LONG_MAX_V8_EXACT_FROZEN`

이 후보는 `LM18_041_STOP115_RR520_BODY025`와 동일해야 한다.
