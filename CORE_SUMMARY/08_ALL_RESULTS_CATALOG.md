결과 카탈로그

이 카탈로그에는 현재 비교 가능한 유효 결과와 역사적 참조 결과를 함께 남긴다.
단, invalid_env 실험은 남기지 않는다.

기록 원칙
공식 우선순위는 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 다.
max_return_pct는 반드시 기록한다.
legacy 결과 중 max_return_pct가 없는 항목은 unknown_legacy_not_recorded로 적고, current_cd_value는 pending_recompute_under_current_formula로 표시한다.
final_return_pct는 참고 지표다.
거래 수가 0이거나 극단적으로 적은 전략은 cd_value 숫자가 높아 보여도 공식 승격 후보로 보지 않는다.

중요 보정
현재 프로젝트의 공식 cd_value는 max_return_pct / max_drawdown_pct다.
기존 6V2~8V5 문서에 기록된 121.5300, 132.7352 같은 값은 과거 legacy_equity_cd_value 성격이 섞여 있을 수 있다.
공식 ratio 비교가 필요한 경우 max_return_pct / max_drawdown_pct로 재계산한다.
예: 6V2_L01_doubleflush_core는 23.9191 / 1.7512 = 13.6587이다.

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
current_cd_value_ratio: 13.6587
legacy_equity_cd_value: 121.5300
verdict: official_long_reference
notes: 현재 long 공식 기준선. 공식 승격 비교에는 current_cd_value_ratio를 사용한다.

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
- 공식 ratio: max_return_pct 23.9191 / max_drawdown_pct 1.7512 = 13.6587.
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
- L09 beartrap, L07 wick 제한형이 MDD<5에서도 cd 110대 legacy 영역 도달.
- 공식 기준선 ratio를 넘는 MDD<5 전략은 없음.
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
- batch best candidate_cd_win_mdd_fail: 8V4_V51_V002_core_rare22_c1 | trades 2276 | max_return_pct 44.2664 | final_return_pct 43.6673 | max_drawdown_pct 6.7587 | official_ratio 6.5481 | legacy_cd_value 133.9572
- next: 8V4_V51_V001_core_base | trades 2277 | max_return_pct 43.8091 | final_return_pct 43.2929 | max_drawdown_pct 6.7547 | official_ratio 6.4857 | legacy_cd_value 133.6139
- best under MDD<5 overall: 8V4_V51_V022_lowanchor_rare22_c1 | trades 1040 | max_return_pct 21.5445 | final_return_pct 21.2903 | max_drawdown_pct 3.0752 | official_ratio 7.0059 | legacy_cd_value 117.5603
- next under MDD<5: 8V4_V51_V021_lowanchor_base | trades 1040 | max_return_pct 21.1577 | final_return_pct 20.9035 | max_drawdown_pct 3.1165 | official_ratio 6.7889 | legacy_cd_value 117.1355
- 8V4는 V51 microbase_pop 계열이 clear 최우선 코어로 부상한 라운드였다.
- raw/cd는 유망했지만, 남은 핵심 과제는 V51의 MDD를 6.7대에서 5 아래로 더 내리는 것으로 정리되었다.

18. recent round note: 8V5_LONG300_REVIEWED
side: long_only
version_reference: 8V5_LONG300_REVIEWED
summary_file: local_results/8V5_LONG300_REVIEWED/*/summary.json
verdict: no_promotion_v51_parameter_tuning_helped_top_mdd_but_safe_branch_slightly_weaker
notes:
- batch best candidate_cd_win_mdd_fail: 8V5_V51P_V002_core_rare22_c1 | trades 2277 | max_return_pct 42.1517 | final_return_pct 41.6763 | max_drawdown_pct 6.3109 | official_ratio 6.6792 | legacy_cd_value 132.7352
- next: 8V5_V51P_V001_core_base | trades 2277 | max_return_pct 41.4900 | final_return_pct 41.0096 | max_drawdown_pct 6.2801 | official_ratio 6.6066 | legacy_cd_value 132.1541
- best under MDD<5 overall: 8V5_V51P_V012_strict_rare22_c1 | trades 1040 | max_return_pct 19.7596 | final_return_pct 19.5333 | max_drawdown_pct 2.7359 | official_ratio 7.2223 | legacy_cd_value 116.2630
- next under MDD<5: 8V5_V51P_V011_strict_base | trades 1040 | max_return_pct 19.4241 | final_return_pct 19.1976 | max_drawdown_pct 2.6505 | official_ratio 7.3285 | legacy_cd_value 116.0383
- 8V5는 V51만 300개로 확장해 파라미터 조정, 장점 극대화, 단점 커버를 함께 시험한 라운드였다.
- top candidate의 MDD는 8V4의 6.75대에서 8V5의 6.28~6.31대로 실제 개선되었다.
- 반면 MDD<5 최고권은 8V4의 legacy 117.5603보다 약간 낮은 legacy 116.2630에 그쳤다.
- 해석은 명확하다. 파라미터 조정은 top candidate를 더 근접하게 만들었지만, safe branch를 더 강하게 만들지는 못했다.

19. recent round note: 8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3
side: long_only
version_reference: 8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3
summary_file: local_results/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3/master_summary.txt
registry_file: local_results/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3/8V6_TOP3_300_FROM_8V5_WINDOWS_SAFE_V3_registry.csv
verdict: no_promotion_mdd_compressed_but_edge_overfiltered
notes:
- failed_symbols: 0
- batch best official_ratio: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V001_core_base | trades 652 | max_return_pct 5.2510 | final_return_pct 3.0599 | max_drawdown_pct 2.1312 | cd_value 2.4639 | legacy_equity_cd_value 100.8636
- next: 8V6_P2_CORE_BASE_I050_mdd_compress_mdd15 | parent 8V5_V51P_V001_core_base | trades 501 | max_return_pct 3.7822 | final_return_pct 2.2944 | max_drawdown_pct 1.5658 | cd_value 2.4155 | legacy_equity_cd_value 100.6927
- next: 8V6_P3_SHOCKLOW_RARE22_C1_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V032_shocklow_rare22_c1 | trades 666 | max_return_pct 5.1129 | final_return_pct 2.7986 | max_drawdown_pct 2.2018 | cd_value 2.3222 | legacy_equity_cd_value 100.5352
- next: 8V6_P1_CORE_RARE22_C1_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V002_core_rare22_c1 | trades 668 | max_return_pct 4.9854 | final_return_pct 2.6855 | max_drawdown_pct 2.1985 | cd_value 2.2677 | legacy_equity_cd_value 100.4280
- 8V6는 MDD 5 미만을 다수 만들었으나, max_return_pct가 8V5의 41~42%대에서 3~5%대로 급감했다.
- 핵심 해석: V51 문제를 진입 희소화와 강한 전단 필터로 해결하려 하면 MDD보다 edge가 먼저 죽는다.
- 다음 단계: core_base/core_rare22_c1의 진입 밀도를 최대한 유지하면서 사후 브레이크, 손실 군집 회피, exit/hold/stop 재조정으로 MDD를 낮춰야 한다.

후속 규칙
새 전략 결과를 업로드하면 이 형식대로 항목을 추가한다.
공식 1위가 바뀌면 verdict와 notes를 즉시 갱신한다.
정상 환경 실패는 기록으로 남기되 invalid_env는 남기지 않는다.