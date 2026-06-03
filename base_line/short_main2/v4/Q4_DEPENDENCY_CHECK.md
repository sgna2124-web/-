short_main2 v4 Q4 의존도 점검

대상 전략
V3MIX07_N02_stop255_rr630_t375

점검 목적
2025년 4분기 숏 유리 특이점에만 성과가 몰린 전략인지 확인한다.
FULL, Q4 제외, Q4 단독 성과를 비교해 Q4 몰빵 여부를 판정한다.

점검 결과 출처
local_results/short_main/SHORT_MAIN2_V3MIX07_SINGLE_RETEST_Q4_V1_3/v3mix07_single_q4_summary_compact.csv

실행 조건
initial_asset: 100.0
position_fraction: 0.01
leverage: 1.0
fee_per_side: 0.0004
round_trip_fee: 0.0008
slippage_per_side: 0.0
position_limit: 없음
completed_scenario_count: 6
load_errors: 0

V3MIX07 FULL 성과
period: FULL_TRAIN_TO_2025_END
trades: 149151
max_return_pct: 113147.92211118022
max_drawdown_pct: 5.540389442518634
official_cd_value: 106973.54619066067
profit_factor: 1.9543969406097241
mtm_worstbar_cd_value: 97353.0658974033
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

V3MIX07 Q4 제외 성과
period: EXCL_2025_Q4_ALL_BEFORE_2025_10_01
trades: 126062
max_return_pct: 25199.522577353076
max_drawdown_pct: 5.398813559725191
official_cd_value: 23933.648521901203
profit_factor: 1.8163499010894757
mtm_worstbar_cd_value: 21751.602897414876
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

V3MIX07 Q4 단독 성과
period: 2025_Q4_ONLY
trades: 23003
max_return_pct: 350.6343895138026
max_drawdown_pct: 5.540389442518778
official_cd_value: 425.66748937282097
profit_factor: 2.005921088772498
mtm_worstbar_cd_value: 418.0776166361803
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

Q4 의존도 계산
Q4 제외 CD / FULL CD = 23933.648521901203 / 106973.54619066067 = 약 22.37%
Q4 단독 CD / FULL CD = 425.66748937282097 / 106973.54619066067 = 약 0.40%

판정
V3MIX07은 Q4 의존 전략이 아니다.
Q4 단독 CD는 전체의 약 0.40% 수준이다.
Q4 제외 구간에서도 official_cd_value 23933.648521901203을 기록했다.
Q4 제외 구간에서도 v3 기준선 MIX05보다 CD, MDD, PF, MTM worstbar CD, MTM worstbar MDD가 모두 개선되었다.
따라서 2025년 4분기 특이점 때문에만 좋아 보인 전략으로 보지 않는다.

v3 MIX05 Q4 제외 비교
MIX05 EXCL_Q4 official_cd_value: 19227.287110761717
MIX05 EXCL_Q4 max_drawdown_pct: 5.879344393880359
MIX05 EXCL_Q4 profit_factor: 1.7563255890257752
MIX05 EXCL_Q4 mtm_worstbar_cd_value: 17525.721414295374
MIX05 EXCL_Q4 mtm_worstbar_max_drawdown_pct: 14.233064755345204

V3MIX07 EXCL_Q4 official_cd_value: 23933.648521901203
V3MIX07 EXCL_Q4 max_drawdown_pct: 5.398813559725191
V3MIX07 EXCL_Q4 profit_factor: 1.8163499010894757
V3MIX07 EXCL_Q4 mtm_worstbar_cd_value: 21751.602897414876
V3MIX07 EXCL_Q4 mtm_worstbar_max_drawdown_pct: 14.046920216852365

delta_excl_q4_cd_vs_v3: +4706.361411139485
delta_excl_q4_mdd_vs_v3: -0.48053083415516795
delta_excl_q4_pf_vs_v3: +0.06002431206370051
delta_excl_q4_mtm_worstbar_cd_vs_v3: +4225.881483119501
delta_excl_q4_mtm_worstbar_mdd_vs_v3: -0.1861445384928384

주의
Q4 단독 성과는 전체 성과의 핵심 근거가 아니다.
핵심 근거는 Q4 제외 구간에서도 v3 기준선을 이겼다는 점이다.
