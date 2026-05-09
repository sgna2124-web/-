# short_main 기준선 장단점

전략명: short_beh_dd_brake
축: short_main
상태: 현재 597 CSV 기준 공식 short_main 기준선

1. 현재 성과

trades: 28308
final_return_pct: 322.48410704162137
max_return_pct: 322.7577232826396
max_drawdown_pct: 4.4066222161057595
official_cd_value: 404.12838752816384
win_rate: 0.15257171117705243
pf: 1.441356672437088
max_conc: 286
max_conc_unique_symbols: 286
same_bar_trades: 3357
active_leftover: 0

2. 장점

1. MDD가 5% 미만이다.
short_main의 가장 중요한 조건은 main 축답게 손실 억제력을 유지하는 것이다. short_beh_dd_brake는 max_drawdown_pct 4.4066%로 이 기준을 만족한다.

2. 수익률과 방어력이 동시에 강하다.
max_return_pct가 322.7577%이고 official_cd_value가 404.1284다. 단순 방어형이 아니라 수익성과 안정성을 동시에 가진 숏 메인 기준선이다.

3. dd_brake가 포트폴리오 급락 구간을 막아준다.
현재 drawdown이 -3% 이하로 내려가면 5 timestamp 동안 신규 진입을 멈춘다. 이 장치 때문에 short_max보다 수익률은 낮지만 MDD가 크게 낮아진다.

4. 진입 조건이 short_max보다 엄격하다.
short_dev 0.033, short_rsi_min 77, score_min_short 2.2를 사용해 과열 품질이 약한 진입을 줄인다.

5. 거래 수가 충분하다.
trades 28308로 main 기준에서 너무 희소하지 않다. 거래 수 20000 이상 조건을 만족하므로 데이터 구간 변화에 대한 기본 표본 수가 확보되어 있다.

6. 손익비 구조가 분명하다.
승률은 낮지만 rr_mult 6.0 구조로 큰 이익 거래가 누적 수익을 만든다. pf도 1.4413으로 기준선으로 사용할 만하다.

3. 약점

1. 승률이 낮다.
win_rate가 약 15.26%다. 손익비와 청산 구조가 조금만 훼손되어도 성과가 빠르게 약해질 수 있다.

2. max_conc가 낮지 않다.
max_conc 286은 실제 운용에서 동시 포지션 관리 부담이 있다. main 축이라도 동시 진입 압력이 완전히 낮은 것은 아니다.

3. dd_brake가 좋은 진입도 막을 수 있다.
dd_brake는 손실 확대를 줄이는 대신, 급락 직후의 좋은 숏 진입까지 막을 가능성이 있다.

4. short_max보다 수익 기회가 적다.
short_max는 trades 36834, short_main은 trades 28308이다. 방어력을 얻는 대신 약 8500건 이상의 기회를 포기한다.

5. score_min_short와 rsi 기준이 데이터 변화에 민감할 수 있다.
score_min_short 2.2, rsi 77은 과열 진입을 좁히는 조건이므로, 시장 regime이 바뀌면 거래 수와 성과가 흔들릴 수 있다.

4. 보존해야 할 성질

1. MDD 5% 미만
2. trades 20000 이상
3. active_leftover 0
4. next_bar_open 진입
5. fee_per_side 0.0004
6. position_fraction 0.01 복리 구조
7. dd_brake의 portfolio evaluation 단계 작동
8. 숏 과열 진입 구조

5. 개선 방향

1. 진입 조건을 크게 바꾸지 않는다.
short_main은 이미 진입 품질이 강하다. 완전히 새로운 조건을 만들기보다 부모 진입 조건을 유지하고 미세 조정해야 한다.

2. 청산과 위험관리 미세 조정이 우선이다.
최근 v1.4 테스트에서는 rr_mult 5.75 계열과 time_reduce 조정 계열이 좋은 후보로 나타났다. 따라서 rr, time_reduce, fail_fast, dd_brake 조합을 좁은 범위에서 검증하는 것이 우선이다.

3. MDD 방어형 후보를 별도로 관리한다.
SM31_tr8_frac003처럼 MDD 4% 미만을 노릴 수 있는 후보는 수익형과 분리해서 관리한다.

4. 승격 전에는 주변값 검증이 필요하다.
SM24_rr575가 좋은 후보였지만 단일 피크인지 안정 구간인지 확인해야 한다. RR 5.65~5.90, time_reduce_bars 8~14, risk_frac 0.03~0.08 범위를 추가 검증한 뒤 공식 승격한다.

6. 현재 승격 후보 기록

후보명: SM24_rr575
상태: v1.4 결과 기준 short_main 새 승격 후보
특징: 기준선보다 official_cd_value가 높고 MDD가 소폭 낮다.
판단: 즉시 공식 기준선으로 덮어쓰기보다 v1.5에서 주변값 검증 후 승격 여부를 결정한다.
