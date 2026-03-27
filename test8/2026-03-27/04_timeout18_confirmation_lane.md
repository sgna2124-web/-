Timeout18 confirmation lane

Purpose
This lane keeps timeout_18bars as the base strategy but changes entry architecture rather than just tuning parameters.
Instead of entering immediately on the next bar open after a signal candle, it waits one extra bar and enters only when a confirmation structure appears.

Why this lane exists
- the user explicitly asked for another structural improvement attempt when baseline still remained the top strategy
- prior micro-parameter tuning and broad filter stacks did not outperform baseline on cd_value
- confirmation-based entry changes the timing logic itself, not just thresholds

Base strategy
- timeout_18bars baseline
- initial_asset 100
- position_fraction 1%
- fee_per_side 0.04%
- leverage effectively 1x in current engine

Confirmation styles tested
1. reclaim_confirm
- enter only if the next candle closes in a reclaim direction relative to the signal candle midpoint and its own body direction

2. followthrough_confirm
- enter only if the next candle extends beyond the signal candle extreme in the intended reversal direction and closes favorably

3. volume_reclaim_confirm
- reclaim confirmation plus volume confirmation versus recent average volume

4. reclaim_no_chase_confirm
- reclaim confirmation plus a no-chase rule so the actual entry open is not too far from the confirmation close in ATR terms

5. followthrough_no_chase_confirm
- followthrough confirmation plus the same no-chase rule

How to run
- workflow: Repository Backtest JSON Only Timeout18 Confirmation Repo Assets
- input repo_data_dir: repo_assets_5m

How to judge
Primary:
- cd_value versus timeout_18bars baseline
- return retention
- PF change
- MDD change
Interpretation:
- if confirmation improves quality but cuts too many good entries, it will lose on cd_value
- only keep a confirmation architecture if it meaningfully preserves upside while reducing damage enough to compensate
