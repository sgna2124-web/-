SHORT_MAX v11 exit dev fast 1h v1

이 결과는 2025-12-31 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

기준선:
short_max v11 = smv10_dev1_01_v10_stop210_rr550

이번 목적:
새 기준선의 진입 조건은 그대로 유지하고, stop/rr/time_reduce/fail_fast 주변부만 좁게 조정한다.
후보별 elapsed_seconds_candidate, elapsed_minutes_candidate, elapsed_minutes_total_so_far를 summary에 기록한다.
전체 실행 시간은 run_metadata.json의 elapsed_minutes에 기록한다.

속도 개선:
진입 신호를 사전 벡터화하고, 메인 루프에서는 active position과 raw signal timestamp만 처리한다.
trade detail은 저장하지 않고 summary만 저장한다.
