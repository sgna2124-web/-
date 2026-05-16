# short_main v8 장단점

## 기준선

- strategy: `short_main_v8_wick125_actual_bar_engine`
- source_candidate: `SM21_A05_wick125`
- parent_strategy: `short_main_v6_timeout210_actual_bar_engine`
- previous_baseline: `short_main/v7`
- baseline_version: `short_main/v8`

## 핵심 변경

v8은 v7 기준선에서 `short_wick_mult`만 1.30에서 1.25로 완화한 버전이다.

이 변경은 윗꼬리 조건을 약간 넓혀서, 기존 v7이 놓치던 약한 rejection candle까지 일부 포함한다.

## 공식 성과

- trades: 35,803
- wins: 5,070
- losses: 30,733
- win_rate_pct: 14.16082451191241
- final_return_pct: 1155.7636213036806
- max_return_pct: 1156.1081244457819
- max_drawdown_pct: 4.612307655489422
- official_cd_value: 1198.1725532607445
- profit_factor: 1.5763819188582828
- max_conc: 285
- same_bar_trades: 3,246
- active_leftover: 0
- pending_leftover: 0

## v7 대비 개선

- official_cd_value: 1159.0202763344078 -> 1198.1725532607445
- delta_official_cd_value: +39.152276926336754
- max_return_pct: 1115.0033786152128 -> 1156.1081244457819
- delta_max_return_pct: +41.10474583056907
- trades: 35,330 -> 35,803
- delta_trades: +473
- profit_factor: 1.5743323511471792 -> 1.5763819188582828

## 장점

1. 기준선 재현 성공 상태에서 승격된 후보

v8 후보는 `SHORT_MAIN_V7_ACTUALBAR_DEV_V2_1_FROZEN_ENGINE` 결과에서 기준선 재현 게이트가 true인 상태로 검증되었다. 따라서 이전 v2.0처럼 엔진 재현 실패 상태에서 나온 착시 결과가 아니다.

2. 작은 조건 변경으로 성과 개선

진입 조건 중 `short_wick_mult`만 1.30에서 1.25로 낮췄다. 전략의 성격은 유지하면서 거래 수와 수익성을 늘린 개발형 개선이다.

3. MDD 5% 미만 유지

MDD가 4.612307655489422%로 short_main 기준의 5% 방어선을 유지한다.

4. CD 개선 폭이 큼

v7 대비 official_cd_value가 +39.152276926336754 상승했다. 단순 소폭 개선이 아니라 기준선 갱신 가치가 있는 개선폭이다.

5. profit factor도 소폭 개선

거래 수가 늘었는데 profit_factor도 1.5743에서 1.5764로 상승했다. 단순히 진입을 많이 늘려 수익만 커진 것이 아니라 평균 손익 구조도 약간 개선되었다.

6. actual bar engine 유지

same timestamp 청산 자금 재사용 금지, pending entry, forced_end, 2025 train only 구조를 유지한다. 5분봉 실제 운용 시간 해석과 맞는다.

## 단점

1. MDD가 소폭 증가

v7 MDD 4.607649926423363%에서 v8 MDD 4.612307655489422%로 +0.004657729066058991%p 증가했다. 매우 작지만 방어력 개선형 후보는 아니다.

2. 동시 포지션 밀도 증가

max_conc가 284에서 285로 1 증가했다. 실거래에서 동시 포지션 수나 주문 처리량이 약간 늘어날 수 있다.

3. same-bar trades 증가

same_bar_trades가 3,187에서 3,246으로 59개 증가했다. 진입 직후 같은 캔들에서 TP/SL에 닿는 거래가 늘어났다는 뜻이다.

4. 낮은 승률 구조 유지

win_rate가 14.16082451191241%다. 이 전략은 높은 RR과 큰 winner에 의존한다. 심리적으로는 연속 손실 구간을 견뎌야 한다.

5. 2026 holdout 검증 전

이 기준선은 2025년까지 train 기준이다. 2026년 데이터는 검증용으로 남겨두었으므로, 실전 적용 전 별도 holdout 검증이 필요하다.

## 다음 개선 방향

1. wick 주변값 정밀 탐색

v8은 wick 1.25가 좋아진 결과다. 다음 개선은 아래 주변값을 좁게 확인하는 것이 적절하다.

- short_wick_mult 1.20
- short_wick_mult 1.225
- short_wick_mult 1.25
- short_wick_mult 1.275
- short_wick_mult 1.30

2. wick125 + dev03475 조합

동일 결과에서 `SM21_A03_dev03475`도 v7 대비 개선되었다. 따라서 v8 기준으로 아래 조합을 확인할 가치가 있다.

- short_wick_mult 1.25 + short_dev 0.03475
- short_wick_mult 1.25 + short_dev 0.03525

3. 방어형 보정

v8은 수익 확장형이다. MDD와 same-bar 증가를 줄이려면 아래 조합을 확인한다.

- wick125 + dd_brake_trigger_pct 0.0275
- wick125 + timeout_bars 215
- wick125 + score_min_short 2.375

## 판정

short_main v8은 공격적이지만 기준선으로 승격 가능한 개선이다.

MDD가 5% 미만을 유지하고, official_cd_value가 뚜렷하게 상승했으며, 기준선 재현 게이트가 통과된 frozen actual bar engine 결과에서 나온 후보이므로 이후 short_main 개발은 v8을 기준으로 한다.
