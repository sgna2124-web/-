# LONG_MAIN_RESEARCH_LOG_2026_05_26_CROSS_SECTIONAL_OVERSOLD_REVERSAL_V8

## 목적
롱 메인 새 원류 전략 탐색 8차 결과를 기록한다.
다음 대화창에서 동일한 Cross-Sectional Oversold Reversal 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
7차 Cross-Sectional Relative Safety에서는 TOP_ANY_MDD 후보가 일부 나왔지만, 최고 후보도 MDD가 약 29.9%로 높았다.
따라서 relative_safety 축을 바로 MDD 압축하는 것보다 다른 cross-sectional 축을 탐색하는 것이 낫다고 판단했다.

## 8차 시도
파일:
run_long_cross_sectional_oversold_reversal_v8_1h.py

결과 폴더:
local_results/LONG_CROSS_SECTIONAL_OVERSOLD_REVERSAL_V8_1H

주의:
이번 결과는 사용자가 업로드할 때 local_results/long_main 아래가 아니라 local_results 바로 아래에 업로드되었다.
향후 롱 메인 결과는 반드시 local_results/long_main 아래에 업로드해야 한다.

탐색 family:
- Cross-Sectional Short-Term Oversold Reversal
- Cross-Sectional Drawdown Reversal
- Cross-Sectional Oversold Safe Vol Reversal
- Breadth-Gated Oversold Reversal

핵심 가설:
시장 전체가 완전 붕괴하지 않은 상태에서, 같은 timestamp 기준 특정 종목만 과도하게 밀리고 단기 반등 confirmation이 나오면 평균회귀 long edge가 있을 수 있다.

조건 방향:
- timestamp 기준 ret5/ret20/ret60 하위권
- timestamp 기준 dd20/dd60 하위권
- market breadth 최소 유지
- market median return이 과도하게 나쁘지 않은 구간
- 장기 완전 붕괴 종목 제외
- 변동성 및 range 안전 필터
- close_pos 회복 또는 ret1 반등 확인
- 짧은 stop
- 짧은 hold
- 거래수 제한

## 결과
master_summary 기준:
- 후보 63개
- rows 63
- errors 0
- TOP_MDD_LT5 없음
- TOP_ANY_MDD 없음
- BEST_BY_FAMILY 없음

판정:
실패.

## 해석
이번 8차는 relative strength / relative safety 계열과 달리 평균회귀 축을 탐색했다.
그러나 현재 조건에서는 유효 후보가 전혀 나오지 않았다.

따라서 같은 timestamp 기준 과도하게 밀린 종목의 단기 반등을 노리는 단순 cross-sectional oversold reversal 구조는 현재 형태로 edge가 확인되지 않았다.

현재까지 제거된 long side 중심축:
1. 강한 움직임 지속
2. 눌림 후 회복
3. 돌파 후 추종
4. 돌파 실패 후 회복
5. 조용한 축적 / 저변동 drift
6. 개별 종목 내부 segment filter + 단순 long entry
7. cross-sectional relative safety는 약한 단서만 있음, 즉시 개선 우선순위 낮음
8. cross-sectional oversold reversal 단독 구조 실패

## 반복 금지
다음 구조는 그대로 반복하지 말 것.

- market breadth 유지 + cross-sectional ret 하위권 평균회귀 단독
- ret5/ret20/ret60 하위권 + close_pos 회복 단독
- dd20/dd60 하위권 + 짧은 hold 평균회귀 단독
- oversold safe volatility 조합 단독
- breadth-gated oversold reversal 단독

## 살아남은 단서
v8은 실패했지만 v7 relative_safety에서는 약한 TOP_ANY_MDD 후보가 있었다.
따라서 cross-sectional이라는 큰 방향 자체는 완전 폐기하지 않는다.
다만 단순 평균회귀보다는 relative_safety 또는 다른 cross-sectional 구조가 더 유망할 수 있다.

## 다음 방향 후보
다음은 단순 oversold reversal이 아니라 다음 중 하나로 이동하는 것이 적합하다.

1. Cross-sectional pair bucket 방식
- 같은 timestamp에서 상위 강도군과 하위 약세군을 분리
- 하위군을 사는 것이 아니라 하위군이 더 이상 악화되지 않는 시점만 포착

2. Market regime first 방식
- 개별 종목 선택보다 먼저 전체 시장이 long 가능한 구간인지 판정
- 이후 매우 제한된 entry만 허용

3. Relative safety 재검토는 보류
- v7에서 단서가 있었지만 MDD가 너무 높음
- 바로 MDD 압축보다 다른 축을 더 탐색한 뒤 조합 후보로 재검토

## 다음 대화창용 요약
v8 Cross-Sectional Oversold Reversal은 실패했다.
결과는 local_results/LONG_CROSS_SECTIONAL_OVERSOLD_REVERSAL_V8_1H에 업로드되었고, long_main 하위가 아니었으므로 주의한다.
이 축은 현재 형태로 반복하지 않는다.
