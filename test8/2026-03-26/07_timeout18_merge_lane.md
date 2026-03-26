Timeout18 merge lane

Purpose
This file records the next concrete experiment lane created after the 2026-03-26 handoff review.
The lane promotes timeout_18bars to baseline and tests whether the best concurrency reducer can be merged into that promoted winner.

Why this lane was created
- timeout_18bars was the strongest MDD-oriented result and improved return, PF, and MDD simultaneously.
- long_strict_stronger was the strongest practical concurrency reducer while preserving relatively strong PF and acceptable return.
- The highest-value unanswered question was whether these two strengths can coexist in one promoted branch.

Files added for this lane
- experiments/base_config_json_only_timeout18_merge.json
- experiments/combinations_json_only_timeout18_merge.json
- scripts/run_backtest_batch_json_only_timeout18_merge.py
- scripts/summarize_results_json_only_timeout18_merge.py
- .github/workflows/backtest_json_only_timeout18_merge_repo_assets.yml

Experiment set
1. baseline
- timeout_18bars promoted baseline

2. plus_long_strict_stronger
- tests the direct merge of timeout_18bars winner with the best concurrency reducer

3. plus_short_stricter
- tests whether short-side tightening still helps after timeout_18bars promotion

4. plus_long_strict_stronger_and_short_stricter
- tests the stronger quality-focused three-way merge candidate

Decision logic
Promote only if a candidate keeps most of timeout_18bars return while improving or at least not materially worsening:
- MDD
- PF
- max_conc

Primary read target after workflow completion
- results_json_only_timeout18_merge/master_summary.csv

Recommended comparison order after results exist
1. baseline vs plus_long_strict_stronger
2. baseline vs plus_short_stricter
3. baseline vs plus_long_strict_stronger_and_short_stricter
4. winner vs current timeout_18bars and long_strict_stronger references
