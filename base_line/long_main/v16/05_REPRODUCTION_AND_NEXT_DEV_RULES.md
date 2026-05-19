# long_main v16 재현 및 다음 개발 규칙

## source of truth

long_main v16의 기준 정보는 다음 파일을 따른다.

1. `00_START_HERE_REPRODUCTION_GUIDE.md`
2. `01_RESULT_SUMMARY.md`
3. `02_ENTRY_EXIT_CONDITIONS.md`
4. `03_STRATEGY_CODE_REFERENCE.py`
5. `04_STRENGTHS_WEAKNESSES.md`
6. `06_FULL_REPRODUCTION_SPEC.md`

## 다음 개발 첫 후보

다음 long_main 개발 파일의 첫 후보는 반드시 다음이어야 한다.

`LM##_000_LONG_MAIN_V16_EXACT_FROZEN`

이 후보는 `LM23R_001_RETEST_S121_RR505_B022_H17`와 동일해야 한다.

## 반드시 재현할 값

| metric | expected |
|---|---:|
| trades | 56551 |
| wins | 21969 |
| losses | 34582 |
| win_rate_pct | 38.84811939665081 |
| final_return_pct | 454.0898854634718 |
| max_return_pct | 455.0171719748199 |
| max_drawdown_pct | 1.3974597812998368 |
| official_cd_value | 547.2610302171641 |
| max_conc | 445 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## baseline audit 필수 항목

다음 개발 파일은 반드시 `baseline_audit.json`을 생성한다.

필수 항목:

- baseline_version: `long_main/v16`
- baseline_candidate: `LM##_000_LONG_MAIN_V16_EXACT_FROZEN`
- expected
- actual
- diff
- pass_frozen_reproduction_gate
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- out_dir_policy: `Path.cwd()/local_results/long_main only`
- round_trip_cost_bps: `8.0`
- position_fraction: `0.01`
- entry_key: `child::orig_V09_extreme_vol18::tp03`
- entry_source_atr_stop: `1.10`
- entry_source_rr_target: `3.80`
- final_exit_params: `atr_stop=1.21, rr_target=5.05, max_hold_bars=17, cooldown_bars=31`

## 기준선 재현 실패 시 규칙

기준선 exact가 실패하면 개선 후보 결과는 전부 무효다.

해야 할 일:

1. summary 순위를 말하지 않는다.
2. 기준선 갱신 가능 여부를 말하지 않는다.
3. `BASELINE_REPRODUCTION_FAILED`로 기록한다.
4. errors.csv가 있으면 먼저 확인한다.
5. TP03 source가 1.10/3.80 기준인지 확인한다.
6. final exit가 1.21/5.05/17/31인지 확인한다.
7. body_atr >= 0.22가 entry_source 뒤에 AND로 붙었는지 확인한다.
8. 2026년 데이터가 섞이지 않았는지 확인한다.

## 다음 갱신 조건

long_main 다음 기준선 갱신 조건:

1. 2025년까지의 데이터만 사용
2. errors == 0
3. ruined == false
4. max_drawdown_pct < 5
5. official_cd_value > 547.2610302171641
6. 단독 재백테스트에서 재현 가능
7. 06_FULL_REPRODUCTION_SPEC까지 기록 완료

## 금지 사항

- 기준선 전략명을 보고 조건을 추정하지 않는다.
- TP03 source를 final RR 5.05로 다시 계산하지 않는다.
- TP03 source를 final stop 1.21로 다시 계산하지 않는다.
- 2026년 데이터를 기준선 산출에 섞지 않는다.
- 기준선 exact 없이 개선 후보를 평가하지 않는다.
- close_pos/quiet_ratio를 우선 추가하지 않는다. 이전 결과에서 성과가 크게 훼손됐다.

## 우선 탐색 방향

- stop: 1.21, 1.22, 1.23
- rr_target: 5.05, 5.10, 5.15
- body_atr: 0.20, 0.22, 0.24, 0.26
- hold: 17 고정 우선
