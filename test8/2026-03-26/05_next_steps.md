Next steps

Immediate recommended next experiments
1. Combine the strongest MDD improvement with the strongest concurrency reducer.
Most important candidate:
- long_strict_stronger + timeout_18bars
Rationale:
- timeout_18bars was the best MDD-lane winner overall and even improved return.
- long_strict_stronger reduced max_conc to 367 and had the strongest PF in that lane.
This combination is the highest-value next test because it may reduce MDD further while also attacking concurrency.

2. If the above works, consider one stronger quality version:
- long_strict_stronger + short_stricter + timeout_18bars
Rationale:
short_stricter improved PF quality in prior branches, though it often sacrificed some return. It may be worth testing only after the 2-way combo above.

3. If the above fails, test a softer concurrency-focused path:
- long_strict_light baseline + long_strict_stronger only (already done as a single change in MDD branch)
- compare directly against timeout_18bars winner to decide whether concurrency reduction is worth the return cost.

How the next assistant should decide the next promoted baseline
Use two winners, not one.
A. Balance winner
Current best candidate: timeout_18bars
Reason: it improved return, PF, and MDD together.

B. Risk-quality winner
Current best candidate: long_strict_stronger
Reason: it reduced max_conc materially and improved PF / MDD strongly.

Then run the direct merge test:
- timeout_18bars + long_strict_stronger
If this merged test keeps most of timeout_18bars return while preserving much of long_strict_stronger concurrency improvement, it should become the next promoted baseline.

What to do if max_conc remains too high even after that
If max_conc still stays near the high 300s, the next assistant should design a separate concurrency-control lane. Possible future axes:
1. stricter long filtering around body/wick and RSI together
2. symbol-side short cooldown only, instead of both sides
3. global same-timestamp ranking / top-N selection
This third one is more invasive because it changes the execution model and needs careful implementation.

What not to prioritize right now
- tp_min-only changes
- aggressive cooldown variants
- release workflows
- Git LFS fixes as a strategy prerequisite
These are not the highest-value next steps in the current state.

Recommended practical action sequence
1. Run the existing combo and MDD repo-assets workflows if not already complete.
2. Create a new combo-on-top-of-MDD-winner lane that tests:
   - baseline = timeout_18bars promoted
   - plus_long_strict_stronger
   - plus_long_strict_stronger_and_short_stricter (optional second step)
3. Compare the resulting master_summary.csv files.
4. Promote exactly one new baseline only after that direct comparison.

Expected outputs the next assistant should look at first
- results_json_only_long_strict_combos/master_summary.csv
- results_json_only_long_strict_mdd/master_summary.csv
- any future merged-branch master_summary.csv

Decision rule for the next baseline promotion
Prefer the candidate that satisfies most of these at once:
- lower MDD than current best balance branch
- return retention above 90% relative to the branch it extends
- PF improvement or at least no material PF deterioration
- lower max_conc if possible
If no candidate satisfies all, keep two baselines in parallel:
- one balance baseline
- one risk-quality baseline
