Guardrails and failure modes

Non-negotiable backtest guardrails
1. No lookahead.
If any higher timeframe is used later, only use the previous completed higher-timeframe candle. Never use the currently forming higher-timeframe candle.
User example that must be remembered: if 5m time is 17:30, do not use the 17:00 1h candle because it contains future 5m bars. Use the previous completed hour instead.

2. Capital and fee assumptions for this phase
- initial asset = 100
- position fraction = 0.01
- fee per side = 0.0004
These assumptions were central to the comparisons and should not be silently changed.

3. Sequential backtesting matters
Treat entries and exits through time. Avoid any aggregated shortcut that can reintroduce unrealistic fills or future knowledge.

4. Keep strategy and data transport separate
Many past failures were not caused by strategy logic. They were caused by transport layers: Git LFS, release downloads, manifests, etc. Diagnose the layer before changing strategy logic.

Important historical failure modes encountered
A. Git LFS pointer-file failures
Symptoms:
- CSV loader reads only 'version https://git-lfs.github.com/spec/v1'
- ValueError saying the file is an LFS pointer, not a real CSV
Meaning:
The workflow obtained pointer files instead of real data.

B. Git LFS budget exceeded
Symptoms:
- This repository exceeded its LFS budget
- lfs fetch / lfs pull fails before backtests run
Meaning:
The workflow cannot even download data. This is not a strategy failure.

C. Release-based manifest/download failures
Symptoms encountered:
- JSONDecodeError while trying to parse data_manifest.json
- release not found
Meaning:
The release-asset lane was brittle in this environment. It required correct published releases, correct tags, correct auth, and correctly fetched assets. The repo-assets lane became the more practical path.

D. Cooldown over-tightening failures
Observed issue:
Aggressive cooldowns (for example 6 bars in one branch, and 2-3 bars in the MDD branch) often damaged returns much more than they helped quality.
Interpretation:
Cooldown is not useless, but it is dangerous and should be treated as a secondary, not primary, MDD lever.

E. TP-min axis becoming neutral
Observed issue:
tp_min_0045 and tp_min_006 were nearly identical to baseline in one branch.
Interpretation:
Do not over-invest time in this axis unless the base branch changes materially.

F. Timeout sensitivity
Observed issue:
- timeout_30bars was a decent balance improvement in combos
- timeout_18bars became the strongest MDD-lane winner
- timeout_24bars underperformed in one lane
Interpretation:
Timeout matters, but it is highly branch-sensitive. It should be retested after any major baseline promotion.

How to think about unresolved MDD now
Current MDD is still too high even after important improvements.
This is likely because:
1. entry quality improved, but
2. concurrency is still high in many branches
Therefore the next stage should not only chase MDD numerically. It should also look for branches that reduce max_conc without destroying return.
This is why long_strict_stronger matters despite lower return than timeout_18bars.

What not to repeat blindly
- Do not re-open Git LFS as the primary path unless the environment clearly changes.
- Do not assume release workflows are the best path in this environment.
- Do not re-run old rejected cooldown variants unless there is a new rationale.
- Do not introduce HTF logic without explicit previous-completed-candle protection.
- Do not compare experiments that are not based on the same promoted baseline.
