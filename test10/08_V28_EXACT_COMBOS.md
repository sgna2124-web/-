# v28 확정 실험 조합

목적:
- top200 제거 대체축을 좁고 날카롭게 재검증한다.
- v27 최선 후보 `score_l16_s20_shortheavy`를 중심으로 threshold, short-only soft asym, weight, wick normalization만 조정한다.
- fail-fast, top250/300, wick_or_atr 주력화는 제외한다.

기준선
- official_top200_reference

후보 12개

## 1. short threshold 미세조정 5개
- score_l16_s19_shortheavy
- score_l16_s20_shortheavy
- score_l16_s21_shortheavy
- score_l155_s20_shortheavy
- score_l165_s20_shortheavy

## 2. short-only soft asym 3개
- soft_asym_short_score_l16_s19
- soft_asym_short_score_l16_s20
- soft_asym_short_score_l16_s21

soft asym 의미:
- long side는 그대로 유지
- short side만 quality guard를 약하게 강화
- short_dev 0.033, short_rsi_min 77

## 3. weight 조정 2개
- score_l16_s20_shortheavy_wick06
- score_l16_s20_shortheavy_rsi10

## 4. wick normalization 조정 2개
- score_l16_s20_shortheavy_atr020
- score_l16_s20_shortheavy_atr025_cap22

권장 판정 순서
1. 수익 보존율
2. MDD 악화/개선
3. max_conc 억제 여부
4. PF 개선 여부
5. official_top200_reference 대체 가능성

실행 파일
- experiments/base_config_json_only_timeout18_time_reduce_v28_strict_score_replace_topn.json
- experiments/combinations_json_only_timeout18_time_reduce_v28_strict_score_replace_topn.json
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v28_strict_score_replace_topn.py
- scripts/summarize_results_json_only_timeout18_time_reduce_v28_strict_score_replace_topn.py
- .github/workflows/backtest_json_only_timeout18_time_reduce_v28_strict_score_replace_topn_repo_assets_fixed.yml
