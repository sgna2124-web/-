전략 등록부

이 문서는 새 대화창의 어시스턴트가 현재 공식 기준 전략과 현재 개발 초점을 빠르게 이해하기 위한 등록부다.
정확한 진입/청산 로직은 반드시 code_path의 실제 코드를 다시 확인한다.
이 문서는 전략의 역할, 기준선 여부, 참조 경로를 고정하는 목적이다.

1. official long reference
strategy_name: long_hybrid_wick_bridge_halfhalf
side: long_only
family: long_only_hybrid_wick_bridge
version_reference: legacy_v67
role: official_long_reference
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/summary.json
strength_hint: 현재 long-only 공식 비교 기준선으로 유지되는 전략 계열
risk_hint: legacy 기준선이므로 max_return_pct 기반 현행 공식으로는 재검증이 필요할 수 있음
usage_rule: 새로운 long 전략은 이 전략을 기준으로 비교한다.

2. official short reference
strategy_name: short_beh_dd_brake
side: short_only
family: short_only_behavioral_guards
version_reference: legacy_v52
role: official_short_reference
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
strength_hint: 현재 short-only 공식 비교 기준선으로 유지되는 전략 계열
risk_hint: legacy 기준선이므로 max_return_pct 기반 현행 공식으로는 재검증이 필요할 수 있음
usage_rule: 새로운 short 전략은 이 전략을 기준으로 비교한다.

3. current development focus
long_focus: 기존 long 성과가 약하므로, 고수익 잠재력이 보였던 reclaim/capitulation 계열이나 전혀 다른 신규 long 구조를 적극 탐색한다.
short_focus: 공식 short 1위는 유지하되, 전혀 다른 계열의 신규 short 전략도 병행 탐색한다.
comparison_rule: 결과 비교는 long-only와 short-only를 섞지 않는다.
environment_rule: 자산 진입 비중 1%, 수수료 0.04%, FAST 미사용, 풀 백테스트 기준을 유지한다.
result_rule: max_return_pct를 반드시 남긴다.

4. invalid_env 처리 원칙
환경 설정 오류, 자산 비중 오류, 수수료 오류, 비교 불가능한 실험은 invalid_env로 처리한다.
invalid_env 실험은 전략 실패 기록으로 누적하지 않고 결과 카탈로그에서 제거한다.
