# long_main v12 재현 및 다음 개발 규칙

## source of truth

long_main v12의 기준 정보는 다음 파일을 따른다.

1. `00_START_HERE_REPRODUCTION_GUIDE.md`
2. `01_RESULT_SUMMARY.md`
3. `02_ENTRY_EXIT_CONDITIONS.md`
4. `03_STRATEGY_CODE_REFERENCE.py`
5. `04_STRENGTHS_WEAKNESSES.md`

## 다음 개발의 첫 후보

다음 long_main 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LM##_000_LONG_MAIN_V12_EXACT_FROZEN`

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

## baseline audit 필수 항목

다음 개발 파일은 반드시 `baseline_audit.json`을 생성한다.

필수 항목:

- baseline_version: `long_main/v12`
- baseline_candidate: `LM##_000_LONG_MAIN_V12_EXACT_FROZEN`
- expected
- actual
- pass_frozen_reproduction_gate
- train_end_exclusive_utc
- out_dir_policy
- round_trip_cost_bps
- position_fraction
- entry_mask_source
- final_exit_params

## 기준선 재현 실패 시 규칙

기준선 exact가 실패하면 개선 후보 결과는 전부 무효다.

해야 할 일:

1. summary 순위를 말하지 않는다.
2. 기준선 갱신 가능 여부를 말하지 않는다.
3. `BASELINE_REPRODUCTION_FAILED`로 기록한다.
4. entry source TP03 계산 기준을 먼저 확인한다.
5. body_atr 필터 적용 위치를 확인한다.
6. atr_stop/rr_target을 entry source와 final exit에서 혼동했는지 확인한다.

## 다음 갱신 조건

long_main 다음 기준선 갱신 조건:

1. 2025년까지의 데이터만 사용
2. errors == 0
3. ruined == false
4. max_drawdown_pct < 5
5. official_cd_value > 491.134662921777
6. 단독 재백테스트에서 재현 가능

## 금지 사항

- 기준선 전략명을 보고 조건을 추정하지 않는다.
- V09/extreme/vol18/tp03를 임의로 재해석하지 않는다.
- entry source TP03를 rr_target 5.20으로 다시 계산하지 않는다.
- 2026년 데이터를 기준선 산출에 섞지 않는다.
- 기준선 exact 없이 개선 후보를 평가하지 않는다.

## 우선 탐색 방향

- `atr_stop=1.15`, `rr_target=5.20`, `body_atr >= 0.25`를 중심축으로 유지
- vol_ratio 1.10, 1.15, 1.20, 1.25 비교
- body_atr 0.20, 0.25, 0.30 비교
- max_hold 24/27 확장은 후순위
- close_pos >= 0.70은 제외 우선
