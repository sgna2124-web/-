short_max2 기준선 인덱스

현재 공식 기준선
- v2: smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1

이전 기준선
- v1: smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1

선정 원칙
short_max2는 기존 short_max의 단순 전체 수익률 극대화가 아니라, 2025년 4분기 특수 구간의 비중을 낮게 보고 일반 구간 성과와 MDD를 더 높게 평가하는 축이다.

현재 v2 위치
base_line/short_max2/v2

현재 v2 핵심
- short_dev: 0.032
- short_wick_mult: 1.30
- score_min_short: 2.35
- atr_stop_mult: 2.50
- rr_mult: 5.00
- timeout_bars: 320
- time_reduce_bars: 3
- fail_fast_bars: 12
- dd_brake_trigger_pct: 0.035
- dd_brake_freeze_steps: 4

현재 v2 공식 full train 결과
- trades: 65180
- max_return_pct: 15588.585271121465
- max_drawdown_pct: 2.274010039088681
- official_cd_value: 15331.825267065175
- profit_factor: 2.6142284817799504

현재 v2 Q4 제외 pre-Q4 결과
- trades: 53580
- max_return_pct: 3554.3308235947543
- max_drawdown_pct: 2.1769570997805077
- official_cd_value: 3574.7776092810404
- profit_factor: 2.29014107209504
- avg_month_pnl: 50.0609975154197

핵심 문서
- README.md: 기준선 개요
- STRATEGY.md: 진입 조건, 청산 조건, 장단점
- REPRODUCE.md: 재현 방법과 gate 값
- strategy_spec.py: 파라미터와 gate 값을 코드 형태로 고정
- result_summary.csv: pre-Q4/full train 결과 요약
- Q4_LOW_WEIGHT_POLICY.md: Q4 저비중 선정 정책
