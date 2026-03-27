Timeout18 multimethod lane

Purpose
This lane is designed for broader improvement styles, not just micro parameter tuning.
It keeps the current top strategy family centered on timeout_18bars, but tests several structurally different quality filters.

Design principle
- ranking summaries should exclude duplicate-equity variants by default in interpretation
- no top-N concurrent selection
- no portfolio-level gating
- improve entry quality directly before entry

Base strategy
- timeout_18bars baseline
- initial_asset 100
- position_fraction 1%
- fee_per_side 0.04%
- leverage effectively 1x in current engine

Broad improvement styles tested
1. trend_context_guard
- requires EMA slope context to match the intended mean-reversion direction

2. reclaim_close_guard
- requires the signal candle to close in a better reclaim position within its range

3. deviation_band_guard
- uses ATR-normalized EMA deviation band to reject weak and overly chaotic stretches

4. risk_width_guard
- rejects trades where the initial stop distance is too wide relative to entry price

5. hybrid_quality_stack
- combines trend context and reclaim close quality requirements

How to run
- workflow: Repository Backtest JSON Only Timeout18 Multimethod Repo Assets
- input repo_data_dir: repo_assets_5m

How to judge
Primary:
- cd_value versus timeout_18bars baseline
- final return retention
- PF improvement
- MDD improvement
Interpretation rule:
- if a new variant lowers cd_value materially versus baseline, treat it as non-effective even if one submetric improves
