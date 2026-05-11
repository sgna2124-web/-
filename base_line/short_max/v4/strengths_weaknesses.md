# short_max v4 장단점

## 전략명

short_max_v4_combo_rsi755_timeout280

## 공식 성과

- trades: 36,430
- wins: 4,862
- losses: 31,568
- win_rate_pct: 13.34614328849849
- final_return_pct: 535.5572171675869
- max_return_pct: 536.5429980399269
- max_drawdown_pct: 6.373508371397563
- official_cd_value: 595.9728767723071
- profit_factor: 1.4501345502446736
- max_conc: 295
- max_conc_unique_symbols: 295
- same_bar_trades: 3,705
- generated_trades_before_score_filter: 39,446
- active_leftover: 0
- errors: 0

## v3 대비 개선점

short_max v3 기준선:

- trades: 34,782
- win_rate_pct: 14.070496233684091
- final_return_pct: 451.45526435735064
- max_return_pct: 451.8246548170149
- max_drawdown_pct: 7.484506060174601
- official_cd_value: 510.52330508569787
- profit_factor: 1.4377856344586135
- max_conc: 292

short_max v4 개선폭:

- trades: +1,648
- win_rate_pct: -0.724352945185601
- final_return_pct: +84.10195281023626
- max_return_pct: +84.718343222912
- max_drawdown_pct: -1.110997688777038
- official_cd_value: +85.44957168660923
- profit_factor: +0.0123489157860601
- max_conc: +3

## 장점

### 1. 수익과 MDD가 동시에 개선되었다

v4는 v3 대비 max_return_pct가 약 84.72%p 증가했고, max_drawdown_pct는 약 1.11%p 낮아졌다. 공격성과 안정성이 동시에 좋아진 결과다.

### 2. official_cd_value 개선폭이 크다

official_cd_value가 510.52330508569787에서 595.9728767723071로 상승했다. 단순 미세 개선이 아니라 기준선 갱신급 개선이다.

### 3. 거래 수가 늘었지만 품질이 유지되었다

trades가 34,782에서 36,430으로 증가했다. RSI 조건을 75.5로 완화했기 때문에 진입 기회가 늘었지만, score_min_short 2.0을 포트폴리오 단계에서 유지하면서 신호 품질을 통제한다.

### 4. timeout 280이 큰 RR 구조에 잘 맞는다

short_max 계열은 RR 6.0 구조이기 때문에 목표가 도달까지 시간이 필요하다. v4는 timeout을 280으로 늘리면서 수익 기회를 더 확보했고, 동시에 MDD도 낮아졌다.

### 5. active_leftover가 없다

strict time-axis 평가에서 active_leftover 0을 유지했다. same-bar 즉시 청산 처리가 포함되어 실거래형 시뮬레이션 구조가 안정적이다.

### 6. 수수료와 자산 분할 조건을 지켰다

fee_per_side 0.0004, position_fraction 0.01 환경에서 나온 결과다. 즉 편도 수수료 0.04%, 현재 equity 1% 진입 기준이다.

## 단점

### 1. 승률은 낮아졌다

win_rate_pct는 v3의 14.0705%에서 v4의 13.3461%로 낮아졌다. 수익 개선은 승률 개선이 아니라 RR 구조, timeout 확대, 거래 수 증가에서 나온다.

### 2. 최대 동시 포지션 수가 증가했다

max_conc가 292에서 295로 증가했다. 큰 차이는 아니지만, 실거래에서는 동시 포지션 관리 부담이 약간 커진다.

### 3. RSI 조건 완화로 진입 범위가 넓어졌다

short_rsi_min을 76.0에서 75.5로 낮췄다. 이로 인해 과열성이 약한 일부 신호도 포함될 수 있다. score_min_short 2.0이 이를 통제하지만, 향후 개발에서는 과도한 완화를 주의해야 한다.

### 4. timeout 280은 긴 보유 리스크를 만든다

timeout이 240에서 280으로 늘었다. 목표가 도달 기회를 늘리는 장점이 있지만, 강한 상승 추세가 지속되는 환경에서는 불리한 포지션을 더 오래 끌고 갈 수 있다.

### 5. 숏 메인 기준선으로는 부적합하다

MDD가 6.3735%이므로 short_main의 MDD 5% 미만 기준에는 맞지 않는다. 이 전략은 short_max 기준선으로 사용해야 한다.

## 취약 구간

- 강한 상승 추세가 계속되는 구간
- 급등 후 상단 꼬리가 나왔지만 추가 급등이 이어지는 구간
- 여러 종목이 동시에 과열되어 max_conc가 높아지는 구간
- 시장 전체가 숏 리버전보다 모멘텀 지속 성격을 보이는 구간

## 다음 개선 방향

### 1. timeout 주변 탐색

v4의 핵심 개선축은 timeout 확대다. 다음 후보는 다음 구간을 우선 본다.

- timeout 260
- timeout 270
- timeout 280
- timeout 290
- timeout 300
- timeout 320

### 2. RSI 주변 탐색

RSI 75.5가 강하게 작동했다. 다음은 세밀한 주변값을 확인한다.

- short_rsi_min 75.0
- short_rsi_min 75.2
- short_rsi_min 75.5
- short_rsi_min 75.8
- short_rsi_min 76.0

### 3. short_dev 주변 탐색

EMA20 대비 이격 조건은 0.033을 유지하되 주변값을 탐색한다.

- short_dev 0.0328
- short_dev 0.0330
- short_dev 0.0332
- short_dev 0.0335

### 4. time_reduce 조정

MDD를 더 낮추기 위해 time_reduce를 조정한다.

- time_reduce_bars 8~12
- time_reduce_to_risk_frac 0.03~0.05

### 5. score_min_short 약한 강화

진입 수를 너무 줄이지 않는 선에서 score_min_short를 약하게 높인다.

- score_min_short 2.02
- score_min_short 2.05
- score_min_short 2.08

### 6. max_conc 완화 가드

max_conc 295를 줄이기 위해 약한 포트폴리오 가드를 테스트한다.

- max_active_cap 280~295
- timestamp 신규 진입 cap 220~280
- DD brake는 약하게만 사용

## 유지해야 할 규칙

- short_max v4를 부모 전략으로 유지한다.
- 완전히 새로운 진입식을 만들지 않는다.
- 진입 조건의 소폭 변형, 추가, 제거만 허용한다.
- score_min_short 적용 위치를 포트폴리오 평가 단계로 유지한다.
- same-bar 즉시 청산을 유지한다.
- MDD 10% 미만을 유지한다.
- active_leftover 0을 유지한다.
