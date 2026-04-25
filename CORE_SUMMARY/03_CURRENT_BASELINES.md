현재 공식 기준선

이 문서는 새 대화창의 어시스턴트가 현재 공식 long 1위와 short 1위를 즉시 파악하기 위한 기준선 문서다.
비교는 long-only와 short-only를 분리하여 수행한다.

현재 프로젝트의 공식 판단 기준
공식 판단 기준은 MDD와 cd_value다.
현재 프로젝트에서 cd_value의 공식 정의는 다음과 같다.
cd_value = max_return_pct / max_drawdown_pct
final_return_pct는 참고 지표다.

중요한 주의사항
현재 기준선 교체 판단은 동일한 프로젝트 규칙을 따른 결과끼리 비교한다.
즉 신규 전략은 MDD 5% 미만을 먼저 통과해야 하며, 그 다음 cd_value(max_return_pct 기반)를 본다.
거래 수가 0이거나 극단적으로 적은 전략은 cd_value 숫자가 높아 보여도 공식 기준선으로 승격하지 않는다.

1. 현재 공식 long-only 기준선
strategy_name: 6V2_L01_doubleflush_core
family: long_only_doubleflush_cap_reclaim
version_reference: 6V2_LONG10_REVIEWED
code_path: unknown_local_backtest_file_not_in_repo
config_path: unknown_local_backtest_file_not_in_repo
combinations_path: unknown_local_backtest_file_not_in_repo
result_path: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/
summary_file: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/summary.json
final_return_pct: 23.6961
max_return_pct: 23.9191
max_drawdown_pct: 1.7512
current_cd_value: 121.5300
pf: unknown_not_recorded
win_rate_pct: 58.1081
trades: 592
processed_symbols: 597
source_of_truth: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/summary.json
status: official_long_reference
note: 6V2_LONG10_REVIEWED에서 첫 공식 long 승격이 발생했다. 기존 legacy long reference 108.8106을 넘는 cd_value 121.5300을 기록했고, MDD도 1.7512로 규칙을 충족했다. 현재 long 설계의 코어는 broad continuation이 아니라 selective double flush + cap reclaim 계열이다.

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

3. 직전 long 기준선 보관
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
current_cd_value: archived_after_6V2_promotion
pf: 1.3033
win_rate_pct: 54.9859
max_conc: 50
source_of_truth: state/global_top_reference_under_mdd5_cd.json
status: archived_previous_long_reference
note: 6V2_L01_doubleflush_core 승격 전까지 사용하던 long 공식 기준선. 이후 비교용 역사 참조로만 남긴다.

4. mixed historical reference
strategy_name: official_top200_reference
result_path: summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md
legacy_final_return_pct: 1120.69995
legacy_mdd_pct: -36.03441
legacy_cd_value: 780.8279
status: archive_reference_only
note: mixed historical reference only. long-only / short-only 공식 비교선으로 사용하지 않음.

5. 최근 상태 메모
6V2_LONG10_REVIEWED에서 long 쪽 두 개의 baseline_win 후보가 나왔다.
- 1위: 6V2_L01_doubleflush_core | final_return_pct 23.6961 | max_return_pct 23.9191 | max_drawdown_pct 1.7512 | cd_value 121.5300 | trades 592
- 2위: 6V2_L04_doubleflush_extremeclose | final_return_pct 19.2086 | max_return_pct 19.4782 | max_drawdown_pct 1.0102 | cd_value 118.0043 | trades 442
6V3_LONG10_REVIEWED에서는 기준선 교체가 없었다.
- 배치 최고: 6V3_L04_core_redtogreen | final_return_pct 0.2983 | max_return_pct 0.3507 | max_drawdown_pct 0.0542 | cd_value 100.2439 | trades 9
- 차점: 6V3_L08_extreme_inside_pop | final_return_pct 0.0975 | max_return_pct 0.0975 | max_drawdown_pct 0.0591 | cd_value 100.0384 | trades 8
6V4_LONG10_REVIEWED에서도 기준선 교체가 없었다.
- 형식상 배치 최고: 6V4_L01_core_volcool_state | final_return_pct 0.0000 | max_return_pct 0.0000 | max_drawdown_pct 0.0000 | cd_value 100.0000 | trades 0
- 실질 생존 후보: 6V4_L06_extreme_regime_score | final_return_pct -0.1578 | max_return_pct 0.1927 | max_drawdown_pct 0.3498 | cd_value 99.4930 | trades 44
- 과선택화: L01, L02, L04는 0트레이드, L05는 1트레이드였다.
- 과다거래 붕괴: L07, L08, L09, L10은 cooldown과 rarity guard 부족으로 trades가 각각 1701, 875873, 1644460, 334127까지 폭증하며 대형 MDD 실패가 발생했다.
6V5_LONG10_REVIEWED에서도 기준선 교체가 없었다.
- 배치 최고: 6V5_L05_core_score_shockfresh | final_return_pct 3.9127 | max_return_pct 4.3842 | max_drawdown_pct 1.0476 | cd_value 102.8241 | trades 337
- 차점: 6V5_L10_extreme_score_shockfresh | final_return_pct 2.5475 | max_return_pct 3.0029 | max_drawdown_pct 0.7294 | cd_value 101.7995 | trades 254
- 3위: 6V5_L06_extreme_score_balance | final_return_pct 2.4189 | max_return_pct 2.8736 | max_drawdown_pct 0.6719 | cd_value 101.7307 | trades 254
- quiet 계열 L02, L07은 다시 0트레이드였다.
- 반대로 6V4에서 문제였던 과다거래는 사라졌고, 대부분 전략이 61~337 trades / 1.05% 이하 MDD 범위로 안정화됐다.
- 그러나 수익 엣지가 크게 희석되어 6V2 기준선과는 큰 격차를 보였다. 즉 soft score + spacing은 안정화에는 성공했지만 승격용 초과 성과는 만들지 못했다.
7V1_LONG10_REVIEWED에서도 기준선 교체가 없었다.
- raw upside 최고: 7V1_L10_shock_reversal_balance | final_return_pct 51.0204 | max_return_pct 56.5963 | max_drawdown_pct 15.1033 | cd_value 128.2113 | trades 33481
- 실질 상위 raw reversal: 7V1_L04_engulf_panic_retake | final_return_pct 34.2567 | max_return_pct 36.4517 | max_drawdown_pct 7.9660 | cd_value 123.5618 | trades 5071
- low-MDD 최고: 7V1_L06_deep_ema20_retake | final_return_pct 0.9083 | max_return_pct 0.9889 | max_drawdown_pct 0.6282 | cd_value 100.2744 | trades 332
- broad same-bar reversal 계열인 L10, L04, L09, L07, L01, L02는 raw edge는 확인됐지만 모두 MDD 5% 초과로 실패했다.
- 반대로 L03, L05, L06, L08은 MDD는 1.9005 이하였지만 수익 엣지가 너무 약했다.
- 즉 신규 reversal family 자체는 살아 있었지만, 현재 형태로는 “고수익-고MDD”와 “저위험-저수익” 사이의 간극을 메우지 못했다.
즉 L01이 공식 long 1위로 유지되고, L04는 같은 코어의 품질 강화형 후보로 계속 보관한다.
숏 공식 기준선도 변동 없다.

6. 승격 규칙
신규 long 전략은 1번 기준선과 비교한다.
신규 short 전략은 2번 기준선과 비교한다.
새 전략 결과에는 최소한 final_return_pct, max_return_pct, max_drawdown_pct, cd_value, result_path가 포함되어야 한다.
현재 공식 1위를 교체하려면 challenger와 incumbent가 동일 계산 규칙으로 비교 가능해야 한다.
