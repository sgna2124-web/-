8V14 4AXIS 50 EACH STREAMSAFE 결과 및 장단점 Addendum

배치 정보
batch: 8V14_4AXIS_50_EACH_STREAMSAFE
result_path: local_results/8V14_4AXIS_50_EACH_STREAMSAFE/
summary_file: local_results/8V14_4AXIS_50_EACH_STREAMSAFE/master_summary.txt
registry_file: local_results/8V14_4AXIS_50_EACH_STREAMSAFE/8V14_4AXIS_50_EACH_STREAMSAFE_registry.csv
strategies: 200
axis 구성: long_main 50개, long_max 50개, short_main 50개, short_max 50개
cd_value_formula: 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)
official_promotion: max_drawdown_pct < 5.0 and official_cd_value beats incumbent
trade_cap: none

참조 기준선
long_main_v1: 6V2_L01_doubleflush_core | cd 121.7490287208 | mdd 1.7512 | max_return_pct 23.9191
long_max_v1: 8V4_V51_V002_core_rare22_c1 | cd 134.5158668232 | mdd 6.7587 | max_return_pct 44.2664
short_main_v1: short_beh_dd_brake | cd 392.214469 | mdd 4.7589 | max_return_pct 311.8122
short_max_v1: short_only_reference_1x | cd 456.137449 | mdd 7.7792 | max_return_pct 394.6145

기준선 갱신 여부
long_main_v1: 갱신 없음
long_max_v1: 갱신 없음
short_main_v1: 갱신 없음
short_max_v1: 갱신 없음

중요 판정
8V14는 단순 no_promotion이 아니라 전 축 과다거래 붕괴 라운드다.
MDD 5% 미만 후보가 네 축 모두에서 0개였다.
전체 top30의 max_return_pct가 모두 0.0이었다.
가장 높은 official_cd_value도 1.406328에 그쳤다.
따라서 8V14의 어떤 전략도 다음 부모 후보로 쓰면 안 된다.

축별 리더

1. long_main any-MDD best
strategy: 8V14_long_main_v1_040_lm_return_lift
side: long
axis: long_main
parent: 6V2_L01_doubleflush_core
group: lm_return_lift
entry: long_return_lift
trades: 106453
wins: 27992
losses: 78461
win_rate_pct: 26.2951725174
final_return_pct: -92.3434220461
max_return_pct: 0.0
max_drawdown_pct: 98.5936722081
official_cd_value: 1.4063277919
verdict: invalid_as_candidate_overtrade_collapse

해석:
- 공식 long 기준선 부모를 사용했지만, 원본 6V2의 선택적 doubleflush edge가 보존되지 않았다.
- trades가 592에서 106453으로 폭증했고, max_return_pct가 23.9191에서 0.0으로 사라졌다.
- return_lift라는 이름과 달리 실제로는 수익 확장이 아니라 광범위한 상태 라벨형 진입으로 변질됐다.

2. long_max any-MDD best
strategy: 8V14_long_max_v1_026_lx_dd_compress
side: long
axis: long_max
parent: 8V4_V51_V002_core_rare22_c1
group: lx_dd_compress
entry: long_dd_compress
trades: 290854
wins: 44965
losses: 245889
win_rate_pct: 15.4596464205
final_return_pct: -99.8342208171
max_return_pct: 0.0
max_drawdown_pct: 99.9795718039
official_cd_value: 0.0204281961
verdict: invalid_as_candidate_overtrade_collapse

해석:
- V51 raw edge를 살리는 데 실패했다.
- 원본 long_max_v1의 trades 2276 수준이 290854로 폭증했고, max_return_pct 44.2664가 0.0으로 소실됐다.
- dd_compress가 실제 손실 압축이 아니라 대량 진입 후 계좌 붕괴로 작동했다.

3. short_main any-MDD best
strategy: 8V14_short_main_v1_022_sm_edge_preserve
side: short
axis: short_main
parent: short_beh_dd_brake
group: sm_edge_preserve
entry: short_edge_preserve
trades: 369762
wins: 74155
losses: 295607
win_rate_pct: 20.0547920013
final_return_pct: -99.9677133928
max_return_pct: 0.0
max_drawdown_pct: 99.9990786381
official_cd_value: 0.0009213619
verdict: invalid_as_candidate_overtrade_collapse

해석:
- short_main 개선도 원본 edge 보존에 실패했다.
- edge_preserve 그룹이 이름과 반대로 원본 short_beh_dd_brake의 고수익/저MDD 구조를 전혀 보존하지 못했다.
- short 쪽은 특히 광범위한 역추세 진입이 누적되면 곧바로 99%대 MDD로 붕괴한다.

4. short_max any-MDD best
strategy: 8V14_short_max_v1_026_sx_dd_compress
side: short
axis: short_max
parent: short_only_reference_1x
group: sx_dd_compress
entry: short_dd_compress
trades: 334992
wins: 58566
losses: 276426
win_rate_pct: 17.4828055595
final_return_pct: -99.9261306840
max_return_pct: 0.0
max_drawdown_pct: 99.9944212178
official_cd_value: 0.0055787822
verdict: invalid_as_candidate_overtrade_collapse

해석:
- short_max_v1의 raw upside를 보존하지 못했다.
- MDD 압축을 목적으로 한 sx_dd_compress가 실제로는 진입 난사 구조가 되어 short 원본 edge를 완전히 훼손했다.

8V14 구조적 장점
1. 실행 자체는 streamsafe 구조로 결과 파일을 생성했다.
2. 600개 전체 확장 대신 4축 50개씩 200개로 줄인 방향은 런타임 절감 관점에서 맞다.
3. 축별 기준선 비교 출력 구조는 후속 실험에서도 재사용 가능하다.

8V14 구조적 단점
1. 부모 전략의 실제 entry edge를 보존하지 못했다.
2. strategy name은 parent를 가리키지만 실제 signal은 parent의 정밀 조건과 분리되어 broad entry로 작동했다.
3. 네 축 모두 trades가 10만~37만 회 이상으로 폭증했다.
4. max_return_pct가 모든 상위 전략에서 0.0으로, 수익 곡선이 시작 이후 한 번도 의미 있게 우상향하지 못했다.
5. MDD 5% 미만 후보가 0개였으므로 공식 기준선 비교 단계로 올라갈 후보 자체가 없다.
6. long/short 양쪽 모두 사후 브레이크나 DD 압축보다 먼저 entry fidelity가 무너졌다.

핵심 원인
8V14 실패의 핵심은 파라미터 수나 축 구성 문제가 아니다.
핵심은 원본 부모 신호 보존 실패다.
기존 우수 전략의 장단점을 보완하려면 parent signal을 그대로 유지한 뒤 그 위에 약한 exit, brake, cooldown, partial skip만 붙여야 한다.
그런데 8V14는 parent 이름만 참조하고 실제 entry를 새로 넓게 정의하면서 원본 edge가 사라졌다.

다음 단계 지침
1. 8V14 전략은 어떤 축에서도 다음 부모로 쓰지 않는다.
2. 4축 50개씩 줄이는 실행 방식은 유지하되, parent entry mask는 원본 코드에서 그대로 가져온다.
3. long은 다시 8V10 A/B로 돌아간다.
   - A: 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176 | MDD<5 top | max_return_pct 20.9416 | MDD 4.4791 | cd 115.524476
   - B: 8V10_B_ANYCD_I013_I302_b_trend_runner_b102 | any-MDD top | max_return_pct 26.3362 | MDD 5.6679 | cd 119.175585
4. short는 short_main_v1/short_max_v1의 실제 원본 signal fidelity를 먼저 복원한다.
5. 다음 코드 생성 시 금지사항:
   - parent 이름만 붙이고 entry를 재작성하지 말 것
   - return_lift, dd_compress, edge_preserve를 broad 상태 조건으로 만들지 말 것
   - 거래 수가 원본 대비 10배 이상 증가하는 구조를 허용하지 말 것
   - MDD 압축을 hard pre-filter로만 해결하지 말 것
6. 다음 코드 생성 시 필수사항:
   - 각 parent별 원본 entry boolean을 먼저 만들고, 그 신호를 기본값으로 둔다.
   - candidate별 변경은 exit/hold/stop/trailing/post-loss brake/symbol-DD pause/volatility shock pause 정도로 제한한다.
   - parent 대비 trades 증가율과 감소율을 출력한다.
   - top candidate에 max_return_pct, MDD, official_cd_value, trades, parent_trade_ratio를 함께 출력한다.

현재 유지되는 기준
long_main_v1 = 6V2_L01_doubleflush_core
long_max_v1 = 8V4_V51_V002_core_rare22_c1
short_main_v1 = short_beh_dd_brake
short_max_v1 = short_only_reference_1x

다음 개선 우선순위
1순위: 8V10 B b_trend_runner_b102의 MDD 5.6679를 4.9 이하로 낮추되 max_return_pct 24~26%대를 최대한 유지한다.
2순위: 8V10 A b_rescue_mix_b176의 MDD 4.4791을 유지하면서 max_return_pct를 23.9 이상으로 올린다.
3순위: parent signal fidelity 보존형 4축 50개 구조를 새로 만든다.
4순위: short는 원본 신호를 보존한 뒤 사후 리스크 제어만 약하게 붙인다.
