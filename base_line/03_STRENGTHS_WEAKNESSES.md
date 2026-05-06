기준선 전략 장단점 기록

작성 목적
기준선 전략을 개선할 때 단순히 수치만 보지 않고, 어떤 성질을 보존하고 어떤 약점을 보완해야 하는지 명확히 한다.

1. short_only_reference_1x
축: short_max
상태: 현재 데이터 597 CSV 기준 새 기준선 후보

현재 성과
trades: 36834
max_return_pct: 408.9954916988155
max_drawdown_pct: 7.395550425783604
official_cd_value: 471.3524734452645
win_rate: 0.1471466579790411
pf: 1.4013066651299806
max_conc: 294

장점
1. 전체 기준선 중 절대 수익률과 official_cd_value가 가장 강한 축이다.
2. MDD가 10% 미만이며, max_return 대비 drawdown 효율이 높다.
3. 거래 수가 많아 단일 종목 또는 소수 이벤트 의존도가 낮다.
4. score_min_short 2.0으로 너무 과도하게 진입을 줄이지 않아 수익 기회를 많이 포착한다.
5. rr 6.0 구조로 승률은 낮지만 손익비 기반 수익 곡선이 강하다.
6. position_fraction 1% 기준에서도 max_conc 294 수준을 감당하며 높은 성장률을 보였다.

약점
1. win_rate가 약 14.7%로 낮다. 연속 손실 구간에 취약할 수 있다.
2. max_conc가 294로 높아, 실제 체결 환경에서는 동시 포지션 관리와 거래소 제한 문제가 생길 수 있다.
3. 숏 전용 전략이므로 강한 상승장 지속 구간에서는 손실 연속 발생 가능성이 있다.
4. rr 6.0 구조라 목표가가 멀고, time_reduce와 timeout 경로의 품질이 성과에 중요하다.
5. dd_brake가 없기 때문에 포트폴리오 drawdown 급락 구간에서 신규 진입을 계속 허용한다.

개선 방향
1. short_max 축 개선은 수익 극대화보다 MDD와 max_conc 완화가 우선이다.
2. score_min_short를 소폭 높이거나, 과열 품질 필터를 추가하되 거래 수를 과도하게 줄이면 안 된다.
3. dd_brake 또는 loss streak guard를 약하게 추가하는 실험이 가능하다.
4. parent_trade_ratio가 0.7 미만으로 내려가면 short_max의 장점을 훼손한 것으로 본다.

2. short_beh_dd_brake
축: short_main
상태: 현재 데이터 597 CSV 기준 새 기준선 후보

현재 성과
trades: 28308
max_return_pct: 322.7577232826396
max_drawdown_pct: 4.4066222161057595
official_cd_value: 404.12838752816384
win_rate: 0.15257171117705243
pf: 1.441356672437088
max_conc: 286

장점
1. MDD가 5% 미만으로 공식 main 기준에 적합하다.
2. dd_brake 덕분에 short_only_reference_1x보다 drawdown 방어력이 좋다.
3. score_min_short 2.2, short_dev 0.033, short_rsi_min 77로 더 엄격한 숏 과열 진입만 선택한다.
4. 수익률 300% 이상과 MDD 5% 미만을 동시에 달성한 매우 강한 main 축이다.
5. short_max보다 수익률은 낮지만 risk-adjusted 기준으로 매우 안정적이다.

약점
1. 거래 수가 short_max보다 적어 일부 수익 기회를 포기한다.
2. dd_brake가 특정 구간에서 좋은 진입까지 막을 수 있다.
3. max_conc가 여전히 286으로 낮지는 않다.
4. win_rate가 약 15.3%로 낮아, 손익비 구조가 훼손되면 빠르게 약해질 수 있다.
5. score_min_short 2.2 조건 때문에 데이터 구간이 바뀌면 거래 수 민감도가 생길 수 있다.

개선 방향
1. short_main 축은 MDD 5% 미만을 절대 보존해야 한다.
2. 수익 극대화보다 drawdown 방어를 유지한 상태에서 max_return을 소폭 높이는 방향이 맞다.
3. dd_brake_freeze_steps, score_min_short, short_dev, short_rsi_min을 작은 단위로 조정하는 실험이 적합하다.
4. 거래 수가 2만 건 아래로 급감하면 main 축의 안정성이 훼손될 수 있다.

3. long_main: 6V2_L01_doubleflush_core
상태: 원본 복원 미완료

기존 장점
1. MDD가 매우 낮은 방어형 롱 기준선이다.
2. 거래 수가 592건으로 희소 진입형이며, 품질 중심 전략으로 보인다.
3. long_main 축의 기준선으로 MDD 5% 미만 조건을 만족한다.

기존 약점
1. 거래 수가 적어 데이터 구간 변화에 민감할 수 있다.
2. 수익률은 숏 기준선에 비해 낮다.
3. 현재 V40 clone 계열에서 거래 수가 13116건으로 폭증했기 때문에 원본 진입 조건 또는 엔진 복원이 아직 불안정하다.

개선 전 필수 조건
원본 복원 전에는 long_main 개선 금지.

4. long_max: 8V4_V51_V002_core_rare22_c1
상태: 원본 복원 미완료

기존 장점
1. long_main보다 수익률이 높고 거래 수가 많다.
2. rare22 조건을 사용한 롱 고수익 후보 축이다.
3. long_max 기준선으로 raw 개선 후보 비교에 사용된다.

기존 약점
1. MDD가 5%를 초과해 main 기준에는 부적합하다.
2. 현재 V40 clone 계열에서 거래 수가 433571건으로 폭증했기 때문에 원본 복원이 실패한 상태다.
3. 원본 엔진과 clone 엔진 차이를 분해하기 전에는 개선 결과를 신뢰할 수 없다.

개선 전 필수 조건
원본 복원 전에는 long_max 개선 금지.
