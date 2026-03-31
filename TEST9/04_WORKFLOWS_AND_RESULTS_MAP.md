워크플로와 결과 폴더 맵

기본 실행 규칙
- 거의 모든 최신 레인은 workflow_dispatch + repo_assets_5m 입력으로 실행한다.
- 입력값은 보통 repo_data_dir = repo_assets_5m 로 둔다.
- 결과는 각 results_json_only_timeout18_* 폴더 아래 master_summary.csv/json/txt 및 실험별 summary.json 으로 저장된다.

최근 핵심 레인과 결과 폴더
1. Time Reduce V4
- workflow: Repository Backtest JSON Only Timeout18 Time Reduce V4 Repo Assets Fixed
- results dir: results_json_only_timeout18_time_reduce_v4
- 현재 최신 1위가 나온 레인

2. Time Reduce V3
- workflow: Repository Backtest JSON Only Timeout18 Time Reduce V3 Repo Assets Fixed
- results dir: results_json_only_timeout18_time_reduce_v3
- v4 직전 1위가 나온 레인

3. Time Reduce V2
- workflow: Repository Backtest JSON Only Timeout18 Time Reduce V2 Repo Assets Fixed
- results dir: results_json_only_timeout18_time_reduce_v2

4. Time Reduce Refine
- workflow: Repository Backtest JSON Only Timeout18 Time Reduce Refine Repo Assets Fixed
- results dir: results_json_only_timeout18_time_reduce_refine

5. Attack V2
- workflow: Repository Backtest JSON Only Timeout18 Attack V2 Repo Assets Fixed
- results dir: results_json_only_timeout18_attack_v2

6. Attack Refine
- workflow: Repository Backtest JSON Only Timeout18 Attack Refine Repo Assets Fixed
- results dir: results_json_only_timeout18_attack_refine

7. EMA ATR Refine
- workflow: Repository Backtest JSON Only Timeout18 EMA ATR Refine Repo Assets Fixed
- results dir: results_json_only_timeout18_ema_atr_refine

8. EMA Structure Refine
- workflow: Repository Backtest JSON Only Timeout18 EMA Structure Refine Repo Assets Fixed
- results dir: results_json_only_timeout18_ema_structure_refine

9. EMA Target Refine
- workflow: Repository Backtest JSON Only Timeout18 EMA Target Refine Repo Assets Fixed
- results dir: results_json_only_timeout18_ema_target_refine

10. Stopshape
- workflow: Repository Backtest JSON Only Timeout18 Stopshape Repo Assets Fixed
- results dir: results_json_only_timeout18_stopshape

11. Hybrid Stack
- workflow: Repository Backtest JSON Only Timeout18 Hybrid Stack Repo Assets Fixed
- results dir: results_json_only_timeout18_hybrid_stack

결과 읽는 순서
- 각 레인 실행 후 master_summary.csv 를 먼저 본다.
- 그다음 상위 실험의 summary.json 을 필요 시 열어 effective_config 를 확인한다.
- 전체 순위 재정렬은 여러 results_json_only_timeout18_* 폴더의 master_summary.csv 를 모아서 수행한다.

중요 메모
- 과거에 workflow 파일이 main에 없어서 Actions 탭에 안 보인 적이 있었다.
- 다음 대화창에서는 새 레인을 만들면 반드시 아래 세 파일 세트를 같이 만들 것.
  1. experiments/base_config_*.json
  2. experiments/combinations_*.json
  3. scripts/run_backtest_batch_*.py
  4. scripts/summarize_results_*.py
  5. .github/workflows/*_repo_assets_fixed.yml
- 이 다섯 세트 중 workflow가 빠지면 Actions에서 안 보인다.

실무 팁
- 동시 실행 시 push 충돌 가능성이 있으니 fixed workflow 패턴을 유지한다.
- 결과 커밋이 안 생기거나 workflow가 안 보이면 먼저 main 기준 파일 존재 여부를 확인한다.
