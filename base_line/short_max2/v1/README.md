short_max2 v1 기준선

전략명
smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1

축
short_max2

선정 배경
기존 short_max v13 이후 개발 과정에서 전체 2025 train 수익률 1위 후보들은 2025년 4분기 성과 집중도가 지나치게 높았다. 사용자는 2025년 4분기를 트럼프 이슈 등으로 인한 비정상적 급락/고변동 특수 구간으로 판단했다. 따라서 전체 수익률 1위가 아니라 2025년 4분기 제외 일반 구간 성과와 MDD를 더 높게 반영하는 Q4 저비중 점수제를 기준으로 새 기준선을 선택했다.

기준선 위치
base_line/short_max2/v1

기준선 성격
- short_max v13 계열 진입 조건을 유지한다.
- 청산/방어 파라미터는 Q4 저비중 순위 1위인 stop245_timeout320_rr520을 사용한다.
- 2025년 4분기를 제외해도 수익성이 유지되는 일반 구간형 숏맥스 기준선이다.
- full train에서는 여전히 2025년 4분기 기여도가 크므로, 기록상 Q4 의존성 수치를 함께 보존한다.

공식 리테스트
파일: frozen_reproduce_runner.py
원본 리테스트: run_short_max_v13_q4_low_weight_top1_stop245_rr520_retest_v1.py
데이터: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
CSV 수: full train 기준 597개
엔진: actual bar engine
수수료: 0.0004 per side
자산 분할: 0.01
레버리지: 1.0

공식 full train 결과
trades: 65265
wins: 5130
losses: 60135
win_rate_pct: 7.860262008733625
max_return_pct: 14902.949980048708
max_drawdown_pct: 2.2774507674795497
official_cd_value: 14661.265180583516
profit_factor: 2.567757993841345
active_leftover: 0
pending_leftover: 0
load_errors: 0

Q4 제외 pre-Q4 결과
trades: 53649
wins: 4158
losses: 49491
win_rate_pct: 7.750377453447409
max_return_pct: 3466.4855917171863
max_drawdown_pct: 2.2774507674795497
official_cd_value: 3485.2606382365757
profit_factor: 2.2589719429377744
positive_month_ratio_pct: 92.95774647887323
avg_month_pnl: 48.823740728411394
positive_year_ratio_pct: 100.0

Q4 의존성 기록
q4_delta_return_pct: 11436.464388331522
q4_share_of_full_return_pct: 76.73960124433124
full_top3_month_share_pct: 76.94581060709373

판정
short_max2 v1은 전체 수익률만 본 후보가 아니라 Q4 저비중 실전형 기준선이다. full train 성과는 매우 높지만, 기록과 개선 방향에서는 2025-Q4 제외 성과를 핵심 평가값으로 사용한다.
