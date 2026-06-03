short_main2 v4 CHANGELOG

2026-06-03
V3MIX07_N02_stop255_rr630_t375를 short_main2 v4 공식 기준선으로 승격.

개발 흐름
1. short_main2/v3 MIX05 기준선에서 개선 후보 topmix2 진행.
2. topmix2 v1.2에서 V3MIX07이 1위 후보로 확인.
3. V3MIX07 단독 리테스트 + Q4 점검 v1.3에서 topmix2 수치와 동일하게 재현.
4. Q4 의존도 점검에서 GENERAL_EDGE_CONFIRMED 확인.
5. Q4 제외 구간에서도 v3 MIX05보다 우위 확인.

주요 변경점
v3 MIX05 대비:
atr_stop_mult: 2.45 -> 2.55
rr_mult: 6.30 -> 6.30
timeout_bars: 345 -> 375
fail_fast_bars: 14 -> 15
dd_brake_trigger_pct: 0.085 -> 0.088

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
short_main2/v4 기준선으로 확정.
이후 short_main2 개선은 v4 기준으로 진행한다.
