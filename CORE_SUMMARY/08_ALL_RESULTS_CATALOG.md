결과 카탈로그

이 카탈로그에는 현재 비교 가능한 유효 결과와 역사적 참조 결과를 함께 남긴다.
단, invalid_env 실험은 남기지 않는다.

기록 원칙
공식 우선순위는 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 다.
max_return_pct는 반드시 기록한다.
legacy 결과 중 max_return_pct가 없는 항목은 unknown_legacy_not_recorded로 적고, current_cd_value는 pending_recompute_under_current_formula로 표시한다.
final_return_pct는 참고 지표다.

현재 정리 상태
4V2R1을 제외한 V2 실험군은 제거되었다.
기존 1V2, 2V2, 3V2, 4V2(구버전), 5V2, 6V2 결과는 현재 비교 기준으로 사용하지 않는다.
다만 4V2R4 이후의 신규 진입 조건 실험군은 최근 탐색 흐름을 파악하기 위한 기록으로 남긴다.

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

4. recent experimental block summary: 4V2R4 ~ 4V2R9
side: split long_only / short_only experiments
family: new-entry-structure exploration
version_reference: 4V2R4_to_4V2R9
summary_file: local_results/*/master_summary*.txt and strategy folders
verdict: no_promotion_yet
notes:
- 최근 실험군은 기존 저장소 전략의 단순 파라미터 수정이 아니라, 신규 진입 조건과 신규 확인 구조를 탐색한 블록이다.
- 전반적으로 MDD를 누르는 방향성은 개선되었지만, 공식 승격을 만들 만큼 max_return_pct가 길게 뻗은 사례는 아직 부족했다.
- 특히 4V2R8, 4V2R9 구간에서는 손실 통제형 long/short 후보가 일부 나왔으나, 공식 long-only / short-only 기준선을 교체할 수준으로 정리되지는 않았다.
- 따라서 이 블록은 실패보다 '새 구조 탐색 기록'으로 해석하고, 장단점은 CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md에서 함께 본다.

5. recent round note: 4V2R4
side: mixed experimental block
version_reference: 4V2R4
verdict: broad_underperformance
notes:
- 당시 후보군은 눈에 띄는 승격 사례 없이 전반적으로 성과가 약했다.
- 문서상 의미는 "단순 신규 시도만으로는 부족했고, 구조적 장단점 정리가 필요했다"는 출발점이다.

6. recent round note: 4V2R8
side: split long_only / short_only
version_reference: 4V2R8
verdict: partial_candidates_only
notes:
- 일부 후보는 MDD 억제와 구조적 참신성 측면에서 의미가 있었다.
- 그러나 공식 교체까지 갈 정도의 cd_value 우위는 확인되지 않았다.
- 다음 단계는 낮은 MDD를 유지한 채 max_return_pct를 더 길게 끌어내는 하이브리드 구조 탐색으로 연결된다.

7. recent round note: 4V2R9
side: split long_only / short_only
version_reference: 4V2R9
verdict: no_promotion_bug_fixed_run_reviewed
notes:
- 초기 실행본은 process_symbol 누락 버그가 있었고, fixed 버전 기준으로 다시 검토했다.
- fixed 버전 결과에서도 공식 1위 교체는 발생하지 않았다.
- 다만 신규 진입 조건 탐색 자체는 계속 유효하며, 기존 저장소 전략 반복이 아니라 새로운 조건군을 확장하는 흐름으로 유지되었다.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경에서 실패한 전략은 reject 또는 archive로 남길 수 있지만, invalid_env는 남기지 않는다.
사용자가 결과를 저장소에 올렸으면, 결과 확인 직후 이 파일과 CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md를 함께 갱신한다.
