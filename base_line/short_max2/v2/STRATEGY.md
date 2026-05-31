short_max2 v2 전략 설명

전략명
smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1

전략 계열
short_max2 v1 기반 Q4 저비중 실전형 과열 숏 되돌림 전략

선정 기준
2025년 4분기를 특수 고변동 구간으로 간주한다. 따라서 전체 train 수익률만으로 후보를 고르지 않고, 2025년 4분기 제외 일반 구간의 월별 평균 수익과 MDD를 우선 평가했다. v2는 v1 대비 pre-Q4 월평균 수익, MDD, PF, CD가 모두 개선되어 기준선으로 승격했다.

진입 조건
진입 조건은 short_max2/v1 계열을 유지한다.

핵심 진입 파라미터
- side: short
- short_dev: 0.032
- short_wick_mult: 1.30
- score_min_short: 2.35
- RSI gate: 사용하지 않음

청산/방어 파라미터
- atr_stop_mult: 2.50
- rr_mult: 5.00
- timeout_bars: 320
- time_reduce_bars: 3
- time_reduce_to_risk_frac: 0.00
- fail_fast_bars: 12
- dd_brake_trigger_pct: 0.035
- dd_brake_freeze_steps: 4

체결 방식
- 5분봉 actual bar engine을 사용한다.
- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
- t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
- 같은 timestamp에서 청산 결과를 이용해 곧바로 재진입하지 않는다.
- same-bar TP/SL은 유지한다.
- same-bar에서 stop과 target이 동시에 닿으면 stop 우선 처리한다.
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

진입 가격
신호가 발생한 캔들의 다음 캔들 open에서 진입한다.

수수료/자산
- initial_asset: 100.0
- position_fraction: 0.01
- leverage: 1.0
- fee_per_side: 0.0004
- round_trip_fee: 0.0008

데이터 정책
- full train: 2025-12-31 23:59:59까지
- holdout: 2026-01-01 이후
- 2026 데이터는 지표 계산 전 제외한다.
- pre-Q4 진단: 2025-09-30 23:59:59까지

공식 full train 결과
- trades: 65180
- wins: 5130
- losses: 60050
- win_rate_pct: 7.8705124271248845
- max_return_pct: 15588.585271121465
- max_drawdown_pct: 2.274010039088681
- official_cd_value: 15331.825267065175
- profit_factor: 2.6142284817799504
- positive_month_ratio_pct: 93.24324324324324
- q4_share_of_full_return_pct: 77.19914436251436
- top3_month_share_pct: 77.40116227608569
- load_errors: 0

Q4 제외 pre-Q4 결과
- trades: 53580
- wins: 4156
- losses: 49424
- win_rate_pct: 7.7566256065696155
- max_return_pct: 3554.3308235947543
- max_drawdown_pct: 2.1769570997805077
- official_cd_value: 3574.7776092810404
- profit_factor: 2.29014107209504
- positive_month_ratio_pct: 92.95774647887323
- avg_month_pnl: 50.0609975154197
- positive_year_ratio_pct: 100.0

장점
1. v1보다 pre-Q4 월평균 수익이 개선됐다.
2. v1보다 pre-Q4 MDD가 낮다.
3. v1보다 pre-Q4 PF와 CD가 개선됐다.
4. full train에서도 CD와 PF가 개선됐다.
5. 실제 매매 방식의 actual bar engine을 유지했다.
6. full train 기준 load_errors 0으로 전체 597개 CSV를 사용했다.

단점/주의점
1. full train 수익 중 약 77.20%가 2025-Q4 쪽에서 나온다.
2. full_top3_month_share_pct가 77.40%로 높다.
3. v1보다 Q4 share와 top3 month share가 약간 상승했다.
4. 승률은 7.87%로 낮고, 소수 큰 익절이 기대값을 만든다.
5. 이후 개선은 Q4 의존도 완화와 pre-Q4 안정성 강화를 동시에 봐야 한다.

운영 판단
short_max2 v2는 short_max2/v1을 대체하는 최신 Q4 저비중 실전형 기준선이다. 단, 전체 수익률이 아니라 pre-Q4 성과 중심으로 관리한다.
