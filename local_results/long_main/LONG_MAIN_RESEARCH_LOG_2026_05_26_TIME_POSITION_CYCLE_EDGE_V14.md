# LONG_MAIN_RESEARCH_LOG_2026_05_26_TIME_POSITION_CYCLE_EDGE_V14

## 목적
롱 메인 새 원류 전략 탐색 14차 결과를 기록한다.
다음 대화창에서 동일한 Time-Position / Cycle Transition Edge 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
v8~v13에서 다음 축이 실패했다.

- v8 Cross-Sectional Oversold Reversal
- v9 Cross-Sectional State Transition
- v10 Cross-Sectional Decoupling / Recoupling
- v11 Intrabar Risk Shape / Stop-Take Interaction
- v12 Holding-Time Edge / Early Path Filter
- v13 Compression / Expansion Microcycle

따라서 v14에서는 가격 패턴, 상대비교, 캔들 shape, 보유 경로, 압축 해제 이벤트가 아니라 시간 위치와 내부 사이클 phase를 보는 축으로 이동했다.

## 14차 시도
파일:
run_long_time_position_cycle_edge_v14_1h.py

결과 폴더:
local_results/long_main/LONG_TIME_POSITION_CYCLE_EDGE_V14_1H

탐색 family:
- Modulo 24 Position Edge
- Volatility Cycle Phase
- Return Cycle Phase
- Modulo + Cycle Phase Combined

핵심 가설:
암호화폐는 24시간 시장이지만, bar_index modulo, volatility phase, return phase가 결합된 특정 시간 위치/주기 전환 구간에서 long edge가 있을 수 있다.

조건 방향:
- bar_index modulo 24 위치
- volatility phase window
- return phase window
- modulo + phase 결합
- 기본 회복형 가격 조건
- 고정 SL/TP
- 종목 간 cross-sectional rank 사용 안 함

## 결과
master_summary 기준:
- 후보 38개
- rows 38
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
v14는 단순 세션 필터가 아니라, 시간 위치와 내부 변동성/수익률 cycle phase를 결합한 구조였다.
그러나 현재 조건에서는 유효 후보가 전혀 나오지 않았다.

따라서 다음 구조는 현재 형태로 반복하지 않는다.

- modulo 24 position edge 단독
- volatility cycle phase 단독
- return cycle phase 단독
- modulo + cycle phase 결합 단독
- 단순 시간 위치 + 기본 회복형 long entry

## 현재까지 제거된 long side 중심축
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift
6. 개별 종목 내부 segment filter + 단순 long entry
7. cross-sectional oversold reversal
8. cross-sectional state transition
9. cross-sectional decoupling / recoupling
10. intrabar risk shape / stop-take interaction
11. holding-time edge / early path filter
12. compression / expansion microcycle
13. time-position / cycle transition edge

## 살아남은 단서
v7 cross-sectional relative safety에서만 약한 TOP_ANY_MDD 후보가 있었지만, MDD가 높아 신규 기준선 후보로는 약하다.
현재 단계에서는 단일 정보축 탐색만으로는 롱 메인 개선이 쉽지 않다는 신호가 강해지고 있다.

## 다음 방향 후보
다음은 단일 축 신규 전략보다 상태 이주(State Migration) 또는 다단계 구조를 보는 것이 적합하다.

후보:
State Migration / Multi-Stage Qualification Long

핵심 가설:
한 시점의 조건이 아니라, 최근 N봉 동안 상태가 나쁜 상태에서 중립으로, 중립에서 회복으로 이동하는 순서 자체에 edge가 있을 수 있다.

주의:
v9의 단순 state transition과 다르게, 다음은 1-step 변화량이 아니라 여러 상태 구간의 순서와 지속 시간을 본다.
예: 하락 과열 → 변동성 둔화 → 회복 시도 → 재하락 실패 → 진입.
