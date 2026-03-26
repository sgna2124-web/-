Project state and major decisions

Project objective
Primary objective: make money from crypto charts through a robust, reality-checked backtesting process.
This is not a pure research notebook. Practical execution quality matters.

User priorities that must remain fixed
- Responses and work should continue in Korean by default.
- Backtests must be done as if trades unfold through time, not by any future-aware shortcut.
- Capital model used during this phase:
  - initial asset = 100
  - position fraction = 1%
  - fee per side = 0.04%
- Report at minimum:
  - final return / final asset
  - MDD
  - peak return / peak asset
  - number of trades
  - win rate
  - max concurrency
- The user explicitly cares about max_conc because practical live execution can split capital across the observed maximum number of simultaneous positions.
- The user strongly dislikes repeated backtest mistakes and repeated explanations with no action.

Most important methodological warning from the user
If higher timeframes are used, never use any incomplete current higher-timeframe candle. Example from the user: if the current 5m bar is 17:30, do not use the 17:00 1h candle, because that candle contains future 5m bars up to 17:55. Use the previous completed 1h candle instead (for example, 16:00). This is a non-negotiable guardrail.

Separation of concerns that emerged during this conversation
A. Strategy layer
- experiment configs
- signal thresholds
- timeout / cooldown / filtering logic
- result ranking and next-step decisions

B. Data / execution-infrastructure layer
- data transport
- Git LFS problems
- release-asset attempts
- repo-assets path
- workflows and artifact handling

This separation is important because several failures were not caused by strategy logic, but by data transport.

Completed-engine branch that remained usable
The safest engine family for continuing work is the completed-engine / JSON-only path:
- experiments/base_config.json
- experiments/single_changes.json
- scripts/run_backtest_batch.py
- scripts/summarize_results.py
and later separated descendants based on the same engine structure.

Why separate descendants were created instead of overwriting everything
The user wanted clean, isolated experimental comparisons. Therefore the repo evolved toward:
- a stable base engine
- separate config files per branch
- small wrapper runners / workflows per experiment lane
This avoided contaminating one experiment set with another.

Most important strategy path found so far
1. Original baseline under JSON-only short-strict branch
A short-strict baseline was created by promoting the earlier winning short-only tightening change into the new base config.

2. On top of that, several single changes were tested.
The strongest single winner was:
- long_strict_light

Meaning of long_strict_light
- long_dev tightened from 0.025 to 0.028
- long_rsi_max tightened from 28 to 25
- long_wick_mult increased from 1.0 to 1.2
Interpretation: the remaining weakness after short_strict seemed to come largely from too many long entries rather than short entries.

3. After that, a combo lane and an MDD-focused lane were created on top of long_strict_light.

Practical current branch logic
Current effective base idea is no longer the old raw baseline. It is closer to:
short_strict promoted to baseline -> long_strict_light selected as strongest single improvement -> then combos and MDD-focused follow-up tests were added.

Main unresolved issue
Even after improvements, MDD is still high, and max_conc is still too high in many branches. This means the strategy quality improved, but concurrency pressure is still not solved well enough.
