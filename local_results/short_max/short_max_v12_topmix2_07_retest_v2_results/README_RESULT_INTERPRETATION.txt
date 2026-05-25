SHORT_MAX V12 TOPMIX2_07 SINGLE RETEST

대상:
smv12_topmix2_07_mix2_07_top1_reduce_frac000

기준선:
short_max/v12 / smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540

핵심 변경:
- time_reduce_bars = 3
- time_reduce_to_risk_frac = 0.00
- timeout_bars = 240
- fail_fast_bars = 12
- dd_brake_trigger_pct = 0.035
- dd_brake_freeze_steps = 4
- atr_stop_mult = 2.15
- rr_mult = 5.4

진입 조건:
short_max v12와 동일.

공식 train 범위:
2025-12-31 23:59:59까지 사용.
2026-01-01 00:00:00 이후 데이터는 지표 계산 전부터 제외.

Gate:
expected_gate_ok = True
mismatches = []

expected_gate_ok가 True이면 short_max v13 / short_main v14 승격 후보로 볼 수 있다.
