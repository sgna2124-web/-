# RESULTS CATALOG SEED 2026-04-16

이 파일은 CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md의 보조 원장이다.
목표는 결과 재평가를 위해 최소한의 식별 정보와 해석 메모를 남기는 것이다.

## 해석 규칙
- 현재 공식 정의에서 cd_value = max_return_pct / max_drawdown_pct 이다.
- legacy 항목 중 max_return_pct가 없으면 current_cd_value는 재계산 pending으로 둔다.
- final_return_pct는 보조 해석용이다.

## seeded references

### mixed historical reference
- strategy_name: official_top200_reference
- side: mixed
- version_reference: legacy_pre_split
- result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- final_return_pct: 1120.69995
- max_drawdown_pct: 36.03441
- cd_value: pending_recompute_under_current_formula
- max_conc: 271
- verdict: archive_reference_only

### official long reference
- strategy_name: long_hybrid_wick_bridge_halfhalf
- side: long_only
- version_reference: legacy_v67
- result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
- final_return_pct: 9.9603
- max_drawdown_pct: 1.0456
- pf: 1.3033
- win_rate_pct: 54.9859
- max_conc: 50
- cd_value: pending_recompute_under_current_formula
- verdict: official_long_1

### official short reference
- strategy_name: short_beh_dd_brake
- side: short_only
- version_reference: legacy_v52
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
- final_return_pct: 311.5456
- max_drawdown_pct: 4.7589
- pf: 1.4457
- win_rate_pct: 15.0623
- max_conc: 286
- cd_value: pending_recompute_under_current_formula
- verdict: official_short_1

## recent experiment notes

### 4V2R4
- verdict: no_promotion
- note: 광범위한 신규 시도였으나 눈에 띄는 승격 사례는 없었다.

### 4V2R8
- verdict: partial_candidates_only
- note: 일부 후보가 손실 통제와 구조적 참신성 측면에서 의미가 있었지만 공식 교체까지는 미달했다.

### 4V2R9_fixed
- verdict: reviewed_no_promotion
- note: 초기 버그 수정 후 재검토했으나 공식 1위 교체는 없었다. 신규 조건 탐색 흐름 자체는 계속 유효하다.

## follow-up
- 새 결과 업로드 후 이 파일, 08_ALL_RESULTS_CATALOG, 12_STRATEGY_STRENGTHS_WEAKNESSES를 세트로 갱신한다.
- 공식 1위가 바뀌면 verdict를 즉시 수정한다.
