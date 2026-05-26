SHORT_MAX v13 stop230 temporal diagnostic v1

목적:
smv13_structdev1_24_dev1_24_stop230_rr540의 성과가 백테스트 기간 전반에 걸친 꾸준한 신호인지, 특정 특수 구간에 집중된 결과인지 확인한다.

기본 실행:
python run_short_max_v13_stop230_temporal_diagnostic_v1.py --data-dir "C:\Users\user\Desktop\LCD\파이썬\코인\Data\time"

기준선 v13과 함께 비교:
python run_short_max_v13_stop230_temporal_diagnostic_v1.py --data-dir "C:\Users\user\Desktop\LCD\파이썬\코인\Data\time" --include-baseline

확인 파일:
- summary_compact.csv: 전체 성과 요약
- monthly_breakdown.csv: 월별 거래수, 손익, 승률, PF, 청산사유
- quarterly_breakdown.csv: 분기별 분해
- yearly_breakdown.csv: 연도별 분해
- concentration_report.csv: 상위 1/3/6개월 손익 의존도와 양수월 비율
- equity_month_end.csv: 월말 equity와 drawdown
- trade_detail.csv: 거래별 상세 기록

판정 기준:
- positive_month_ratio_pct가 높고 top3_month_share_pct가 낮으면 꾸준한 신호에 가깝다.
- top1/top3 month share가 과도하게 높거나 특정 연도만 대부분의 수익을 만들면 특수 구간 의존도가 높다.
- yearly_breakdown에서 여러 연도에 걸쳐 양호하면 구조적 신호로 볼 수 있다.
