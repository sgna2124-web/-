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

8. recent round note: 4V2R12
side: split long_only / short_only
version_reference: 4V2R12
summary_file: local_results/4V2R12/*/summary.json
verdict: no_promotion_all_mdd_fail
notes:
- 4V2R12의 10개 전략은 전부 passes_mdd_lt_5=false, verdict=mdd_fail 이었다.
- batch long best(max_return_pct 기준): 4V2_L54_pullback_reset_resume | trades 45134 | max_return_pct 0.0290 | final_return_pct -42.8141 | max_drawdown_pct 42.9564 | cd_value 57.0602
- batch short best(max_return_pct 기준): 4V2_S54_bounce_reset_resume | trades 32619 | max_return_pct 2.4026 | final_return_pct -36.2795 | max_drawdown_pct 38.0478 | cd_value 63.4406
- 상대적으로 덜 나빴던 것은 fail-reject / reset-resume 계열이었지만, 공식 long reference cd_value 108.8106 및 official short reference cd_value 391.9606을 크게 하회했다.
- nr_ladder / midband tag / wick accumulation 계열은 거래 수가 과다하게 늘어나며(약 24만~68만 회) max_return_pct가 거의 0에 수렴했고, MDD도 91~99%대로 붕괴했다.
- 따라서 이번 라운드는 승격 후보 발굴보다는 "과다거래형 구조를 배제하고, 선택도가 높은 reset-resume / fail-reject 계열에 더 강한 위치 필터를 붙여야 한다"는 학습 기록으로 남긴다.

9. recent round note: 4V2R13
side: split long_only / short_only
version_reference: 4V2R13
summary_file: local_results/4V2R13/*/summary.json
verdict: partial_candidates_but_no_promotion
notes:
- 4V2R13은 10개 중 4개 전략이 passes_mdd_lt_5=true 를 기록했다. long에서는 L61, L65가, short에서는 S61, S65가 생존했다.
- batch long best(max_return_pct 기준): 4V2_L61_stacked_fail_reclaim | trades 3602 | max_return_pct 0.0683 | final_return_pct -3.2824 | max_drawdown_pct 3.4064 | cd_value 96.6595
- batch short best(max_return_pct 기준): 4V2_S65_ema50_upthrust_reversal | trades 404 | max_return_pct 0.3963 | final_return_pct 0.2828 | max_drawdown_pct 0.4946 | cd_value 99.8997
- long 쪽에서는 L61과 L65가 둘 다 MDD 5% 미만을 통과했고, 특히 L61은 공식 long reference 108.8106에 근접한 cd_value 96.6595까지 올라왔다. 다만 아직 공식 교체에는 실패했다.
- short 쪽에서는 S65가 가장 안정적이었다. 거래 수 404, max_drawdown_pct 0.4946, final_return_pct 0.2828로 구조적 생존성은 강했지만, 공식 short reference cd_value 391.9606과의 격차는 매우 컸다.
- 반면 EMA pullback / bounce pivot, inside breakout / breakdown, mid reclaim / loss resume 계열은 거래 수가 다시 수만~10만 회대로 커지며 MDD 29~69% 구간으로 무너졌다.
- 따라서 이번 라운드는 "강한 방향 필터와 매우 선택적인 상단/하단 스윕 반전 구조는 MDD를 확실히 줄일 수 있다"는 긍정적 진전으로 평가하되, 아직 max_return_pct 기반 cd_value가 공식 기준을 넘지는 못했으므로 승격은 보류한다.

10. recent round note: 4V2R14
side: split long_only / short_only
version_reference: 4V2R14
summary_file: local_results/4V2R14/*/summary.json
verdict: no_promotion_high_variance_archive_candidates
notes:
- 4V2R14는 selective fail-reclaim / fail-reject 계열을 다시 밀어본 배치였지만, 공식 승격 후보는 나오지 않았다.
- batch long best(max_return_pct 기준): 4V2_L71_tp03_fail_reclaim
- batch short best(max_return_pct 기준): 4V2_S72_tp03_upthrust_resume
- 숏 S72는 배치 내에서는 상대적으로 강한 폭발력을 보였지만 MDD 조건을 넘겨 공식 후보가 될 수 없었다.
- 롱 쪽도 일부 후보가 국지적 반응은 있었으나, 공식 long reference를 흔들 수준의 cd_value나 안정성을 만들지 못했다.
- 결론적으로 이번 배치는 "tp03류 실패 복귀 구조는 아이디어 저장 가치는 있으나, 방향/위치 필터 없이 단독 승격용으로 쓰기 어렵다"는 기록으로 남긴다.

11. recent round note: 4V2R15
side: split long_only / short_only
version_reference: 4V2R15
summary_file: local_results/4V2R15/*/summary.json
verdict: no_promotion_behavioral_family_needs_stronger_gates
notes:
- 4V2R15는 behavior flush, dd brake, post shock, tight flag, underreaction 같은 행동 서술형 구조를 탐색한 배치였다.
- batch long best(max_return_pct 기준): 4V2_L81_behavior_flush_absorb
- batch short best(max_return_pct 기준): 4V2_S84_upthrust_base_loss
- 롱 L81과 숏 S84가 배치 내 상대 강자였지만, 전체 풀 기준으로는 공식 승격에 필요한 MDD 통제와 재현성을 보여주지 못했다.
- 이번 배치는 이름이 설득력 있는 행동 기반 구조라도, 추세 위치 필터와 거래 수 제어가 없으면 실제 성능 우위로 이어지지 않는다는 점을 보여준다.

12. recent round note: 4V2R16
side: split long_only / short_only
version_reference: 4V2R16
summary_file: local_results/4V2R16/*/summary.json
verdict: no_promotion_overselection_and_zero_trade_warning
notes:
- 4V2R16은 shakeout reclaim, stair pullback, false loss, quiet base, vol reset 계열을 실험한 배치였다.
- batch long best(max_return_pct 기준): 4V2_L86_shakeout_reclaim_drive
- batch short best(max_return_pct 기준): 4V2_S86_bounce_reject_roll
- L88에서는 0트레이드가 발생했다. 이후부터는 거래 수와 재현성을 별도 체크 항목으로 본다.
- 이번 배치는 조건을 계속 좁히면 MDD는 줄어들 수 있어도 전략 자체가 사라질 수 있다는 점을 분명히 보여줬다.
- 따라서 selective 구조는 유지하되, 과선택화로 0트레이드가 나는 조합은 회피하는 방향으로 다음 전략을 설계한다.

13. recent round note: 5V2_COMBO10_REVIEWED
side: split long_only / short_only
version_reference: 5V2_COMBO10_REVIEWED
summary_file: local_results/5V2_COMBO10_REVIEWED/*/summary.json
verdict: long_candidate_but_no_promotion_short_defensive_only
notes:
- 10개 중 의미 있게 남은 것은 사실상 long L01과 short S01뿐이었다.
- batch long best(max_return_pct 기준): 5V2_L01_capitulation_reclaim | trades 3333 | max_return_pct 51.7718 | final_return_pct 50.9423 | max_drawdown_pct 13.7240 | cd_value 130.2269
- L01은 공식 long reference legacy_cd_value 108.8106을 max_return 기반 cd_value로 넘어섰지만, max_drawdown_pct 13.7240으로 MDD 규칙을 위반해 승격 실패했다.
- batch short best(max_return_pct 기준): 5V2_S01_blowoff_reject | trades 4063 | max_return_pct 3.9929 | final_return_pct 3.8276 | max_drawdown_pct 2.2939 | cd_value 101.4459
- S01은 MDD는 우수했지만 official short reference 391.9606에 크게 못 미쳐 baseline_fail 이다.
- 반면 L02~L05와 S02~S05는 거래 수가 약 24만~143만 회까지 폭증했고, max_drawdown_pct 90~100% 붕괴로 사실상 구조 실패가 확인됐다.
- 따라서 이번 라운드는 "급락 후 회수형 capitulation reclaim은 수익 잠재력이 실제로 존재하지만 아직 위험 압축이 부족하고, broad pullback / retest / compression / false-break 구조는 단독 운용 시 과다거래로 붕괴한다"는 학습 기록으로 남긴다.

14. recent round note: 6V2_LONG10_REVIEWED
side: long_only
version_reference: 6V2_LONG10_REVIEWED
summary_file: local_results/6V2_LONG10_REVIEWED/*/summary.json
verdict: long_promotion_doubleflush_core_established
notes:
- 6V2_LONG10_REVIEWED는 최근 long 전용 실험 중 처음으로 공식 기준선 교체를 만들었다.
- batch long best(max_return_pct 기준): 6V2_L01_doubleflush_core | trades 592 | max_return_pct 23.9191 | final_return_pct 23.6961 | max_drawdown_pct 1.7512 | cd_value 121.5300
- L01은 MDD 5% 미만을 유지한 상태에서 기존 long 기준선 108.8106을 넘어, 새 공식 long reference로 승격되었다.
- batch runner-up: 6V2_L04_doubleflush_extremeclose | trades 442 | max_return_pct 19.4782 | final_return_pct 19.2086 | max_drawdown_pct 1.0102 | cd_value 118.0043
- L04 역시 baseline_win 이지만, 수익 확장과 cd_value 모두 L01보다 낮아 2위 품질 강화형 후보로 보관한다.
- 반면 L02는 trend floor 강화 후 trades 54, final_return_pct -0.5371, cd_value 98.6931로 약화됐고, L05는 delayed second push 구조에서 trades 354, win_rate_pct 21.1864, final_return_pct -2.3852로 악화됐다.
- L03, L06, L08은 0트레이드였고 L10은 3트레이드에 그쳤다. 즉 quiet / absorb / contraction / 과도한 품질 게이트는 double flush 코어를 개선하는 대신 전략 자체를 소거할 위험이 크다.
- 따라서 이번 라운드는 "5V2의 capitulation reclaim 잠재력을 double flush 코어로 재구성하면 MDD를 크게 줄이면서도 공식 long 승격이 가능하다"는 것을 증명했고, 다음 long 설계는 broad continuation이 아니라 selective shock-reclaim 코어를 중심으로 진행해야 한다.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경에서 실패한 전략은 reject 또는 archive로 남길 수 있지만, invalid_env는 남기지 않는다.
사용자가 결과를 저장소에 올렸으면, 결과 확인 직후 이 파일과 CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md를 함께 갱신한다.
