Results and rankings

A. JSON-only short_strict branch: single-change ranking
Reference branch: results_json_only_short_strict/master_summary.csv

Baseline in this lane
- final_return_pct = 833.0415
- pf = 1.127769
- mdd_pct = -61.8732
- max_conc = 419

Candidates that were tested
1. long_strict_light
- final_return_pct = 747.4158
- pf = 1.171075
- mdd_pct = -54.3699
- max_conc = 389
- interpretation: best quality improvement among the first batch. Return fell, but PF improved strongly, MDD improved materially, and concurrency dropped by 30.

2. short_stricter
- final_return_pct = 698.9852
- pf = 1.133614
- mdd_pct = -61.3426
- max_conc = 419
- interpretation: mild improvement, but could not reduce concurrency.

3. timeout_30bars
- final_return_pct = 793.4693
- pf = 1.127569
- mdd_pct = -61.4567
- max_conc = 419
- interpretation: small MDD improvement, almost no concurrency relief, PF slightly worse.

4. tp_min_0045 and tp_min_006
- almost identical to baseline
- interpretation: this axis was effectively neutral in this branch.

5. cooldown_6bars
- final_return_pct collapsed to around 80.6377
- pf worsened heavily
- interpretation: practically rejected.

Single-change ranking from that lane
1. long_strict_light
2. short_stricter
3. timeout_30bars
4. tp_min_0045 / tp_min_006 (neutral)
5. cooldown_6bars (reject)

B. Combo lane on top of long_strict_light
Reference values were user-provided from the combo workflow output.
Base for this lane = long_strict_light baseline
- final_return_pct = 747.4158
- pf = 1.171075
- mdd_pct = -54.3699
- max_conc = 389

Combo results
1. plus_timeout_30bars
- final_return_pct = 722.4198
- pf = 1.171740
- mdd_pct = -53.0910
- max_conc = 389
- interpretation: best balance. Very strong return retention, small PF improvement, solid MDD improvement.

2. plus_short_stricter_timeout_30bars
- final_return_pct = 612.2476
- pf = 1.189302
- mdd_pct = -52.4442
- max_conc = 389
- interpretation: best PF and strongest combo-lane MDD improvement, but noticeably larger return sacrifice.

3. plus_short_stricter
- final_return_pct = 625.6619
- pf = 1.187582
- mdd_pct = -53.7383
- max_conc = 389
- interpretation: quality up, but weaker than the timeout combo.

Combo ranking
1. plus_timeout_30bars
2. plus_short_stricter_timeout_30bars
3. plus_short_stricter

C. MDD-focused lane on top of long_strict_light
Reference values were user-provided from the MDD workflow output.
Base for this lane = long_strict_light baseline
- final_return_pct = 747.4158
- pf = 1.171075
- mdd_pct = -54.3699
- max_conc = 389

MDD lane results
1. timeout_18bars
- final_return_pct = 765.7315
- pf = 1.188958
- mdd_pct = -48.4157
- max_conc = 389
- interpretation: dominant single result in this lane. It improved return, PF, and MDD at the same time.

2. long_strict_stronger
- final_return_pct = 684.7968
- pf = 1.197069
- mdd_pct = -48.5228
- max_conc = 367
- interpretation: strongest PF in the MDD lane and one of the only candidates that materially reduced concurrency. Return fell, but still stayed relatively high.

3. cooldown_3bars
- final_return_pct = 302.7443
- pf = 1.130033
- mdd_pct = -49.5813
- max_conc = 388
- interpretation: MDD improved, but return collapsed too much.

4. cooldown_2bars
- final_return_pct = 321.9644
- pf = 1.129168
- mdd_pct = -50.7598
- max_conc = 388
- interpretation: also too destructive to return.

5. baseline
- final_return_pct = 747.4158
- pf = 1.171075
- mdd_pct = -54.3699
- max_conc = 389

6. timeout_24bars
- final_return_pct = 710.2555
- pf = 1.174928
- mdd_pct = -55.0378
- max_conc = 389
- interpretation: lost to baseline on MDD.

MDD ranking by MDD quality
1. timeout_18bars
2. long_strict_stronger
3. cooldown_3bars
4. cooldown_2bars
5. baseline
6. timeout_24bars

MDD ranking by return
1. timeout_18bars
2. baseline
3. timeout_24bars
4. long_strict_stronger
5. cooldown_2bars
6. cooldown_3bars

Current cross-lane interpretation
- Best balance-oriented candidate from combos: plus_timeout_30bars
- Best MDD-oriented candidate overall so far: timeout_18bars
- Best concurrency-reduction candidate so far: long_strict_stronger

What matters most now
timeout_18bars is currently the strongest direct candidate because it beat the long_strict_light baseline on both return and MDD simultaneously.
However, it did not reduce max_conc.
long_strict_stronger is important because it reduced max_conc to 367 while still keeping a strong PF and acceptable return.
Therefore the next highest-value combined test is likely:
- long_strict_stronger + timeout_18bars
and then, possibly,
- long_strict_stronger + short_stricter + timeout_18bars

Practical ranked list of current strongest directions
1. timeout_18bars
2. long_strict_stronger
3. plus_timeout_30bars
4. plus_short_stricter_timeout_30bars
5. plus_short_stricter
6. short_stricter
7. timeout_30bars
Reject / deprioritize
- cooldown_6bars
- cooldown_2bars
- cooldown_3bars as primary candidates
- tp_min_0045
- tp_min_006
- timeout_24bars
