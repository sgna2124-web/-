# V42 TREND ACCEL / BREAKOUT LONG FAILURE

실험 배치:
- LONG_MAX_V23_2025_TREND_ACCEL_ENGINE_DEV_V42_FIXED_STANDALONE

핵심 철학:
- 기존 반등형 long_max를 버리고 상승 추세 지속형 long 엔진 탐색.
- short_max 계열의 momentum continuation 철학을 long에 이식 시도.

핵심 조건:
- EMA20/EMA50 이격
- EMA20 slope
- RSI momentum
- breakout20
- ret3_up / ret6_up acceleration
- volume expansion
- close position strength
- upper wick suppression

실행 시간:
- 16 candidates
- 약 13.4분
- runtime 효율은 매우 우수.

결과:
- 전체 1위는 기존 반등형 V38 reference.
- 신규 trend engine은 모두 실패.
- 일부 breakout 계열은 계좌 붕괴 수준 MDD 발생.

최고 신규 후보:
- V42_ACC03_RET3_024_RET6_036
- final_return_pct: -37.93
- max_drawdown_pct: 41.17
- official_cd_value: 61.46

핵심 실패 패턴:
1. 거래 수 과다.
2. 승률 붕괴.
3. breakout chase가 5분봉 전체 심볼 구조에서 지나치게 노이즈 민감.
4. long은 short처럼 continuation edge가 강하지 않음.
5. 상승 추세 추종이 오히려 whipsaw 증가.

중요 결론:
- long 시장 구조는 short와 비대칭적일 가능성이 큼.
- short momentum continuation 철학을 단순 long화하면 실패 가능성 높음.
- long은 여전히 mean reversion 성향이 강함.

다음 단계:
- breakout continuation long은 우선순위 하락.
- long 개선은 entry보다 exit 구조 쪽 가능성 높음.
