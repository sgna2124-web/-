# short_max v3 장단점

## 전략명

short_max_v3_combo_dev033_timeout240

## 기준 성과

- trades: 34,782
- parent_trade_ratio: 0.9442906010750937
- win_rate_pct: 14.070496233684091
- final_return_pct: 451.45526435735064
- max_return_pct: 451.8246548170149
- max_drawdown_pct: 7.484506060174601
- official_cd_value: 510.52330508569787
- profit_factor: 1.4377856344586135
- max_conc: 292
- same_bar_trades: 3,585
- active_leftover: 0
- errors: 0

## v2 대비 개선점

short_max v2 기준 성과:

- trades: 36,834
- max_return_pct: 408.9954916988155
- max_drawdown_pct: 7.395550425783604
- official_cd_value: 471.3524734452645

short_max v3 개선폭:

- trades: -2,052
- parent_trade_ratio: 94.4291%
- max_return_pct: +42.8291631181994
- max_drawdown_pct: +0.08895563439099696
- official_cd_value: +39.17083164043339

## 장점

### 1. 수익 증가 대비 MDD 증가가 매우 작다

v3는 v2보다 max_return_pct가 약 42.83%p 증가했지만 MDD는 약 0.089%p만 증가했다. short_max 축의 핵심 목표인 MDD 10% 미만 수익 극대화에 잘 맞는다.

### 2. 거래 수를 과도하게 줄이지 않는다

trades는 36,834에서 34,782로 줄었지만 parent_trade_ratio는 0.9443이다. 즉 v2의 거래 밀도를 대부분 유지하면서 성과가 개선되었다.

### 3. 과열 진입 품질이 약하게 강화되었다

short_dev를 0.032에서 0.033으로 높여 EMA20 대비 더 강한 과열 상태에서만 숏 진입한다. 단순히 거래를 크게 줄이는 필터가 아니라 과열 강도만 소폭 높인 구조다.

### 4. timeout 확대가 수익 극대화에 기여했다

timeout을 200에서 240으로 늘려 목표가 도달까지 기다리는 시간을 확보했다. v5 결과에서 timeout_240, timeout_260, combo_dev033_timeout240이 모두 상위권에 위치했기 때문에 short_max 계열에서는 보유시간 확대가 강한 개선축으로 보인다.

### 5. 동시 포지션 부담이 줄었다

max_conc가 v2의 294에서 v3의 292로 줄었다. 수익은 증가했지만 최대 동시 포지션 수는 오히려 소폭 낮아졌다.

### 6. active_leftover가 없다

same-bar 즉시 청산 처리를 포함한 strict time-axis 평가에서 active_leftover 0을 유지한다. 실거래형 시뮬레이션 구조상 안정적이다.

## 단점

### 1. MDD가 소폭 증가했다

MDD는 7.3956%에서 7.4845%로 증가했다. 증가폭은 작지만, 방어형 개선이 아니라 공격형 개선이다.

### 2. win_rate는 낮아졌다

win_rate_pct는 v2 약 14.7147%에서 v3 14.0705%로 낮아졌다. 수익 개선은 승률 상승이 아니라 큰 RR 구조와 보유시간 확대에서 발생했다.

### 3. timeout 확대는 긴 불리한 보유를 만들 수 있다

timeout 240은 목표가 도달 시간을 늘려 수익을 키웠지만, 특정 시장 환경에서는 손실 포지션을 더 오래 끌고 갈 가능성이 있다.

### 4. 거래 수가 줄었다

short_dev 강화로 trades가 2,052개 줄었다. short_max 특유의 높은 거래 밀도는 유지했지만, v2 대비 진입 기회 일부는 제거되었다.

### 5. 과열장 지속 구간에서는 여전히 취약할 수 있다

이 전략은 EMA20 대비 과열, RSI 과열, 상단 꼬리 조건을 이용한 숏 리버전 전략이다. 강한 상승 추세가 계속되는 구간에서는 stop과 fail_fast 손실이 누적될 수 있다.

## 다음 개선 방향

### 우선순위 1: timeout 주변 구조

v5 결과에서 timeout 240~260 계열이 강했다. 다음 개발에서는 다음 구간을 살펴본다.

- timeout 230
- timeout 240
- timeout 250
- timeout 260
- timeout 270
- timeout 280

### 우선순위 2: short_dev 주변 구조

v3는 short_dev 0.033에서 가장 좋은 결과를 냈다. 다음은 더 세밀한 주변값을 본다.

- short_dev 0.0328
- short_dev 0.0330
- short_dev 0.0332
- short_dev 0.0335

### 우선순위 3: rsi_755_relax와 결합

v5 결과에서 rsi_755_relax는 MDD를 낮추면서 CD를 크게 개선했다. v3의 공격형 장점과 rsi_755_relax의 안정형 장점을 결합할 가치가 있다.

검토 후보:

- short_dev 0.033 + rsi_min 75.5 + timeout 240
- short_dev 0.033 + rsi_min 75.5 + timeout 250
- short_dev 0.0328 + rsi_min 75.5 + timeout 240

### 우선순위 4: score_min_short 약한 강화

combo_score205_timeout240도 상위권이었다. score_min_short 2.02~2.08 구간을 v3와 결합해볼 수 있다.

### 우선순위 5: time_reduce 조정

time_reduce_8_003이 방어 측면에서 유의미했다. v3에 다음을 결합해볼 수 있다.

- time_reduce_bars 8~12
- time_reduce_to_risk_frac 0.03~0.05

## 유지해야 할 규칙

- short_max v3 기준선을 부모 전략으로 유지한다.
- 완전히 새로운 진입식을 만들지 않는다.
- 진입 조건의 소폭 변형, 추가, 제거만 허용한다.
- score_min_short 적용 위치를 포트폴리오 평가 단계로 유지한다.
- same-bar 즉시 청산을 유지한다.
- MDD 10% 미만을 유지한다.
- active_leftover 0을 유지한다.
