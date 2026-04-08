Timeout18 split entry lane

Purpose
This lane keeps timeout_18bars as the base strategy but changes execution architecture into a split-entry structure.
Instead of either entering fully at the next open or fully waiting for a retrace, it combines both behaviors.

Why this lane exists
- the user asked for another new structural improvement attempt before current retrace-entry results are available
- pure retrace entry may miss too many strong moves
- pure immediate entry may accept too many poor fills
- split entry tests whether combining certainty and price improvement can outperform both extremes

Base strategy
- timeout_18bars baseline
- initial_asset 100
- position_fraction 1%
- fee_per_side 0.04%
- leverage effectively 1x in current engine

Split-entry styles tested
1. half_open_half_atr025
- 50% enters immediately at next open
- 50% waits for a 0.25 ATR better fill for 1 bar

2. half_open_half_wick050
- 50% enters immediately at next open
- 50% waits for a 50% retrace into the signal wick zone for 1 bar

3. one_third_open_two_thirds_atr050
- 1/3 enters immediately
- 2/3 waits for a 0.50 ATR better fill for 2 bars

4. one_third_open_two_thirds_wick075
- 1/3 enters immediately
- 2/3 waits for a 75% retrace into the signal wick zone for 2 bars

How to run
- workflow: Repository Backtest JSON Only Timeout18 Split Entry Repo Assets
- input repo_data_dir: repo_assets_5m

How to judge
Primary:
- cd_value versus timeout_18bars baseline
- return retention
- PF change
- MDD change
Interpretation:
- if split entry keeps enough exposure while improving average fill price, it can beat both baseline and pure retrace entry
- if delayed legs rarely fill or strong moves escape too often, it will lose on cd_value
