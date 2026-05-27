SHORT_MAX v13 fulltrain top-combo from pre-Q4 v1

이 결과는 2025-12-31 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

기준선:
short_max v13 = smv12_topmix2_07_mix2_07_top1_reduce_frac000

이번 목적:
pre-Q4 상위 후보 조건들을 전체 2025 train에 다시 적용해 Q4 폭발력과 일반 구간 안정성을 동시에 확인한다. summary_compact는 official_cd_value와 general_consistency_score를 함께 고려해 정렬된다. 이 점수는 CD, positive_month_ratio, top3_month_share 패널티를 함께 본다.
후보별 elapsed_seconds_candidate, elapsed_minutes_candidate, elapsed_minutes_total_so_far를 summary에 기록한다.
전체 실행 시간은 run_metadata.json의 elapsed_minutes에 기록한다.

속도 개선:
진입 신호를 사전 벡터화하고, 메인 루프에서는 active position과 raw signal timestamp만 처리한다.
trade detail은 저장하지 않고 summary만 저장한다.
