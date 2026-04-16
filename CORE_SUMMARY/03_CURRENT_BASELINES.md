# CURRENT BASELINES

이 문서는 '현재 무엇을 공식 비교 기준선으로 볼 것인가'를 적는 중앙 문서다.
새로운 롱 1위/숏 1위가 나오면 가장 먼저 이 파일을 갱신한다.

## A. 기존 혼합 탐색 구간에서 확인된 주요 기준선

### official_top200_reference
- final_return_pct: 1120.69995
- pf: 1.2199649
- mdd_pct: -36.03441
- max_conc: 271
- 해석: v23 baseline_top200 이후 v26/v27까지도 종합 성과 기준 가장 강했던 비교선
- 주의: 이것은 과거 mixed 탐색의 강한 기준선일 뿐, 현재 프로젝트의 최종 목적(MDD 5% 미만 cd_value 최고)의 정답은 아님

### asym_guard_top200
- final_return_pct: 1030.7929
- pf: 1.2327923
- mdd_pct: -35.22274
- max_conc: 269
- 해석: 공식 기준선보다 방어/균형형 참고선으로 의미가 있었음

### asym_guard_top150
- final_return_pct: 898.76
- pf: 1.21856
- mdd_pct: -32.53
- max_conc: 269
- 해석: MDD 방어형 기준선 참고용

### score_l16_s20_shortheavy
- final_return_pct: 1089.0657
- pf: 1.2242424
- mdd_pct: -41.06885
- max_conc: 386
- 해석: top200 제거 상태에서 수익 보존율이 높았던 유력 대체 후보
- 한계: MDD와 max_conc 악화로 공식 대체 성공은 아님

## B. 현재 롱 전용 / 숏 전용 공식 기준선

주의:
- 이 섹션은 앞으로 프로젝트의 공식 비교 기준선이 된다.
- 현재 값이 확정되면 아래에 전략명, 결과, cd_value, 경로를 기록한다.
- 아직 최신 값 정리가 끝나지 않았다면 임시로 TODO 상태를 둔다.

### LONG_ONLY_OFFICIAL_1
- strategy_name: TODO
- source_path: TODO
- final_return_pct: TODO
- mdd_pct: TODO
- cd_value: TODO
- max_conc: TODO
- notes: 앞으로 새 롱 전략은 반드시 이 값과 비교

### SHORT_ONLY_OFFICIAL_1
- strategy_name: TODO
- source_path: TODO
- final_return_pct: TODO
- mdd_pct: TODO
- cd_value: TODO
- max_conc: TODO
- notes: 앞으로 새 숏 전략은 반드시 이 값과 비교

## C. 갱신 규칙
- 새 롱 전략이 기존 LONG_ONLY_OFFICIAL_1보다 우수하면 즉시 교체
- 새 숏 전략이 기존 SHORT_ONLY_OFFICIAL_1보다 우수하면 즉시 교체
- 우수 판정은 MDD 우선, 그 다음 cd_value, 그 다음 final_return_pct 순서로 판단
- 교체 시 이전 1위는 ARCHIVED_BASELINES 섹션 또는 별도 아카이브 문서로 이동

## D. TODO
- 저장소 내 최신 long-only / short-only 결과를 추려 위 빈칸을 채울 것
- long/short 전용 1위의 코드 경로와 결과 폴더 경로를 같이 명시할 것
