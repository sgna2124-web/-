# LONG_MAIN_RESEARCH_LOG_2026_05_26_CROSS_SECTIONAL_STATE_TRANSITION_V9

## 목적
롱 메인 새 원류 전략 탐색 9차 결과를 기록한다.
다음 대화창에서 동일한 Cross-Sectional State Transition 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
8차까지 다음 축이 제거 또는 보류되었다.

- 강한 움직임 지속
- 눌림 후 회복
- 돌파 후 추종
- 돌파 실패 후 회복
- 조용한 축적 / 저변동 drift
- 개별 종목 내부 segment filter + 단순 long entry
- cross-sectional relative safety: 약한 단서만 있음, MDD 과다로 즉시 개선 우선순위 낮음
- cross-sectional oversold reversal: 실패

따라서 9차에서는 정적 상태가 아니라 상태 변화량을 보는 방식으로 전환했다.

## 9차 시도
파일:
run_long_cross_sectional_state_transition_v9_1h.py

결과 폴더:
local_results/long_main/LONG_CROSS_SECTIONAL_STATE_TRANSITION_V9_1H

탐색 family:
- Breadth Recovery Transition
- Median Return Recovery Transition
- Individual Rank Improvement Transition
- Dispersion / Volume Participation Transition

핵심 가설:
좋은 상태를 사는 것이 아니라, 시장 내부 구조가 나쁜 상태 또는 중립 상태에서 좋아지기 시작하는 전환 순간에 long edge가 있을 수 있다.

조건 방향:
- market breadth20 / breadth60 변화량
- market median ret20 / ret60 변화량
- market dispersion 변화량
- volume participation 변화량
- symbol cross-sectional rank 개선량
- 절대 과열 구간 배제
- ret1 / close_pos 기반 단순 반등 확인
- 짧은 stop
- 짧은 hold

## 결과
master_summary 기준:
- 후보 54개
- rows 54
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
v9는 현재 상태 자체가 아니라 상태가 개선되는 변화량을 중심으로 설계했다.
그럼에도 유효 후보가 없었다.

따라서 다음 구조는 현재 형태로 반복하지 말 것.

- breadth 개선 전환 단독
- median return 회복 전환 단독
- 개별 cross-sectional rank 개선 단독
- dispersion 안정화 + volume participation 회복 단독
- timestamp 직전 상태 대비 1-step improvement만으로 long 진입

## 현재까지 제거된 long side 중심축
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift
6. 개별 종목 내부 segment filter + 단순 long entry
7. cross-sectional oversold reversal
8. cross-sectional state transition

## 살아남은 단서
v7 cross-sectional relative safety에서만 약한 TOP_ANY_MDD 후보가 있었다.
다만 MDD가 높아 바로 압축하기보다는 다른 구조 탐색 후 조합 후보로 보류한다.

## 다음 방향 후보
다음은 단순 상태, 평균회귀, 전환이 아니라 시장 내부의 분리와 재동조화 구조를 보는 것이 적합하다.

다음 후보:
Cross-Sectional Decoupling / Recoupling Long

핵심 가설:
전체 시장과 특정 종목군이 일시적으로 분리된 뒤 다시 동조화되는 순간에 long edge가 있을 수 있다.

탐색 아이디어:
- 시장 median은 중립 또는 개선
- 특정 종목은 market median 대비 과도하게 이탈
- 단순 oversold가 아니라 market beta/동조화 회복 확인
- 종목 rank 자체보다 market-relative residual 변화 확인
- decoupling 후 recoupling confirmation

주의:
다음 방향은 v8 oversold reversal과 다르다.
v8은 단순 하위권 평균회귀였고, 다음은 market-relative residual과 재동조화 구조를 봐야 한다.
