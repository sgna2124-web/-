# short_main v4 기준선 정리

이 폴더는 short_main 축의 v4 기준선을 정리한다.

전략명: SM16_C05_remove_no_rsi_dev035
부모 기준선: SM15_B10_rr575_tr8_f005
상위 계보: short_beh_dd_brake -> SM15_B10_rr575_tr8_f005 -> SM16_C05_remove_no_rsi_dev035
축: short_main
상태: v1.6 short_main v3 진입 조건 추가/변형/제거 개발 결과 기준 전체 1위
기준 데이터 수: 597 CSV

1. v4 기준선 성과

trades: 31798
wins: 4638
losses: 27160
win_rate_pct: 14.585823007736334
final_asset: 921.5165864710646
final_return_pct: 821.5165864710646
peak_asset: 921.9869251730971
max_return_pct: 821.9869251730971
max_drawdown_pct: 4.6783483625391975
official_cd_value: 878.8531649564361
pf: 1.5778442611030818
max_conc: 275
max_conc_unique_symbols: 275
same_bar_trades: 4559
active_leftover: 0
gross_profit: 2243.2086266460665
gross_loss: 1421.6920401750067
raw_trades_generated: 61818
errors: 0

2. 실행 환경

initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
entry: signal candle i -> next bar open i+1
csv_file_count: 597

3. v3 기준선 대비

v3 기준선: SM15_B10_rr575_tr8_f005
v3 trades: 28313
v3 max_return_pct: 331.3434403627648
v3 max_drawdown_pct: 3.9772559021280185
v3 official_cd_value: 414.18780792249464

v4 개선폭:
trades: +3485
max_return_pct: +490.6434848103323
max_drawdown_pct: +0.701092460411179
official_cd_value: +464.66535703394146
parent_trade_ratio: 1.1230883339808568

4. v4 핵심 변경점

v3에서 유지한 것:
- short_main 축
- next bar open 진입
- fee_per_side 0.0004
- position_fraction 0.01
- wick gate 유지
- score gate 유지
- rr_mult 5.75
- time_reduce_bars 8
- time_reduce_to_risk_frac 0.05
- fail_fast_bars 10
- dd_brake 3% / freeze 5

v3에서 변경한 것:
- RSI gate 제거
- short_dev 0.033 -> 0.035
- score_min_short 2.2 -> 2.35

중요:
RSI gate는 제거되었지만 score 계산 내부의 RSI score 구성 요소는 유지된다. 즉 rsi14 > 77을 직접 진입 필수 조건으로 쓰지 않을 뿐, score 계산에서는 rsi14가 77을 넘을 때 가산점으로 반영된다.

5. v4 진입 조건 요약

short_signal 조건:
close / ema20 - 1 >= 0.035
upper_wick >= 1.3 * body
score >= 2.35
expected_tp >= 0.003

비활성화된 조건:
rsi14 > 77 직접 gate는 사용하지 않는다.

6. v4 운영 판단

SM16_C05_remove_no_rsi_dev035는 short_main v4 기준선으로 승격한다.
이유는 다음과 같다.

1. official_cd_value가 v3보다 +464.6654 개선됐다.
2. max_return_pct가 v3보다 +490.6435%p 상승했다.
3. MDD가 4.6783%로 short_main 기준인 5% 미만을 유지한다.
4. trades가 31798로 v3보다 증가했고 20000 이상 기준을 충분히 만족한다.
5. active_leftover가 0이다.
6. errors가 0이다.
7. 수수료 0.04%, 자산 1% 분할 진입 환경에서 확인된 결과다.

7. 다음 개발 기준

다음 short_main 개발은 SM16_C05_remove_no_rsi_dev035를 부모로 삼는다.
완전히 새로운 전략을 만들지 않는다.
기준선 진입 조건은 다음을 중심으로 개선한다.

핵심 고정축:
- use_rsi_gate: false
- short_dev: 0.035 부근
- score_min_short: 2.35 부근
- wick_mult: 1.3 부근
- rr_mult: 5.75 부근
- time_reduce_bars: 8 부근

다음 탐색 권장 범위:
- short_dev: 0.0345, 0.0350, 0.0355, 0.0360
- score_min_short: 2.30, 2.35, 2.40, 2.45
- short_wick_mult: 1.2, 1.3, 1.4
- rr_mult: 5.65, 5.75, 5.85
- time_reduce_bars: 7, 8, 9
- time_reduce_to_risk_frac: 0.04, 0.05, 0.06

8. 폴더 구성

README.md: v4 기준선 개요와 성과
strategy_code.py: v4 기준선 전략 코드
entry_conditions.md: 진입 조건, score, 청산, 위험관리 조건
strengths_weaknesses.md: 장점, 약점, 다음 개선 방향
reproduction_notes.md: 재현 시 반드시 지켜야 할 환경과 주의사항
