short_max2 v1 전략 설명

전략명
smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1

전략 계열
short_max v13 계열 과열 숏 되돌림 전략

선정 기준
2025년 4분기를 특수 고변동 구간으로 간주한다. 따라서 전체 train 수익률이 가장 큰 후보가 아니라, 2025년 4분기를 제외한 일반 구간에서 월별 평균 수익과 MDD가 우수한 후보를 우선했다.

핵심 진입 조건
진입 조건은 short_max v13 계열을 유지한다.

지표
- ema 기간: 기존 short_max v13과 동일
- rsi 기간: 기존 short_max v13과 동일
- atr 기간: 기존 short_max v13과 동일
- 지표 계산 시 2026년 이후 데이터는 사전에 제외한다.

진입 핵심값
- short_dev: 0.032
- short_wick_mult: 1.3
- score_min_short: 2.35

청산/방어 핵심값
- atr_stop_mult: 2.45
- rr_mult: 5.2
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
- 신호가 발생한 캔들의 다음 캔들 open에서 진입한다.

수수료/자산
- initial_asset: 100.0
- position_fraction: 0.01
- leverage: 1.0
- fee_per_side: 0.0004
- round_trip_fee: 0.0008

공식 full train 결과
- 기간: 2025-12-31 23:59:59까지
- trades: 65265
- wins: 5130
- losses: 60135
- win_rate_pct: 7.860262008733625
- max_return_pct: 14902.949980048708
- max_drawdown_pct: 2.2774507674795497
- official_cd_value: 14661.265180583516
- profit_factor: 2.567757993841345

Q4 제외 pre-Q4 결과
- 기간: 2025-09-30 23:59:59까지
- trades: 53649
- wins: 4158
- losses: 49491
- win_rate_pct: 7.750377453447409
- max_return_pct: 3466.4855917171863
- max_drawdown_pct: 2.2774507674795497
- official_cd_value: 3485.2606382365757
- profit_factor: 2.2589719429377744
- active_months: 71
- positive_months: 66
- negative_months: 5
- positive_month_ratio_pct: 92.95774647887323
- avg_month_pnl: 48.823740728411394
- positive_year_ratio_pct: 100.0

장점
1. 2025-Q4 제외 일반 구간에서도 수익성이 유지된다.
2. full train 기준 MDD가 2.277%로 낮다.
3. PF가 full train 2.5677, pre-Q4 2.259로 양호하다.
4. 월별 플러스 비율이 90% 이상이다.
5. 기존 short_max v13보다 CD, MDD, PF가 모두 개선됐다.

단점/주의점
1. full train 전체 수익 중 약 76.74%가 2025-Q4에서 나온다.
2. full train top3 month share가 76.95%로 높다.
3. 승률이 7.86%로 낮고, 소수 큰 익절이 전체 기대값을 끌어올리는 구조다.
4. pre-Q4 평가에서는 2025-09-30까지 유효 데이터가 부족한 심볼 45개가 제외됐다. 따라서 공식 재현값은 full train 597개 결과를 우선한다.
5. 향후 개선은 Q4 수익 극대화보다 Q4 제외 월평균 수익, MDD, PF, top3 month share 완화를 우선한다.

운영 판단
short_max2 v1은 short_max v13을 대체하는 실전형/Q4 저비중 기준선이다. 단순 전체 수익률 1위가 아니라, 2025-Q4 제외 일반 구간 성과를 기준으로 선택됐다.
