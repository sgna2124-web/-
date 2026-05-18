# short_main v9 장단점

## 기준선

- strategy: `short_main_v9_wick120_dev03475_timeout215_actual_bar_engine`
- source_candidate: `SM23_D02_wick120_dev03475_timeout215`
- parent_strategy: `short_main_v8_wick125_actual_bar_engine`
- previous_baseline: `short_main/v8`
- baseline_version: `short_main/v9`

## 핵심 변경

v9은 v8 기준선에서 다음 3개 값을 변경한 버전이다.

- `short_wick_mult`: 1.25 -> 1.20
- `short_dev`: 0.035 -> 0.03475
- `timeout_bars`: 210 -> 215

이 변경은 v8보다 진입 조건을 약간 넓히고, timeout을 조금 늘려 수익 확장성과 유지 시간을 함께 조정한 조합이다.

## 공식 성과

- trades: 36,791
- wins: 5,171
- losses: 31,620
- win_rate_pct: 14.055067815498356
- final_return_pct: 1194.9206565723089
- max_return_pct: 1195.2759019740386
- max_drawdown_pct: 4.770262221769094
- official_cd_value: 1233.487844954492
- profit_factor: 1.5698636647889879
- max_conc: 287
- same_bar_trades: 3,354
- active_leftover: 0
- pending_leftover: 0

## v8 대비 개선

- official_cd_value: 1198.1725532607445 -> 1233.487844954492
- delta_official_cd_value: +35.31529169374744
- max_return_pct: 1156.1081244457819 -> 1195.2759019740386
- delta_max_return_pct: +39.16777752825669
- trades: 35,803 -> 36,791
- delta_trades: +988

## 장점

1. short_main 기준 통과 후보 중 CD 1위

v2.3 조합 실험에서 MDD 5% 미만, 거래 수 20,000 이상, parent CD 초과, active/pending leftover 0 조건을 모두 통과한 후보 중 official_cd_value가 가장 높았다.

2. wick120 단독보다 개선

직전 유력 후보였던 `SM22_A01_wick120`보다 CD가 높고 MDD가 낮다. wick120 단독은 CD 1217.5998, MDD 4.8103이었고, v9 후보는 CD 1233.4878, MDD 4.7703이다.

3. v8 대비 확실한 수익 확장

max_return_pct가 +39.16777752825669%p 증가했다. CD도 +35.31529169374744 증가했다.

4. actual bar engine 유지

same timestamp 청산 자금 재사용 금지, pending entry, forced_end, 2025 train only 구조를 유지한다. 5분봉 실제 운용 시간 해석과 맞는다.

5. MDD 5% 미만 유지

MDD가 4.770262221769094%로 short_main 기준의 5% 방어선을 통과한다.

## 단점

1. v8 대비 MDD 상승

v8 MDD 4.612307655489422%에서 v9 MDD 4.770262221769094%로 +0.1579545662796722%p 증가했다.

2. profit factor 하락

v8 profit_factor 1.5763819188582828에서 v9 profit_factor 1.5698636647889879로 하락했다. 수익 총량은 늘었지만 평균적인 손익 효율은 약해졌다.

3. 동시 포지션 밀도 증가

max_conc가 285에서 287로 증가했다. 실거래에서 동시 포지션 수와 주문 처리량이 약간 늘어날 수 있다.

4. same-bar trades 증가

same_bar_trades가 3,246에서 3,354로 108개 증가했다. 진입 직후 같은 캔들에서 TP/SL에 닿는 거래가 늘었다.

5. 낮은 승률 구조 유지

win_rate가 14.055067815498356%다. 이 전략은 높은 RR과 큰 winner에 의존한다. 연속 손실 구간을 견딜 수 있어야 한다.

6. 2026 holdout 검증 전

이 기준선은 2025년까지 train 기준이다. 2026년 데이터는 검증용으로 남겨두었으므로, 실전 적용 전 별도 holdout 검증이 필요하다.

## 다음 개선 방향

1. 주변값 정밀 탐색

v9의 핵심 조합인 wick120 + dev03475 + timeout215 주변을 좁게 확인한다.

- short_wick_mult: 1.175 / 1.20 / 1.2125 / 1.225
- short_dev: 0.0345 / 0.03475 / 0.0350
- timeout_bars: 210 / 215 / 220

2. MDD 방어형 조합

v9은 수익 확장형이라 MDD가 v8보다 올랐다. 다음 개선은 CD를 유지하면서 MDD를 낮추는 방향이 좋다.

- wick120 + dev03475 + timeout215 + dd00285
- wick120 + dev03475 + timeout220
- wick12125 + dev03475 + timeout215

3. score2325 계열 주의

score2325를 섞으면 CD는 크게 올라가지만 MDD가 5%를 넘는 경향이 있다. short_main 기준선에는 신중히 써야 한다.

## 판정

short_main v9은 공격적 수익 확장형 기준선이다.

MDD가 v8보다 상승했지만 5% 미만을 유지하고, official_cd_value가 뚜렷하게 상승했으며, 기준선 재현 게이트가 통과된 actual bar engine 결과에서 나온 후보이므로 이후 short_main 개발은 v9을 기준으로 한다.
