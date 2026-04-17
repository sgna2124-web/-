# STRATEGY REGISTRY

이 문서는 전략들을 '전략 카드'처럼 등록하는 중앙 등록부다.
새 전략을 만들면 최소 1줄이라도 여기에 추가한다.

## 작성 형식
- strategy_id:
- side: long_only / short_only / mixed
- family:
- concept:
- core_filters:
- entry_logic:
- exit_logic:
- risk_logic:
- expected_edge:
- known_strengths:
- known_weaknesses:
- result_path:
- code_path:
- status: active / archived / failed / needs_retest
- notes:

---

## 예시 등록

### official_top200_reference
- strategy_id: official_top200_reference
- side: mixed
- family: top-ranked candidate selection
- concept: top200 기반 후보 선택과 비대칭 guard를 활용한 혼합형 기준선
- core_filters: top200 selection, hardened score 계열, quality guard 계열
- entry_logic: 기존 mixed baseline 계열 참조
- exit_logic: 기존 러너 기준
- risk_logic: same-bar revalidated 엔진, 수수료 0.0004, 동시 포지션 분할 반영
- expected_edge: 전체 수익성과 균형
- known_strengths: 현재 mixed 탐색 역사에서 종합 기준선으로 강했음
- known_weaknesses: MDD가 매우 큼, 현재 최종 목표(MDD 5% 미만)와 거리 멂
- result_path: results_json_only_timeout18_time_reduce_v23_strict_revalidated/ 또는 v26/v27 비교 문서 참고
- code_path: 관련 v23~v27 러너 참조
- status: archived_reference
- notes: 현재 long/short 단독 프로젝트의 직접 정답은 아니지만 비교 문화의 기점

### score_l16_s20_shortheavy
- strategy_id: score_l16_s20_shortheavy
- side: mixed
- family: non-top200 replacement attempt
- concept: short threshold를 더 엄격하게 둔 절대 score 컷 대체 실험
- core_filters: absolute score threshold, short-heavy bias
- entry_logic: 기존 v27 계열 참조
- exit_logic: 기존 러너 기준
- risk_logic: MDD와 max_conc 개선이 미흡
- expected_edge: top200 제거 후에도 수익 보존
- known_strengths: 대체 후보 중 수익 보존율 우수
- known_weaknesses: MDD 악화, max_conc 악화
- result_path: results_json_only_timeout18_time_reduce_v27_strict_score_replace_topn/
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py
- status: archived_candidate
- notes: 구조적 힌트는 남지만 최종 채택 아님

## LONG ONLY / SHORT ONLY 등록 구역

### LONG_ONLY_OFFICIAL_1
- strategy_id: TODO
- side: long_only
- family: TODO
- concept: TODO
- core_filters: TODO
- entry_logic: TODO
- exit_logic: TODO
- risk_logic: TODO
- expected_edge: TODO
- known_strengths: TODO
- known_weaknesses: TODO
- result_path: TODO
- code_path: TODO
- status: active_baseline
- notes: 현재 롱 공식 1위를 여기에 기록

### SHORT_ONLY_OFFICIAL_1
- strategy_id: TODO
- side: short_only
- family: TODO
- concept: TODO
- core_filters: TODO
- entry_logic: TODO
- exit_logic: TODO
- risk_logic: TODO
- expected_edge: TODO
- known_strengths: TODO
- known_weaknesses: TODO
- result_path: TODO
- code_path: TODO
- status: active_baseline
- notes: 현재 숏 공식 1위를 여기에 기록
