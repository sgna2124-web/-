# Current Integrated 1st 4-Leader Anomaly Score Report

- generated_at: 2026-04-29 11:25:26
- repo_root: C:\Users\user\Desktop\LCD\파이썬
- capital: 1,000,000
- profit_target: 1,000,000
- mdd_limit: 20.00%
- sparse_trade_threshold: 3

## Ranking

| rank | strategy | score | grade | decision | active_symbols | total_trades | mean_profit_est | max_mdd | target_hit | mdd_violation | anomalies |
|---:|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | short_beh_dd_brake | 27.52 | D | REJECT_LOW_TARGET_HIT | 209 | 1620 | 0 | 26.50% | 0.00% | 2.87% | MDD_LIMIT_EXCEEDED max_mdd=26.50% > 20.00% | LOW_TARGET_HIT ratio=0.00% | LOW_PROFITABLE_SYMBOL_RATIO ratio=0.00% |
| 2 | 6V2_L01_doubleflush_core | 21.75 | D | REJECT_LOW_TARGET_HIT | 294 | 592 | 0 | 20.29% | 0.00% | 0.34% | MDD_LIMIT_EXCEEDED max_mdd=20.29% > 20.00% | SPARSE_TRADE_FRAGILITY ratio=74.49% | LOW_TARGET_HIT ratio=0.00% | LOW_PROFITABLE_SYMBOL_RATIO ratio=0.00% |
| 3 | 8V4_V51_V002_core_rare22_c1 | 19.84 | D | REJECT_LOW_TARGET_HIT | 477 | 2276 | 0 | 30.95% | 0.00% | 0.21% | MDD_LIMIT_EXCEEDED max_mdd=30.95% > 20.00% | LOW_TARGET_HIT ratio=0.00% | LOW_PROFITABLE_SYMBOL_RATIO ratio=0.00% |
| 4 | short_only_reference_1x | 0.00 | D | REJECT_RISK | 223 | 4398 | 0 | 58.11% | 0.00% | 22.87% | MDD_LIMIT_EXCEEDED max_mdd=58.11% > 20.00% | LOW_TARGET_HIT ratio=0.00% | LOW_PROFITABLE_SYMBOL_RATIO ratio=0.00% |

## Interpretation

- KEEP_CORE: 현 기준에서 코어 유지 후보.
- KEEP_WITH_GUARD: 유지 가능하지만 MDD/희소거래/종목편중 가드 필요.
- REVIEW: 다음 개선 대상. 원인 분해 후 조건 추가 또는 비중 축소 판단.
- REJECT_RISK: MDD 기준 초과가 커서 현 기준선에는 부적합.
- REJECT_LOW_TARGET_HIT: 목표 수익 달성 빈도가 낮아 현 목표와 맞지 않음.

## Result Directories

- short_beh_dd_brake: `C:\Users\user\Desktop\LCD\파이썬\local_results\8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP\short_main_v1_100_sm12_dd_sanitizer_sm12_4_19`
- 6V2_L01_doubleflush_core: `C:\Users\user\Desktop\LCD\파이썬\local_results\6V2_LONG10_REVIEWED\6V2_L01_doubleflush_core`
- 8V4_V51_V002_core_rare22_c1: `C:\Users\user\Desktop\LCD\파이썬\local_results\8V4_LONG400_REVIEWED\8V4_V51_V002_core_rare22_c1`
- short_only_reference_1x: `C:\Users\user\Desktop\LCD\파이썬\local_results\8V12_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP\short_max_v1_100_sx12_asymmetric_trail_sx12_4_19`
