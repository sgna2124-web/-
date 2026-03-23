# 04_RESEARCH_TIMELINE

큰 흐름 요약

1단계: 차트형/추세형/구조형 전략
- 추세추종, 구조 기반, 패턴 기반, fractal pullback 등 다수 시도
- 결과: 과적합 또는 EV 부족으로 실패

2단계: Casino Probability Engine
- 상태 -> 확률 -> EV 구조
- 초기 feature: ATR percentile, momentum, wick skew
- 결과: 상태 공간이 너무 거칠고 신뢰도 부족, EV 음수

3단계: 세션/시간/변동성 접근
- 결론: 방향 엣지보다 변동성 설명력만 약간 존재
- 하지만 결국 압축폭발/구조 해석 루프로 되돌아감
- 사용자 입장에서 의미 없는 반복으로 판단

4단계: 이벤트 스캐너 v1/v2
- 사람이 정의한 이벤트를 대량 스캔
- 메이저/마이너 모두 durable edge 부재
- strict 후보 대부분 0

5단계: Threshold Scanner
- 연속형 피처 임계값 조합 탐색
- 마이너 알트 쪽 약한 단서 잠깐 존재
- 전략화 후 전체 유니버스에서 재현 실패

6단계: Minor Washout / Symbol Fit / Symbol State Washout
- 종목 분류 기준 잘못 잡음
- 상태 필터가 전체 시장에 퍼짐
- 시뮬/포지션 관리 문제까지 겹침
- 결과적으로 전략 카드로 폐기 수준

7단계: State Miner v1
- 가능한 많은 OHLCV 연속형 상태를 single/pair/triple로 광범위하게 스캔
- BTC 단독 strict survivors = 0
- 다른 단일 알트도 strict survivors = 0
- 전체 종목 결과는 프로젝트 종료/계속 여부를 판정할 중요한 실험으로 간주

8단계: Failed Displacement Reclaim 철학 제시
- 최근 수용 범위 이탈 후 빠른 reclaim을 역추세로 잡는 사건 중심 구조
- 사용자 반응은 상대적으로 좋았음('오호 나쁘지 않은데?')
- 그러나 20개 종목 테스트 기준 성능은 손실, 승률도 낮아 아직 실패 상태