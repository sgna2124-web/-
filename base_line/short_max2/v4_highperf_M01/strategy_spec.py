STRATEGY_NAME='SMX2V3_B04_M01_S02D_plus_upper020'
PARENT='SMX2V2_C08_EX20_02_N02_stop257_rr5075'
AXIS='short_max2'
BRANCH='v4_highperf_M01'

# core exit/risk
atr_stop_mult=2.57
rr_mult=5.075
timeout_bars=320
fail_fast_bars=12
dd_brake_trigger_pct=0.035
dd_brake_freeze_steps=4

# core entry
short_dev=0.032
short_rsi_min=76.0
short_wick_mult=1.30
score_min_short=2.35

# M01 soft modifiers
soft_volr_min=1.10
soft_volr_bonus=0.