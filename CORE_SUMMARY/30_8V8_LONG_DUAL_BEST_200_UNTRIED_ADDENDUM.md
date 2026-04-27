8V8 LONG DUAL BEST 200 UNTRIED addendum

batch_name: 8V8_LONG_DUAL_BEST_200_UNTRIED
side: long_only
strategy_count: 200
failed_symbols: 0
result_summary: local_results/8V8_LONG_DUAL_BEST_200_UNTRIED/master_summary.txt
registry_file: local_results/8V8_LONG_DUAL_BEST_200_UNTRIED/8V8_LONG_DUAL_BEST_200_UNTRIED_registry.csv

공식 cd_value 정의
cd_value = 100 * (1 - (abs(max_drawdown_pct) / 100)) * (1 + (max_return_pct / 100))
max_return_pct / max_drawdown_pct는 old_ratio_cd로만 보며 공식 cd_value가 아니다.

1. 결론
8V8은 no_promotion이다.
MDD 5% 미만 중 cd_value 1위와 MDD 관계없는 전체 cd_value 1위는 동일하다.
공식 long 기준선 6V2_L01_doubleflush_core의 official_cd_value 121.7490을 넘지 못했다.

baseline_candidate_under_mdd5:
8V8_RAWV51_I080_raw_official_conversion_r080
parent: 8V4_V51_V002_core_rare22_c1
group: raw_official_conversion
trades: 1027
win_rate_pct: 52.6777
final_return_pct: 6.0489
max_return_pct: 9.6311
max_drawdown_pct: 3.5251
official_cd_value: 105.766560
old_ratio_cd: 2.7322
verdict: official_mdd_pass_but_no_promotion

raw_cd_candidate_any_mdd:
same_as_baseline_candidate_under_mdd5

candidate_cd_win_mdd_fail:
none

2. TOP 확인
1위: 8V8_RAWV51_I080_raw_official_conversion_r080 | trades 1027 | max_return_pct 9.6311 | max_drawdown_pct 3.5251 | official_cd_value 105.766560
2위: 8V8_RAWV51_I090_raw_official_conversion_r090 | trades 584 | max_return_pct 7.7293 | max_drawdown_pct 2.5052 | official_cd_value 105.030527
3위: 8V8_SAFE6V2_I040_safe_dd_brake_s040 | trades 1110 | max_return_pct 6.4903 | max_drawdown_pct 2.3197 | official_cd_value 104.020008
4위: 8V8_RAWV51_I100_raw_official_conversion_r100 | trades 675 | max_return_pct 6.5341 | max_drawdown_pct 2.7078 | official_cd_value 103.649405
5위: 8V8_RAWV51_I004_raw_cluster_cover_r004 | trades 1324 | max_return_pct 7.1702 | max_drawdown_pct 3.3138 | official_cd_value 103.618780

3. 장점
raw_official_conversion 계열은 V51 raw 후보의 MDD를 5% 아래로 낮추는 데 성공했다.
8V8_RAWV51_I080은 1027 trades를 유지하면서 MDD 3.5251로 공식 MDD 조건을 통과했다.
이는 8V6/8V7처럼 trades를 93~652 수준까지 죽인 방식보다 구조적으로 낫다.
즉 V51 raw 구조를 공식 통과 형태로 변환하는 방향 자체는 가능성이 있다.

safe_dd_brake 계열은 공식 기준선인 6V2_L01_doubleflush_core를 더 방어적으로 만드는 데 성공했다.
8V8_SAFE6V2_I040은 1110 trades, MDD 2.3197, official_cd_value 104.020008을 기록했다.
다만 기준선보다 낮으므로 승격 후보가 아니라 defensive module 후보로만 본다.

raw_cluster_cover와 raw_safe_graft는 일부 trade density를 유지하면서 MDD를 5% 아래로 낮추는 데 성공했다.
하지만 max_return_pct가 크게 훼손되어 단독 부모로는 약하다.

4. 단점
가장 큰 단점은 edge 손실이다.
8V4/8V5의 V51 raw top은 max_return_pct 41~44%대, MDD 6.28~6.75대였지만, 8V8 top은 max_return_pct 9.6311까지 낮아졌다.
MDD 압축은 성공했지만 수익 잠재력 보존에는 실패했다.

8V8 top official_cd_value 105.766560은 8V5 strict_rare22_c1의 116.4858보다도 낮고, 공식 기준선 121.7490과는 큰 격차가 있다.
따라서 8V8 top을 다음 라운드의 직접 부모로 삼으면 개선 폭이 제한될 가능성이 높다.

safe6V2 개선군은 공식 기준선 자체를 변형했지만, 기준선의 장점인 max_return_pct 23.9191을 보존하지 못했다.
즉 6V2를 방어적으로 더 깎는 접근은 현재 공식 기준선을 넘기 어렵다.

5. 다음 전략 생성 규칙에 반영할 점
8V8 top을 그대로 부모로 삼지 않는다.
8V8_RAWV51_I080의 raw_official_conversion 로직은 부분 모듈로만 재사용한다.
목표는 V51 raw core의 trades를 최소 1500 이상, 가능하면 2000 내외로 유지하면서 MDD를 4.9 이하로 낮추는 것이다.
max_return_pct가 10% 아래로 떨어지는 구조는 공식 기준선 초과 가능성이 낮으므로 버린다.

다음 개선은 다음 중 하나로 가야 한다.
1) 8V5_V51P_V002_core_rare22_c1 또는 8V5_V51P_V001_core_base에 8V8 raw_official_conversion의 일부 조건만 약하게 이식한다.
2) strict/lowanchor safe branch를 다시 살리되, 8V8처럼 수익을 깎는 hard conversion이 아니라 exit/hold/stop 재배열로 보완한다.
3) MDD 압축은 전단 entry filter보다 손실 군집 회피, 최근 손실 후 일시 브레이크, 변동성 폭발 후 exit 조정, partial hold 축소를 우선한다.
4) 6V2 official baseline 변형은 당분간 보조 실험으로 낮추고, V51 심화를 계속 우선한다.

6. 상태 업데이트
현재 공식 long 기준선은 변동 없음.
strategy_name: 6V2_L01_doubleflush_core
official_cd_value: 121.7490
max_return_pct: 23.9191
max_drawdown_pct: 1.7512

현재 최우선 코어도 변동 없음.
V51 core_base / core_rare22_c1의 edge 보존형 MDD 압축이 최우선이다.
strict / lowanchor는 safe branch 핵심 축이다.
새로운 family 탐색보다 V51 심화가 우선이다.
