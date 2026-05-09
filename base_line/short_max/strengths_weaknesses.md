# short_max 기준선 장단점

전략명: short_only_reference_1x
축: short_max
상태: 현재 597 CSV 기준 공식 short_max 기준선

1. 현재 성과

trades: 36834
final_return_pct: 408.6547709998406
max_return_pct: 408.9954916988155
max_drawdown_pct: 7.395550425783604
official_cd_value: 471.3524734452645
win_rate: 0.1471466579790411
pf: 1.4013066651299806
max_conc: 294
max_conc_unique_symbols: 294
same_bar_trades: 3766
active_leftover: 0

2. 장점

1. 현재 숏 계열 중 절대 수익률이 가장 강하다.
max_return_pct 408.9955%로 short_main보다 높다. 수익 극대화 축의 기준선으로 적합하다.

2. official_cd_value가 가장 높다.
official_cd_value 471.3525로 short_main의 404.1284보다 높다. MDD가 더 크지만 수익 증가폭이 이를 보상한다.

3. 거래 수가 많다.
trades 36834로 short_main보다 약 8500건 이상 많다. 기회를 많이 잡는 구조이며, 수익 누적에 유리하다.

4. 조건이 과도하게 엄격하지 않다.
short_dev 0.032, short_rsi_min 76, score_min_short 2.0으로 short_main보다 넓게 숏 과열을 포착한다.

5. dd_brake가 없어 수익 기회를 막지 않는다.
포트폴리오 drawdown 구간에서도 신규 진입을 계속 허용하므로 수익 기회를 최대한 가져간다.

6. MDD가 10% 미만이다.
수익 극대화 축임에도 max_drawdown_pct 7.3956%로 10% 미만을 유지한다.

3. 약점

1. MDD가 short_main보다 높다.
short_max MDD는 7.3956%, short_main MDD는 4.4066%다. main 축으로 쓰기에는 방어력이 부족하다.

2. 승률이 낮다.
win_rate가 약 14.71%다. rr 6.0 기반이라 연속 손실을 전제로 하는 전략이다.

3. max_conc가 높다.
max_conc 294로 실제 운용에서는 동시 포지션 관리, 자금 배분, 거래소 제한, 체결 품질 문제가 생길 수 있다.

4. dd_brake가 없어 급락 방어가 약하다.
포트폴리오 drawdown이 커지는 구간에서도 신규 진입을 막지 않는다. 수익성에는 좋지만 손실 집중 구간을 키울 수 있다.

5. 상승장 지속 구간에서 취약하다.
숏 전용 전략이므로 과열 신호 이후에도 상승이 이어지는 구간에서는 손절이 연속될 수 있다.

4. 보존해야 할 성질

1. 높은 거래 수
2. 높은 max_return_pct
3. official_cd_value 우위
4. MDD 10% 미만
5. active_leftover 0
6. next_bar_open 진입
7. fee_per_side 0.0004
8. position_fraction 0.01 복리 구조
9. 숏 과열 진입 구조

5. 개선 방향

1. 수익성을 먼저 보존한다.
short_max는 수익 극대화 축이므로 거래 수와 max_return을 과도하게 줄이면 안 된다.

2. MDD와 max_conc를 부드럽게 낮춘다.
필터를 강하게 걸기보다 약한 dd_brake, loss streak guard, max_conc 완화, time_reduce 조정을 우선 실험한다.

3. score_min_short는 소폭만 조정한다.
score_min_short를 너무 올리면 short_max가 short_main처럼 변한다. 2.0 근처에서 미세 조정해야 한다.

4. parent_trade_ratio를 중시한다.
거래 수가 기준선 대비 70% 미만으로 내려가면 short_max의 정체성이 훼손된 것으로 본다.

5. short_main과 같은 목표로 개발하지 않는다.
short_max의 목표는 MDD 5% 미만이 아니라 수익률과 CD 극대화다. MDD는 10% 미만에서 관리한다.

6. 실험 후보

1. dd_brake를 약하게 추가
예: trigger 0.05~0.07, freeze 2~4

2. time_reduce 조정
예: time_reduce_bars 8~14, risk_frac 0.03~0.08

3. rr 조정
예: rr_mult 5.7~6.2

4. max_conc 완화
동일 timestamp 과밀 진입을 일부 제한하되 거래 수를 크게 줄이지 않는 방식

5. weak trend filter 추가
강한 상승 추세 지속 구간에서 무리한 숏 진입을 일부 줄이는 방식
