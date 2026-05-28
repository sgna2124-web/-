SHORT_MAX v13 general top-combo2 pre-Q4 v3 memsafe

이 결과는 2025-09-30 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

기준선:
short_max v13 = smv12_topmix2_07_mix2_07_top1_reduce_frac000

이번 목적:
2025-Q4 폭발 구간을 제외한 상태에서 pre-Q4 상위 후보 2차 조합을 테스트한다. stop 2.40 / timeout 320 축을 중심으로 RR, DD brake, fail_fast, time_reduce, timeout 280/360, stop 2.35/2.45, 소폭 진입 필터, ATR 필터를 섞어 일반 구간의 꾸준함과 수익 집중도 완화 가능성을 확인한다. summary_compact는 general_consistency_score 기준으로 정렬된다.
후보별 elapsed_seconds_candidate, elapsed_minutes_candidate, elapsed_minutes_total_so_far를 summary에 기록한다.
전체 실행 시간은 run_metadata.json의 elapsed_minutes에 기록한다.

속도 개선:
진입 신호를 사전 벡터화하고, 메인 루프에서는 active position과 raw signal timestamp만 처리한다.
trade detail은 저장하지 않고 summary만 저장한다.
