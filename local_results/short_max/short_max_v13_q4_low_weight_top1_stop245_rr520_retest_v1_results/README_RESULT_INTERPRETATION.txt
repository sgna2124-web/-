SHORT_MAX v13 Q4 low weight TOP1 stop245 rr520 float64 retest v1

이 러너는 2025년 4분기를 비정상/특수 장세로 보고, 해당 구간 성과가 순위를 지배하지 않도록 점수제를 적용한다.
pre-Q4 구간과 full train 구간을 따로 돌린 뒤, full - preQ4 차이를 Q4 기여분으로 계산한다.

주요 결과 파일:
- scored_summary.csv: 최종 점수 순위
- summary_compact.csv: scored_summary와 동일한 사용자 확인용 파일
- preq4_raw_summary.csv: 2025-09-30까지의 일반 구간 원본 성과
- fulltrain_raw_summary.csv: 2025-12-31까지의 전체 train 원본 성과
- SCORING_FORMULA.txt: 점수식 설명

주의:
float64 원본형 단독 리테스트다. 기준선 승격 판단에는 이 결과를 우선한다.
