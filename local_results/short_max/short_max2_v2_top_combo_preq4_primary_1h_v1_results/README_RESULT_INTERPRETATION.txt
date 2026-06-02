SHORT_MAX2 v2 embedded exact baseline-gated top-candidate combo development v1

이 러너는 최신 유효 결과의 상위 후보 조건을 혼합한다.
2025년 4분기는 비정상/특수 장세로 보고, 순위는 Q4 제외 pre-Q4 성과를 1차 기준으로 계산한다.
full train 결과와 full - preQ4 차이는 참고 지표로만 기록한다.

주요 결과 파일:
- scored_summary.csv: Q4 제외 pre-Q4 1차 점수 순위
- summary_compact.csv: scored_summary와 동일한 사용자 확인용 파일
- preq4_raw_summary.csv: 2025-09-30까지의 일반 구간 원본 성과
- fulltrain_raw_summary.csv: 2025-12-31까지의 전체 train 원본 성과
- SCORING_FORMULA.txt: 점수식 설명

주의:
float64 원본형 내장 재현/개발 러너다. embedded_baseline_gate.json의 ok가 true일 때만 후보 결과를 해석한다.
