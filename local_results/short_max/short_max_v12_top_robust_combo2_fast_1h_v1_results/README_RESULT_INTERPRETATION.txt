SHORT_MAX v12 top robust combo2 fast 1h v1

이 결과는 2025-12-31 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

기준선:
short_max v12 = smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540

이번 목적:
직전 top robust combo 결과의 공격형 1위와 안정형 1위를 바탕으로 timeout 확장, DD brake 완화, fail_fast 완화, 보호청산 강도(time_reduce_to_risk_frac)를 의미 단위로 조합한다. stop/rr 촘촘 보간은 하지 않고 기준선 진입 조건의 핵심 구조는 유지한다.
후보별 elapsed_seconds_candidate, elapsed_minutes_candidate, elapsed_minutes_total_so_far를 summary에 기록한다.
전체 실행 시간은 run_metadata.json의 elapsed_minutes에 기록한다.

속도 개선:
진입 신호를 사전 벡터화하고, 메인 루프에서는 active position과 raw signal timestamp만 처리한다.
trade detail은 저장하지 않고 summary만 저장한다.
