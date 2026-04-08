# TEST10 인수인계 인덱스

이 폴더는 다음 대화창의 어시스턴트가 바로 읽고 이어가기 위한 운영 문서다.
사용자에게 보여주기 위한 문서가 아니라, 다음 실험자가 빠르게 현재 상태를 파악하고 같은 실수를 반복하지 않기 위한 문서다.

핵심 결론만 먼저 적는다.

1. 현재 공식 비교 기준선은 `official_top200_reference`다.
   - 최근 기준 수치: final_return_pct 1120.69995, pf 1.2199649, mdd_pct -36.03441, max_conc 271
   - 단, top200 규칙 자체는 구조적 신뢰가 아직 약하다. 성과는 가장 좋지만, 메커니즘은 아직 충분히 증명되지 않았다.

2. pre-v22 시기의 상위 결과는 최종 기준으로 신뢰하면 안 된다.
   - same-timestamp(entry/exit 같은 시각) 처리 문제로 max_conc와 수익률이 과장된 구간이 있었다.
   - 반드시 v22 revalidation 이후 결과만 공식 기준으로 취급한다.

3. 현재 가장 중요한 전략적 긴장점은 다음 두 가지다.
   - top200은 현재까지 가장 높은 성과를 주는 기준선이다.
   - 그러나 top200은 실제로 매우 드문 burst 시점에서만 작동하고, 잘려나간 거래들이 명확히 더 나쁘다는 증거가 약하다.
   - 따라서 top200은 현재 “최고 성과의 임시 기준선”이지 “최종 배포 규칙”이 아니다.

4. v26, v27까지의 결론
   - hardened absolute score 절대 컷만으로는 아직 top200 대체 실패
   - top200 제거 후보 중 최선은 `score_l16_s20_shortheavy`
   - top200 제거 대체축을 계속 탐색하려면 이 축을 중심으로 이어간다.

5. 다음 단계 권장
   - v28에서 top200 없는 대체축만 집중 탐색
   - 주축: `score_l16_s20_shortheavy`, `asym_guard_score_l16_s20_shortheavy`
   - 조정 대상: short threshold, long/short quality guard, hardened score 가중치, wick/ATR 정규화 강도
   - fail-fast는 현재까지 성과가 약하므로 후순위 혹은 제외

문서 안내

- 01_NONNEGOTIABLES_AND_ENGINE_VALIDATION.md
  반드시 지켜야 할 원칙, 엔진 오류 이력, 재검증 기준

- 02_V22_TO_V27_TIMELINE.md
  v22~v27 결과 흐름과 해석

- 03_CURRENT_BASELINES_AND_INTERPRETATION.md
  현재 공식 기준선, 방어형 후보, top200 없는 최선 후보 정리

- 04_TOP200_DIAGNOSTICS_AND_SCORE_DIRECTION.md
  top200 의심 근거, v25 진단 결과, score 재정의 방향

- 05_SKIP_LIST_AND_FAILED_DIRECTIONS.md
  이미 해봤고 우선순위 낮거나 실패한 방향 목록

- 06_NEXT_STEPS_V28_RUNBOOK.md
  다음 대화창에서 바로 이어갈 v28 실험 제안

- 07_FILE_AND_WORKFLOW_MAP.md
  관련 실험 파일/워크플로우 지도

- 99_STATE_SNAPSHOT.json
  현재 상태를 기계적으로 빠르게 읽기 위한 요약 스냅샷
