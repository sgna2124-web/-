Q4 저비중 기준선 선정 정책

배경
2025년 4분기는 트럼프 이슈 등으로 인해 비정상적인 급락/고변동 시장일 가능성이 높다고 판단했다. 이 구간에서만 성과가 폭발한 후보를 그대로 기준선으로 삼으면 일반적인 시장 상황에 대한 전략 신뢰도가 과대평가될 수 있다.

따라서 short_max2 v1은 전체 수익률 1위가 아니라 다음 관점으로 선택했다.

1. 2025년 4분기를 제외한 일반 구간의 월별 평균 수익률을 높게 평가한다.
2. 2025년 4분기를 제외한 일반 구간의 MDD를 높게 평가한다.
3. pre-Q4 profit factor와 positive_month_ratio를 보조 평가한다.
4. 2025년 4분기 성과는 낮은 비중으로만 반영한다.
5. Q4 성과 집중도가 지나치게 높은 후보는 수익 극대화형 후보로 분리하고, 실전형 기준선에서는 낮춰 평가한다.

선택된 후보
smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1

선택 사유
- pre-Q4 max_return_pct 3466.4855917171863
- pre-Q4 MDD 2.2774507674795497
- pre-Q4 PF 2.2589719429377744
- pre-Q4 positive_month_ratio_pct 92.95774647887323
- pre-Q4 positive_year_ratio_pct 100.0
- full train에서도 MDD가 2.2774507674795497로 낮고 CD가 14661.265180583516으로 강하다.

탈락 또는 후순위 처리한 성격의 후보
stop250_timeout320_rr560 계열은 full train 수익률과 CD는 더 강했지만, 2025-Q4 성과 집중도가 높아 수익 극대화형 후보로 분류했다. short_max2 v1은 이 후보보다 일반 구간 안정성을 우선한다.

운영 원칙
이후 short_max2 개선은 다음 우선순위를 따른다.

1. pre-Q4 avg_month_pnl 개선
2. pre-Q4 max_drawdown_pct 축소
3. pre-Q4 profit_factor 개선
4. pre-Q4 positive_month_ratio_pct 유지 또는 개선
5. full train CD 개선
6. Q4 share와 top3 month share 완화

주의
full train 수익 중 q4_share_of_full_return_pct가 76.73960124433124로 여전히 높다. 따라서 이 기준선은 Q4 의존성이 없는 전략이 아니라, Q4 제외 일반 구간에서도 충분한 성과를 확인한 Q4 저비중 실전형 기준선이다.
