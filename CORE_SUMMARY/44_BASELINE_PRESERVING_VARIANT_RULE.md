기준선 보존형 변형 규칙

작성 배경
사용자는 완전히 새로운 전략 조합을 원하는 것이 아니라, 현재 성과가 검증된 4개 기준선 전략의 수익을 극대화하고 MDD를 최소화하는 개선을 원한다. 따라서 개선안은 기준선의 기본 틀, 진입 구조, 포지션 발생 규모, 거래 데이터량을 크게 벗어나면 안 된다.

핵심 정의
기준선 보존형 변형은 기존 1위 기준선 전략의 로컬 개선이다.
완전히 새로운 전략 탐색이 아니다.

기준선 보존형 변형의 조건
1. 기준선 조건, base_spec, BASELINES, entry/exit 엔진, parent gate는 수정하지 않는다.
2. 개선안은 반드시 base_spec(axis)에서 파생한다.
3. 기준선의 진입 구조를 넓히는 OR 조건, 대체 진입 조건, 신규 독립 진입 조건을 추가하지 않는다.
4. entry를 수정해야 한다면 parent baseline entry를 먼저 통과한 뒤 AND 조건으로만 제한한다.
5. 진입 조건을 느슨하게 풀어 기준선보다 훨씬 많은 거래를 만들지 않는다.
6. 기본 개선은 exit, hold, rr, trail, cooldown, post-loss, risk brake 같은 사후 관리 또는 약한 파라미터 조정부터 한다.
7. 수익 극대화와 MDD 최소화는 기준선의 거래 집합을 크게 흔들지 않는 범위에서 수행한다.
8. 캔들 제한은 사용하지 않는다. 기준선과 같은 전체 데이터 환경에서 비교한다.
9. 시간 조절은 캔들 수가 아니라 후보 수와 축 선택으로 한다.
10. TP 기대값 0.3% 이상 조건은 신규 개선안에 적용하되, 이 조건과 다른 강한 진입 필터를 동시에 결합해 trade starvation을 만들지 않는다.

기준선별 현재 거래 규모
long_main 기준선 6V2_L01_doubleflush_core
- trades: 592
- max_return_pct: 23.919060
- max_drawdown_pct: 1.751183

long_max 기준선 8V4_V51_V002_core_rare22_c1
- trades: 2276
- max_return_pct: 44.266371
- max_drawdown_pct: 6.758722

short_main 기준선 short_beh_dd_brake
- trades: 28017
- max_return_pct: 311.812150
- max_drawdown_pct: 4.758886

short_max 기준선 short_only_reference_1x
- trades: 36505
- max_return_pct: 394.614496
- max_drawdown_pct: 7.779240

거래량 보존 가드레일
기준선 보존형 개선안은 parent_trade_ratio를 반드시 확인한다.

공식 비교 후보 권장 범위
- long_main: 0.50 ~ 1.20
- long_max: 0.50 ~ 1.20
- short_main: 0.60 ~ 1.10
- short_max: 0.60 ~ 1.10

탐색 후보 허용 범위
- long_main: 0.35 ~ 1.40
- long_max: 0.35 ~ 1.35
- short_main: 0.40 ~ 1.20
- short_max: 0.40 ~ 1.20

무효 판정
1. parent_trade_ratio가 너무 낮으면 trade starvation으로 본다.
2. parent_trade_ratio가 너무 높으면 baseline-preserving variant가 아니라 new strategy drift로 본다.
3. short_main, short_max처럼 기준선 거래량이 큰 축은 거래량 증가를 매우 엄격히 제한한다.
4. 기준선보다 거래가 과도하게 많아져 실행 시간이 폭증하면 개선안이 아니라 기준선 이탈로 본다.

시간 예산과의 관계
시간이 오래 걸리는 가장 큰 원인은 조건이 느슨해져 entry 후보와 trade_rows가 폭증하는 것이다.
따라서 1시간 예산을 맞출 때는 캔들 제한이 아니라 기준선 대비 거래량 비율을 통제한다.
기준선의 포지션 규모를 유지하면 시간 예측도 안정된다.

다음 코드 작성 규칙
1. 개선안은 기준선의 로컬 변형만 만든다.
2. 신규 독립 진입 조합을 만들지 않는다.
3. 한 후보에서 여러 진입 필터를 동시에 바꾸지 않는다.
4. 가장 먼저 exit-only, rr-only, hold-only, trail-only, cooldown-only, postloss-only 변형을 우선한다.
5. entry를 건드리는 경우 기준선 entry의 부분집합이 되도록 AND 제한만 허용한다.
6. 후보별 예상 parent_trade_ratio를 사전 또는 사후로 기록한다.
7. 결과 분석 시 수익률과 MDD뿐 아니라 parent_trade_ratio를 동급 핵심 지표로 본다.
