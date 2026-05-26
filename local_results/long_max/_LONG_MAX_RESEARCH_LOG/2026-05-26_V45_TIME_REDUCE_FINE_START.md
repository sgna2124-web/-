# V45 TIME REDUCE FINE SEARCH START

실험 배치 예정:
- LONG_MAX_V26_2025_TIME_REDUCE_FINE_DEV_V45_STANDALONE

출발점:
- V44에서 reversal entry 유지 + time_reduce exit가 강하게 성공.
- V44 top: V44_TR_B3_FR00
- 조건: time_reduce_bars 3, time_reduce_to_risk_frac 0.00

V44 top 성과:
- final_return_pct: 659.6972833137083
- max_drawdown_pct: 0.8068643683832977
- official_cd_value: 754.1161469801397

V44 runtime 문제:
- 32 candidates
- 141.78131736914318 minutes
- 후보 1개당 약 4.43분

V45 목적:
- V44 top 주변만 정밀 탐색.
- 1시간 내외를 맞추기 위해 후보 수를 14개로 제한.

실험 축:
- time_reduce_bars: 2, 3, 4
- time_reduce_to_risk_frac: -0.05, 0.00, 0.05, 0.10
- RR small check: 7.25, 7.75, 8.25
- hold small check: 15, 17, 19

중요:
- 진입 조건은 변경하지 않는다.
- best reversal entry 유지.
- exit 구조 중 time_reduce만 정밀 검증한다.

성공 판정:
- baseline_reproduction_ok true
- errors 0
- ruined false
- V44 top CD 754.1161469801397 초과
- runtime 약 1시간 내외
