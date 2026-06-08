short_main2 v5 Q4 의존도 점검

대상 전략
V4R05_stop262_rr620_t390_ff15

점검 목적
2025년 4분기 숏 유리 특이점에만 성과가 몰린 전략인지 확인한다.
FULL, Q4 제외, Q4 단독 성과를 비교해 Q4 몰빵 여부를 판정한다.

점검 결과 출처
local_results/short_main/SHORT_MAIN2_V4R05_SINGLE_RETEST_Q4_V1_2_1_MEMFIX/v4r05_single_q4_summary_compact.csv

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

V4R05 FULL 성과
period: FULL_TRAIN_TO_2025_END
trades: 148281
max_return_pct: 129234.32408204528
max_drawdown_pct: 5.692488096031778
official_cd_value: 121971.9830795917
profit_factor: 1.998821411024562
mtm_worstbar_cd_value: 111166.12280897668
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

V4R05 Q4 제외 성과
period: EXCL_2025_Q4_ALL_BEFORE_2025_10_01
trades: 125332
max_return_pct: 28233.123496524935
max_drawdown_pct: 5.429499124497861
official_cd_value: 26794.776804338213
profit_factor: 1.8627143547071625
mtm_worstbar_cd_value: 24354.33885487651
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

V4R05 Q4 단독 성과
period: 2025_Q4_ONLY
trades: 22865
max_return_pct: 360.44819803668065
max_drawdown_pct: 5.692488096029469
official_cd_value: 434.2372391750604
profit_factor: 2.048426717905147
mtm_worstbar_cd_value: 426.697273874005
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

Q4 의존도 계산
Q4 제외 CD / FULL CD = 26794.776804338213 / 121971.9830795917 = 약 21.97%
Q4 단독 CD / FULL CD = 434.2372391750604 / 121971.9830795917 = 약 0.36%

판정
V4R05는 Q4 의존 전략이 아니다.
Q4 단독 CD는 전체의 약 0.36% 수준이다.
Q4 제외 구간에서도 official_cd_value 26794.776804338213을 기록했다.
Q4 제외 구간에서도 v4 기준선 V3MIX07보다 CD, PF, MTM worstbar CD가 개선되었다.
MDD는 v4보다 소폭 증가했으나 Q4 제외 구간에서는 +0.030685564772669593%p 수준으로 작다.
따라서 2025년 4분기 특이점 때문에만 좋아 보인 전략으로 보지 않는다.

v4 V3MIX07 Q4 제외 비교
V3MIX07 EXCL_Q4 official_cd_value: 23933.648521901203
V3MIX07 EXCL_Q4 max_drawdown_pct: 5.398813559725191
V3MIX07 EXCL_Q4 profit_factor: 1.8163499010894757
V3MIX07 EXCL_Q4 mtm_worstbar_cd_value: 21751.602897414876
V3MIX07 EXCL_Q4 mtm_worstbar_max_drawdown_pct: 14.046920216852365

V4R05 EXCL_Q4 official_cd_value: 26794.776804338213
V4R05 EXCL_Q4 max_drawdown_pct: 5.429499124497861
V4R05 EXCL_Q4 profit_factor: 1.8627143547071625
V4R05 EXCL_Q4 mtm_worstbar_cd_value: 24354.33885487651
V4R05 EXCL_Q4 mtm_worstbar_max_drawdown_pct: 14.059033930133126

delta_excl_q4_cd_vs_v4: +2861.12828243701
delta_excl_q4_mdd_vs_v4: +0.030685564772669593
delta_excl_q4_pf_vs_v4: +0.04636445361768682
delta_excl_q4_mtm_worstbar_cd_vs_v4: +2602.735957461635
delta_excl_q4_mtm_worstbar_mdd_vs_v4: +0.012113713280760052

주의
Q4 단독 성과는 전체 성과의 핵심 근거가 아니다.
핵심 근거는 Q4 제외 구간에서도 v4 기준선을 이겼다는 점이다.
