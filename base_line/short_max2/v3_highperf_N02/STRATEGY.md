short_max2 v3_highperf_N02 strategy

Strategy
SMX2V2_C08_EX20_02_N02_stop257_rr5075

Side
short only

Timeframe
The runner uses the official OHLCV files in Data/time without external indicators or external baseline imports.

Entry concept
The strategy enters short when the market is extended upward relative to EMA20, RSI is overheated, and the upper wick condition confirms rejection pressure.

Entry parameters
short_dev: 0.032
short_rsi_min: 76.0
short_wick_mult: 1.30
score_min_short: 2.35
score_dev_weight: 1.30
score_rsi_weight: 0.80
score_wick_weight: 0.70
score_dev_cap: 2.0
score_rsi_cap: 2.0
score_wick_cap: 2.5

Exit and risk parameters
atr_stop_mult: 2.57
rr_mult: 5.075
timeout_bars: 320
time_reduce_bars: 3
time_reduce_to_risk_frac: 0.0
fail_fast_bars: 12
fail_fast_min_progress_r: 0.10
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4

Broad filters used in this branch
atr_pct_min: 0.0
atr_pct_max: 999.0
close_position_min: -999.0
close_position_max: 999.0
upper_body_ratio_min: 0.0
upper_body_ratio_max: 999.0
range20_pct_max: 999.0
ret3_ceil: 999.0
ret5_ceil: 999.0
ret10_ceil: 999.0
ret20_ceil: 999.0
require_upper_sweep: False
require_ema_reject: False

Engine rules
- t close signal enters at t+1 open.
- same-bar TP/SL is allowed.
- if stop and target touch in the same bar, stop is prioritized.
- end-of-test active positions are force-closed at final close.
- fee_per_side is 0.0004.
- position_fraction is 0.01.

Strengths
- positive yearly performance in 2023, 2024, and 2025.
- strong 2025 expansion.
- 2026 is low activity but still positive in the available result.
- PF stays around 2.0 in major validation windows.

Weaknesses
- realized MDD is higher than old short_max2/v2 Q4-low branch.
- trade count and same-bar clustering are much higher than the old official v2 branch.
- 2026 Q2 to Q4 showed no trades in the current data snapshot.
- this branch should not be mixed up with the original Q4-low official branch.

Classification
short_max2 v3 high-performance branch.
