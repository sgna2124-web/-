short_main2 v3 공식 기준선

현재 공식 기준선
MIX05_A02_A03_failfast14_rr630

갱신 판정
short_main2/v3 기준선으로 갱신한다.
이후 short_main2 개선은 이 v3 기준선에서 시작한다.

핵심 요약
short_main2/v3는 short_main2/v2의 진입 조건을 그대로 유지한다.
변경점은 청산, 보유, 방어 파라미터다.
MIX05는 v2 C03보다 official_cd_value와 profit_factor가 높고 realized MDD가 낮다.
Q4 제외 구간에서도 v2 C03보다 우위다.

공식 결과
trades: 150791
max_return_pct: 86520.8367663832
max_drawdown_pct: 5.879344393880359
official_cd_value: 81528.0994560266
profit_factor: 1.882073174356906
mtm_worstbar_cd_value: 74307.00038895881

v2 대비 개선
v2 official_cd_value: 69498.03075622236
v3 official_cd_value: 81528.0994560266
delta_cd_vs_v2: +12030.068699804237

v2 max_drawdown_pct: 5.888592725709996
v3 max_drawdown_pct: 5.879344393880359
delta_mdd_vs_v2: -0.009248331829637024

v2 profit_factor: 1.8286053579584032
v3 profit_factor: 1.882073174356906
delta_pf_vs_v2: +0.05346781639850273

주요 파일
STRATEGY.md: 전략 조건, 성과, 장단점
REPRODUCE.md: 재현 방법과 공식 기대값
Q4_DEPENDENCY_CHECK.md: Q4 의존도 및 Q4 제외 성과
RESULT_SUMMARY.csv: 공식 결과 요약

실행 원칙
전체 거래 기록 파일은 기본 저장하지 않는다.
summary 중심의 결과만 남긴다.
--save-trades 옵션은 기준선 기록용 실행에서 사용하지 않는다.
