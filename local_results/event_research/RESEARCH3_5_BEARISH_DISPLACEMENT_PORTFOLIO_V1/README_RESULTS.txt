RESEARCH 3-5 결과 읽는 순서

1. research3_5_portfolio_summary.csv
   - BASE, Q4 제외, 2026 entry-only, 상위 종목/극단값 제거 결과
2. research3_5_portfolio_quarterly.csv
   - 분기별 수익률과 분기 내 MDD
3. research3_5_symbol_contribution.csv
   - BASE의 종목별 실제 자산 기여도
4. research3_5_daily_equity.csv
   - BASE / EX_2025Q4 / 2026_ENTRY_ONLY 일별 자산
5. research3_5_tail_thresholds.csv
   - 극단값 제거 기준과 상위 기여 종목
6. research3_5_runtime_summary.json

공식 조건
- 레버리지: 1.0
- 진입 비중: 1.0000%
- 수수료: 편도 0.0400%
- 슬리피지: 편도 1bp
- 진입: 신호 다음 봉 시가
- 청산: 72번째 봉 종가
- 손절/익절: 없음
- 종목별 동시 포지션: 1개
- 글로벌 포지션 상한: 없음
- MDD: 보유 중 매 봉 종가 MTM
- 최종 판정: TERMINATE_RESEARCH3_EVENT_BRANCH
