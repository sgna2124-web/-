Timeout18 retrace entry lane

Purpose
This lane keeps timeout_18bars as the base strategy but changes the entry execution architecture.
Instead of buying or selling immediately at the next bar open after a signal, it tries to get filled at a better price through short-window retrace limit entries.

Why this lane exists
- the user asked for another new structural improvement attempt rather than parameter-only tuning
- prior confirmation and exit-craft experiments did not beat the baseline
- retrace-limit entry changes how the strategy gets filled, which can improve entry quality without changing the signal definition itself

Base strategy
- timeout_18bars baseline
- initial_asset 100
- position_fraction 1%
- fee_per_side 0.04%
- leverage effectively 1x in current engine

Retrace entry styles tested
1. atr_pullback_025_1bar
- after signal, place a limit entry 0.25 ATR better than signal close and allow 1 bar for fill

2. atr_pullback_050_2bars
- after signal, place a limit entry 0.50 ATR better than signal close and allow 2 bars for fill

3. wick_retrace_050_1bar
- after signal, place a limit entry at 50% retrace into the signal wick zone and allow 1 bar for fill

4. wick_retrace_075_2bars
- after signal, place a limit entry at 75% retrace into the signal wick zone and allow 2 bars for fill

How to run
- workflow: Repository Backtest JSON Only Timeout18 Retrace Entry Repo Assets
- input repo_data_dir: repo_assets_5m

How to judge
Primary:
- cd_value versus timeout_18bars baseline
- return retention
- PF change
- MDD change
Interpretation:
- if retrace entry improves fill quality but misses too many good moves, it will lose on cd_value
- only keep a retrace architecture if it preserves enough upside while reducing entry damage meaningfully
