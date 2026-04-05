# 관련 파일 / 워크플로우 지도

## 1. 결과를 공식적으로 참고할 디렉터리

### v22 revalidation
- results_json_only_timeout18_time_reduce_v22_strict_revalidate/

### v23 revalidated improvement
- results_json_only_timeout18_time_reduce_v23_strict_revalidated/

### v24 lanes
- results_json_only_timeout18_time_reduce_v24_1_strict_revalidated/
- results_json_only_timeout18_time_reduce_v24_2_strict_revalidated/
- results_json_only_timeout18_time_reduce_v24_3_strict_revalidated/

주의:
- v24 original workflows는 None threshold 비교 버그가 있었다.
- 실제 rerun은 FIX 워크플로우를 사용했음을 기억할 것.
- 재실행 시 original 24-x 대신 FIX 계열 사용 여부를 먼저 확인할 것.

### v25 diagnostics
- results_json_only_timeout18_time_reduce_v25_strict_diagnostics/

중요 파일:
- diagnostics_summary.csv
- revalidated_baseline_top200/candidate_count_distribution.csv
- revalidated_baseline_top200/selection_quality_summary.csv
- revalidated_baseline_top200/rank_bucket_quality.csv
- revalidated_baseline_top200/top_candidate_burst_timestamps.csv

### v26 hardened score
- results_json_only_timeout18_time_reduce_v26_strict_score/

### v27 top200 replacement attempts
- results_json_only_timeout18_time_reduce_v27_strict_score_replace_topn/

## 2. 실험 설정 파일

### v22
- experiments/base_config_json_only_timeout18_time_reduce_v22_strict_revalidate.json
- experiments/combinations_json_only_timeout18_time_reduce_v22_strict_revalidate.json

### v23
- experiments/base_config_json_only_timeout18_time_reduce_v23_strict_revalidated.json
- experiments/combinations_json_only_timeout18_time_reduce_v23_strict_revalidated.json

### v24
- experiments/base_config_json_only_timeout18_time_reduce_v24_1_strict_revalidated.json
- experiments/combinations_json_only_timeout18_time_reduce_v24_1_strict_score.json
- experiments/base_config_json_only_timeout18_time_reduce_v24_2_strict_revalidated.json
- experiments/combinations_json_only_timeout18_time_reduce_v24_2_strict_cd.json
- experiments/base_config_json_only_timeout18_time_reduce_v24_3_strict_revalidated.json
- experiments/combinations_json_only_timeout18_time_reduce_v24_3_strict_mdd.json

### v25
- experiments/base_config_json_only_timeout18_time_reduce_v25_strict_diagnostics.json
- experiments/combinations_json_only_timeout18_time_reduce_v25_strict_diagnostics.json

### v26
- experiments/base_config_json_only_timeout18_time_reduce_v26_strict_score.json
- experiments/combinations_json_only_timeout18_time_reduce_v26_strict_score.json

### v27
- experiments/base_config_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.json
- experiments/combinations_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.json

## 3. 주요 러너 파일

- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v22_strict_revalidate.py
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v23_strict_revalidated.py
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v24_strict_revalidated.py
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v24_strict_revalidated_fixed.py
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v25_strict_diagnostics.py
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v26_strict_score.py
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py

## 4. 주요 워크플로우 이름

### v22
22V Repository Backtest JSON Only Timeout18 Time Reduce V22 Strict Revalidate Repo Assets Fixed

### v23
23V Repository Backtest JSON Only Timeout18 Time Reduce V23 Strict Revalidated Repo Assets Fixed

### v24
주의: 가능하면 FIX 계열 사용

- 24-1V FIX Repository Backtest JSON Only Timeout18 Time Reduce V24-1 Strict Revalidated Repo Assets Fixed
- 24-2V FIX Repository Backtest JSON Only Timeout18 Time Reduce V24-2 Strict Revalidated Repo Assets Fixed
- 24-3V FIX Repository Backtest JSON Only Timeout18 Time Reduce V24-3 Strict Revalidated Repo Assets Fixed

### v25
25V Repository Backtest JSON Only Timeout18 Time Reduce V25 Strict Diagnostics Repo Assets Fixed

### v26
26V Repository Backtest JSON Only Timeout18 Time Reduce V26 Strict Score Repo Assets Fixed

### v27
27V Repository Backtest JSON Only Timeout18 Time Reduce V27 Strict Score Replace TopN Repo Assets Fixed

## 5. 다음 어시스턴트가 바로 확인할 우선 파일 순서

1. test10/00_INDEX.md
2. test10/01_NONNEGOTIABLES_AND_ENGINE_VALIDATION.md
3. test10/02_V22_TO_V27_TIMELINE.md
4. test10/03_CURRENT_BASELINES_AND_INTERPRETATION.md
5. test10/04_TOP200_DIAGNOSTICS_AND_SCORE_DIRECTION.md
6. test10/06_NEXT_STEPS_V28_RUNBOOK.md
7. results_json_only_timeout18_time_reduce_v27_strict_score_replace_topn/master_summary.csv
8. results_json_only_timeout18_time_reduce_v25_strict_diagnostics/revalidated_baseline_top200/*.csv

## 6. 실행 전 체크리스트

- pre-v22 기준선 재사용 금지 확인
- fee_per_side = 0.0004 확인
- same-bar revalidated 엔진 사용 여부 확인
- topN을 공식 정답처럼 밀어붙이지 말 것
- top200 제거 대체 실험이면 official_top200_reference는 비교선으로만 두고, 신규 후보에는 topN을 넣지 말 것
