short_main2 v6 strategy

Strategy:
V5M01_D02_D03_rr615_stop265_t390

Entry conditions:
Same as short_main2 v5.

Exit and risk parameters:
atr_stop_mult: 2.65
rr_mult: 6.15
timeout_bars: 390
fail_fast_bars: 15
dd_brake_trigger_pct: 0.092

Engine rules:
Signal is confirmed at candle close.
Entry is next candle open.
No same timestamp reentry after exit.
Stop first if stop and target touch in the same candle.
No position count limit.
fee_per_side: 0.0004
position_fraction: 0.01
leverage: 1.0

Validation:
2025 train, Q4 exclusion, Q4 only, 2026 Q1, FULL_TO_2026_END all passed against v5 baseline.
