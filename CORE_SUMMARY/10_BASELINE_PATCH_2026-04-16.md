# BASELINE PATCH 2026-04-16

이 파일은 기존 CORE_SUMMARY/03_CURRENT_BASELINES.md의 내용을 보정하기 위한 패치 문서다.
현재 대화 시점에서 공식 기준선은 아래로 본다.

## 1. 현재 목표 우선순위
- 필터: MDD 5% 미만
- 정렬 1순위: cd_value 내림차순
- 정렬 2순위: final_return_pct 내림차순

cd_value 공식:
- cd_value = 100 * (1 - abs(mdd_pct)/100) * (1 + final_return_pct/100)

## 2. 공식 long-only 기준선
- strategy_name: long_hybrid_wick_bridge_halfhalf
- family: long_only_hybrid_wick_bridge
- version_reference: legacy_v67
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
- source_of_truth: state/global_top_reference_under_mdd5_cd.json

## 3. 공식 short-only 기준선
- strategy_name: short_beh_dd_brake
- family: short_only_behavioral_guards
- version_reference: legacy_v52
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
- source_of_truth: state/global_top_reference_under_mdd5_cd.json

## 4. mixed historical reference
- strategy_name: official_top200_reference
- result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
- final_return_pct: 1120.69995
- mdd_pct: -36.03441
- cd_value: 780.8279
- note: mixed historical reference only. long-only / short-only 공식 비교선으로 사용하지 않음.

## 5. 적용 원칙
- 신규 long 전략은 2번 기준선과 비교
- 신규 short 전략은 3번 기준선과 비교
- 새로운 공식 1위가 나오면 03_CURRENT_BASELINES.md와 08_ALL_RESULTS_CATALOG.md를 함께 갱신
