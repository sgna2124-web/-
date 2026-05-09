# short_max 기준선 정리

이 폴더는 short_max 축의 현재 공식 기준선인 short_only_reference_1x를 독립적으로 확인하기 위한 정리 공간이다.

전략명: short_only_reference_1x
축: short_max
상태: 현재 597 CSV 기준 공식 short_max 기준선
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
- trades: 36834
- final_return_pct: 408.6547709998406
- max_return_pct: 408.9954916988155
- max_drawdown_pct: 7.395550425783604
- official_cd_value: 471.3524734452645
- win_rate: 0.1471466579790411
- pf: 1.4013066651299806
- max_conc: 294
- same_bar_trades: 3766
- active_leftover: 0

폴더 구성:
- strategy_code.py: short_only_reference_1x 기준선의 핵심 전략 코드와 파라미터
- entry_conditions.md: 진입 조건, 청산 조건, short_max 고유 설정
- strengths_weaknesses.md: 장점, 약점, 개선 방향

운영 기준:
short_max 개선은 수익 극대화 축이다. 다만 MDD가 10%를 넘지 않도록 관리하고, parent_trade_ratio가 지나치게 낮아져 short_max의 거래량 장점이 사라지면 실패로 본다.

승격 기준:
- MDD 10% 미만 유지
- trades 25000 이상 유지
- active_leftover 0 유지
- official_cd_value가 기준선보다 개선될 것
- short_max의 많은 거래 수와 수익 극대화 성질을 훼손하지 않을 것
