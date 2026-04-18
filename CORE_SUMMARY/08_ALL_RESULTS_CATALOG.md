결과 카탈로그

이 카탈로그에는 현재 비교 가능한 유효 결과와 역사적 참조 결과를 함께 남긴다.
단, invalid_env 실험은 남기지 않는다.

기록 원칙
공식 우선순위는 cd_value와 MDD다.
max_return_pct는 반드시 기록한다.
legacy 결과 중 max_return_pct가 없는 항목은 unknown_legacy_not_recorded로 적고, current_cd_value는 pending_recompute_under_current_formula로 표시한다.
final_return_pct는 참고 지표다.

현재 정리 상태
4V2R1을 제외한 V2 실험군은 제거되었다.
기존 1V2, 2V2, 3V2, 4V2(구버전), 5V2, 6V2 결과는 현재 비교 기준으로 사용하지 않는다.

현재 등록 항목

1. official long reference
strategy_name: long_hybrid_wick_bridge_halfhalf
side: long_only
family: long_only_hybrid_wick_bridge
version_reference: legacy_v67
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/summary.json
trades: unknown_legacy_not_recorded
win_rate_pct: 54.9859
pf: 1.3033
final_return_pct: 9.9603
max_return_pct: unknown_legacy_not_recorded
max_drawdown_pct: 1.0456
legacy_cd_value: 108.8106
current_cd_value: pending_recompute_under_current_formula
max_conc: 50
verdict: official_long_reference
notes: 현재 long-only 공식 기준 전략명과 경로. legacy 수치는 과거 기준에서 가져온 값이다.

2. official short reference
strategy_name: short_beh_dd_brake
side: short_only
family: short_only_behavioral_guards
version_reference: legacy_v52
code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
trades: unknown_legacy_not_recorded
win_rate_pct: 15.0623
pf: 1.4457
final_return_pct: 311.5456
max_return_pct: unknown_legacy_not_recorded
max_drawdown_pct: 4.7589
legacy_cd_value: 391.9606
current_cd_value: pending_recompute_under_current_formula
max_conc: 286
verdict: official_short_reference
notes: 현재 short-only 공식 기준 전략명과 경로. legacy 수치는 과거 기준에서 가져온 값이다.

3. mixed historical reference
strategy_name: official_top200_reference
side: mixed
family: mixed_reference
version_reference: legacy_pre_split
code_path: unknown_legacy_reference
config_path: unknown_legacy_reference
combinations_path: unknown_legacy_reference
result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
summary_file: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
trades: unknown_legacy_not_recorded
win_rate_pct: unknown_legacy_not_recorded
pf: unknown_legacy_not_recorded
final_return_pct: 1120.69995
max_return_pct: unknown_legacy_not_recorded
max_drawdown_pct: 36.03441
legacy_cd_value: 780.8279
current_cd_value: not_applicable_archive_reference
max_conc: 271
verdict: archive_reference_only
notes: mixed historical top reference. long-only / short-only 공식 비교 기준으로 사용하지 않음.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경에서 실패한 전략은 reject 또는 archive로 남길 수 있지만, invalid_env는 남기지 않는다.
