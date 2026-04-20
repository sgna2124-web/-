# EXPERIMENT UPDATE PROTOCOL

## 실험 하나를 끝냈을 때 반드시 남길 것
1. 실험 이름
2. side(long_only / short_only / mixed)
3. 이전 기준선 이름
4. 변경한 요소
5. 기대 효과
6. 결과 요약
7. 판정(승격 / 보류 / 폐기)
8. 후속 액션
9. 장점
10. 단점

## 비교 출력 기본 형식
- compare_target:
- experiment_name:
- max_return_pct:
- final_return_pct:
- mdd_pct:
- cd_value:
- pf:
- max_conc:
- delta_vs_baseline:
- verdict:
- one_line_reason:

## 승격 규칙
- 롱 전략이면 LONG_ONLY_OFFICIAL_1과 비교
- 숏 전략이면 SHORT_ONLY_OFFICIAL_1과 비교
- mixed 전략이면 현재 참고 mixed 기준선과 비교하되, long/short 단독 프로젝트에 주는 시사점을 별도 기재
- 공식 판정 순서는 반드시 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 순으로 해석한다

## 파일 업데이트 순서
실험 종료 후 아래 순서로 업데이트한다.
1. 결과 폴더 저장
2. 전략 코드 저장
3. CORE_SUMMARY/04_STRATEGY_REGISTRY.md 갱신
4. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md에 이번 실험 결과를 추가
5. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md에 이번 실험의 장점/단점 요약을 추가 또는 기존 항목 보강
6. 새 1위면 CORE_SUMMARY/03_CURRENT_BASELINES.md 갱신
7. 기준 정의와 충돌이 생기면 CORE_SUMMARY/01_OBJECTIVE_AND_METRICS.md와 CORE_SUMMARY/10_BASELINE_PATCH_2026-04-16.md를 함께 정정
8. 상세 분석은 해당 test 폴더 또는 새 실험 폴더에 저장

## 매우 중요한 운영 규칙
- 사용자가 백테스트를 돌리고 결과를 저장소에 올린 뒤에는, 다음 세션의 내가 반드시 결과 정리와 CORE_SUMMARY 갱신까지 수행해야 한다.
- 결과를 확인만 하고 문서 업데이트를 건너뛰면 인수인계 실패로 간주한다.
- local_results 커밋과 CORE_SUMMARY 갱신 커밋이 분리되더라도, 대화 흐름상 같은 실험이면 세트로 처리한다.

## 네이밍 규칙
- 워크플로우 이름은 사용자가 지정한 규칙을 따른다.
- 예: 1V2, 2V2, 4V2R9 등 버전 선두 prefix 유지
- 코드 파일/결과 폴더/실험 문서도 가능하면 같은 버전 prefix를 맞춘다.

## 판정 레이블 정의
- promoted: 기존 공식 1위를 교체함
- candidate: 의미 있는 개선 가능성이 있어 후속 실험 필요
- hold: 결과는 나쁘지 않지만 우선순위 낮음
- failed: 기준선 대비 명확히 열세
- invalid: 엔진/데이터/검증 문제로 결과 무효

## 한 줄 평가 규칙
반드시 결과마다 '왜 이 실험을 기억해야 하는가'를 한 줄로 남긴다.
예시:
- MDD는 개선됐지만 cd_value 열세라 승격 실패
- 수익 보존은 좋았으나 동시 포지션 급증으로 실전성 악화
- 구조는 신선하지만 재현성 검증 전까지 무효
- 리스크는 안정적이었지만 max_return이 충분히 뻗지 못해 승격 실패
