# short_main v5 장단점

## 전략명

SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge

## 공식 성과

- trades: 34,005
- win_rate_pct: 14.406704896338773
- final_return_pct: 898.4999401921407
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984
- profit_factor: 1.555465134190124
- max_conc: 277
- max_conc_unique_symbols: 277
- same_bar_trades: 3,115
- active_leftover: 0
- blocked_by_guard: 39
- generated_trades_before_score_filter: 34,044
- errors: 0

## 장점

### 1. short_main 기준을 충족하면서 CD가 크게 높다

MDD가 4.559023920452521로 5% 미만이다. 이 조건을 유지하면서 official_cd_value가 953.4644856111984까지 상승했다.

### 2. 기존 v4보다 수익률과 MDD가 동시에 개선되었다

기존 v4는 max_return_pct 821.9869251730971, MDD 4.6783483625391975, CD 878.8531649564361이었다. v5는 max_return_pct가 높고 MDD는 더 낮다.

### 3. RSI 직접 gate 제거 구조가 유지된다

RSI를 필수 진입 조건으로 쓰지 않기 때문에 강한 dev와 wick 조건을 가진 유효 숏 기회를 더 잘 포착한다.

### 4. score gate를 entry mask에 포함해 후보 충돌을 줄인다

score_min_short 2.35를 entry mask에 포함함으로써 낮은 품질 후보가 포트폴리오 평가 단계까지 넘어가지 않는다. 이 구조에서 generated_trades_before_score_filter는 34,044로 정리되며, 최종 trades는 34,005다.

### 5. dd_brake가 과도하게 거래를 죽이지 않는다

edge_current 방식은 drawdown이 기준선을 처음 넘는 순간에만 freeze를 부여한다. continuous 방식처럼 drawdown 상태가 지속될 때마다 신규 진입을 계속 막지 않는다.

### 6. 재현성이 확인되었다

단독 리테스트에서 gate_pass=True가 확인되었다. trades, max_return_pct, max_drawdown_pct, official_cd_value, generated_trades_before_score_filter, errors, active_leftover가 모두 기준값과 일치했다.

## 단점

### 1. 승률은 낮다

win_rate_pct가 14.406704896338773이다. 이 전략은 높은 승률 전략이 아니라 낮은 승률, 큰 RR, 분산 진입, 포트폴리오 관리로 수익을 만든다.

### 2. same-bar 거래가 많다

same_bar_trades가 3,115다. 따라서 same-bar 즉시 청산 로직이 빠지면 성과와 active_leftover가 달라질 수 있다.

### 3. max_conc가 여전히 높다

max_conc가 277이다. 기존 short_max v5의 275보다 약간 높다. 실거래에서는 동시 포지션 관리와 API 주문량 부담을 고려해야 한다.

### 4. score_min_short 위치가 민감하다

이 전략은 score_min_short를 entry mask 안에 넣은 exact-entry-mask 구조다. score를 포트폴리오 단계로 옮기면 다른 전략으로 보아야 한다.

### 5. dd_brake 해석이 민감하다

dd_brake는 edge_current로 고정해야 한다. continuous 방식으로 바꾸면 거래 수와 성과가 크게 달라진다.

## 취약 구간

- 강한 상승 추세가 지속되는 구간
- 급등 후 상단 꼬리가 발생했지만 추가 급등이 이어지는 구간
- 여러 종목에서 동시에 숏 신호가 몰리는 구간
- 거래소 변동성이 커져 same-bar성 체결이 많아지는 구간
- dd_brake가 작동한 직후 좋은 신호가 몰리는 구간

## 개선 방향

### 1. short_dev 주변 탐색

- 0.0345
- 0.0350
- 0.0355
- 0.0360

### 2. score_min_short 주변 탐색

- 2.30
- 2.35
- 2.40
- 2.45

### 3. RR 조정

- 5.65
- 5.75
- 5.85
- 6.00

### 4. time_reduce 조정

- time_reduce_bars 7, 8, 9
- time_reduce_to_risk_frac 0.04, 0.05, 0.06

### 5. dd_brake 조정

- trigger 0.025, 0.030, 0.035
- freeze_steps 3, 5, 7

### 6. max_conc 완화

- timestamp 신규 진입 cap
- max_active_cap 260~280
- close position 필터
- upper_wick / ATR 필터

## 개선 시 주의점

- RSI 직접 gate를 켜면 다른 전략이 된다.
- score_min_short를 포트폴리오 단계로 옮기면 다른 전략이 된다.
- dd_brake를 continuous 방식으로 바꾸면 다른 전략이 된다.
- 수수료와 자산 분할 설정을 바꾸면 기준선 비교가 불가능하다.
