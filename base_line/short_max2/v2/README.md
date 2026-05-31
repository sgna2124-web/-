short_max2 v2 기준선

전략명
smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1

원 탐색 후보
smx2v1_devq4low_18_stop250_rr500_t320

축
short_max2

이전 기준선
base_line/short_max2/v1

기준선 위치
base_line/short_max2/v2

선정 배경
short_max2/v1은 2025년 4분기 특수 구간의 성과 비중을 낮게 보고, Q4 제외 일반 구간의 월별 평균 수익과 MDD를 더 높게 평가해 선택한 기준선이었다. v2는 v1을 기준으로 실제 매매 방식의 actual bar engine을 유지한 상태에서 소폭 파라미터 변형을 수행했고, Q4 저비중 점수 기준 1위였던 stop250_rr500_t320을 float64 원본형 단독 리테스트로 확정한 기준선이다.

선정 정책
- 전체 수익률 1위가 아니라 Q4 저비중 실전형 순위를 우선한다.
- 2025-Q4 제외 pre-Q4 월별 평균 수익을 높게 평가한다.
- 2025-Q4 제외 pre-Q4 MDD를 높게 평가한다.
- pre-Q4 profit factor와 positive_month_ratio를 보조 평가한다.
- 2025-Q4 성과는 낮은 비중으로만 반영한다.

핵심 변경점
v1 대비 손절폭을 2.45에서 2.50으로 넓히고, RR을 5.20에서 5.00으로 낮췄다. timeout, time_reduce, fail_fast, dd_brake는 유지했다.

v1 핵심 파라미터
atr_stop_mult: 2.45
rr_mult: 5.20
timeout_bars: 320

v2 핵심 파라미터
atr_stop_mult: 2.50
rr_mult: 5.00
timeout_bars: 320

공식 리테스트
원본 리테스트 파일: run_short_max2_v1_q4low_top1_stop250_rr500_retest_v1.py
권장 고정 재현 파일: base_line/short_max2/v2/frozen_reproduce_runner.py
데이터: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
CSV 수: full train 기준 597개
엔진: actual bar engine
수수료: 0.0004 per side
자산 분할: 0.01
레버리지: 1.0
데이터 사용: 2025-12-31 23:59:59까지 train, 2026-01-01 이후는 holdout

공식 full train 결과
trades: 65180
wins: 5130
losses: 60050
win_rate_pct: 7.8705124271248845
max_return_pct: 15588.585271121465
max_drawdown_pct: 2.274010039088681
official_cd_value: 15331.825267065175
profit_factor: 2.6142284817799504
positive_month_ratio_pct: 93.24324324324324
active_leftover: 0
pending_leftover: 0
load_errors: 0

Q4 제외 pre-Q4 결과
trades: 53580
wins: 4156
losses: 49424
win_rate_pct: 7.7566256065696155
max_return_pct: 3554.3308235947543
max_drawdown_pct: 2.1769570997805077
official_cd_value: 3574.7776092810404
profit_factor: 2.29014107209504
positive_month_ratio_pct: 92.95774647887323
avg_month_pnl: 50.0609975154197
positive_year_ratio_pct: 100.0

Q4 의존성 기록
q4_share_of_full_return_pct: 77.19914436251436
full_top3_month_share_pct: 77.40116227608569

v1 대비 개선
pre-Q4 max_return_pct: +87.84523187756795
pre-Q4 MDD: -0.1004936676990419
pre-Q4 official_cd_value: +89.5169710444647
pre-Q4 profit_factor: +0.0311691291572657
pre-Q4 avg_month_pnl: +1.237256787008306
full train max_return_pct: +685.635291072757
full train MDD: -0.0034407283908688
full train official_cd_value: +670.5600864816588
full train profit_factor: +0.0464704879386053

판정
short_max2 v2는 v1보다 Q4 제외 일반 구간의 월평균 수익, MDD, CD, PF가 모두 개선되었고, full train에서도 CD와 PF가 개선되었다. 다만 Q4 share와 top3 month share는 v1보다 약간 상승했으므로, 이후 개선 방향은 수익 집중도 완화를 계속 유지해야 한다.
