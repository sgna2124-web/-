short_main2 v4 공식 기준선

현재 공식 기준선
V3MIX07_N02_stop255_rr630_t375

갱신 판정
short_main2/v4 기준선으로 갱신한다.
이후 short_main2 개선은 이 v4 기준선에서 시작한다.

이전 기준선
base_line/short_main2/v3
MIX05_A02_A03_failfast14_rr630

핵심 요약
short_main2/v4는 short_main2/v3의 진입 조건을 그대로 유지한다.
변경점은 청산, 보유, 방어 파라미터다.
V3MIX07은 v3 기준선 MIX05보다 official_cd_value, max_drawdown_pct, profit_factor, mtm_worstbar_cd_value, mtm_worstbar_max_drawdown_pct가 모두 개선되었다.
Q4 제외 구간에서도 v3 기준선보다 우위다.

공식 결과, 2025 train, no slippage
trades: 149151
max_return_pct: 113147.92211118022
max_drawdown_pct: 5.540389442518634
official_cd_value: 106973.54619066067
profit_factor: 1.9543969406097241
mtm_worstbar_cd_value: 97353.0658974033
mtm_worstbar_max_drawdown_pct: 14.046920216852365

v3 대비 개선
v3 official_cd_value: 81528.0994560266
v4 official_cd_value: 106973.54619066067
delta_cd_vs_v3: +25445.446734634068

v3 max_drawdown_pct: 5.879344393880359
v4 max_drawdown_pct: 5.540389442518634
delta_mdd_vs_v3: -0.3389549513617247

v3 profit_factor: 1.882073174356906
v4 profit_factor: 1.9543969406097241
delta_pf_vs_v3: +0.07232376625281822

v3 mtm_worstbar_cd_value: 74307.00038895881
v4 mtm_worstbar_cd_value: 97353.0658974033
delta_mtm_worstbar_cd_vs_v3: +23046.065508444488

주요 파일
STRATEGY.md: 전략 조건, 성과, 장단점
REPRODUCE.md: 재현 방법과 공식 기대값
Q4_DEPENDENCY_CHECK.md: Q4 의존도 및 Q4 제외 성과
RESULT_SUMMARY.csv: 공식 결과 요약
CHANGELOG.md: v4 승격 흐름

결과 출처
local_results/short_main/SHORT_MAIN2_V3MIX07_SINGLE_RETEST_Q4_V1_3/v3mix07_single_q4_summary_compact.csv

실행 원칙
전체 거래 기록 파일은 기본 저장하지 않는다.
summary 중심의 결과만 남긴다.
--save-trades 옵션은 기준선 기록용 실행에서 사용하지 않는다.

판정
V3MIX07_N02_stop255_rr630_t375를 short_main2/v4 공식 기준선으로 확정한다.
