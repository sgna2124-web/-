RESEARCH 4-1 결과 읽는 순서

1. research4_1_robustness_ranking.csv
   - BTC / 전종목 MARKET_MOM factor
   - unit_beta / rolling_beta
   - 평균회귀와 지속 중 우세 방향 및 안정성
2. research4_1_summary.csv
   - 전체 이벤트 통계
3. research4_1_period_summary.csv
   - ALL / EX_2025Q4 / 2025Q4 / PRE_2025Q4 / 2026
4. research4_1_quarterly.csv
   - 분기별 안정성
5. research4_1_symbol_breadth.csv
   - 종목 확장성
6. research4_1_cluster_summary.csv
   - 같은 시각 이벤트 군집 크기별 성과
7. research4_1_market_shock_summary.csv
   - 시장 공통 충격 크기/방향별 성과
8. research4_1_factor_diagnostics.csv
   - factor 커버리지

기본 저장은 위 핵심 요약만 수행한다. --save-diagnostics 사용 시 raw summary/breadth/event-counts를 추가 저장한다.

주의
- 이 단계는 이벤트 방향 연구다.
- 동일 시각 상/하위 K 선택과 시장중립 포트폴리오는 Research 4-2 대상이다.
- robust_pass는 탐색 편의를 위한 엄격한 자동 기준이며 전략 승격을 뜻하지 않는다.
