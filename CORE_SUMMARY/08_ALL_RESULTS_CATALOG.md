결과 카탈로그

이 카탈로그에는 현재 비교 가능한 유효 결과와 역사적 참조 결과를 함께 남긴다.
단, invalid_env 실험은 남기지 않는다.

기록 원칙
공식 우선순위는 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 다.
max_return_pct는 반드시 기록한다.
legacy 결과 중 max_return_pct가 없는 항목은 unknown_legacy_not_recorded로 적고, current_cd_value는 pending_recompute_under_current_formula로 표시한다.
final_return_pct는 참고 지표다.
거래 수가 0이거나 극단적으로 적은 전략은 cd_value 숫자가 높아 보여도 공식 승격 후보로 보지 않는다.

현재 등록 항목

1. official long reference
strategy_name: 6V2_L01_doubleflush_core
side: long_only
family: long_only_doubleflush_cap_reclaim
version_reference: 6V2_LONG10_REVIEWED
result_path: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/
summary_file: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/summary.json
trades: 592
final_return_pct: 23.6961
max_return_pct: 23.9191
max_drawdown_pct: 1.7512
current_cd_value: 121.5300
verdict: official_long_reference
notes: 현재 long 공식 기준선.

2. official short reference
strategy_name: short_beh_dd_brake
side: short_only
family: short_only_behavioral_guards
version_reference: legacy_v52
result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
legacy_final_return_pct: 311.5456
legacy_mdd_pct: 4.7589
legacy_cd_value: 391.9606
verdict: official_short_reference
notes: 현재 short 공식 기준선.

3. archived previous long reference
strategy_name: long_hybrid_wick_bridge_halfhalf
version_reference: legacy_v67
legacy_final_return_pct: 9.9603
legacy_mdd_pct: 1.0456
legacy_cd_value: 108.8106
verdict: archive_previous_long_reference
notes: 6V2 승격 이전 long 기준선.

4. mixed historical reference
strategy_name: official_top200_reference
legacy_final_return_pct: 1120.69995
legacy_mdd_pct: 36.03441
legacy_cd_value: 780.8279
verdict: archive_reference_only

5. recent round note: 5V2_COMBO10_REVIEWED
verdict: long_candidate_but_no_promotion_short_defensive_only
notes:
- 5V2_L01_capitulation_reclaim가 높은 raw upside를 보였지만 MDD 13.7240으로 승격 실패.
- broad pullback/retest/compression 계열은 과다거래로 붕괴.

6. recent round note: 6V2_LONG10_REVIEWED
verdict: long_promotion_doubleflush_core_established
notes:
- 6V2_L01_doubleflush_core가 long 공식 기준선으로 승격.
- 6V2_L04_doubleflush_extremeclose도 강한 runner-up으로 보관.

7. recent round note: 6V3_LONG10_REVIEWED
verdict: no_promotion_post_signal_gates_overnarrow_or_chase
notes:
- 후속 패턴 게이트 강화는 샘플 수를 죽이거나 늦은 추격형 진입으로 악화.

8. recent round note: 6V4_LONG10_REVIEWED
verdict: no_promotion_state_filters_overshot_or_unbounded
notes:
- hard state gate는 과선택화.
- 신규 전략군은 cooldown/rarity guard 부족으로 과다거래 붕괴.

9. recent round note: 6V5_LONG10_REVIEWED
verdict: no_promotion_softscore_stabilized_but_edge_diluted
notes:
- soft score + spacing으로 안정화에는 성공했지만 엣지가 희석.
- 같은 family 미세조정보다 신규 family 개발로 이동.

10. recent round note: 7V1_LONG10_REVIEWED
verdict: no_promotion_new_reversal_family_raw_edge_found_but_samebar_overtrading_failed
notes:
- 신규 reversal family의 raw upside 확인.
- same-bar reversal을 넓게 허용하면 과다거래와 MDD 팽창 재현.

11. recent round note: 7V2_LONG40_REVIEWED
verdict: no_promotion_new_family_mdd_lt_5_reached_110_cd_zone
notes:
- L09 beartrap, L07 wick 제한형이 MDD<5에서도 cd 110대 도달.
- 공식 기준선 121.5300을 넘는 MDD<5 전략은 없음.
- 다음 우선순위는 L09 1순위, L07 2순위.

12. recent round note: 7V3_LONG40_REVIEWED
verdict: no_promotion_l09_l07_priority_reconfirmed_and_runtime_improved
notes:
- L09 beartrap family가 여전히 최우선.
- L07 wick family가 안정적 2순위.
- 속도 개선 실행 구조가 실제 성과로 확인됨.

13. recent round note: 7V4_LONG40_REVIEWED
side: long_only
version_reference: 7V4_LONG40_REVIEWED
summary_file: local_results/7V4_LONG40_REVIEWED/*/summary.json
verdict: no_promotion_candidate_cd_win_mdd_fail_locked_l09_priority
notes:
- batch top candidate_cd_win_mdd_fail: 7V4_L09_V09_beartrap_cluster_pressure | trades 6863 | max_return_pct 42.1291 | final_return_pct 41.1544 | max_drawdown_pct 11.2133 | cd_value 125.3264
- next candidate_cd_win_mdd_fail: 7V4_L09_V03_beartrap_lowanchor_drive | trades 7664 | max_return_pct 40.1602 | final_return_pct 39.3617 | max_drawdown_pct 11.9139 | cd_value 122.7583
- best under MDD<5: 7V4_L09_V02_beartrap_extreme_synergy | trades 730 | max_return_pct 16.0180 | final_return_pct 15.8330 | max_drawdown_pct 2.5330 | cd_value 112.8990
- next under MDD<5: 7V4_L07_V02_wick_drive_reclaim | trades 1443 | max_return_pct 16.0068 | final_return_pct 15.6410 | max_drawdown_pct 3.2136 | cd_value 111.9247
- 7V4는 candidate_cd_win_mdd_fail 규칙을 적용한 첫 라운드로, L09 family 안에 기준선 이상 cd를 가진 개선 후보가 실제로 존재함을 고정했다.
- 다음 단계는 L09의 high-cd raw 후보를 보관하면서 MDD를 낮추는 구조 개선 시도였다.

14. recent round note: 8V1_LONG50_REVIEWED
side: long_only
version_reference: 8V1_LONG50_REVIEWED
summary_file: local_results/8V1_LONG50_REVIEWED/*/summary.json
verdict: no_promotion_new_families_failed_to_create_edge_return_to_l09_l07
notes:
- batch best: 8V1_L25_V01_washout_squeeze_release | trades 54 | max_return_pct 1.2888 | final_return_pct 1.2567 | max_drawdown_pct 0.1903 | cd_value 101.0640
- next: 8V1_L25_V08_squeeze_shockage_window | trades 222 | max_return_pct 0.9310 | final_return_pct 0.9310 | max_drawdown_pct 0.4424 | cd_value 100.4845
- best non-squeeze but still weak: 8V1_L22_V06_inside_lowanchor_pop | trades 3372 | max_return_pct 3.2382 | final_return_pct 1.7901 | max_drawdown_pct 1.7176 | cd_value 100.0417
- 8V1의 새로운 family들(L21 shock_absorb, L22 inside, L23 microbase, L24 holdpop, L25 squeeze)은 이전 L09/L07 family와 달리 raw upside 자체가 거의 없었다.
- 특히 L24 holdpop family는 trades 5만~19만 회대로 폭증하며 MDD 44~87% 구간으로 붕괴해 현재 형태로는 폐기 대상이다.
- L25 squeeze family는 MDD는 낮았지만 수익과 max_return_pct가 지나치게 얕아 long 기준선 도전력은 거의 없었다.
- 결론적으로 8V1은 "이전과 다른 50개 전략"이라는 조건은 충족했지만, 새로운 엣지를 만들지 못했다. 다음 단계는 다시 L09/L07 중심으로 회귀하고, 8V1에서는 after_pause, shockage_window, lowanchor_pop 같은 일부 보조 태그만 제한적으로 참고한다.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경 실패는 기록으로 남기되 invalid_env는 남기지 않는다.
