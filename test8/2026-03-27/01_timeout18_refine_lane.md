Timeout18 refine lane

Purpose
This lane continues from the current top strategy family centered on timeout_18bars.
The goal is not to cap concurrency globally, but to improve signal quality directly so that low-quality entries are filtered out before entry.

Why this lane exists
- The user does not want top-N concurrent selection.
- The user wants quality thresholds, not portfolio-level ranking gates.
- Therefore refinement should come from stricter entry quality conditions rather than execution-level concurrency control.

Base strategy
- timeout_18bars promoted baseline
- same capital model: initial_asset 100, position_fraction 1%, fee_per_side 0.04%
- leverage remains effectively 1x at this stage

Experiments
1. baseline
- current best timeout_18bars baseline

2. plus_short_stricter_light
- slightly stronger short-side quality filter
- intended to remove noisier short entries while preserving more return than the full short_stricter version

3. plus_short_stricter
- previously tested stronger short-side filter for direct re-check against the current baseline

4. plus_long_quality_light
- slightly stronger long-side quality filter
- intended to remove weaker rebound attempts without over-tightening as much as long_strict_stronger

5. plus_dual_quality_light
- light quality tightening on both long and short sides
- intended as a balanced stability-focused variant

How to run
- workflow: Repository Backtest JSON Only Timeout18 Refine Repo Assets
- input repo_data_dir: repo_assets_5m

How to judge
Primary targets:
- maintain or improve PF
- maintain acceptable return retention versus timeout_18bars baseline
- lower MDD
Secondary:
- observe whether peak growth remains competitive
