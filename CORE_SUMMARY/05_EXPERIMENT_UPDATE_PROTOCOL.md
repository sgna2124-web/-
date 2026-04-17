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

## 비교 출력 기본 형식
- compare_target:
- experiment_name:
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

## 파일 업데이트 순서
실험 종료 후 아래 순서로 업데이트한다.
1. 결과 폴더 저장
2. 전략 코드 저장
3. CORE_SUMMARY/04_STRATEGY_REGISTRY.md 갱신
4. 새 1위면 CORE_SUMMARY/03_CURRENT_BASELINES.md 갱신
5. 상세 분석은 해당 test 폴더 또는 새 실험 폴더에 저장

## 네이밍 규칙
- 워크플로우 이름은 사용자가 지정한 규칙을 따른다.
- 예: 1V2, 2V2 등 버전 선두 prefix 유지
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
