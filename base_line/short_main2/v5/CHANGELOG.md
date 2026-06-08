short_main2 v5 CHANGELOG

2026-06-07
V4R05_stop262_rr620_t390_ff15를 short_main2 v5 공식 기준선으로 승격.

개발 흐름
1. short_main2/v4 V3MIX07 기준선에서 next_dev 진행.
2. V4N01이 1위 후보로 확인되었으나 상위 후보 차이가 조건 혼합이 아니라 파라미터 차이임을 확인.
3. V4N01 주변 국소 파라미터 refine 진행.
4. topparam refine v1.1에서 V4R05가 1위 후보로 확인.
5. V4R05 단독 리테스트 + Q4 점검 v1.2.1 memfix에서 탐색 수치와 동일하게 재현.
6. Q4 의존도 점검에서 GENERAL_EDGE_CONFIRMED 확인.
7. Q4 제외 구간에서도 v4 V3MIX07보다 우위 확인.
8. 2026 Q1 validation에서도 v4 V3MIX07보다 우위 확인.

주요 변경점
v4 V3MIX07 대비:
atr_stop_mult: 2.55 -> 2.62
rr_mult: 6.30 -> 6.20
timeout_bars: 375 -> 390
fail_fast_bars: 15 -> 15
dd_brake_trigger_pct: 0.088 -> 0.090

유지한 것
entry_mode: climax_exhaustion
short_dev: 0.025
ret12_min: 0.030
ret3_min: 0.004
volume_spike_min: 0.75
upper_range_ratio_min: 0.16
close_position_max: 0.94
ema20_slope12_min: -0.025
ema20_slope12_max: 0.095
atr_pct_min: 0.0008
atr_pct_max: 0.135
dist_roll_high20_min: -0.08
climax_score_min: 2.7

최종 판정
short_main2/v5 기준선으로 확정.
이후 short_main2 개선은 v5 기준으로 진행한다.
