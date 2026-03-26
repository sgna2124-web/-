Test8 handoff index

Purpose
This folder is a full handoff package for the current trading-strategy project state as of 2026-03-26. It is written for the next assistant, not for the user. The goal is that the next assistant can scan this folder and immediately understand:
1. What strategy family is currently active
2. Which backtest engine/path is currently stable
3. What experiments were already run, with results and ranking
4. Which paths failed and should not be repeated blindly
5. What the next highest-value experiments are

Read order
1. 01_project_state_and_decisions.md
2. 02_results_and_rankings.md
3. 03_repo_files_and_workflows.md
4. 04_guardrails_and_failure_modes.md
5. 05_next_steps.md
6. 06_state.json

High-level summary
- The active strategy family is overextension_reversion_v1.
- The completed-engine branch was preserved, and new experiment sets were added as separate config/runner/workflow files instead of overwriting prior files.
- Git LFS became unusable because of LFS budget / pointer-file problems. Multiple release-based attempts were explored, but the stable path became repo-assets (monthly csv.gz committed directly to the repo, read by Actions workflows).
- The strongest single improvement found so far is long_strict_light over the short_strict baseline.
- The strongest MDD-oriented single improvement found so far is timeout_18bars.
- The strongest balance-oriented combo found so far is plus_timeout_30bars on top of long_strict_light, but timeout_18bars in the MDD branch outperformed it overall on both return and MDD.
- Max concurrency remains a core unresolved issue. Most strong candidates still keep max_conc around 389. long_strict_stronger is notable because it reduced max_conc to 367.

Important current recommendation
The next assistant should not go back to LFS or release-asset workflows unless there is a compelling reason and a verified working environment. The current practical lane is repo_assets_5m + repo-assets workflows.
