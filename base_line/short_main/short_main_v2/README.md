# short_main 기준선 정리

이 폴더는 short_main 축의 현재 공식 기준선인 short_beh_dd_brake를 독립적으로 확인하기 위한 정리 공간이다.

전략명: short_beh_dd_brake
축: short_main
상태: 현재 597 CSV 기준 공식 short_main 기준선
기준 데이터 수: 597 CSV
실행 환경:
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- entry_on_next_bar_open: true
- allow_long: false
- allow_short: true

현재 597 CSV 기준 성과:
- trades: 28308
- final_return_pct: 322.48410704162137
- max_return_pct: 322.7577232826396
- max_drawdown_pct: 4.4066222161057595
- official_cd_value: 404.12838752816384
- win_rate: 0.15257171117705243
- pf: 1.441356672437088
- max_conc: 286
- same_bar_trades: 3357
- active_leftover: 0

폴더 구성:
- strategy_code.py: short_beh_dd_brake 기준선의 핵심 전략 코드와 파라미터
- entry_conditions.md: 진입 조건, 청산 조건, dd_brake 작동 방식
- strengths_weaknesses.md: 장점, 약점, 개선 방향

운영 기준:
short_main 개선은 이 기준선의 진입 구조를 부모로 삼는다. 완전히 새로운 숏 전략을 만들지 않는다. 개선안은 short_dev, short_rsi_min, short_wick_mult, score_min_short, rr_mult, time_reduce, fail_fast, dd_brake를 좁은 범위에서 조정하거나 필터를 추가하는 방식으로 진행한다.

승격 기준:
- MDD 5% 미만 보존
- trades 20000 이상 보존
- active_leftover 0 유지
- official_cd_value가 기준선보다 개선될 것
- 기준선 진입 구조를 훼손하지 않을 것

주의:
최근 v1.4 테스트에서 SM24_rr575가 좋은 승격 후보로 확인되었지만, 이 폴더의 공식 기준선은 아직 short_beh_dd_brake다. SM24는 추가 검증 후 승격 여부를 판단한다.
