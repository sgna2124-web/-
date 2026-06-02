short_main2 v3 Q4 의존도 점검

대상 전략
MIX05_A02_A03_failfast14_rr630

점검 목적
2025년 4분기 숏 유리 특이점에만 성과가 몰린 전략인지 확인한다.
FULL, Q4 제외, Q4 단독 성과를 비교해 Q4 몰빵 여부를 판정한다.

점검 결과 출처
local_results/short_main/SHORT_MAIN2_V2_MIX05_Q4_DEPENDENCY_CHECK_V1_7/q4_dependency_summary_compact.csv

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

MIX05 FULL 성과
period: FULL_TRAIN_TO_2025_END
trades: 150791
max_return_pct: 86520.8367663832
max_drawdown_pct: 5.879344393880359
official_cd_value: 81528.0994560266
profit_factor: 1.882073174356906
mtm_worstbar_cd_value: 74307.00038895881
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

MIX05 Q4 제외 성과
period: EXCL_2025_Q4_ALL_BEFORE_2025_10_01
trades: 127405
max_return_pct: 20328.339546661187
max_drawdown_pct: 5.879344393880359
official_cd_value: 19227.287110761717
profit_factor: 1.7563255890257752
mtm_worstbar_cd_value: 17525.721414295374
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

MIX05 Q4 단독 성과
period: 2025_Q4_ONLY
trades: 23294
max_return_pct: 326.65596976886883
max_drawdown_pct: 5.326636078837166
official_cd_value: 403.9295589506476
profit_factor: 1.9322977333861096
mtm_worstbar_cd_value: 397.94849241191406
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

Q4 의존도 계산
Q4 제외 CD / FULL CD = 19227.287110761717 / 81528.0994560266 = 약 23.58%
Q4 단독 CD / FULL CD = 403.9295589506476 / 81528.0994560266 = 약 0.50%

판정
MIX05는 Q4 의존 전략이 아니다.
Q4 단독 CD는 전체의 약 0.50% 수준이다.
Q4 제외 구간에서도 official_cd_value 19227.287110761717을 기록했다.
Q4 제외 구간에서도 v2 기준선 C03보다 CD, MDD, PF, MTM worstbar CD가 모두 개선되었다.
따라서 2025년 4분기 특이점 때문에만 좋아 보인 전략으로 보지 않는다.

v2 C03 Q4 제외 비교
C03 EXCL_Q4 official_cd_value: 16979.64262769056
C03 EXCL_Q4 max_drawdown_pct: 5.888592725709996
C03 EXCL_Q4 profit_factor: 1.7110313125769783
C03 EXCL_Q4 mtm_worstbar_cd_value: 15476.651550710532

MIX05 EXCL_Q4 official_cd_value: 19227.287110761717
MIX05 EXCL_Q4 max_drawdown_pct: 5.879344393880359
MIX05 EXCL_Q4 profit_factor: 1.7563255890257752
MIX05 EXCL_Q4 mtm_worstbar_cd_value: 17525.721414295374

delta_excl_q4_cd_vs_v2: +2247.644483071159
delta_excl_q4_mdd_vs_v2: -0.009248331829637024
delta_excl_q4_pf_vs_v2: +0.04529427644879691
delta_excl_q4_mtm_worstbar_cd_vs_v2: +2049.069863584842

주의
Q4 단독 성과는 전체 성과의 핵심 근거가 아니다.
핵심 근거는 Q4 제외 구간에서도 v2 기준선을 이겼다는 점이다.
