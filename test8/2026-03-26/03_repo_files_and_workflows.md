Repo files and workflows map

Core completed-engine files
1. experiments/base_config.json
2. experiments/single_changes.json
3. scripts/run_backtest_batch.py
4. scripts/summarize_results.py
These are the original stable JSON-config engine files used after the earlier refactor.

JSON-only short_strict branch
1. experiments/base_config_json_only_short_strict.json
2. experiments/single_changes_json_only_short_strict.json
3. scripts/run_backtest_batch_json_only_short_strict.py
4. scripts/summarize_results_json_only_short_strict.py
5. .github/workflows/backtest_json_only_short_strict.yml
6. .github/workflows/backtest_json_only_short_strict_repo_assets.yml
This is the main stable branch for repo-assets execution.

Combo branch on top of long_strict_light
1. experiments/base_config_json_only_long_strict_combos.json
2. experiments/combinations_json_only_long_strict.json
3. scripts/run_backtest_batch_json_only_long_strict_combos.py
4. scripts/summarize_results_json_only_long_strict_combos.py
5. .github/workflows/backtest_json_only_long_strict_combos_repo_assets.yml
Use this lane to test combinations after choosing long_strict_light as the promoted baseline.

MDD-focused branch on top of long_strict_light
1. experiments/base_config_json_only_long_strict_mdd.json
2. experiments/single_changes_json_only_long_strict_mdd.json
3. scripts/run_backtest_batch_json_only_long_strict_mdd.py
4. scripts/summarize_results_json_only_long_strict_mdd.py
5. .github/workflows/backtest_json_only_long_strict_mdd_repo_assets.yml
Use this lane for aggressive MDD reduction experiments.

Data packaging helpers
1. scripts/package_release_assets.py
2. scripts/package_repo_assets_monthly.py
The release path was explored but became secondary. The repo-monthly path is the currently practical one.

Current practical data folder
repo_assets_5m
Expected contents:
- data_manifest.json
- monthly csv.gz files, e.g. BTC_2025_03_5m.csv.gz, RLS_2024_01_5m.csv.gz, etc.
The repo-assets workflows accept this directory as input through workflow_dispatch input repo_data_dir.

Workflows that should usually be ignored now
- backtest_json_only_short_strict_release.yml
- backtest_json_only_short_strict_release_v2.yml
- backtest_json_only_short_strict_release_v3.yml
Those were part of the release-asset attempts and are not the default recommended path now.

Workflow execution order that makes the most sense now
1. Repository Backtest JSON Only Short Strict Repo Assets
Use for the single-change branch on top of short_strict baseline.

2. Repository Backtest JSON Only Long Strict Combos Repo Assets
Use for combo tests after choosing long_strict_light as a promoted baseline.

3. Repository Backtest JSON Only Long Strict MDD Repo Assets
Use for MDD-focused experiments on top of long_strict_light.

Where results appear
Each repo-assets workflow:
- uploads a full artifact
- commits summary files back into the repo
Key result folders:
- results_json_only_short_strict
- results_json_only_long_strict_combos
- results_json_only_long_strict_mdd

How to read results quickly
Each result folder has:
- master_summary.csv
- master_summary.json
- master_summary.txt
- per-experiment summary.json files
The fastest ranking source is master_summary.csv.
