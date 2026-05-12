# short_max v7 장단점

## 전략명

short_max_v7_devw120

## 공식 성과

- trades: 43,681
- win_rate_pct: 13.827522263684438
- final_return_pct: 1221.3299878755902
- max_return_pct: 1221.9746135454966
- max_drawdown_pct: 5.6636954922983485
- official_cd_value: 1247.1019969487918
- profit_factor: 1.5021526593629504
- max_conc: 295
- max_conc_unique_symbols: 295
- same_bar_trades: 3,694
- active_leftover: 0
- blocked_by_guard: 152
- generated_trades_before_score_filter: 43,833
- errors: 0

## 장점

### 1. short_max 기준 CD가 크게 상승했다

v6의 official_cd_value는 953.4644856111984였고, v7은 1247.1019969487918이다. 개선폭은 +293.6375113375934다.

### 2. 수익률이 크게 증가했다

max_return_pct가 899.0095709169104에서 1221.9746135454966으로 증가했다. 이는 dev_score 가중치를 높여 EMA20 대비 과열 이격이 강한 신호를 더 적극적으로 채택한 결과로 해석된다.

### 3. 부모 전략의 핵심 구조를 유지한다

RSI 직접 gate 제거, score gate entry mask 적용, edge_current dd_brake, next bar open 진입 구조를 그대로 유지한다. 변경점은 score_dev_weight 1.2 하나로 명확하다.

### 4. active_leftover와 errors가 없다

리테스트에서 active_leftover 0, errors 0이다. 미청산 포지션 잔존이나 실행 오류가 없다.

### 5. short_max 전용으로 강하다

MDD가 5.6637%로 short_main 기준에는 맞지 않지만, short_max 기준인 MDD 10% 미만에서는 충분히 안정권이다. 수익성을 우선하는 short_max 축에 적합하다.

## 단점

### 1. short_main 기준에는 부적합하다

MDD가 5.6636954922983485로 short_main 기준인 5% 미만을 초과한다. 이 전략은 short_max 전용으로만 사용해야 한다.

### 2. MDD가 부모보다 증가했다

v6 대비 MDD가 +1.1046715718458273 증가했다. 수익률이 크게 오른 대가로 낙폭이 커졌다.

### 3. 승률이 낮아졌다

v6 승률은 14.406704896338773이고 v7 승률은 13.827522263684438다. 수익은 증가했지만 승률은 낮아졌다.

### 4. max_conc가 증가했다

v6 max_conc는 277이고 v7 max_conc는 295다. 동시 포지션 관리 부담이 커졌다.

### 5. 후보 수가 증가했다

generated_trades_before_score_filter가 34,044에서 43,833으로 증가했다. 거래 기회가 늘어난 만큼 과열 구간에서 포지션 밀집이 커질 수 있다.

## 취약 구간

- 강한 상승 추세가 이어지는 구간
- 과열 이격이 발생했지만 추세가 계속 확장되는 구간
- 여러 종목이 동시에 dev 조건을 만족하는 시장 급등 구간
- max_conc가 290 이상으로 커지는 구간
- dd_brake 직전 또는 직후에 신호가 몰리는 구간

## 개선 방향

### 1. dev weight 주변값 재검증

- score_dev_weight 1.10
- score_dev_weight 1.15
- score_dev_weight 1.20
- score_dev_weight 1.25

### 2. MDD 완화 필터

- max_active_cap 280~295
- timestamp 신규 진입 cap
- short_dev 0.0355~0.0360
- score_min_short 2.40~2.45

### 3. dd_brake 조정

- dd_brake_trigger_pct 0.025~0.035
- dd_brake_freeze_steps 3~7

### 4. time/protect 조정

- timeout_bars 190~210
- time_reduce_bars 7~9
- time_reduce_to_risk_frac 0.04~0.05

## 반드시 유지할 규칙

- short_max v7은 short_max 전용 기준선이다.
- RSI 직접 gate를 켜지 않는다.
- RSI score 내부 기여는 유지한다.
- score_min_short는 entry mask 내부에 둔다.
- dd_brake는 edge_current 방식으로 유지한다.
- next bar open 진입을 유지한다.
- fee_per_side 0.0004를 유지한다.
- position_fraction 0.01을 유지한다.
- same-bar 즉시 청산을 유지한다.
