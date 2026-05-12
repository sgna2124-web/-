# short_main v6 장단점

## 전략명

short_main_v6_timeout210

## 공식 성과

- trades: 33,989
- win_rate_pct: 14.213421989467182
- final_return_pct: 931.1433546380067
- max_return_pct: 931.6464095007982
- max_drawdown_pct: 4.506694290977831
- official_cd_value: 985.153259660748
- profit_factor: 1.5653897913886468
- max_conc: 277
- max_conc_unique_symbols: 277
- same_bar_trades: 3,112
- active_leftover: 0
- blocked_by_guard: 30
- generated_trades_before_score_filter: 34,019
- errors: 0

## 장점

### 1. short_main 기준을 안정적으로 충족한다

MDD가 4.506694290977831로 5% 미만이다. short_main 기준을 만족하면서 official_cd_value가 기존 v5보다 높다.

### 2. 수익률 증가와 MDD 감소가 동시에 발생했다

v5 대비 max_return_pct는 +32.636838583887766 증가했고, MDD는 -0.05232962947469044 낮아졌다. 단순히 위험을 늘려 수익을 높인 것이 아니라 안정성도 약간 개선되었다.

### 3. 변경점이 작다

부모 기준선 대비 변경점은 timeout_bars 200에서 210으로 늘어난 것뿐이다. 구조 변경 리스크가 낮고 재현성이 좋다.

### 4. max_conc가 유지된다

max_conc는 277로 부모 기준선과 동일하다. 동시 포지션 부담이 증가하지 않았다.

### 5. active_leftover와 errors가 없다

리테스트에서 active_leftover 0, errors 0이다.

## 단점

### 1. 개선폭은 short_max v7보다 작다

official_cd_value 개선폭은 +31.68877404954958이다. short_max용 devw120보다 수익률 상승폭은 작다.

### 2. 승률은 약간 낮아졌다

부모 기준선의 win_rate_pct는 14.406704896338773이고, timeout210은 14.213421989467182다.

### 3. timeout 연장에 따른 노출 시간 증가

timeout_bars가 200에서 210으로 늘었으므로 일부 포지션의 시장 노출 시간이 길어진다.

### 4. same-bar 거래 의존성이 있다

same_bar_trades가 3,112다. same-bar 즉시 청산 로직은 반드시 유지해야 한다.

## 취약 구간

- 급등 후 추가 상승이 이어지는 강한 추세 구간
- 포지션이 timeout 근처까지 오래 끌리는 구간
- 여러 종목에서 동시에 숏 신호가 발생하는 급등장
- dd_brake가 작동한 직후 좋은 신호가 몰리는 구간

## 개선 방향

### 1. timeout 주변값 검증

- timeout_bars 205
- timeout_bars 210
- timeout_bars 215
- timeout_bars 220

### 2. time_reduce 조정

- time_reduce_bars 7, 8, 9
- time_reduce_to_risk_frac 0.04, 0.05, 0.06

### 3. score 안정화

- score_min_short 2.35, 2.40
- score_dev_weight 1.0, 1.05, 1.10

### 4. MDD 추가 완화

- dd_brake_trigger_pct 0.025, 0.030, 0.035
- dd_brake_freeze_steps 3, 5, 7

## 반드시 유지할 규칙

- short_main v6은 short_main 안정형 기준선이다.
- RSI 직접 gate를 켜지 않는다.
- RSI score 내부 기여는 유지한다.
- score_min_short는 entry mask 내부에 둔다.
- dd_brake는 edge_current 방식으로 유지한다.
- next bar open 진입을 유지한다.
- fee_per_side 0.0004를 유지한다.
- position_fraction 0.01을 유지한다.
- same-bar 즉시 청산을 유지한다.
