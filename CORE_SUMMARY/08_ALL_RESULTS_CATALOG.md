결과 카탈로그

이 카탈로그에는 현재 비교 가능한 유효 결과와 역사적 참조 결과를 함께 남긴다.
단, invalid_env 실험은 남기지 않는다.

기록 원칙
공식 우선순위는 MDD 5% 미만 통과 여부 -> official_cd_value -> max_return_pct/trades/재현성 보조 판단이다.
max_return_pct는 반드시 기록한다.
final_return_pct는 참고 지표다.
거래 수가 0이거나 극단적으로 적은 전략은 cd_value 숫자가 높아 보여도 공식 승격 후보로 보지 않는다.

중요 보정
현재 프로젝트의 공식 cd_value는 사용자가 정의한 자산 기준 계산식으로 고정한다.
cd_value = 100 * (1 - (abs(max_drawdown_pct) / 100)) * (1 + (max_return_pct / 100))
max_return_pct / max_drawdown_pct 방식은 폐기된 비공식 ratio이며 앞으로 공식 cd_value로 쓰지 않는다.
이전 문서에 남아 있는 official_ratio, current_cd_value_ratio, legacy_equity_cd_value 표기는 혼동 가능성이 있으므로 신규 판정에서는 official_cd_value 또는 cd_value만 사용한다.

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
official_cd_value: 121.7490
verdict: official_long_reference
notes: 현재 long 공식 기준선. 공식 승격 비교에는 official_cd_value를 사용한다.

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
notes: 현재 short 공식 기준선. legacy 결과는 max_return_pct가 없으면 current formula 재계산 전까지 참고값으로만 본다.

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
- official_cd_value: 121.7490.
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
- L09 beartrap, L07 wick 제한형이 MDD<5에서도 110대 cd 영역 도달.
- 공식 기준선을 넘는 MDD<5 전략은 없음.
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
- batch top candidate_cd_win_mdd_fail: 7V4_L09_V09_beartrap_cluster_pressure | trades 6863 | max_return_pct 42.1291 | final_return_pct 41.1544 | max_drawdown_pct 11.2133 | legacy_cd_value 125.3264
- next candidate_cd_win_mdd_fail: 7V4_L09_V03_beartrap_lowanchor_drive | trades 7664 | max_return_pct 40.1602 | final_return_pct 39.3617 | max_drawdown_pct 11.9139 | legacy_cd_value 122.7583
- best under MDD<5: 7V4_L09_V02_beartrap_extreme_synergy | trades 730 | max_return_pct 16.0180 | final_return_pct 15.8330 | max_drawdown_pct 2.5330 | legacy_cd_value 112.8990
- next under MDD<5: 7V4_L07_V02_wick_drive_reclaim | trades 1443 | max_return_pct 16.0068 | final_return_pct 15.6410 | max_drawdown_pct 3.2136 | legacy_cd_value 111.9247
- 7V4는 candidate_cd_win_mdd_fail 규칙을 적용한 첫 라운드로, L09 family 안에 고잠재력 개선 후보가 실제로 존재함을 고정했다.

14. recent round note: 8V1_LONG50_REVIEWED
side: long_only
version_reference: 8V1_LONG50_REVIEWED
summary_file: local_results/8V1_LONG50_REVIEWED/*/summary.json
verdict: no_promotion_new_families_failed_to_create_edge_return_to_l09_l07
notes:
- batch best: 8V1_L25_V01_washout_squeeze_release | trades 54 | max_return_pct 1.2888 | final_return_pct 1.2567 | max_drawdown_pct 0.1903 | legacy_cd_value 101.0640
- 8V1의 새로운 family들은 이전 L09/L07 family와 달리 raw upside 자체가 거의 없었다.
- 특히 L24 holdpop family는 과다거래로 붕괴해 폐기 대상이다.

15. recent round note: 8V2_LONG100_REVIEWED
side: long_only
version_reference: 8V2_LONG100_REVIEWED
summary_file: local_results/8V2_LONG100_REVIEWED/*/summary.json
verdict: no_promotion_new_families_100_failed_again_return_to_l09_l07
notes:
- batch best: 8V2_L31_V01_core_relaunch | trades 107 | max_return_pct 1.7448 | final_return_pct 1.6503 | max_drawdown_pct 0.3516 | legacy_cd_value 101.2929
- 8V2의 신규 family들은 8V1보다 약간 나아졌지만, 이전 L09/L07 reversal family와 비교할 raw upside가 전혀 없었다.
- 특히 L32, L33, L40 축은 trades 20만~92만 회대로 폭증하며 MDD 93~99.99% 구간으로 붕괴해 broad overtrading failure로 분류한다.

16. recent round note: 8V3_LONG100_REVIEWED
side: long_only
version_reference: 8V3_LONG100_REVIEWED
summary_file: local_results/8V3_LONG100_REVIEWED/*/summary.json
verdict: no_promotion_l09_l07_return_success_candidate_pool_expanded
notes:
- batch best candidate_cd_win_mdd_fail: 8V3_L09_V51_microbase_pop | trades 2277 | max_return_pct 42.0017 | final_return_pct 41.5097 | max_drawdown_pct 6.3144 | legacy_cd_value 132.5742
- next candidate_cd_win_mdd_fail: 8V3_L09_V27_failed_break_pivot | trades 7656 | max_return_pct 40.2473 | final_return_pct 39.4890 | max_drawdown_pct 11.4314 | legacy_cd_value 123.5435
- next candidate_cd_win_mdd_fail: 8V3_L09_V09_cluster_pressure | trades 6869 | max_return_pct 38.9188 | final_return_pct 38.1414 | max_drawdown_pct 11.3164 | legacy_cd_value 122.5087
- next candidate_cd_win_mdd_fail: 8V3_L09_V28_refire_block | trades 6347 | max_return_pct 42.3732 | final_return_pct 41.4101 | max_drawdown_pct 14.0253 | legacy_cd_value 121.5769
- best under MDD<5: 8V3_L09_V41_exhaustion_recover | trades 1126 | max_return_pct 19.7022 | final_return_pct 19.4175 | max_drawdown_pct 3.0952 | legacy_cd_value 115.7213
- 8V3는 8V1/8V2 이후 다시 L09/L07으로 회귀하자 즉시 성과가 회복됐고, L09의 candidate_cd_win_mdd_fail 풀이 4개로 늘어났다.

17. recent round note: 8V4_LONG400_REVIEWED
side: long_only
version_reference: 8V4_LONG400_REVIEWED
summary_file: local_results/8V4_LONG400_REVIEWED/*/summary.json
verdict: no_promotion_v51_became_clear_primary_core
notes:
- batch best candidate_cd_win_mdd_fail: 8V4_V51_V002_core_rare22_c1 | trades 2276 | max_return_pct 44.2664 | final_return_pct 43.6673 | max_drawdown_pct 6.7587 | official_cd_value 134.5172
- next: 8V4_V51_V001_core_base | trades 2277 | max_return_pct 43.8091 | final_return_pct 43.2929 | max_drawdown_pct 6.7547 | official_cd_value 134.0943
- best under MDD<5 overall: 8V4_V51_V022_lowanchor_rare22_c1 | trades 1040 | max_return_pct 21.5445 | final_return_pct 21.2903 | max_drawdown_pct 3.0752 | official_cd_value 117.8075
- next under MDD<5: 8V4_V51_V021_lowanchor_base | trades 1040 | max_return_pct 21.1577 | final_return_pct 20.9035 | max_drawdown_pct 3.1165 | official_cd_value 117.3784
- 8V4는 V51 microbase_pop 계열이 clear 최우선 코어로 부상한 라운드였다.
- raw/cd는 유망했지만, 남은 핵심 과제는 V51의 MDD를 6.7대에서 5 아래로 더 내리는 것으로 정리되었다.

18. recent round note: 8V5_LONG300_REVIEWED
side: long_only
version_reference: 8V5_LONG300_REVIEWED
summary_file: local_results/8V5_LONG300_REVIEWED/*/summary.json
verdict: no_promotion_v51_parameter_tuning_helped_top_mdd_but_safe_branch_slightly_weaker
notes:
- batch best candidate_cd_win_mdd_fail: 8V5_V51P_V002_core_rare22_c1 | trades 2277 | max_return_pct 42.1517 | final_return_pct 41.6763 | max_drawdown_pct 6.3109 | official_cd_value 133.1863
- next: 8V5_V51P_V001_core_base | trades 2277 | max_return_pct 41.4900 | final_return_pct 41.0096 | max_drawdown_pct 6.2801 | official_cd_value 132.6036
- best under MDD<5 overall: 8V5_V51P_V012_strict_rare22_c1 | trades 1040 | max_return_pct 19.7596 | final_return_pct 19.5333 | max_drawdown_pct 2.7359 | official_cd_value 116.4858
- next under MDD<5: 8V5_V51P_V011_strict_base | trades 1040 | max_return_pct 19.4241 | final_return_pct 19.1976 | max_drawdown_pct 2.6505 | official_cd_value 116.2587
- 8V5는 V51만 300개로 확장해 파라미터 조정, 장점 극대화, 단점 커버를 함께 시험한 라운드였다.
- top candidate의 MDD는 8V4의 6.75대에서 8V5의 6.28~6.31대로 실제 개선되었다.
- 반면 MDD<5 최고권은 8V4의 official_cd_value 117.8075보다 낮은 116.4858에 그쳤다.
- 해석은 명확하다. 파라미터 조정은 top candidate를 더 근접하게 만들었지만, safe branch를 더 강하게 만들지는 못했다.

19. recent round note: 8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3
side: long_only
version_reference: 8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3
summary_file: local_results/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3/master_summary.txt
registry_file: local_results/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3_registry.csv
verdict: no_promotion_mdd_compressed_but_edge_overfiltered
notes:
- failed_symbols: 0
- baseline_candidate_under_mdd5: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V001_core_base | trades 652 | max_return_pct 5.2510 | final_return_pct 3.0599 | max_drawdown_pct 2.1312 | official_cd_value 103.0070
- raw_cd_candidate_any_mdd: same_as_baseline_candidate_under_mdd5
- next: 8V6_P2_CORE_BASE_I050_mdd_compress_mdd15 | parent 8V5_V51P_V001_core_base | trades 501 | max_return_pct 3.7822 | final_return_pct 2.2944 | max_drawdown_pct 1.5658 | official_cd_value 102.1572
- next: 8V6_P3_SHOCKLOW_RARE22_C1_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V032_shocklow_rare22_c1 | trades 666 | max_return_pct 5.1129 | final_return_pct 2.7986 | max_drawdown_pct 2.2018 | official_cd_value 102.7978
- next: 8V6_P1_CORE_RARE22_C1_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V002_core_rare22_c1 | trades 668 | max_return_pct 4.9854 | final_return_pct 2.6855 | max_drawdown_pct 2.1985 | official_cd_value 102.6784
- 8V6는 MDD 5 미만을 다수 만들었으나, max_return_pct가 8V5의 41~42%대에서 3~5%대로 급감했다.
- 핵심 해석: V51 문제를 진입 희소화와 강한 전단 필터로 해결하려 하면 MDD보다 edge가 먼저 죽는다.
- 다음 단계: core_base/core_rare22_c1의 진입 밀도를 최대한 유지하면서 사후 브레이크, 손실 군집 회피, exit/hold/stop 재조정으로 MDD를 낮춰야 한다.

20. recent round note: 8V7_AB_BEST_200_FROM_8V6_CANDIDATE
side: long_only
version_reference: 8V7_AB_BEST_200_FROM_8V6_CANDIDATE
summary_file: local_results/8V7_AB_BEST_200_FROM_8V6_CANDIDATE/master_summary.txt
registry_file: local_results/8V7_AB_BEST_200_FROM_8V6_CANDIDATE/8V7_AB_BEST_200_FROM_8V6_CANDIDATE_registry.csv
verdict: no_promotion_more_mdd_compression_but_edge_destroyed
notes:
- failed_symbols: 0
- baseline_candidate_under_mdd5: 8V7_AB_BEST_I070_post_loss_brake_plb20 | parent 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | group post_loss_brake | trades 93 | win_rate_pct 60.2151 | final_return_pct 1.1655 | max_return_pct 1.3290 | max_drawdown_pct 0.2122 | official_cd_value 101.1140
- raw_cd_candidate_any_mdd: same_as_baseline_candidate_under_mdd5
- candidate_cd_win_mdd_fail: none
- next: 8V7_AB_BEST_I068_post_loss_brake_plb18 | trades 104 | max_return_pct 1.2213 | max_drawdown_pct 0.2154 | official_cd_value 101.0033
- next: 8V7_AB_BEST_I193_soft_safe_mix_ssm13 | trades 96 | max_return_pct 0.9030 | max_drawdown_pct 0.1729 | official_cd_value 100.7285
- 8V7은 MDD를 0.15~0.42% 수준까지 더 낮추었지만, max_return_pct가 0.7~1.8% 수준으로 붕괴했다.
- post_loss_brake와 soft_safe_mix는 손실 군집 차단 도구로 유효하지만, 이미 희소화된 8V6 후보 위에 얹으면 edge가 완전히 죽는다.
- 다음 단계는 8V7 top 전략을 부모로 삼지 않고, 8V5 core_base/core_rare22_c1로 되돌아가 post_loss_brake를 가벼운 부분 브레이크로만 이식하는 것이다.

21. recent round note: 8V8_LONG_DUAL_BEST_200_UNTRIED
side: long_only
version_reference: 8V8_LONG_DUAL_BEST_200_UNTRIED
summary_file: local_results/8V8_LONG_DUAL_BEST_200_UNTRIED/master_summary.txt
registry_file: local_results/8V8_LONG_DUAL_BEST_200_UNTRIED/8V8_LONG_DUAL_BEST_200_UNTRIED_registry.csv
verdict: no_promotion_mdd_pass_but_edge_still_too_low
notes:
- failed_symbols: 0
- baseline_candidate_under_mdd5: 8V8_RAWV51_I080_raw_official_conversion_r080 | parent 8V4_V51_V002_core_rare22_c1 | group raw_official_conversion | trades 1027 | win_rate_pct 52.6777 | final_return_pct 6.0489 | max_return_pct 9.6311 | max_drawdown_pct 3.5251 | official_cd_value 105.766560
- raw_cd_candidate_any_mdd: same_as_baseline_candidate_under_mdd5
- candidate_cd_win_mdd_fail: none
- next: 8V8_RAWV51_I090_raw_official_conversion_r090 | trades 584 | max_return_pct 7.7293 | max_drawdown_pct 2.5052 | official_cd_value 105.030527
- next: 8V8_SAFE6V2_I040_safe_dd_brake_s040 | trades 1110 | max_return_pct 6.4903 | max_drawdown_pct 2.3197 | official_cd_value 104.020008
- next: 8V8_RAWV51_I100_raw_official_conversion_r100 | trades 675 | max_return_pct 6.5341 | max_drawdown_pct 2.7078 | official_cd_value 103.649405
- next: 8V8_RAWV51_I004_raw_cluster_cover_r004 | trades 1324 | max_return_pct 7.1702 | max_drawdown_pct 3.3138 | official_cd_value 103.618780
- 8V8은 raw_official_conversion으로 V51 raw 후보를 MDD 5% 미만으로 변환하는 데는 성공했지만, max_return_pct가 9.6311까지 낮아져 기준선 121.7490을 넘지 못했다.
- 8V8 top은 8V6/8V7보다 trade density 보존은 낫지만, 8V5 raw의 41~42%대 max_return_pct와 비교하면 edge 손실이 여전히 크다.
- 다음 단계는 8V8 top을 직접 부모로 삼기보다 V51 core_base/core_rare22_c1에 raw_official_conversion의 일부 로직만 약하게 이식하는 것이다.

22. recent round note: 8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED
side: long_only
version_reference: 8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED
summary_file: local_results/8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED/master_summary.txt
registry_file: local_results/8V9_LONG_DUAL_BEST_200_UNTRIED_NO_TRADE_CAP_FIXED_registry.csv
verdict: no_promotion_trade_density_improved_but_mdd_rise_cancelled_cd_gain
notes:
- failed_symbols: 0
- baseline_candidate_under_mdd5: 8V9_RAWV51_I013_entry_timing_window_r013 | parent 8V4_V51_V002_core_rare22_c1 | group entry_timing_window | trades 1292 | win_rate_pct 52.9412 | final_return_pct 6.3735 | max_return_pct 10.4863 | max_drawdown_pct 4.3852 | official_cd_value 105.640342
- raw_cd_candidate_any_mdd: same_as_baseline_candidate_under_mdd5
- candidate_cd_win_mdd_fail: none
- next: 8V9_RAWV51_I014_entry_timing_window_r014 | trades 1387 | max_return_pct 9.2488 | max_drawdown_pct 4.0206 | official_cd_value 104.857076
- next: 8V9_RAWV51_I012_entry_timing_window_r012 | trades 1403 | max_return_pct 10.7723 | max_drawdown_pct 5.7564 | official_cd_value 104.392873 | MDD 초과
- next: 8V9_RAWV51_I054_candle_quality_gate_cq054 | trades 1123 | max_return_pct 8.7562 | max_drawdown_pct 4.2363 | official_cd_value 104.149400
- next: 8V9_RAWV51_I046_candle_quality_gate_cq046 | trades 1546 | max_return_pct 8.7499 | max_drawdown_pct 5.0119 | official_cd_value 103.299765 | MDD 초과
- 8V9는 거래 수 제한을 제거하고도 top 후보 거래 수를 1292~1546까지 회복했다.
- 8V9는 8V8보다 max_return_pct를 9.6311에서 10.4863까지 올렸지만 MDD도 3.5251에서 4.3852로 상승해 official_cd_value는 105.766560에서 105.640342로 소폭 하락했다.
- 핵심 해석: trade cap 제거 방향은 맞지만, entry_timing_window와 candle_quality_gate만으로는 V51 raw edge를 기준선 초과 수준까지 복원하지 못한다.
- 다음 단계: 거래 수를 인위적으로 제한하지 않고, V51 raw core에 사후 위험 제어, 손실 군집 회피, exit/hold/stop 조정, 시장 상태 회피를 약하게 결합해야 한다.

23. recent round note: 8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP
side: long_only
version_reference: 8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP
summary_file: local_results/8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP/master_summary.txt
verdict: no_promotion_big_improvement_but_6v2_still_not_exceeded
notes:
- failed_symbols: 0
- baseline_candidate_under_mdd5: 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176 | parent 8V9_RAWV51_I013_entry_timing_window_r013 | group b_rescue_mix | trades 1714 | win_rate_pct 38.7981 | final_return_pct 15.7815 | max_return_pct 20.9416 | max_drawdown_pct 4.4791 | official_cd_value 115.524476
- raw_cd_candidate_any_mdd: 8V10_B_ANYCD_I013_I302_b_trend_runner_b102 | parent 8V9_RAWV51_I013_entry_timing_window_r013 | group b_trend_runner | trades 1263 | win_rate_pct 46.9517 | final_return_pct 20.0025 | max_return_pct 26.3362 | max_drawdown_pct 5.6679 | official_cd_value 119.175585 | MDD 초과
- official long reference remains 6V2_L01_doubleflush_core | max_return_pct 23.9191 | max_drawdown_pct 1.7512 | official_cd_value 121.7490
- 8V10은 8V8/8V9의 105대 cd_value 정체를 115.524476까지 끌어올렸다.
- MDD<5 1위는 거래 수 1714로 거래 밀도도 좋고 max_return_pct도 20.9416까지 회복했다.
- MDD 무관 1위는 max_return_pct 26.3362와 cd_value 119.175585로 기준선에 근접했지만 MDD 5.6679로 승격 실패.
- 다음 후보 A는 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176, 후보 B는 8V10_B_ANYCD_I013_I302_b_trend_runner_b102.
- 다음 라운드는 A의 max_return_pct를 23~26%로 올리거나, B의 MDD를 4.9 이하로 압축하는 방향이다.

24. recent round note: 8V11_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP
side: long_and_short
version_reference: 8V11_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP
summary_file: local_results/8V11_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/master_summary.txt
addendum_file: CORE_SUMMARY/33_8V11_LONG_SHORT_MAIN_MAX_400_ADDENDUM.md
verdict: no_promotion_long_safe_below_8v10_short_failed_by_low_trade_count
notes:
- failed_symbols: 0
- long_mdd5_cd_1: long_max_v1_51_lx_deep_absorb_lx051 | parent 8V4_V51_V002_core_rare22_c1 | group lx_deep_absorb | trades 1024 | win_rate_pct 47.5586 | final_return_pct 14.0480 | max_return_pct 18.2706 | max_drawdown_pct 3.5871 | official_cd_value 114.028108
- long_any_cd_1: same_as_long_mdd5_cd_1
- short_mdd5_cd_1: short_max_v1_87_sx_vol_reversal_sx087 | parent short_only_reference_1x | group sx_vol_reversal | trades 6 | win_rate_pct 16.6667 | final_return_pct 0.3790 | max_return_pct 0.3800 | max_drawdown_pct 0.0554 | official_cd_value 100.324360
- short_any_cd_1: same_as_short_mdd5_cd_1
- baseline change check: long_main_v1 beat False, long_max_v1 beat False, short_main_v1 beat False, short_max_v1 beat False.
- 8V11 long top은 8V8/8V9보다는 낫지만 8V10 MDD<5 1위 115.524476보다 낮고, 공식 long 기준선 121.749029를 넘지 못했다.
- lx_deep_absorb는 MDD 압축 모듈로 보관하되 단독 심화 우선순위는 낮춘다.
- short 개선군은 trades 2~38 수준으로 극단적으로 적어 기준 후보로 삼지 않는다.
- 다음 라운드는 8V10 후보 A b_rescue_mix와 후보 B b_trend_runner를 중심으로 하고, 8V11 lx_deep_absorb/lx_trend_repair는 보조 모듈로만 혼합한다.

25. recent round note: 8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP
side: long_and_short
version_reference: 8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP
summary_file: local_results/8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/master_summary.txt
addendum_file: CORE_SUMMARY/34_8V12_LONG_SHORT_MAIN_MAX_400_ADDENDUM.md
verdict: no_promotion_mdd_compression_or_density_recovery_but_below_8v10_short_invalid_low_trades
notes:
- failed_symbols: 0
- long_mdd5_cd_1: long_max_v1_55_lx12_second_leg_absorption_lx12_2_14 | parent 8V4_V51_V002_core_rare22_c1 | group lx12_second_leg_absorption | trades 849 | win_rate_pct 43.2273 | final_return_pct 5.7941 | max_return_pct 7.0913 | max_drawdown_pct 1.2955 | official_cd_value 105.703904
- long_any_cd_1: long_max_v1_1_lx12_range_expansion_runner_lx12_0_00 | parent 8V4_V51_V002_core_rare22_c1 | group lx12_range_expansion_runner | trades 5737 | max_return_pct 17.3243 | max_drawdown_pct 7.5061 | official_cd_value 108.517839 | MDD 초과
- short_mdd5_cd_1: short_max_v1_25_sx12_pullback_continuation_sx12_1_04 | parent short_only_reference_1x | group sx12_pullback_continuation | trades 3 | max_return_pct 0.0304 | max_drawdown_pct 0.0077 | official_cd_value 100.022693 | low_trade_invalid
- short_any_cd_1: same_as_short_mdd5_cd_1 | low_trade_invalid
- baseline change check: long_main_v1 beat False, long_max_v1 beat False, short_main_v1 beat False, short_max_v1 beat False.
- 8V12는 기준선 갱신 실패다.
- 8V12 long top은 8V11 long top 114.028108 및 8V10 A 115.524476보다 낮다.
- lx12_second_leg_absorption은 MDD 압축 보조 모듈로 보관한다.
- lx12_range_expansion_runner는 거래 밀도/수익률 회복 보조 모듈로 보관한다.
- short 개선군은 trades 3 수준으로 검증 불능이므로 부모 후보로 쓰지 않는다.
- 다음 라운드는 8V10 후보 A b_rescue_mix와 후보 B b_trend_runner를 중심으로 하고, 8V12 모듈은 hard filter가 아니라 부분 brake/점수 보정/exit-hold 조정으로만 혼합한다.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경 실패는 기록으로 남기되 invalid_env는 남기지 않는다.
