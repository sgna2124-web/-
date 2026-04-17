# RESULTS CATALOG SEED 2026-04-16

이 파일은 CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md를 보강하기 위한 초기 원장(seed)이다.
목표는 모든 결과를 path와 수치와 함께 남겨, 향후 우선순위가 바뀌더라도 재평가할 수 있게 하는 것이다.

## 기록 규칙
각 항목은 아래를 남긴다.
- side
- family
- version_reference
- strategy_name
- code_path
- config_path
- combinations_path
- result_path
- summary_file
- final_return_pct
- mdd_pct
- cd_value
- pf
- win_rate_pct
- max_conc
- verdict
- note

## seeded entries

### 1) mixed historical reference / official_top200_reference
- side: mixed
- family: mixed_reference
- version_reference: legacy_pre_split
- strategy_name: official_top200_reference
- code_path: unknown_legacy_reference
- config_path: unknown_legacy_reference
- combinations_path: unknown_legacy_reference
- result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- summary_file: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- final_return_pct: 1120.69995
- mdd_pct: -36.03441
- cd_value: 780.8279
- pf: n/a
- win_rate_pct: n/a
- max_conc: 271
- verdict: archive_reference_only
- note: mixed historical top reference. long/short 공식 기준으로는 사용하지 않음.

### 2) mixed historical reference / asym_guard_top200
- side: mixed
- family: mixed_reference
- version_reference: legacy_pre_split
- strategy_name: asym_guard_top200
- code_path: unknown_legacy_reference
- config_path: unknown_legacy_reference
- combinations_path: unknown_legacy_reference
- result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- summary_file: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- final_return_pct: 1030.79290
- mdd_pct: -35.22274
- cd_value: 732.4967
- pf: n/a
- win_rate_pct: n/a
- max_conc: 230
- verdict: archive_reference_only
- note: mixed historical reference.

### 3) mixed historical reference / score_l16_s20_shortheavy
- side: mixed
- family: mixed_reference
- version_reference: legacy_pre_split
- strategy_name: score_l16_s20_shortheavy
- code_path: unknown_legacy_reference
- config_path: unknown_legacy_reference
- combinations_path: unknown_legacy_reference
- result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- summary_file: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- final_return_pct: 1089.06570
- mdd_pct: -41.06885
- cd_value: 700.7301
- pf: n/a
- win_rate_pct: n/a
- max_conc: 200
- verdict: archive_reference_only
- note: mixed historical reference.

### 4) long official / long_hybrid_wick_bridge_halfhalf
- side: long_only
- family: long_only_hybrid_wick_bridge
- version_reference: legacy_v67
- strategy_name: long_hybrid_wick_bridge_halfhalf
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
- summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/summary.json
- final_return_pct: 9.9603
- mdd_pct: -1.0456
- cd_value: 108.8106
- pf: 1.3033
- win_rate_pct: 54.9859
- max_conc: 50
- verdict: official_long_1
- note: 현재 long-only 공식 1위.

### 5) long candidate / long_hybrid_wick_bridge_quiet48
- side: long_only
- family: long_only_hybrid_wick_bridge
- version_reference: legacy_v67
- strategy_name: long_hybrid_wick_bridge_quiet48
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_quiet48/
- summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_quiet48/summary.json
- final_return_pct: 7.3383
- mdd_pct: -0.7779
- cd_value: 106.5032
- pf: 1.3327
- win_rate_pct: 55.7799
- max_conc: 48
- verdict: strong_candidate_not_promoted
- note: long 공식 1위에는 못 미치지만 매우 낮은 MDD 계열의 유력 후보.

### 6) long candidate / long_hybrid_wick_bridge_us_max40
- side: long_only
- family: long_only_hybrid_wick_bridge
- version_reference: legacy_v67
- strategy_name: long_hybrid_wick_bridge_us_max40
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_us_max40/
- summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_us_max40/summary.json
- final_return_pct: 9.3464
- mdd_pct: -1.2874
- cd_value: 107.9384
- pf: 1.2940
- win_rate_pct: 54.7593
- max_conc: 40
- verdict: strong_candidate_not_promoted
- note: max_conc 제약이 더 낮지만 cd_value는 공식 1위보다 소폭 낮음.

### 7) long carry-forward reference / long_hybrid_wick_bridge_halfhalf
- side: long_only
- family: long_only_hybrid_wick_bridge_profit_boost
- version_reference: legacy_v69
- strategy_name: long_hybrid_wick_bridge_halfhalf
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost.json
- result_path: results_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost/long_hybrid_wick_bridge_halfhalf/
- summary_file: results_json_only_timeout18_time_reduce_v69_long_only_hybrid_wick_bridge_profit_boost/long_hybrid_wick_bridge_halfhalf/summary.json
- final_return_pct: 9.9603
- mdd_pct: -1.0456
- cd_value: 108.8106
- pf: 1.3033
- win_rate_pct: 54.9859
- max_conc: 50
- verdict: carry_forward_same_as_official_long_1
- note: profit_boost 실험에서도 baseline 성능 자체는 동일하게 유지됨.

### 8) short official / short_beh_dd_brake
- side: short_only
- family: short_only_behavioral_guards
- version_reference: legacy_v52
- strategy_name: short_beh_dd_brake
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
- final_return_pct: 311.5456
- mdd_pct: -4.7589
- cd_value: 391.9606
- pf: 1.4457
- win_rate_pct: 15.0623
- max_conc: 286
- verdict: official_short_1
- note: 현재 short-only 공식 1위.

### 9) short candidate / short_beh_baseline_s22
- side: short_only
- family: short_only_behavioral_guards
- version_reference: legacy_v52
- strategy_name: short_beh_baseline_s22
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_baseline_s22/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_baseline_s22/summary.json
- final_return_pct: 244.6224
- mdd_pct: -4.5077
- cd_value: 328.3688
- pf: 1.4216
- win_rate_pct: 15.6312
- max_conc: 294
- verdict: candidate
- note: 공식 1위보다 안정성은 비슷하지만 cd_value 열위.

### 10) short candidate / short_beh_conservative_combo
- side: short_only
- family: short_only_behavioral_guards
- version_reference: legacy_v52
- strategy_name: short_beh_conservative_combo
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_conservative_combo/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_conservative_combo/summary.json
- final_return_pct: 240.4151
- mdd_pct: -4.6180
- cd_value: 324.6434
- pf: 1.4238
- win_rate_pct: 15.8134
- max_conc: 272
- verdict: candidate
- note: PF는 양호하지만 cd_value 기준 열위.

### 11) short candidate / short_beh_loss_streak_brake
- side: short_only
- family: short_only_behavioral_guards
- version_reference: legacy_v52
- strategy_name: short_beh_loss_streak_brake
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_loss_streak_brake/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_loss_streak_brake/summary.json
- final_return_pct: 211.8146
- mdd_pct: -4.2916
- cd_value: 298.4337
- pf: 1.4084
- win_rate_pct: 15.8389
- max_conc: 284
- verdict: candidate
- note: drawdown은 약간 낮지만 공식 1위 대비 수익이 부족.

### 12) short candidate / short_beh_max80_plus_lossbrake
- side: short_only
- family: short_only_behavioral_guards
- version_reference: legacy_v52
- strategy_name: short_beh_max80_plus_lossbrake
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_max80_plus_lossbrake/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_max80_plus_lossbrake/summary.json
- final_return_pct: 209.6279
- mdd_pct: -4.4782
- cd_value: 295.7416
- pf: 1.4041
- win_rate_pct: 15.9032
- max_conc: 80
- verdict: candidate
- note: max_conc를 크게 낮춘 계열이라는 점에서 참조 가치가 있음.

## follow-up rule
- 이후 사용자가 새 전략 결과를 업로드하면 이 seed 형식을 그대로 따라 항목을 추가한다.
- 공식 1위가 바뀌면 verdict와 note를 즉시 갱신한다.
- 실패 전략도 삭제하지 말고 archive 또는 reject로 누적한다.
