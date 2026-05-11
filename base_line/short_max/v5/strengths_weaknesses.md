# short_max v5 장단점

## 전략명

SM16_C05_remove_no_rsi_dev035

## short_max v5 기록명

short_max_v5_SM16_C05_remove_no_rsi_dev035

## 공식 성과

- trades: 31,798
- wins: 4,638
- losses: 27,160
- win_rate_pct: 14.585823007736334
- final_asset: 921.5165864710646
- final_return_pct: 821.5165864710646
- peak_asset: 921.9869251730971
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361
- pf: 1.5778442611030818
- max_conc: 275
- max_conc_unique_symbols: 275
- same_bar_trades: 4,559
- active_leftover: 0
- gross_profit: 2243.2086266460665
- gross_loss: 1421.6920401750067
- raw_trades_generated: 61,818
- errors: 0

## 이전 short_max v4 대비 개선점

이전 short_max v4 기준선:

- strategy: short_max_v4_combo_rsi755_timeout280
- trades: 36,430
- max_return_pct: 536.5429980399269
- max_drawdown_pct: 6.373508371397563
- official_cd_value: 595.9728767723071
- profit_factor: 1.4501345502446736
- max_conc: 295

short_max v5 개선폭:

- trades: -4,632
- max_return_pct: +285.4439271331702
- max_drawdown_pct: -1.6951600088583655
- official_cd_value: +282.880288184129
- profit_factor: +0.1277097108584082
- max_conc: -20

## 핵심 장점

### 1. official_cd_value가 압도적으로 높다

short_max 기준은 official_cd_value 1위다. v5의 official_cd_value는 878.8531649564361로, 이전 short_max v4의 595.9728767723071을 크게 뛰어넘는다.

### 2. 수익률이 크게 높다

max_return_pct가 821.9869251730971이다. 이전 short_max v4의 536.5429980399269보다 약 285.44%p 높다.

### 3. MDD가 오히려 낮다

수익이 크게 증가했음에도 max_drawdown_pct는 4.6783483625391975로 이전 short_max v4의 6.373508371397563보다 낮다. short_max 기준인 MDD 10% 미만은 물론, short_main 기준인 5% 미만도 충족한다.

### 4. max_conc가 낮아졌다

이전 short_max v4 max_conc는 295였고, v5는 275다. 수익은 늘었지만 최대 동시 포지션 수는 줄었다.

### 5. RSI 직접 gate 제거가 유효 기회를 열었다

v5는 RSI를 직접 진입 필수 조건으로 쓰지 않는다. 대신 score 내부에서 RSI를 보조 점수로 사용한다. 이 구조가 지나치게 높은 RSI gate 때문에 누락되던 유효 숏 기회를 열어준 것으로 해석된다.

### 6. score 강화로 저품질 진입을 통제한다

RSI 직접 gate를 제거했지만 short_dev를 0.035로 강화하고 score_min_short를 2.35로 올렸다. 즉 진입 범위를 넓히면서도 품질 점수로 저품질 신호를 걸러낸다.

### 7. active_leftover가 없다

백테스트 종료 시 미청산 포지션이 남지 않는다. same-bar 처리와 포트폴리오 평가 구조가 정상적으로 작동한다.

## 핵심 약점

### 1. raw_trades_generated가 많다

raw_trades_generated가 61,818이다. 실제 체결 trades는 31,798이지만, 후보 생성량은 크다. 포트폴리오 평가 단계에서 많은 후보를 통제하는 구조이므로 실거래에서는 후보 밀집도 관리가 필요하다.

### 2. same_bar_trades가 많다

same_bar_trades가 4,559다. 특정 timestamp에서 빠르게 진입과 청산이 발생하는 거래가 많다. same-bar 처리 로직을 빼면 기준선이 깨질 수 있다.

### 3. RSI 직접 gate 제거는 구조적 변화다

RSI gate 제거는 단순 파라미터 조정이 아니라 진입 구조의 중요한 변화다. 이후 개발에서 RSI 직접 gate를 다시 켜면 다른 계열 전략이 된다.

### 4. 승률은 낮은 편이다

win_rate_pct는 14.585823007736334다. 이 전략은 높은 승률 전략이 아니라 낮은 승률 + 큰 RR + 다수 거래 + 포트폴리오 관리로 성과를 만든다.

### 5. dd_brake 의존성이 있다

dd_brake_trigger_pct 0.03, dd_brake_freeze_steps 5가 포트폴리오 평가 단계에서 작동한다. 이 조건의 위치를 잘못 옮기면 성과가 달라진다.

## 취약 구간

- 강한 상승 추세가 지속되는 구간
- 급등 후 상단 꼬리가 나왔지만 추가 급등이 계속되는 구간
- 여러 종목에서 동시에 과열 신호가 발생하는 구간
- same-bar 거래가 과도하게 몰리는 구간
- dd_brake가 자주 작동할 정도로 연속 손실이 발생하는 구간

## 해석

이 전략의 핵심은 RSI를 “필수 조건”에서 “보조 점수”로 바꾼 것이다.

이전 계열은 RSI가 특정 기준을 넘지 않으면 아예 진입하지 않았다. v5는 RSI가 높으면 score에 가산점을 주지만, RSI가 기준을 넘지 않아도 EMA20 대비 강한 이격과 상단 꼬리, 충분한 score가 있으면 진입한다.

이 구조는 숏 리버전에서 더 자연스럽다. 가격 과열과 윗꼬리가 강하게 나타난 경우 RSI가 약간 부족하더라도 유효한 숏 기회일 수 있기 때문이다.

## 다음 개선 방향

### 1. C05 주변값 검증

성과 개선폭이 매우 크므로 단일 피크인지 안정 구간인지 확인해야 한다.

탐색 범위:

- short_dev 0.0345~0.0360
- score_min_short 2.30~2.45
- short_wick_mult 1.2~1.4

### 2. score 내부 RSI weight 조정

RSI 직접 gate는 제거하되, score 내부 RSI 영향력은 조정할 수 있다.

탐색 범위:

- score_rsi_weight 0.6~1.0

### 3. same_bar_trades 관리

same_bar_trades가 많으므로 약한 필터로 timestamp 밀집도를 줄일 수 있는지 본다.

후보:

- close_pos 필터
- upper_atr 필터
- max_active_cap 260~280
- timestamp 신규 진입 cap

### 4. dd_brake 주변값 검증

현재 MDD는 낮지만 dd_brake가 핵심이다.

탐색 범위:

- dd_brake_trigger_pct 0.025~0.035
- dd_brake_freeze_steps 3~7

### 5. RR/time_reduce 주변값 검증

현재 rr_mult 5.75, time_reduce_bars 8이 강하다.

탐색 범위:

- rr_mult 5.65~5.85
- time_reduce_bars 7~9
- time_reduce_to_risk_frac 0.04~0.06

## 유지해야 할 규칙

- short_max v5를 부모 전략으로 유지한다.
- 완전히 새로운 진입식을 만들지 않는다.
- RSI 직접 gate 제거 상태를 유지한다.
- score 내부 RSI 요소는 유지한다.
- 진입은 next bar open이다.
- fee_per_side 0.0004를 유지한다.
- position_fraction 0.01을 유지한다.
- expected_tp >= 0.003을 유지한다.
- dd_brake는 포트폴리오 평가 단계에서만 작동시킨다.
- same-bar 즉시 청산을 유지한다.
- active_leftover 0을 유지한다.
