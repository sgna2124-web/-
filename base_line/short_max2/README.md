short_max2 기준선 인덱스

현재 기준선 구조
- v2: smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1
- v3_highperf_N02: SMX2V2_C08_EX20_02_N02_stop257_rr5075

현재 공식 Q4-low 기준선
- v2: smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1
- 위치: base_line/short_max2/v2
- 용도: Q4 저비중 정책 기준선

현재 high-performance 기준선
- v3_highperf_N02: SMX2V2_C08_EX20_02_N02_stop257_rr5075
- 위치: base_line/short_max2/v3_highperf_N02
- 용도: 2023~2025 전 구간 플러스, 2025 성과 폭발형 branch
- 주의: 기존 v2를 덮어쓴 것이 아니라 별도 high-performance branch다.

이전 기준선
- v1: smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1

선정 원칙
short_max2는 기존 short_max의 단순 전체 수익률 극대화가 아니라, Q4 특수 구간 비중, 일반 구간 성과, MDD, 실전 재현성을 함께 본다. v2는 Q4 저비중 정책 기준선으로 보존하고, v3_highperf_N02는 별도 고성과 branch로 기록한다.

v2 핵심
- short_dev: 0.032
- short_wick_mult: 1.30
- score_min_short: 2.35
- atr_stop_mult: 2.50
- rr_mult: 5.00
- timeout_bars: 320
- dd_brake_trigger_pct: 0.035
- dd_brake_freeze_steps: 4

v2 공식 full train 결과
- trades: 65180
- max_return_pct: 15588.585271121465
- max_drawdown_pct: 2.274010039088681
- official_cd_value: 15331.825267065175
- profit_factor: 2.6142284817799504

v3_highperf_N02 핵심
- short_dev: 0.032
- short_wick_mult: 1.30
- score_min_short: 2.35
- atr_stop_mult: 2.57
- rr_mult: 5.075
- timeout_bars: 320
- dd_brake_trigger_pct: 0.035
- dd_brake_freeze_steps: 4

v3_highperf_N02 2025 gate 결과
- PRE-Q4 trades: 88892
- PRE-Q4 official_cd_value: 5412.231712470644
- FULL 2025 trades: 104753
- FULL 2025 official_cd_value: 18454.91075229149
- FULL 2025 max_drawdown_pct: 5.655961392725716
- FULL 2025 profit_factor: 2.0040638913290496

v3_highperf_N02 all-through-2026 결과
- trades: 106337
- final_return_pct: 20964.787242703645
- max_drawdown_pct: 5.655961392725716
- official_cd_value: 19873.371008796516
- profit_factor: 2.0010696725618833

v3_highperf_N02 연도별 성격
- 2023: 플러스, CD 155.1021534263226
- 2024: 플러스, CD 230.31636637103094
- 2025: 강한 확장, CD 1537.5543844098192
- 2026: 저활동 플러스, CD 106.63924313928375

핵심 문서
- v2/README.md: Q4-low 기준선 개요
- v2/STRATEGY.md: v2 진입/청산 조건
- v2/REPRODUCE.md: v2 재현 방법
- v3_highperf_N02/README.md: highperf N02 기준선 개요
- v3_highperf_N02/STRATEGY.md: highperf N02 진입/청산 조건
- v3_highperf_N02/REPRODUCE.md: highperf N02 재현 방법과 gate 값
- v3_highperf_N02/strategy_spec.py: highperf N02 파라미터와 gate 값
- v3_highperf_N02/result_summary.csv: 핵심 결과 요약
- v3_highperf_N02/period_summary.csv: 2023~2026 기간별 결과
