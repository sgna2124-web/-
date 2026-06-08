short_main2 현재 기준선 포인터

현재 기준선
base_line/short_main2/v5

전략명
V4R05_stop262_rr620_t390_ff15

이전 기준선
base_line/short_main2/v4
V3MIX07_N02_stop255_rr630_t375

공식 성과, 2025 train, no slippage
trades: 148281
max_return_pct: 129234.32408204528
max_drawdown_pct: 5.692488096031778
official_cd_value: 121971.9830795917
profit_factor: 1.998821411024562
mtm_worstbar_cd_value: 111166.12280897668
mtm_worstbar_max_drawdown_pct: 14.059033930133126

2025 Q4 제외 검증
EXCL_Q4 official_cd_value: 26794.776804338213
EXCL_Q4 max_drawdown_pct: 5.429499124497861
EXCL_Q4 profit_factor: 1.8627143547071625
EXCL_Q4 mtm_worstbar_cd_value: 24354.33885487651

2026 validation, 현재 데이터 기준 Q1
2026_Q1 official_cd_value: 109.22776166037053
2026_Q1 max_drawdown_pct: 2.066572846244019
2026_Q1 profit_factor: 1.977895137634963
2026_Q1 mtm_worstbar_cd_value: 109.83100615462072

갱신 근거
단독 리테스트 재현 성공.
Q4 의존도 점검 통과.
Q4 제외 구간에서도 v4 기준선보다 우위.
2026 Q1 validation에서도 v4 기준선보다 우위.
수수료 0.04%, 자산 1%, 레버리지 1, 포지션 수 제한 없음.
2026 데이터는 기준선 갱신용 train에는 사용하지 않고 validation으로만 기록함.
전체 거래 로그를 기본 저장하지 않음.

상세 문서
base_line/short_main2/v5/README.md
base_line/short_main2/v5/STRATEGY.md
base_line/short_main2/v5/REPRODUCE.md
base_line/short_main2/v5/Q4_DEPENDENCY_CHECK.md
base_line/short_main2/v5/VALIDATION_2026.md
base_line/short_main2/v5/RESULT_SUMMARY.csv
base_line/short_main2/v5/CHANGELOG.md

판정
이후 short_main2 개선은 v5 기준선에서 시작한다.
