SHORT_MAX v12 top robust combo fast 1h v1

이 결과는 2025-12-31 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

기준선:
short_max v12 = smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540

이번 목적:
직전 robust dev 결과의 상위 후보 조건을 서로 혼합한다. time_reduce=3, timeout=240, dd035_freeze4, fail_fast 12/9, min_expected_tp 0.0032를 의미 단위로 조합한다. 기준선 진입 조건의 핵심 구조는 유지한다.
후보별 elapsed_seconds_candidate, elapsed_minutes_candidate, elapsed_minutes_total_so_far를 summary에 기록한다.
전체 실행 시간은 run_metadata.json의 elapsed_minutes에 기록한다.

속도 개선:
진입 신호를 사전 벡터화하고, 메인 루프에서는 active position과 raw signal timestamp만 처리한다.
trade detail은 저장하지 않고 summary만 저장한다.
