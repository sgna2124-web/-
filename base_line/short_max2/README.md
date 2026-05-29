short_max2 기준선 인덱스

현재 공식 기준선
- v1: smv13_q4lowtop1_stop245_timeout320_rr520_retest_v1

선정 원칙
short_max2는 기존 short_max의 단순 전체 수익률 극대화가 아니라, 2025년 4분기 특수 구간의 비중을 낮게 보고 일반 구간 성과와 MDD를 더 높게 평가하는 축이다.

현재 v1 위치
base_line/short_max2/v1

핵심 문서
- README.md: 기준선 개요
- STRATEGY.md: 진입 조건, 청산 조건, 장단점
- REPRODUCE.md: 재현 방법과 gate 값
- strategy_spec.py: 파라미터와 gate 값을 코드 형태로 고정
- result_summary.csv: pre-Q4/full train 결과 요약
- Q4_LOW_WEIGHT_POLICY.md: Q4 저비중 선정 정책
