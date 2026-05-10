# short_main v3 기준선 정리

이 폴더는 short_main 축의 새롭게 갱신된 v3 기준선을 정리한다.

전략명: SM15_B10_rr575_tr8_f005
부모 기준선: short_beh_dd_brake
축: short_main
상태: v1.5 SM24 주변값 개발 결과 기준 short_main 1위 후보
기준 데이터 수: 597 CSV

1. v3 기준선 성과

trades: 28313
wins: 4136
losses: 24177
win_rate_pct: 14.608130540741001
final_asset: 431.06426729450357
final_return_pct: 331.06426729450357
peak_asset: 431.3434403627648
max_return_pct: 331.3434403627648
max_drawdown_pct: 3.9772559021280185
official_cd_value: 414.18780792249464
pf: 1.4757306514967135
max_conc: 286
max_conc_unique_symbols: 286
same_bar_trades: 3359
active_leftover: 0
gross_profit: 1026.9712185345038
gross_loss: 695.9069512400048
raw_trades_generated: 34107
errors: 0

2. 이전 공식 short_main 기준선 대비

이전 기준선: short_beh_dd_brake
이전 trades: 28308
이전 max_return_pct: 322.7577232826396
이전 max_drawdown_pct: 4.4066222161057595
이전 official_cd_value: 404.12838752816384

v3 개선폭:
trades: +5
max_return_pct: +8.585717080125221
max_drawdown_pct: -0.42936631397774105
official_cd_value: +10.0594203943308

3. SM24 후보 대비

SM24 후보: SM24_00_rr575_candidate
SM24 trades: 28311
SM24 official_cd_value: 408.3085802510934

v3 개선폭:
trades: +2
max_return_pct: +4.412555136855929
drawdown_pct: -0.3846456653731294
official_cd_value: +5.879227671401225

4. 핵심 변경점

기준선 진입 조건은 유지한다.
주요 변경은 rr_mult와 time_reduce이다.

short_beh_dd_brake v2:
rr_mult: 6.0
time_reduce_bars: 10
time_reduce_to_risk_frac: 0.05

short_main v3:
rr_mult: 5.75
time_reduce_bars: 8
time_reduce_to_risk_frac: 0.05

즉 목표 손익비를 6.0R에서 5.75R로 낮추고, 진입 후 위험 축소 시점을 10봉에서 8봉으로 앞당긴 구조다.

5. 운영 판단

이 후보는 수익성과 방어력을 동시에 개선했다.
max_return_pct는 상승했고, MDD는 4% 미만으로 내려갔다.
trades는 기존 기준선과 거의 동일하게 유지되었고 active_leftover도 0이다.

따라서 short_main v3 기준선으로 정리한다.

6. 폴더 구성

strategy_code.py: v3 기준선 전략 코드와 파라미터
entry_conditions.md: 진입 조건, 청산 조건, 위험관리 조건
strengths_weaknesses.md: 장점, 약점, 다음 개선 방향

7. 다음 개발 기준

다음 short_main 개발은 SM15_B10_rr575_tr8_f005를 부모로 삼는다.
완전히 새로운 전략을 만들지 않는다.
진입 조건은 유지하고, rr_mult 5.70~5.85, time_reduce_bars 6~10, risk_frac 0.04~0.06, fail_fast_bars 8~12 범위에서 좁게 검증한다.
