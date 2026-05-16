# long_main v12 기준선 재현 시작 문서

## 공식 기준선

- axis: long_main
- version: v12
- source batch: `LONG_MAIN_DEV_V18_20260516_213239`
- source candidate: `LM18_041_STOP115_RR520_BODY025`
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420__LM18_stop115_rr520_body025`
- side: long
- parent baseline: long_main v11
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 재현 핵심

이 기준선은 v11의 진입 마스크를 그대로 사용한 뒤 `body_atr >= 0.25`를 추가한 전략이다.

중요한 점:

- TP03 진입 마스크는 v10/v11 frozen entry 기준으로 계산한다.
- entry source TP03 계산에는 `atr_stop=1.10`, `rr_target=3.80`을 사용한다.
- 최종 승격 전략의 청산에는 `atr_stop=1.15`, `rr_target=5.20`을 사용한다.
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

## 먼저 확인할 파일

1. `01_RESULT_SUMMARY.md`
2. `02_ENTRY_EXIT_CONDITIONS.md`
3. `03_STRATEGY_CODE_REFERENCE.py`
4. `04_STRENGTHS_WEAKNESSES.md`
5. `05_REPRODUCTION_AND_NEXT_DEV_RULES.md`

## 재현 성공 판정

다음 값이 맞아야 한다.

- trades == 56428
- wins == 20531
- losses == 35897
- max_return_pct ~= 398.29373996834414
- max_drawdown_pct ~= 1.4367182391297861
- official_cd_value ~= 491.134662921777
- max_conc == 443
- errors == 0
- ruined == false

## 다음 개발 기준

다음 long_main 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LM##_000_LONG_MAIN_V12_EXACT_FROZEN`

이 후보는 `LM18_041_STOP115_RR520_BODY025`와 동일해야 한다.
