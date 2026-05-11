# short_max v4 기준선

## 공식 기준선명

short_max_v4_combo_rsi755_timeout280

## 승격 후보

이 기준선은 short_max v3 기준선 `short_max_v3_combo_dev033_timeout240`을 부모로 한 개발 결과에서 1위를 기록한 `combo_rsi755_timeout280` 후보를 새 short_max 기준선으로 승격한 것이다.

## 개발 방식

완전히 새로운 전략이 아니다. short_max v3의 과열 숏 리버전 구조를 유지한 상태에서 다음 두 가지만 변경했다.

1. short_rsi_min: 76.0 → 75.5
2. timeout_bars: 240 → 280

나머지 핵심 조건은 v3와 동일하다.

## 공식 테스트 환경

- 결과 폴더: `local_results/short_max/short_max_v3_dev_candidates_v1_results`
- 선택 후보: `combo_rsi755_timeout280`
- CSV 파일 수: 597
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- side: short only
- entry: next bar open
- score 적용 위치: 포트폴리오 평가 단계
- same-bar 처리: entry_ts == exit_ts 거래는 같은 timestamp에서 즉시 청산
- active_leftover: 0
- errors: 0

## 공식 성과

- strategy: combo_rsi755_timeout280
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

## v3 대비 개선폭

short_max v3 기준선:

- trades: 34,782
- final_return_pct: 451.45526435735064
- max_return_pct: 451.8246548170149
- max_drawdown_pct: 7.484506060174601
- official_cd_value: 510.52330508569787
- profit_factor: 1.4377856344586135
- max_conc: 292

short_max v4 개선폭:

- trades: +1,648
- max_return_pct: +84.718343222912
- max_drawdown_pct: -1.110997688777038
- official_cd_value: +85.44957168660923
- profit_factor: +0.0123489157860601
- max_conc: +3

## 기준선 채택 이유

`combo_rsi755_timeout280`은 short_max v3보다 수익성과 안정성이 동시에 좋아졌다.

max_return_pct는 451.8246548170149에서 536.5429980399269로 크게 상승했고, max_drawdown_pct는 7.484506060174601에서 6.373508371397563으로 낮아졌다. official_cd_value 역시 510.52330508569787에서 595.9728767723071로 상승했다.

이는 단순히 수익만 늘어난 공격형 개선이 아니라 MDD까지 낮아진 품질 좋은 기준선 갱신이다.

## v4 핵심 해석

short_max v3는 `short_dev 0.033 + timeout 240` 구조였다. v4는 여기에 RSI 과열 조건을 76.0에서 75.5로 약하게 완화하고, timeout을 280으로 늘렸다.

즉 v4의 의미는 다음과 같다.

- EMA20 대비 과열 강도는 v3처럼 유지한다.
- RSI 조건은 0.5포인트 완화해 진입 기회를 늘린다.
- timeout을 280으로 늘려 큰 RR 구조가 작동할 시간을 더 준다.
- score_min_short 2.0은 그대로 유지해 품질이 너무 낮은 신호는 포트폴리오 평가 단계에서 배제한다.

## 다음 개발 기준

앞으로 short_max 개발은 이 v4 기준선을 부모 전략으로 사용한다.

우선 개발 방향:

1. timeout 260~320 주변 구조 탐색
2. short_rsi_min 75.0~75.8 주변 구조 탐색
3. short_dev 0.0328~0.0335 주변 구조 탐색
4. time_reduce 8~12, time_reduce_to_risk_frac 0.03~0.05 결합
5. score_min_short 2.00~2.08 결합
6. max_conc 295를 낮추는 약한 포트폴리오 가드 검토

## 반드시 유지할 규칙

- 완전히 새로운 전략으로 바꾸지 않는다.
- short_max v4의 과열 숏 리버전 구조를 유지한다.
- score_min_short는 종목별 entry mask에 넣지 않는다.
- score_min_short는 포트폴리오 평가 단계에서 적용한다.
- same-bar 거래는 같은 timestamp에서 즉시 청산한다.
- 수수료는 fee_per_side 0.0004를 유지한다.
- 자산 분할 진입은 position_fraction 0.01을 유지한다.
- expected_tp는 최소 0.003 이상이어야 한다.
- active_leftover는 0이어야 한다.
