# long_max v8 재현 및 다음 개발 규칙

## source of truth

long_max v8의 기준 정보는 다음 파일을 따른다.

1. `00_START_HERE_REPRODUCTION_GUIDE.md`
2. `01_RESULT_SUMMARY.md`
3. `02_ENTRY_EXIT_CONDITIONS.md`
4. `03_STRATEGY_CODE_REFERENCE.py`
5. `04_STRENGTHS_WEAKNESSES.md`

## 다음 개발 첫 후보

다음 long_max 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LMAX##_000_LONG_MAX_V8_EXACT_FROZEN`

이 후보는 v18의 `LM18_041_STOP115_RR520_BODY025`와 동일해야 한다.

## 반드시 재현할 값

| metric | expected |
|---|---:|
| trades | 56428 |
| wins | 20531 |
| losses | 35897 |
| max_return_pct | 398.29373996834414 |
| max_drawdown_pct | 1.4367182391297861 |
| official_cd_value | 491.134662921777 |
| max_conc | 443 |
| errors | 0 |
| ruined | false |

## 기준선 재현 실패 시 규칙

기준선 exact가 실패하면 개선 후보 결과는 전부 무효다.

우선 확인할 것:

1. entry source TP03 계산이 `atr_stop=1.10`, `rr_target=3.80`인지 확인
2. final exit가 `atr_stop=1.15`, `rr_target=5.20`인지 확인
3. body_atr >= 0.25가 entry source 뒤에 AND로 붙었는지 확인
4. 2026년 데이터가 섞이지 않았는지 확인
5. 수수료 8bps와 position_fraction 0.01이 유지됐는지 확인

## 다음 갱신 조건

long_max 다음 기준선 갱신 조건:

1. 2025년까지의 데이터만 사용
2. errors == 0
3. ruined == false
4. official_cd_value > 491.134662921777
5. 단독 재백테스트에서 재현 가능

## 금지 사항

- 기준선 전략명을 보고 조건을 추정하지 않는다.
- entry source TP03를 rr_target 5.20으로 다시 계산하지 않는다.
- 2026년 데이터를 기준선 산출에 섞지 않는다.
- 기준선 exact 없이 개선 후보를 평가하지 않는다.
