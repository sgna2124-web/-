short_main2 v3 CHANGELOG

2026-06-02
MIX05_A02_A03_failfast14_rr630을 short_main2 v3 공식 기준선으로 승격.

개발 흐름
1. short_main2/v2 C03 기준선에서 개선 후보 topmix 진행.
2. topmix v1.5.2에서 MIX05가 균형형 1위 후보로 확인.
3. MIX05 단독 리테스트 v1.6에서 topmix 수치와 동일하게 재현.
4. Q4 의존도 점검 v1.7에서 GENERAL_EDGE_CONFIRMED 확인.
5. Q4 제외 구간에서도 v2 C03보다 우위 확인.

주요 변경점
v2 C03 대비:
atr_stop_mult: 2.40 -> 2.45
rr_mult: 6.20 -> 6.30
timeout_bars: 315 -> 345
fail_fast_bars: 12 -> 14
dd_brake_trigger_pct: 0.080 -> 0.085

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
short_main2/v3 기준선으로 확정.
