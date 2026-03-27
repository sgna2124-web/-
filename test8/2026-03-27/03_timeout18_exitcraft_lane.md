Timeout18 exitcraft lane

Purpose
This lane keeps the current top strategy timeout_18bars intact on entry logic and tests broader exit-structure improvements instead of more entry-side tuning.

Why this lane exists
- recent entry-side refinements did not beat the timeout_18bars baseline on cd_value
- user explicitly wants to keep iterating on the top strategy
- next logical direction is to change defense and profit-protection after entry rather than filtering more entries

Base strategy
- timeout_18bars baseline
- initial_asset 100
- position_fraction 1%
- fee_per_side 0.04%
- leverage effectively 1x in current engine

Exit improvement styles tested
1. breakeven_075r
- once prior bar reaches 0.75R favorable excursion, move stop to entry

2. trail_after_1r
- once prior bar reaches 1R favorable excursion, trail stop using previous bar low/high

3. fail_fast_6bars
- if after 6 bars the trade has not reached 0.25R progress and is still adverse, close early

4. breakeven_and_fail_fast
- combine breakeven move and early-failure exit

5. trail_and_breakeven
- combine 0.75R breakeven and 1R previous-bar trailing stop

How to run
- workflow: Repository Backtest JSON Only Timeout18 Exitcraft Repo Assets
- input repo_data_dir: repo_assets_5m

How to judge
Primary:
- cd_value versus timeout_18bars baseline
- return retention
- PF change
- MDD change
Interpretation:
- if exit refinement improves MDD but destroys peak growth and cd_value, reject it
- only promote if it keeps most of baseline upside while reducing damage meaningfully
