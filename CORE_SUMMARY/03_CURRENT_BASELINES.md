현재 공식 기준선

이 문서는 새 대화창의 어시스턴트가 현재 공식 long 1위와 short 1위를 즉시 파악하기 위한 기준선 문서다.
비교는 long-only와 short-only를 분리하여 수행한다.

현재 프로젝트의 공식 판단 기준
공식 판단 기준은 MDD와 cd_value다.
현재 프로젝트에서 cd_value의 공식 정의는 다음과 같다.
cd_value = max_return_pct / max_drawdown_pct
final_return_pct는 참고 지표다.

중요한 주의사항
아래 공식 기준선 수치 중 legacy 항목은 과거 state/global_top_reference_under_mdd5_cd.json 및 관련 패치 문서에서 가져온 값이다.
이 legacy 수치의 cd_value는 과거 공식으로 계산된 값일 수 있다.
따라서 현재 max_return_pct 기반 공식으로 엄밀하게 승격/교체를 판정하려면, 기존 공식 1위도 max_return_pct를 포함한 현재 공식으로 재계산하거나, 최소한 challenger와 incumbent 모두 동일한 계산 규칙을 사용해야 한다.
즉, 아래 전략명과 경로는 현재 공식 비교 기준선으로 유지하되, legacy cd_value는 역사적 참고치로 본다.

1. 현재 공식 long-only 기준선
strategy_name: long_hybrid_wick_bridge_halfhalf
family: long_only_hybrid_wick_bridge
version_reference: legacy_v67
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/summary.json
legacy_final_return_pct: 9.9603
legacy_mdd_pct: -1.0456
legacy_cd_value: 108.8106
max_return_pct: unknown_legacy_not_recorded
current_cd_value: pending_recompute_under_current_formula
pf: 1.3033
win_rate_pct: 54.9859
max_conc: 50
source_of_truth: state/global_top_reference_under_mdd5_cd.json
status: official_long_reference
note: 현재 long-only 공식 비교 기준 전략명과 경로. 수치 중 legacy_cd_value는 역사적 참고치다.

2. 현재 공식 short-only 기준선
strategy_name: short_beh_dd_brake
family: short_only_behavioral_guards
version_reference: legacy_v52
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
legacy_final_return_pct: 311.5456
legacy_mdd_pct: -4.7589
legacy_cd_value: 391.9606
max_return_pct: unknown_legacy_not_recorded
current_cd_value: pending_recompute_under_current_formula
pf: 1.4457
win_rate_pct: 15.0623
max_conc: 286
source_of_truth: state/global_top_reference_under_mdd5_cd.json
status: official_short_reference
note: 현재 short-only 공식 비교 기준 전략명과 경로. 수치 중 legacy_cd_value는 역사적 참고치다.

3. mixed historical reference
strategy_name: official_top200_reference
result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
legacy_final_return_pct: 1120.69995
legacy_mdd_pct: -36.03441
legacy_cd_value: 780.8279
status: archive_reference_only
note: mixed historical reference only. long-only / short-only 공식 비교선으로 사용하지 않음.

4. 최근 상태 메모
4V2R4 ~ 4V2R9까지의 최근 신규 진입 조건 실험군에서는 공식 long-only / short-only 기준선 교체가 발생하지 않았다.
즉 현재 공식 1위는 그대로 유지한다.

5. 승격 규칙
신규 long 전략은 1번 기준선과 비교한다.
신규 short 전략은 2번 기준선과 비교한다.
새 전략 결과에는 최소한 final_return_pct, max_return_pct, max_drawdown_pct, cd_value, result_path가 포함되어야 한다.
현재 공식 1위를 교체하려면 challenger와 incumbent가 동일 계산 규칙으로 비교 가능해야 한다.
