8V12 LONG/SHORT MAIN/MAX 400 결과 및 장단점 Addendum

배치 정보
batch: 8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP
result_path: local_results/8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/
summary_file: local_results/8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/master_summary.txt
registry_file: local_results/8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP_registry.csv
strategies: 400
failed_symbols: 0
cd_value_formula: 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)
official_promotion: max_drawdown_pct < 5.0
trade_cap: none

참조 기준선
long_main_v1: 6V2_L01_doubleflush_core | cd 121.749029 | mdd 1.7512 | max_return_pct 23.9191
long_max_v1: 8V4_V51_V002_core_rare22_c1 | cd 134.515867 | mdd 6.7587 | max_return_pct 44.2664
short_main_v1: short_beh_dd_brake | cd 392.214469 | mdd 4.7589 | max_return_pct 311.8122
short_max_v1: short_only_reference_1x | cd 456.137449 | mdd 7.7792 | max_return_pct 394.6145

기준선 갱신 여부
long_main_v1: 갱신 없음
- best candidate: long_max_v1_55_lx12_second_leg_absorption_lx12_2_14
- cand_cd: 105.703904
- ref_cd: 121.749029
- delta_cd: -16.045125
- cand_mdd: 1.2955
- cand_max_return_pct: 7.0913
- trades: 849

long_max_v1: 갱신 없음
- best candidate: long_max_v1_1_lx12_range_expansion_runner_lx12_0_00
- cand_cd: 108.517839
- ref_cd: 134.515867
- delta_cd: -25.998028
- cand_mdd: 7.5061
- cand_max_return_pct: 17.3243
- trades: 5737

short_main_v1: 갱신 없음
- best candidate: short_max_v1_25_sx12_pullback_continuation_sx12_1_04
- cand_cd: 100.022693
- ref_cd: 392.214469
- delta_cd: -292.191776
- cand_mdd: 0.0077
- cand_max_return_pct: 0.0304
- trades: 3

short_max_v1: 갱신 없음
- best candidate: short_max_v1_25_sx12_pullback_continuation_sx12_1_04
- cand_cd: 100.022693
- ref_cd: 456.137449
- delta_cd: -356.114756
- cand_mdd: 0.0077
- cand_max_return_pct: 0.0304
- trades: 3

8V12 리더
1. long_mdd5_cd_1
strategy: long_max_v1_55_lx12_second_leg_absorption_lx12_2_14
side: long
parent: 8V4_V51_V002_core_rare22_c1
family: long_max_v1_improvements
group: lx12_second_leg_absorption
trades: 849
win_rate_pct: 43.2273
final_return_pct: 5.7941
max_return_pct: 7.0913
max_drawdown_pct: 1.2955
official_cd_value: 105.703904
verdict: official_mdd_pass_but_no_promotion

해석:
- MDD 압축은 매우 강하게 됐다.
- 다만 max_return_pct가 7.0913에 그쳐 long_main_v1의 23.9191 및 8V10 A의 20.9416보다 크게 낮다.
- second_leg_absorption은 위험 압축 모듈로는 유효하지만, 단독 부모 또는 단독 진입 구조로는 edge를 너무 많이 깎는다.

2. long_any_cd_1
strategy: long_max_v1_1_lx12_range_expansion_runner_lx12_0_00
side: long
parent: 8V4_V51_V002_core_rare22_c1
family: long_max_v1_improvements
group: lx12_range_expansion_runner
trades: 5737
max_return_pct: 17.3243
max_drawdown_pct: 7.5061
official_cd_value: 108.517839
verdict: mdd_fail_and_no_raw_promotion

해석:
- 거래 밀도는 높고 max_return_pct도 8V12 내부에서는 가장 높다.
- 그러나 MDD가 7.5061로 너무 높고 official_cd_value도 long_max_v1 134.515867, 8V10 B 119.175585보다 낮다.
- range_expansion_runner는 진입 밀도 유지에는 도움이 되지만 손실 군집과 변동성 구간에서 방어가 약하다.

3. short_mdd5_cd_1 / short_any_cd_1
strategy: short_max_v1_25_sx12_pullback_continuation_sx12_1_04
side: short
parent: short_only_reference_1x
group: sx12_pullback_continuation
trades: 3
max_return_pct: 0.0304
max_drawdown_pct: 0.0077
official_cd_value: 100.022693
verdict: not_valid_candidate_due_to_too_few_trades

해석:
- 수치상 MDD는 매우 낮지만 거래 수 3회라 전략 검증 의미가 없다.
- short 쪽 8V12 개선은 원본 short edge 보존에 실패했다.
- 8V11과 마찬가지로 short 개선은 과도한 필터링으로 거래가 사라지는 문제가 반복됐다.

8V12 구조 평가
장점
1. failed_symbols 0으로 실행 안정성은 확보됐다.
2. print 기준선 비교 기능이 정상 작동했고, 각 축의 갱신 여부를 명확히 출력했다.
3. second_leg_absorption은 MDD를 1.2955까지 낮추는 강한 방어 효과를 보였다.
4. range_expansion_runner는 거래 수 5737, max_return_pct 17.3243으로 거래 밀도와 수익 잠재력을 일부 회복했다.

단점
1. long_main 기준 후보가 cd 105.703904에 머물러 8V10 A의 115.524476보다 후퇴했다.
2. long_any 후보도 cd 108.517839에 그쳐 8V10 B의 119.175585보다 낮다.
3. MDD 압축형은 수익률을 과도하게 깎고, 수익률 확장형은 MDD가 7.5까지 커지는 분리가 발생했다.
4. short 개선군은 trades 3 수준으로 다시 검증 불능 상태가 됐다.
5. 8V12 단독 리더는 다음 기준 부모로 삼기 어렵다.

중요 결론
8V12는 기준선 갱신 실패다.
8V12 리더는 8V10 A/B보다 약하다.
다음 라운드에서 8V12 top을 부모로 삼으면 안 된다.
8V12의 유효 자산은 모듈 단위다.
- lx12_second_leg_absorption: MDD 압축 보조 모듈
- lx12_range_expansion_runner: 거래 밀도/수익률 회복 보조 모듈
- lx12_asymmetric_trail: exit/hold 보조 모듈 후보

다음 단계 지침
1. long은 8V10 A와 8V10 B를 계속 중심축으로 둔다.
2. 8V12 second_leg_absorption은 8V10 B의 MDD 압축에 부분 이식한다.
3. 8V12 range_expansion_runner는 8V10 A의 max_return_pct 보강에 부분 이식한다.
4. 두 모듈을 hard filter로 쓰지 말고, 점수 보정, 부분 brake, exit/hold 재조정 형태로만 사용한다.
5. short는 8V11/8V12 방식의 강한 전단 필터를 반복하지 말고, short_main_v1/short_max_v1의 원본 신호 밀도를 보존한 채 사후 리스크 제어만 약하게 붙인다.
6. 다음 코드 생성 시 출력문은 갱신된 기준선만 상세 출력하되, 모든 축의 beat=False인 경우에는 요약으로 no baseline update를 출력하면 된다.

현재 유지되는 기준
long_main_v1 = 6V2_L01_doubleflush_core
long_max_v1 = 8V4_V51_V002_core_rare22_c1
short_main_v1 = short_beh_dd_brake
short_max_v1 = short_only_reference_1x

다음 개선 우선순위
1순위: 8V10 B b_trend_runner_b102의 MDD 5.6679를 4.9 이하로 낮추되 max_return_pct 24~26대 유지.
2순위: 8V10 A b_rescue_mix_b176의 MDD 4.4791을 유지하면서 max_return_pct를 23.9 이상으로 올리기.
3순위: 8V12 second_leg_absorption/range_expansion_runner/asymmetric_trail을 8V10 A/B에 보조 모듈로 혼합.
4순위: short는 원본 short edge 보존형으로 재설계. 저거래수 필터형은 재사용 금지.
