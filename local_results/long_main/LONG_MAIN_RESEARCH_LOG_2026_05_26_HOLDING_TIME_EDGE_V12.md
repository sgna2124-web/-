# LONG_MAIN_RESEARCH_LOG_2026_05_26_HOLDING_TIME_EDGE_V12

## 목적
롱 메인 새 원류 전략 탐색 12차 결과를 기록한다.
다음 대화창에서 동일한 Holding-Time Edge / Early Path Filter 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
v8~v11에서 다음 축이 실패했다.

- v8 Cross-Sectional Oversold Reversal
- v9 Cross-Sectional State Transition
- v10 Cross-Sectional Decoupling / Recoupling
- v11 Intrabar Risk Shape / Stop-Take Interaction

따라서 v12에서는 진입 위치나 캔들 형태보다, 진입 후 초반 경로와 보유시간 적합성을 보는 축으로 이동했다.

## 12차 시도
파일:
run_long_holding_time_edge_v12_1h.py

결과 폴더:
local_results/long_main/LONG_HOLDING_TIME_EDGE_V12_1H

탐색 family:
- Early Adverse Cut
- Early Favorable Required
- Short Holding Window
- Confirmed Longer Holding

핵심 가설:
같은 진입 조건이라도 진입 후 초반 N봉의 손익 경로가 유리한 시간창이 있을 수 있다.
초기 역행이 빠르게 발생하는 경우를 early fail exit로 제거하면 long edge가 개선될 수 있다.

조건 방향:
- 단순 회복형 진입
- 진입 시 고정 SL/TP 설정
- trailing stop 없음
- break-even 없음
- dynamic TP 없음
- early adverse excursion 발생 시 시장가 종료로 간주
- early favorable excursion 요구형도 테스트
- 짧은 hold window와 긴 hold confirmation 모두 테스트

## 결과
master_summary 기준:
- 후보 48개
- rows 48
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
v12는 기존의 진입 조건 탐색이 아니라, 진입 후 초반 경로와 보유시간을 중심으로 설계했다.
그러나 현재 조건에서는 유효 후보가 전혀 나오지 않았다.

따라서 다음 구조는 현재 형태로 반복하지 않는다.

- early adverse cut 단독
- early favorable required 단독
- short holding window 단독
- confirmed longer holding 단독
- 단순 회복형 진입 + early fail exit 조합
- fixed SL/TP 유지 + 초반 N봉 경로 필터만으로 long edge 탐색

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

## 살아남은 단서
v7 cross-sectional relative safety에서만 약한 TOP_ANY_MDD 후보가 있었지만, MDD가 높아 신규 기준선 후보로는 약하다.
현재 단계에서는 계속 새로운 정보축 탐색을 우선한다.

## 다음 방향 후보
다음은 entry 자체, cross-sectional, 캔들 shape, post-entry early path가 아니라 microcycle 구조를 보는 것이 적합하다.

다음 후보:
Event Compression / Expansion Microcycle Long

핵심 가설:
단순 저변동 drift를 사는 것이 아니라, 압축 상태가 해제되는 순간의 확장 초입에는 long edge가 있을 수 있다.

탐색 아이디어:
- 직전 N봉 range/ATR 압축
- volume contraction 후 expansion
- close position 개선
- 첫 확장봉 진입 또는 확장 직후 1봉 확인 진입
- 기존 quiet accumulation과 다르게 '압축 상태 자체'가 아니라 '압축 해제 이벤트'를 본다.

주의:
다음 방향은 v5 quiet drift와 다르다.
quiet drift는 조용한 상태를 매수하는 구조였고, 다음은 compression release event를 매수하는 구조다.
