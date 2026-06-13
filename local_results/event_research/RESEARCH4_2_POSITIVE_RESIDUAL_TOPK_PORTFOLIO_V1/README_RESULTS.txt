RESEARCH 4-2 결과 읽는 순서

1. research4_2_portfolio_ranking.csv
   - BASE 기준 공식 순위. robust_pass 후보를 먼저 본다.
2. research4_2_portfolio_summary.csv
   - BASE / EX_2025Q4 / PRE_2025Q4 / ONLY_2025Q4 / 2026_ENTRY_ONLY 전체 시나리오.
3. research4_2_portfolio_quarterly.csv
   - 분기별 수익률과 분기 내 MDD.
4. research4_2_scenario_selection_counts.csv
   - Top-K, cap, 기간 필터별 선택 전후 거래 수.
5. research4_2_symbol_contribution.csv
   - 주력 robust 또는 최상위 BASE 시나리오의 종목별 기여도.
6. research4_2_daily_equity.csv
   - 주요 시나리오 일별 자산.
7. research4_2_runtime_summary.json

핵심 해석
- positive residual은 시장 대비 과열 종목이다.
- mean reversion 방향은 숏이다.
- Top-K는 동일 시각에서 z-score가 가장 높은 순서로 제한한다.
- cap=0은 글로벌 동시 포지션 제한 없음, cap20/cap50은 최대 동시 보유 제한이다.
- 기본 공식 후보는 MARKET_MOM / rolling_beta / z4 / 72봉이다.
