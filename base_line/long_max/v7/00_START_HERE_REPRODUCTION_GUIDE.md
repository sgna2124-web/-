# long_max v7 기준선 재현 시작 문서

## 공식 기준선

- axis: long_max
- version: v7
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

처음 보는 사람은 이 파일의 상수와 기대값을 기준으로 동일 엔진에서 재현한다. 실제 배치 백테스트 엔진은 v15에서 기준선 exact가 통과한 구조를 따른다.

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
- 기존 기준선 exact 후보: `LM15_000_LONG_MAIN_V10_EXACT_FROZEN`
- 기존 기준선 재현 판정: `pass_frozen_reproduction_gate = true`
- 신규 1위 후보: `LM15_031_V10_RR420`
- long_max식 1위 판정: `official_cd_value` 기준 1위

v7은 v6 대비 진입 조건은 유지하고 `rr_target`만 3.80에서 4.20으로 상향한 전략이다. cd_value가 426.96146593036525에서 453.60741100633686으로 상승했으므로 long_max 기준선 갱신이 가능하다.

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

long_max 다음 개선 목표는 2025년까지의 데이터 기준 `official_cd_value > 453.60741100633686` 달성이다.
