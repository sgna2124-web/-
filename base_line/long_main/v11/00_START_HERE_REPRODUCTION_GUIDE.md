# long_main v11 기준선 재현 시작 문서

## 공식 기준선

- axis: long_main
- version: v11
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350__DEV19_risk_rr_380__LM15_rr420`
- source_candidate: `LM15_031_V10_RR420`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- result_scope: `2025년까지의 데이터 기준`
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- 2026년 데이터는 기준선 산출에서 제외하고 검증용으로 남긴다.

## 가장 먼저 실행할 파일

`03_FROZEN_BASELINE_RUNNER.py`

이 파일은 설명용이 아니라 재현용 frozen runner다. 처음 보는 사람은 이 파일만 실행해서 아래 공식 결과값이 나오는지 먼저 확인한다.

기본 실행 예시:

```bash
python 03_FROZEN_BASELINE_RUNNER.py --data-dir ./Data/time
```

결과 폴더는 실행 위치 기준으로만 생성된다.

`./local_results/long_main/LONG_MAIN_V11_FROZEN_BASELINE_2025_ONLY_YYYYMMDD_HHMMSS/`

## 공식 결과값: 2025년까지의 기록

| 항목 | 값 |
|---|---:|
| trades | 56651 |
| wins | 20168 |
| losses | 36483 |
| win_rate_pct | 35.600430707313194 |
| final_return_pct | 358.93258386772163 |
| max_return_pct | 359.3568623293992 |
| max_drawdown_pct | 1.2516306589841375 |
| official_cd_value | 453.60741100633686 |
| max_conc | 442 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 갱신 근거

- 개발 배치: `LONG_MAIN_DEV_V15_20260516_021836`
- 기준선 exact 후보: `LM15_000_LONG_MAIN_V10_EXACT_FROZEN`
- 기존 기준선 재현 판정: `pass_frozen_reproduction_gate = true`
- 신규 1위 후보: `LM15_031_V10_RR420`
- long_main 갱신 판정: `max_drawdown_pct < 5` 이면서 `official_cd_value > 426.96146593036525`

v11은 v10 대비 진입 조건은 유지하고 `rr_target`만 3.80에서 4.20으로 상향한 전략이다. v15 결과에서 기존 v10 기준선이 완전 재현되었고, 같은 기준선 entry 위에서 `LM15_031_V10_RR420`이 cd_value 453.60741100633686으로 1위를 기록했다.

## 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.10 |
| rr_target | 4.20 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |

## 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

cd_value 계산에는 final_return_pct가 아니라 max_return_pct를 사용한다.

## 재현 성공 판정

1. trades == 56651
2. wins == 20168
3. losses == 36483
4. errors == 0
5. ruined == false
6. official_cd_value가 453.60741100633686 근처일 것
7. max_drawdown_pct가 1.2516306589841375 근처일 것
8. max_return_pct가 359.3568623293992 근처일 것

## 다음 개발 기준

long_main 다음 개선 목표는 2025년까지의 데이터 기준 `max_drawdown_pct < 5` 유지와 `official_cd_value > 453.60741100633686` 달성이다.

## 금지 사항

- 전략명만 보고 진입 조건을 재해석하지 않는다.
- `V09`, `extreme`, `vol18`, `tp03` 이름을 보고 유사 조건을 새로 만들지 않는다.
- 기준선 exact가 실패하면 개선 후보 결과를 인정하지 않는다.
- 2026년 데이터를 기준선 산출에 섞지 않는다.
