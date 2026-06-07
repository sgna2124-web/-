short_main2 v5 공식 기준선

현재 공식 기준선
V4R05_stop262_rr620_t390_ff15

갱신 판정
short_main2/v5 기준선으로 갱신한다.
이후 short_main2 개선은 이 v5 기준선에서 시작한다.

이전 기준선
base_line/short_main2/v4
V3MIX07_N02_stop255_rr630_t375

핵심 요약
short_main2/v5는 short_main2/v4의 진입 조건을 그대로 유지한다.
변경점은 청산, 보유, 방어 파라미터다.
V4R05는 v4 기준선 V3MIX07보다 official_cd_value, profit_factor, mtm_worstbar_cd_value가 크게 개선되었다.
2025 Q4 제외 구간에서도 v4 기준선보다 우위다.
2026 Q1 validation에서도 v4 기준선보다 official_cd_value, max_drawdown_pct, profit_factor, mtm_worstbar_cd_value, mtm_worstbar_max_drawdown_pct가 모두 개선되었다.

공식 결과, 2025 train, no slippage
trades: 148281
max_return_pct: 129234.32408204528
max_drawdown_pct: 5.692488096031778
official_cd_value: 121971.9830795917
profit_factor: 1.998821411024562
mtm_worstbar_cd_value: 111166.12280897668
mtm_worstbar_max_drawdown_pct: 14.059033930133126

v4 대비, 2025 train
v4 official_cd_value: 106973.54619066067
v5 official_cd_value: 121971.9830795917
delta_cd_vs_v4: +14998.436888931028

v4 max_drawdown_pct: 5.540389442518634
v5 max_drawdown_pct: 5.692488096031778
delta_mdd_vs_v4: +0.15209865351314367

v4 profit_factor: 1.9543969406097241
v5 profit_factor: 1.998821411024562
delta_pf_vs_v4: +0.04442447041443777

v4 mtm_worstbar_cd_value: 97353.0658974033
v5 mtm_worstbar_cd_value: 111166.12280897668
delta_mtm_worstbar_cd_vs_v4: +13813.056911573382

2025 Q4 제외 검증
v5 EXCL_Q4 official_cd_value: 26794.776804338213
v4 EXCL_Q4 official_cd_value: 23933.648521901203
delta_excl_q4_cd_vs_v4: +2861.12828243701

v5 EXCL_Q4 max_drawdown_pct: 5.429499124497861
v4 EXCL_Q4 max_drawdown_pct: 5.398813559725191
delta_excl_q4_mdd_vs_v4: +0.030685564772669593

2026 Q1 validation
v5 2026_Q1 official_cd_value: 109.22776166037053
v4 2026_Q1 official_cd_value: 108.34692571427838
delta_2026_q1_cd_vs_v4: +0.880835946092148

v5 2026_Q1 max_drawdown_pct: 2.066572846244019
v4 2026_Q1 max_drawdown_pct: 2.185877830413352
delta_2026_q1_mdd_vs_v4: -0.11930498416933277

주요 파일
STRATEGY.md: 전략 조건, 성과, 장단점
REPRODUCE.md: 재현 방법과 공식 기대값
Q4_DEPENDENCY_CHECK.md: Q4 의존도 및 Q4 제외 성과
VALIDATION_2026.md: 2026 Q1 validation 결과
RESULT_SUMMARY.csv: 공식 결과 요약
CHANGELOG.md: v5 승격 흐름

결과 출처
local_results/short_main/SHORT_MAIN2_V4R05_SINGLE_RETEST_Q4_V1_2_1_MEMFIX/v4r05_single_q4_summary_compact.csv
local_results/short_main/SHORT_MAIN2_V4R05_2026_QUARTER_VALIDATION_V1_1_SKIP_EMPTY/v4r05_2026_quarter_summary_compact.csv

실행 원칙
전체 거래 기록 파일은 기본 저장하지 않는다.
summary 중심의 결과만 남긴다.
--save-trades 옵션은 기준선 기록용 실행에서 사용하지 않는다.

판정
V4R05_stop262_rr620_t390_ff15를 short_main2/v5 공식 기준선으로 확정한다.
