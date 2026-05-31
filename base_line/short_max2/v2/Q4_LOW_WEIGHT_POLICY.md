short_max2 v2 Q4 저비중 선정 정책

배경
2025년 4분기는 비정상적인 급락/고변동 특수 구간일 가능성이 높다. 이 구간에서만 성과가 폭발한 후보는 실전형 기준선으로 과대평가될 수 있다. 따라서 short_max2는 전체 train 수익률만으로 순위를 매기지 않고, 2025-Q4 제외 일반 구간 성과와 MDD를 우선 평가한다.

v2 선정 원칙
1. pre-Q4 avg_month_pnl을 우선한다.
2. pre-Q4 max_drawdown_pct를 우선한다.
3. pre-Q4 profit_factor를 보조 평가한다.
4. pre-Q4 positive_month_ratio_pct를 보조 평가한다.
5. 2025-Q4 수익은 낮은 비중으로만 반영한다.
6. full train 성과가 좋아도 Q4 의존도가 지나치게 높으면 별도 수익 극대화형 후보로 분리한다.

선택된 후보
smx2v1_q4lowtop1_retest_stop250_rr500_t320_v1

선택 사유
v1 대비 다음 항목이 모두 개선됐다.

pre-Q4 max_return_pct: 3466.4855917171863 -> 3554.3308235947543
pre-Q4 MDD: 2.2774507674795497 -> 2.1769570997805077
pre-Q4 official_cd_value: 3485.2606382365757 -> 3574.7776092810404
pre-Q4 profit_factor: 2.2589719429377744 -> 2.29014107209504
pre-Q4 avg_month_pnl: 48.823740728411394 -> 50.0609975154197

주의
v2는 Q4 의존성을 줄인 후보가 아니다. q4_share_of_full_return_pct는 v1 76.73960124433124에서 v2 77.19914436251436으로 약간 상승했다. full_top3_month_share_pct도 v1 76.94581060709373에서 v2 77.40116227608569로 약간 상승했다.

따라서 v2는 Q4 의존성 완화형이 아니라, Q4 제외 일반 구간 성과 개선형이다.

향후 개선 우선순위
1. pre-Q4 avg_month_pnl 유지 또는 개선
2. pre-Q4 MDD 축소
3. pre-Q4 PF 개선
4. full train CD 개선
5. q4_share_of_full_return_pct 완화
6. top3_month_share_pct 완화

실전 해석
short_max2/v2는 Q4 특수 구간을 제거해도 일반 구간에서 수익성이 확인된 기준선이다. 다만 전체 성과 집중도는 여전히 높으므로, 실제 운용/통합 백테스트에서는 Q4 의존성을 별도 리스크로 관리한다.
