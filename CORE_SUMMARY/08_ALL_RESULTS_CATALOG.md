# ALL RESULTS CATALOG

이 문서는 현재 1위만 적는 문서가 아니라,
지금까지 시도한 모든 전략/실험 결과를 파일 경로와 함께 누적 기록하는 원장이다.

핵심 원칙:
- 평가 우선순위가 바뀌어도 이 원장을 다시 정렬하면 된다.
- 따라서 모든 실험은 좋든 나쁘든 여기 남긴다.
- 새 결과를 업로드하면 이 문서를 같이 갱신한다.

## 기록 필드 정의
- experiment_id: 실험 고유 이름
- version_prefix: 1V2, 2V2 등
- side: long_only / short_only / mixed
- strategy_name: 전략명
- family: 전략 계열
- status: promoted / candidate / hold / failed / invalid / archived
- code_path: 코드 파일 경로
- config_path: 설정 파일 경로
- result_path: 결과 폴더 경로
- summary_file: master_summary 또는 대표 요약 파일 경로
- final_return_pct:
- mdd_pct:
- cd_value:
- pf:
- win_rate:
- max_conc:
- compare_target:
- verdict_reason:
- notes:

## 정렬 원칙
기본 열람 순서는 아래처럼 본다.
1. side 구분
2. status
3. 현재 공식 우선 기준(MDD -> cd_value -> final_return_pct)

단, 우선 가치가 바뀌면 이 원장을 기준으로 재평가한다.
예시:
- MDD 최우선 체계
- cd_value 최우선 체계
- max_conc 제한 체계
- PF 안정성 체계

## 기록 양식
| experiment_id | version_prefix | side | strategy_name | family | status | code_path | config_path | result_path | summary_file | final_return_pct | mdd_pct | cd_value | pf | win_rate | max_conc | compare_target | verdict_reason | notes |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| official_top200_reference | legacy | mixed | official_top200_reference | top-ranked candidate selection | archived | scripts/run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py | experiments/v27_strict_score_replace_topn_combinations.json | results_json_only_timeout18_time_reduce_v23_strict_revalidated/ 또는 관련 비교 문서 참조 | test10/03_CURRENT_BASELINES_AND_INTERPRETATION.md | 1120.69995 | -36.03441 | TODO | 1.2199649 | TODO | 271 | mixed historical baseline | 과거 mixed 종합 기준선으로 의미 | 장기 최종목표와 직접 일치하지는 않음 |
| asym_guard_top200 | legacy | mixed | asym_guard_top200 | asymmetric guard baseline | archived | 관련 v26/v27 러너 참조 | 관련 실험 JSON 참조 | test10 기준선 문서 참조 | test10/03_CURRENT_BASELINES_AND_INTERPRETATION.md | 1030.7929 | -35.22274 | TODO | 1.2327923 | TODO | 269 | official_top200_reference | 방어형 참고선 | mixed 참고용 |
| score_l16_s20_shortheavy | legacy | mixed | score_l16_s20_shortheavy | non-top200 replacement attempt | archived_candidate | scripts/run_backtest_batch_json_only_timeout18_time_reduce_v27_strict_score_replace_topn.py | experiments/v27_strict_score_replace_topn_combinations.json | results_json_only_timeout18_time_reduce_v27_strict_score_replace_topn/ | results_json_only_timeout18_time_reduce_v27_strict_score_replace_topn/master_summary.json | 1089.0657 | -41.06885 | TODO | 1.2242424 | TODO | 386 | official_top200_reference | 수익 보존은 좋았으나 MDD와 max_conc 열세 | 대체 실패이지만 힌트는 남김 |
| LONG_ONLY_OFFICIAL_1 | TODO | long_only | TODO | TODO | active_baseline | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | 현재 롱 공식 1위 자리 | 최신 long-only 결과 반영 필요 |
| SHORT_ONLY_OFFICIAL_1 | TODO | short_only | TODO | TODO | active_baseline | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | 현재 숏 공식 1위 자리 | 최신 short-only 결과 반영 필요 |

## 업데이트 규칙
- 새 실험 결과를 업로드하면 반드시 한 줄 추가한다.
- 새 1위가 나오면 status와 compare_target을 갱신한다.
- 폐기 전략도 지우지 않고 status만 failed/archived로 남긴다.
- 수치가 일부 비어 있으면 TODO로 남기되, 경로는 반드시 적는다.

## 역할 분담
- 사용자: 로컬에서 백테스트 실행, 코드와 결과 업로드
- 어시스턴트: 업로드된 정보들을 취합하여 이 원장과 기준선 문서를 갱신
