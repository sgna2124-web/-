SHORT_MAX v10 entry combo fast 1h v1

이 결과는 2025-12-31 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

기준선:
short_max v10 = smv9_topcombo1_01_tr4_stop205_rr550

직전 1위 참고:
smv10_dev1_01_v10_stop210_rr550

이번 목적:
직전 1위의 청산부(stop 2.10, rr 5.50, time_reduce 4)를 유지하고 상위 후보들의 진입 조건 요소를 조합한다.

속도 개선:
진입 신호를 사전 벡터화하고, 메인 루프에서는 active position과 raw signal timestamp만 처리한다.
