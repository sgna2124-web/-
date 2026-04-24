결과 카탈로그

이 카탈로그에는 현재 비교 가능한 유효 결과와 역사적 참조 결과를 함께 남긴다.
단, invalid_env 실험은 남기지 않는다.

기록 원칙
공식 우선순위는 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 다.
max_return_pct는 반드시 기록한다.
legacy 결과 중 max_return_pct가 없는 항목은 unknown_legacy_not_recorded로 적고, current_cd_value는 pending_recompute_under_current_formula로 표시한다.
final_return_pct는 참고 지표다.
거래 수가 0이거나 극단적으로 적은 전략은 cd_value 숫자가 높아 보여도 공식 승격 후보로 보지 않는다.

현재 정리 상태
4V2R1을 제외한 V2 실험군은 제거되었다.
기존 1V2, 2V2, 3V2, 4V2(구버전) 결과는 현재 비교 기준으로 사용하지 않는다.
다만 4V2R12 이후의 신규 long/short 진입 구조 실험군은 최근 탐색 흐름을 파악하기 위한 기록으로 남긴다.

현재 등록 항목

1. official long reference
strategy_name: 6V2_L01_doubleflush_core
side: long_only
family: long_only_doubleflush_cap_reclaim
version_reference: 6V2_LONG10_REVIEWED
code_path: unknown_local_backtest_file_not_in_repo
config_path: unknown_local_backtest_file_not_in_repo
combinations_path: unknown_local_backtest_file_not_in_repo
result_path: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/
summary_file: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/summary.json
trades: 592
win_rate_pct: 58.1081
pf: unknown_not_recorded
final_return_pct: 23.6961
max_return_pct: 23.9191
max_drawdown_pct: 1.7512
legacy_cd_value: not_applicable
current_cd_value: 121.5300
max_conc: unknown_not_recorded
verdict: official_long_reference
notes: 6V2_LONG10_REVIEWED에서 첫 공식 long 승격이 발생했다. selective double flush + cap reclaim 코어가 현재 long 설계의 기준 구조다.

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
notes: 현재 short-only 공식 비교 기준 전략명과 경로. legacy 수치는 역사적 참고치다.

3. archived previous long reference
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
current_cd_value: archived_after_6V2_promotion
max_conc: 50
verdict: archive_previous_long_reference
notes: 6V2 승격 전까지 사용하던 long 공식 기준선. 역사 참조용으로만 유지한다.

4. mixed historical reference
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
notes: mixed historical top reference. long-only / short-only 공식 비교 기준으로 사용하지 않는다.

5. recent round note: 4V2R12
side: split long_only / short_only
version_reference: 4V2R12
summary_file: local_results/4V2R12/*/summary.json
verdict: no_promotion_all_mdd_fail
notes:
- 10개 전략 전부 passes_mdd_lt_5=false였다.
- fail-reject / reset-resume 계열이 상대적으로 덜 나빴지만, 과다거래 구조가 강해 공식 승격과 거리가 멀었다.
- 학습 포인트는 과다거래형 구조를 배제하고 선택도가 높은 reset-resume / fail-reject 계열에 더 강한 위치 필터를 붙여야 한다는 점이다.

6. recent round note: 4V2R13
side: split long_only / short_only
version_reference: 4V2R13
summary_file: local_results/4V2R13/*/summary.json
verdict: partial_candidates_but_no_promotion
notes:
- 10개 중 4개가 MDD 5% 미만을 통과했다.
- long에서는 L61, L65가, short에서는 S61, S65가 생존했다.
- 강한 방향 필터와 선택적 상단/하단 스윕 반전 구조가 MDD 억제에는 유효하다는 점을 확인했지만 공식 기준선 교체까지는 가지 못했다.

7. recent round note: 4V2R14
side: split long_only / short_only
version_reference: 4V2R14
summary_file: local_results/4V2R14/*/summary.json
verdict: no_promotion_high_variance_archive_candidates
notes:
- selective fail-reclaim / fail-reject 계열을 다시 밀어본 배치였지만 공식 승격 후보는 나오지 않았다.
- tp03류 실패 복귀 구조는 아이디어 저장 가치는 있으나, 방향/위치 필터 없이 단독 승격용으로 쓰기 어렵다는 점을 확인했다.

8. recent round note: 4V2R15
side: split long_only / short_only
version_reference: 4V2R15
summary_file: local_results/4V2R15/*/summary.json
verdict: no_promotion_behavioral_family_needs_stronger_gates
notes:
- behavior flush, dd brake, post shock, tight flag, underreaction 계열을 탐색했다.
- 이름이 설득력 있는 행동 기반 구조라도, 추세 위치 필터와 거래 수 제어가 없으면 실제 성능 우위로 이어지지 않는다는 점을 보여줬다.

9. recent round note: 4V2R16
side: split long_only / short_only
version_reference: 4V2R16
summary_file: local_results/4V2R16/*/summary.json
verdict: no_promotion_overselection_and_zero_trade_warning
notes:
- shakeout reclaim, stair pullback, false loss, quiet base, vol reset 계열을 실험했다.
- 0트레이드 사례가 나왔고, 조건을 계속 좁히면 MDD는 줄어들 수 있어도 전략 자체가 사라질 수 있다는 점이 확인됐다.

10. recent round note: 5V2_COMBO10_REVIEWED
side: split long_only / short_only
version_reference: 5V2_COMBO10_REVIEWED
summary_file: local_results/5V2_COMBO10_REVIEWED/*/summary.json
verdict: long_candidate_but_no_promotion_short_defensive_only
notes:
- batch long best: 5V2_L01_capitulation_reclaim | trades 3333 | max_return_pct 51.7718 | final_return_pct 50.9423 | max_drawdown_pct 13.7240 | cd_value 130.2269
- long 쪽에서 수익 잠재력은 확인됐지만, MDD 13.7240으로 공식 승격에 실패했다.
- broad pullback / retest / compression / false-break 구조는 과다거래로 붕괴하는 경향을 보였다.

11. recent round note: 6V2_LONG10_REVIEWED
side: long_only
version_reference: 6V2_LONG10_REVIEWED
summary_file: local_results/6V2_LONG10_REVIEWED/*/summary.json
verdict: long_promotion_doubleflush_core_established
notes:
- batch long best: 6V2_L01_doubleflush_core | trades 592 | max_return_pct 23.9191 | final_return_pct 23.6961 | max_drawdown_pct 1.7512 | cd_value 121.5300
- runner-up: 6V2_L04_doubleflush_extremeclose | trades 442 | max_return_pct 19.4782 | final_return_pct 19.2086 | max_drawdown_pct 1.0102 | cd_value 118.0043
- 5V2의 capitulation reclaim 잠재력을 double flush 코어로 재구성하면 MDD를 크게 줄이면서도 공식 long 승격이 가능하다는 점을 증명했다.
- 반면 delayed second push, quiet, absorb, contraction류의 과도한 추가 게이트는 성능 악화 또는 0트레이드로 이어졌다.

12. recent round note: 6V3_LONG10_REVIEWED
side: long_only
version_reference: 6V3_LONG10_REVIEWED
summary_file: local_results/6V3_LONG10_REVIEWED/*/summary.json
verdict: no_promotion_post_signal_gates_overnarrow_or_chase
notes:
- batch best: 6V3_L04_core_redtogreen | trades 9 | max_return_pct 0.3507 | final_return_pct 0.2983 | max_drawdown_pct 0.0542 | cd_value 100.2439
- next best: 6V3_L08_extreme_inside_pop | trades 8 | max_return_pct 0.0975 | final_return_pct 0.0975 | max_drawdown_pct 0.0591 | cd_value 100.0384
- L03_core_precompress_release는 0트레이드였고, L02_core_ema20snap과 L07_extreme_ema20hold는 각 1트레이드에 그쳤다.
- L05_core_holdbreak_follow는 trades 115까지 늘었지만 final_return_pct -0.7699, max_drawdown_pct 1.3228, cd_value 97.9175로 악화됐다.
- 즉 6V2의 승리 구조 위에 mid reclaim, ema snap, inside pop, hold-break 같은 후속 패턴 게이트를 덧붙이는 방식은 샘플 수를 지나치게 죽이거나, 반대로 늦은 추격형 진입을 만들어 엣지를 훼손했다.
- 따라서 다음 long 개선은 post-signal 패턴 덧칠보다, core 자체는 유지한 채 종목 상태 진단이나 위치/레짐 필터를 얇게 추가하는 방향이 더 적절하다.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경에서 실패한 전략은 reject 또는 archive로 남길 수 있지만, invalid_env는 남기지 않는다.
사용자가 결과를 저장소에 올렸으면, 결과 확인 직후 이 파일과 장단점 요약 문서를 함께 갱신한다.
