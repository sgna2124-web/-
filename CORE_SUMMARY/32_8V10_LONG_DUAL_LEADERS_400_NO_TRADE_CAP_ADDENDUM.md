8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP addendum

배치 목적
8V9 이후 현재 후보 A/B가 동일해진 8V9_RAWV51_I013_entry_timing_window_r013을 기반으로, 이전과 겹치지 않는 방식의 신규 개선안 400개를 시도했다.
거래 수 제한은 두지 않았다.
단순 파라미터 조정이 아니라 신규 조건 조합, edge 확장, MDD 제어, exit/hold/stop 변형을 중심으로 구성했다.

공식 cd_value 정의
cd_value = 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)
MDD 5% 미만만 공식 승격 가능하다.
MDD와 관계없는 cd_value 1위는 개선 후보 B로 기록한다.

실행 결과
batch: 8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP
strategies: 400
failed_symbols: 0
reference: 8V9_RAWV51_I013_entry_timing_window_r013 | cd_value 105.640342 | max_return_pct 10.4863 | max_drawdown_pct 4.3852 | trades 1292

8V10 배치 내 MDD 5% 미만 cd_value 1위
strategy_name: 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176
parent: 8V9_RAWV51_I013_entry_timing_window_r013
group: b_rescue_mix
verdict: official_mdd_pass
trades: 1714
win_rate_pct: 38.7981
final_return_pct: 15.7815
max_return_pct: 20.9416
max_drawdown_pct: 4.4791
cd_value: 115.524476
delta_vs_8V9_reference: +9.884134
status: 8V10_official_mdd_pass_batch_leader_but_not_global_6V2_promotion

8V10 배치 내 MDD 무관 cd_value 1위
strategy_name: 8V10_B_ANYCD_I013_I302_b_trend_runner_b102
parent: 8V9_RAWV51_I013_entry_timing_window_r013
group: b_trend_runner
verdict: mdd_fail
trades: 1263
win_rate_pct: 46.9517
final_return_pct: 20.0025
max_return_pct: 26.3362
max_drawdown_pct: 5.6679
cd_value: 119.175585
delta_vs_8V9_reference: +13.535243
status: candidate_B_any_cd_leader_mdd_fail

공식 long 기준선 6V2와의 비교
6V2_L01_doubleflush_core: cd_value 121.7490 | max_return_pct 23.9191 | max_drawdown_pct 1.7512 | trades 592
8V10 MDD<5 1위는 cd_value 115.524476으로 6V2 공식 기준선을 넘지 못했다.
8V10 MDD 무관 1위도 cd_value 119.175585로 6V2 공식 기준선 121.7490을 넘지 못했다.
따라서 공식 long 기준선 교체는 없다.

8V10 상위권 해석
8V10은 8V8, 8V9 대비 뚜렷한 개선을 만들었다.
8V8 best cd_value 105.766560, max_return_pct 9.6311, MDD 3.5251에서 8V10 MDD<5 best cd_value 115.524476, max_return_pct 20.9416, MDD 4.4791로 크게 상승했다.
8V9 best cd_value 105.640342, max_return_pct 10.4863, MDD 4.3852에서 8V10 MDD<5 best cd_value 115.524476, max_return_pct 20.9416, MDD 4.4791로 상승했다.
trade density도 8V9 best 1292에서 8V10 MDD<5 best 1714로 늘었다.
이 라운드는 거래 수 제한 제거 방향이 맞다는 것을 재확인했다.

장점
1. b_rescue_mix는 V51 raw edge를 완전히 죽이지 않고 MDD 5% 미만을 유지했다.
2. max_return_pct가 20.9416까지 복원되어 8V6~8V9의 edge 희석 문제를 상당 부분 회복했다.
3. trades 1714로 V51 core의 거래 밀도 목표인 1500 이상을 충족했다.
4. strict_gate + spring_gate + multi_low_reclaim + runner_if_strong 조합이 safe branch와 raw edge 사이의 균형을 만들었다.
5. b_trend_runner는 MDD가 5.6679로 초과했지만 max_return_pct 26.3362와 cd_value 119.175585를 기록해 다음 개선 후보로 가치가 있다.

단점
1. 8V10 MDD<5 1위는 여전히 공식 기준선 6V2의 cd_value 121.7490을 넘지 못했다.
2. b_trend_runner는 수익 확장력은 강하지만 MDD가 5.6679로 공식 승격 조건을 넘는다.
3. 8V10의 좋은 후보들이 대부분 8V9_RAWV51_I013 부모에 집중되어 있어 구조 다양성은 아직 부족하다.
4. rescue_mix의 win_rate는 38.7981로 낮다. 수익은 runner와 손익비에 의존한다.
5. deep_sweep 일부는 안정적이지만 trade 수가 낮거나 return 확장력이 부족하다.

다음 개선 후보
후보 A: MDD 5% 미만 cd_value 1위
8V10_B_ANYCD_I013_I376_b_rescue_mix_b176 | cd_value 115.524476 | max_return_pct 20.9416 | max_drawdown_pct 4.4791 | trades 1714

후보 B: MDD 무관 cd_value 1위
8V10_B_ANYCD_I013_I302_b_trend_runner_b102 | cd_value 119.175585 | max_return_pct 26.3362 | max_drawdown_pct 5.6679 | trades 1263

다음 단계 지침
1. 후보 A는 장점 극대화보다 MDD를 유지하면서 max_return_pct 23~26%대로 끌어올리는 방향을 우선한다.
2. 후보 B는 max_return_pct를 보존하면서 MDD 5.6679를 4.9 이하로 압축하는 방향을 우선한다.
3. 거래 수 제한은 두지 않는다.
4. 단순 파라미터 조정은 아직 하지 않는다.
5. b_rescue_mix와 b_trend_runner의 장점을 교차 이식한다.
6. b_fast_reentry의 일부 구조는 후보 A/B에 보조 모듈로 이식 가능하다.
7. deep_sweep은 MDD 안정화 보조로만 사용하고 단독 부모로 우선하지 않는다.
8. strict/lowanchor/spring은 hard filter가 아니라 상황별 risk brake 또는 rescue 조건으로 섞는다.
9. shocklow는 단독 코어가 아니라 과열/휩쏘 회피 보조 조건으로만 쓴다.
10. 목표는 cd_value 121.7490 초과와 MDD 5% 미만 동시 달성이다.
