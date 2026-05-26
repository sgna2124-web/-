# V43 TREND PULLBACK / RECLAIM LONG FAILURE

실험 배치:
- LONG_MAX_V24_2025_TREND_PULLBACK_ENGINE_DEV_V43_STANDALONE

핵심 철학:
- breakout chase를 버리고 상승 추세 내부 눌림 후 재상승 구조 탐색.
- trend continuation long의 변형 형태.

핵심 조건:
- EMA20 reclaim
- EMA50 reclaim
- pullback from recent high
- controlled drop then recovery
- red candle cluster then green reclaim
- shallow pullback inside strong trend
- high RR reclaim variants

실행 시간:
- 46 candidates
- 약 18.9분
- 매우 높은 runtime 효율.
- 향후 100~140 candidates 수준까지도 가능.

결과:
- 전체 1위는 기존 반등형 V38 reference.
- 신규 pullback/reclaim engine 전체 실패.

최고 신규 후보:
- V43_CONSERV_CP074_UW200_VR140
- final_return_pct: -33.79
- max_drawdown_pct: 33.96
- official_cd_value: 66.20

V42 대비 변화:
- breakout long 대비 MDD 일부 감소.
- 하지만 실전 수준과는 매우 거리가 큼.

핵심 실패 패턴:
1. 상승 추세 내부 pullback도 edge 부족.
2. reclaim 조건이 whipsaw를 충분히 제거하지 못함.
3. 5분봉 멀티심볼 구조에서 추세 지속성이 약함.
4. long continuation 구조 자체가 약할 가능성.

중요 결론:
- long은 breakout형도 실패.
- trend pullback continuation도 실패.
- 현재까지는 reversal/mean-reversion long이 압도적으로 우수.

다음 단계:
- long은 entry 철학 변경보다 exit 구조 개선 가능성이 더 높음.
- fail_fast, trailing, time_reduce, partial_exit 계열 우선 검토.
