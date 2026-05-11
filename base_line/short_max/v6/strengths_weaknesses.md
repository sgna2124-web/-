# short_max v6 장단점

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
- same_bar_trades: 3,115
- active_leftover: 0
- blocked_by_guard: 39
- generated_trades_before_score_filter: 34,044
- errors: 0

## 장점

### 1. short_max 기준 CD가 가장 높다

short_max 기준은 official_cd_value 1위다. v6의 official_cd_value는 953.4644856111984로 기존 v5의 878.8531649564361을 넘는다.

### 2. 수익성과 MDD가 동시에 개선되었다

max_return_pct는 899.0095709169104로 높아졌고, max_drawdown_pct는 4.559023920452521로 낮아졌다.

### 3. MDD가 short_main 기준도 만족한다

MDD 4.5590%는 short_main 기준인 5% 미만도 만족한다. 따라서 이 전략은 short_max뿐 아니라 short_main 기준선으로도 사용할 수 있다.

### 4. entry mask에서 score gate를 먼저 적용한다

score_min_short 2.35를 entry mask에 포함하므로 저품질 신호가 애초에 거래 후보로 들어오지 않는다. 이 구조가 포트폴리오 충돌을 줄이고 결과를 안정화한다.

### 5. dd_brake가 명확히 고정되었다

edge_current 방식으로 고정했다. drawdown 구간에서 freeze가 과도하게 연장되지 않아 좋은 신호를 지나치게 죽이지 않는다.

## 단점

### 1. 승률이 낮다

win_rate_pct 14.4067%다. 높은 승률 전략이 아니라 RR 기반 저승률 전략이다.

### 2. max_conc가 높다

max_conc가 277이다. 포트폴리오 레벨에서 동시 포지션 관리 부담이 있다.

### 3. same-bar 의존성이 있다

same_bar_trades가 3,115다. same-bar 즉시 청산 로직이 없으면 재현이 깨진다.

### 4. score 적용 위치에 민감하다

score_min_short를 entry mask에서 빼고 포트폴리오 단계로 옮기면 다른 전략이 된다.

### 5. dd_brake 모드에 민감하다

edge_current가 아니라 continuous 방식으로 바꾸면 결과가 크게 달라진다.

## 취약 구간

- 강한 상승 추세 지속 구간
- 급등 후 추가 급등이 이어지는 구간
- 동시 신호가 과도하게 몰리는 구간
- same-bar 변동성이 큰 구간
- dd_brake 작동 직후 좋은 숏 신호가 몰리는 구간

## 다음 개선 방향

- short_dev 0.0345~0.0360
- score_min_short 2.30~2.45
- short_wick_mult 1.2~1.4
- rr_mult 5.65~6.00
- timeout_bars 180~220
- time_reduce_bars 7~9
- time_reduce_to_risk_frac 0.04~0.06
- dd_brake_trigger_pct 0.025~0.035
- dd_brake_freeze_steps 3~7
- max_active_cap 260~280
- timestamp 신규 진입 cap

## 반드시 피할 것

- RSI 직접 gate를 다시 켜는 것
- RSI score 자체를 제거하는 것
- score_min_short를 entry mask 밖으로 옮기는 것
- dd_brake를 continuous 방식으로 바꾸는 것
- 수수료 또는 position_fraction을 바꾸는 것
- next bar open 진입을 바꾸는 것
