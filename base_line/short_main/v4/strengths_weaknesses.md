# short_main v4 기준선 장단점

전략명: SM16_C05_remove_no_rsi_dev035
부모 기준선: SM15_B10_rr575_tr8_f005
축: short_main
상태: v1.6 short_main v3 진입 조건 개발 결과 전체 1위

1. 현재 성과

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

2. 핵심 장점

1. official_cd_value가 압도적으로 개선됐다.
v3 CD는 414.1878이고, v4 CD는 878.8532다. 개선폭은 +464.6654다.

2. max_return_pct가 크게 상승했다.
v3 max_return_pct는 331.3434%이고, v4는 821.9869%다. 개선폭은 +490.6435%p다.

3. MDD 5% 미만을 유지했다.
v4 MDD는 4.6783%다. v3의 3.9773%보다는 높지만 short_main 기준선의 핵심 방어선인 5% 미만은 유지한다.

4. 거래 수가 증가했다.
v3 trades는 28313이고, v4 trades는 31798이다. 거래 수가 +3485 증가했다. 이는 RSI 직접 gate 제거가 막고 있던 유효 기회를 열어준 결과로 해석된다.

5. pf가 개선됐다.
v3 pf는 1.4757이고, v4 pf는 1.5778이다. 단순 거래 수 증가가 아니라 손익 구조도 개선됐다.

6. max_conc가 낮아졌다.
v3 max_conc는 286이고, v4 max_conc는 275다. 거래 수는 늘었지만 동시 포지션 최고치는 오히려 낮아졌다.

7. active_leftover가 0이다.
백테스트 종료 시 미청산 포지션이 남지 않는다.

8. 기준선 계보가 명확하다.
short_beh_dd_brake에서 v3로 이어진 진입 구조를 기반으로 하며, v4는 RSI 직접 gate 제거와 dev/score 강화라는 명확한 변경만 적용했다.

3. 핵심 약점

1. MDD가 v3보다 높다.
v3 MDD는 3.9773%이고, v4 MDD는 4.6783%다. v4는 수익성은 압도적이지만 방어력은 v3보다 약하다.

2. RSI 직접 gate 제거는 구조적 변경이다.
v4는 rsi14 > 77 조건을 직접 진입 gate에서 제거했다. 이는 단순 파라미터 조정이 아니라 진입 구조의 큰 변화다. 따라서 다음 개발에서는 이 조건을 기준선으로 명확히 인식해야 한다.

3. same_bar_trades가 증가했다.
v3 same_bar_trades는 3359이고, v4는 4559다. 특정 timestamp에 진입이 몰릴 가능성이 더 커졌다.

4. raw_trades_generated가 크게 증가했다.
v4 raw_trades_generated는 61818이다. v3의 34107보다 훨씬 많다. 포트폴리오 단계에서 많은 후보 중 일부가 체결되는 구조이므로, 실제 운용에서는 후보 밀집도 관리가 필요하다.

5. 승률은 높지 않다.
v4 win_rate_pct는 14.5858%다. v3 14.6081%와 거의 비슷하지만 낮은 승률 기반 전략이라는 점은 그대로다.

6. v1.6 단일 실험에서 나온 큰 점프다.
성과 개선폭이 매우 크기 때문에, 다음 단계에서 C05 주변값을 좁게 검증해 단일 피크인지 안정 구간인지 확인해야 한다.

4. v3 대비 개선 요약

v3 기준선: SM15_B10_rr575_tr8_f005
v4 기준선: SM16_C05_remove_no_rsi_dev035

trades: 28313 -> 31798
max_return_pct: 331.3434 -> 821.9869
max_drawdown_pct: 3.9773 -> 4.6783
official_cd_value: 414.1878 -> 878.8532
pf: 1.4757 -> 1.5778
max_conc: 286 -> 275
same_bar_trades: 3359 -> 4559
active_leftover: 0 -> 0

개선의 핵심:
RSI 직접 gate 제거
short_dev 0.033 -> 0.035
score_min_short 2.2 -> 2.35

5. 해석

v3까지는 RSI 77 초과 조건을 직접 진입 필터로 사용했다.
v1.6 결과는 이 RSI 직접 gate가 지나치게 많은 유효 숏 기회를 막고 있었을 가능성을 보여준다.

그러나 RSI 요소를 완전히 버린 것은 아니다.
score 내부에는 rsi_score가 남아 있다.
즉 v4는 RSI를 필수 조건으로 쓰지 않고, 과열 점수의 일부로만 활용한다.

이 구조가 더 자연스럽다.
강한 가격 이격과 윗꼬리, 높은 score가 있으면 RSI가 77을 넘지 않아도 숏 진입을 허용한다.
반대로 RSI가 높으면 score를 통해 여전히 가산점이 붙는다.

6. 보존해야 할 성질

1. MDD 5% 미만
2. trades 30000 전후 또는 최소 20000 이상
3. active_leftover 0
4. next_bar_open 진입
5. fee_per_side 0.0004
6. position_fraction 0.01 복리 구조
7. dd_brake의 portfolio evaluation 단계 작동
8. RSI 직접 gate 제거
9. score 내부 RSI 요소 유지
10. short_dev 0.035 부근
11. score_min_short 2.35 부근
12. rr_mult 5.75 부근
13. time_reduce_bars 8 부근

7. 다음 개선 방향

1. C05 주변값을 좁게 검증한다.
short_dev 0.0345~0.0360, score_min_short 2.30~2.45, wick_mult 1.2~1.4 범위를 확인한다.

2. RSI를 완전히 버리지 말고 보조점수로 유지한다.
RSI 직접 gate 제거는 유지하되, score 내부 rsi_score weight를 0.6~1.0 범위에서 조정할 수 있다.

3. same_bar_trades 증가를 관리한다.
특정 timestamp 집중 진입이 늘어났기 때문에 close_pos, upper_atr, max_conc 완화 필터를 매우 약하게 붙이는 실험을 할 수 있다.

4. MDD 5% 근처 위험을 관리한다.
v4는 MDD 4.6783%로 여유가 크지 않다. dd_brake 0.025~0.035, freeze 3~7을 좁게 조정해 방어력을 확인해야 한다.

5. rr/time_reduce 주변값을 재검증한다.
rr_mult 5.65~5.85, time_reduce_bars 7~9, risk_frac 0.04~0.06 범위를 확인한다.

8. 공식 승격 판단

SM16_C05_remove_no_rsi_dev035는 short_main v4 기준선으로 승격한다.

승격 사유:
1. v3보다 CD가 크게 높다.
2. v3보다 수익률이 크게 높다.
3. MDD가 5% 미만이다.
4. trades가 증가했다.
5. max_conc는 오히려 낮아졌다.
6. active_leftover 0이다.
7. errors 0이다.
8. 수수료 0.04%, 자산 1% 분할 진입 환경에서 나온 결과다.

단서:
수익성 기준으로는 명백한 승격이다.
다만 안정형 short_main 보조 기준선으로는 SM16_B14_var_rsi765_wick14도 별도 후보로 기록할 가치가 있다. 이 후보는 v3보다 CD가 높고 MDD도 낮다.
