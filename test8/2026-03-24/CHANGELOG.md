# CHANGELOG

## 2026-03-24
- Added TEST8 documentation pack
- Added benchmark strategy note: overextension_reversion_v1
- Added benchmark summary metrics and rebalanced note
- Added strategy attempt log and failure patterns
- Added common indicator/evaluator modules
- Added benchmark runner and candidate batch runner template
- Added data inventory summary from actual local rerun
- Added actual rerun outputs for benchmark strategy (aggregate/per-symbol/raw trades split files to follow)

## Important note
There are two benchmark result layers in TEST8:
1. Confirmed conversation benchmark note
2. Actual reconstructed rerun result from local execution
Keep both. The first preserves session memory; the second is the reproducible rerun baseline.
