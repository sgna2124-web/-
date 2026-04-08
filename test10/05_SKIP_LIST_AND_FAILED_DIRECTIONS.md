# 우선순위 낮음 / 이미 약했음 / 반복 금지 목록

## 1. pre-v22 상위 결과를 다시 기준선으로 올리는 것
금지.
이 구간은 same-bar 누수 이전 결과가 섞여 있어 공식 기준선으로 재사용하면 안 된다.

## 2. wick_or_atr 계열을 주력 축으로 다시 미는 것
v23 revalidated 기준에서 wick_or_atr 계열은 특별한 우위가 없었다.
- wick_or_atr_baseline: MDD와 max_conc 개선도 약했고 수익 우위도 없었음
- long/asym_guard_wick_or_atr도 주력 승격 실패

결론:
- 완전 폐기는 아니지만 우선순위 낮음
- 새 대화창에서는 주력 축으로 삼지 말 것

## 3. top250 / top300으로 느슨하게 풀어 cd_value를 올리려는 것
v24-2에서 실패.
- baseline_top250, baseline_top300 모두 공식 기준선을 넘지 못함
- 수익이 더 좋아지지 않았고 MDD는 악화됨

결론:
- “느슨하게 풀면 더 번다”는 가정은 현재까지 실패
- 근거 없이 topN을 더 키우는 실험 반복 금지

## 4. 강한 score floor 단독 구조
v24-1, v24-3, v26, v27에서 반복적으로 확인됨.
- 점수 필터를 강하게 걸수록 MDD는 줄 수 있으나 수익 훼손이 큼
- 절대 score 컷 단독으로는 아직 공식 기준선 대체 실패

결론:
- score floor 단독 강경 버전은 현재 후순위
- 필요해도 약하게 혹은 보조 구조로만 사용

## 5. fail-fast를 주력 개선축으로 삼는 것
현재까지 일관되게 약했다.
- v24, v27 모두 fail-fast 결합이 수익을 더 깎고 MDD 개선도 뚜렷하지 않았음

결론:
- fail-fast는 현재 후순위 혹은 제외
- 다시 써도 보조 실험 정도로만 취급

## 6. top200을 이미 증명된 정답처럼 취급하는 것
금지.
v25 진단에서 확인된 내용:
- 200 초과 후보 시점은 47,282개 중 13개뿐
- 잘려나간 거래가 명확히 더 나쁘다는 증거도 약함

결론:
- top200은 현재 성과 기준선일 뿐
- 논리적/구조적 최종 정답처럼 다루면 안 됨

## 7. score를 현재 형태 그대로 절대 규칙으로 확정하는 것
금지.
이유:
- hardened score는 방향성은 좋지만 아직 top200 대체 실패
- 가중치, short-heavy threshold, wick normalization을 더 다듬어야 함

## 8. 사용자가 싫어하는 접근
다음 어시스턴트는 아래 행동을 피할 것.

- 성과가 좋다고 검증을 건너뛰는 것
- 이상한 지표가 나와도 그냥 다음 실험으로 넘어가는 것
- 실거래 관점의 구현 가능성을 무시하는 것
- 설명하기 어려운 cross-sectional cap을 최종 규칙처럼 밀어붙이는 것

## 9. 현재 기준에서 상대적으로 살아 있는 것 / 죽은 것

상대적으로 살아 있는 것:
- official_top200_reference (성능 기준선)
- asym_guard_top200 (방어형 기준)
- asym_guard_top150 (MDD practical defense 기준)
- score_l16_s20_shortheavy (top200 제거 대체 최선 후보)
- asym_guard_score_l16_s20_shortheavy (PF 강화된 대체 후보)

상대적으로 죽은 것 / 우선순위 낮은 것:
- wick_or_atr 주력화
- top250/top300 확장형
- 강한 fail-fast 주력화
- 강한 score floor 단독 구조
