# LONG_MAIN_RESEARCH_LOG_2026_05_26_DECOUPLING_RECOUPLING_V10

## 목적
롱 메인 새 원류 전략 탐색 10차 결과를 기록한다.
다음 대화창에서 동일한 Cross-Sectional Decoupling / Recoupling 계열을 반복하지 않기 위한 append 로그다.

## 이전 배경
v8~v9에서 다음 cross-sectional 축이 실패했다.

- v8 Cross-Sectional Oversold Reversal
- v9 Cross-Sectional State Transition

v10에서는 단순 하위권 평균회귀나 시장 상태 개선이 아니라, 종목과 시장 median 간의 관계가 다시 연결되는 recoupling 구조를 테스트했다.

## 10차 시도
파일:
run_long_cross_sectional_decoupling_recoupling_v10_1h.py

결과 폴더:
local_results/long_main/LONG_CROSS_SECTIONAL_DECOUPLING_RECOUPLING_V10_1H

탐색 family:
- Residual20 Recoupling
- Residual60 Recoupling
- Breadth-Supported Recoupling
- Mid-Rank Recoupling

핵심 가설:
시장 median 대비 종목이 일시적으로 약하게 이탈한 뒤, 다시 시장 흐름과 동조화되는 순간에 long edge가 있을 수 있다.

조건 방향:
- market median ret1/ret5/ret20/ret60 계산
- symbol residual = symbol_ret - market_median_ret
- 이전 residual이 음수로 이탈
- 현재 residual 개선
- residual 변화량 양수
- rel_ret1/rel_ret5 확인
- 중간 rank 구간 또는 breadth support 구간
- 과도한 붕괴 및 과열 제외

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
v10은 v8의 단순 oversold reversal, v9의 market state transition과 다른 구조였다.
그러나 market-relative residual recoupling 조건에서도 유효 후보가 없었다.

따라서 현재 형태의 decoupling / recoupling long 구조는 반복하지 않는다.

## v8~v10 종합 결론
v8~v10이 모두 실패했기 때문에 Cross-Sectional 기반 Long Alpha 탐색은 현재 long_main 신규 기준선 탐색 우선순위에서 크게 낮춘다.

세부 실패 축:
1. 하위권 평균회귀: 실패
2. 시장 상태 개선 전환: 실패
3. 시장 대비 residual 재동조화: 실패

즉 다음 대화창에서 다음 계열을 기본 아이디어로 반복하지 말 것.

- 상대강도 상위 매수
- 상대약도 평균회귀
- rank improvement 단독
- market breadth 개선 단독
- market median 회복 단독
- market-relative residual recoupling 단독
- cross-sectional rank 중심 long alpha

## 살아남은 단서
v7 relative_safety에서만 약한 TOP_ANY_MDD 후보가 있었다.
하지만 MDD가 높고 기대값이 강하지 않아, 바로 압축할 우선순위는 낮다.
나중에 다른 축에서 좋은 후보가 나온 뒤 보조 필터나 조합 재료로만 재검토한다.

## 다음 방향 후보
다음은 cross-sectional 축이 아니라 다른 정보 차원을 사용해야 한다.

후보:
1. Intrabar Risk Shape / Stop-Take Interaction
- 진입 조건보다 손절/익절이 잘 먹히는 캔들 구조 탐색
- high-low path proxy, wick asymmetry, ATR 대비 stop/take 거리 적합성

2. Holding-Time Edge
- 진입 직후 N봉의 위험/수익 구조가 유리한 시간창 탐색
- 같은 진입이라도 보유시간과 fail-exit 구조를 중심으로 탐색

3. Event Compression / Expansion Microcycle
- 직전 압축과 직후 확장 자체를 보는 구조
- 기존 quiet drift와 달리 압축 상태를 사는 것이 아니라 압축 해제 직전/직후의 risk shape를 본다.

주의:
다음 단계에서는 cross-sectional rank 중심 접근을 우선 배제한다.
