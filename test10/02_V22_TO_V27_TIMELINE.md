# v22 ~ v27 결과 타임라인

## v22: revalidation 출발점

목적:
- same-bar 처리 누수 수정 후 기존 상위 후보들을 재검증
- 무엇을 공식 기준선으로 삼을지 다시 정함

핵심 결과:
- atr18975_t27_b17_r155_legacy_baseline
  - final_return_pct 1082.0186
  - pf 1.2172142
  - mdd_pct -40.71895
  - max_conc 386
- long_guard_wick_only_top200_baseline
  - final_return_pct 513.2594
  - pf 1.2178385
  - mdd_pct -48.72412
  - max_conc 234
- asym_guard_wick_only_top200
  - final_return_pct 516.4686
  - pf 1.2229563
  - mdd_pct -48.43364
  - max_conc 234

해석:
- pre-v22의 화려했던 wick_only 계열은 과대평가되어 있었음
- revalidated raw 1위는 legacy baseline으로 교체됨
- 이후 모든 개선은 이 기준선에서 다시 시작

## v23: revalidated baseline 위의 구조 개선

목적:
- revalidated baseline에 이전에 의미 있었던 구조들(long guard, asym guard, wick_or_atr, top200 cap)을 다시 얹어보기

핵심 결과:
- baseline_top200
  - final_return_pct 1103.7841
  - pf 1.2176038
  - mdd_pct -36.08383
  - max_conc 271
- asym_guard_top200
  - final_return_pct 1030.7929
  - pf 1.2327923
  - mdd_pct -35.22274
  - max_conc 269
- long_guard_top200
  - final_return_pct 1027.0301
  - pf 1.2270981
  - mdd_pct -35.70334
  - max_conc 270

해석:
- top200 cap이 revalidated baseline보다 명확히 좋아짐
- baseline_top200이 새 공식 기준선으로 승격
- asym_guard_top200은 방어형/균형형 후보로 유의미
- wick_or_atr 계열은 상대적으로 약함

## v24: 세 갈래 실험

### v24-1: topN vs score floor 비교
핵심:
- top N 방식이 score 절대컷보다 더 강하게 나옴
- baseline_top200이 여전히 1위
- score floor / hybrid는 PF나 MDD는 좋아질 수 있으나 수익 훼손이 큼

주요 해석:
- 현 시점에서는 topN 우세
- 하지만 이때부터 topN의 구조적 타당성에 의문이 생김

### v24-2: cd_value 확장 시도
핵심:
- top250 / top300으로 느슨하게 풀어도 공식 기준선을 넘지 못함
- cd_value 극대화 시도 실패
- asym_guard_top200은 여전히 균형형 후보로 유효

### v24-3: MDD 절감 시도
핵심 결과:
- asym_guard_top150
  - final_return_pct 898.76
  - pf 1.21856
  - mdd_pct -32.53
  - max_conc 269
- baseline_top150_score25
  - final_return_pct 478.24
  - pf 1.27553
  - mdd_pct -22.92
  - max_conc 181

해석:
- 극단적으로 MDD를 낮출 수는 있으나 수익 훼손이 큼
- practical defense 후보로는 asym_guard_top150이 의미 있음

## v25: top200 진단 레인

목적:
- top200이 정말 구조적으로 의미 있는지 검증
- 실제 후보 수 분포와 잘려나간 거래들의 품질을 기록

핵심 진단:
- 후보 발생 타임스탬프: 47,282개
- mean_candidates: 1.9084
- median_candidates: 1
- p95_candidates: 3
- max_candidates: 386
- timestamps_over_200: 13개
- share_over_200: 0.000274946

해석:
- top200은 거의 모든 시점에서 작동하지 않음
- 매우 드문 burst 시점에서만 발동하는 장치였음

더 중요한 해석:
- 200 초과 시점에서 선택된 거래가 탈락 거래보다 명확히 더 좋다고 보기는 어려웠음
- rank 201~250은 아주 나쁘지 않았고, 251+부터 더 나빠지는 그림이 나옴
- top200은 “정답 규칙”이라기보다 “희귀 burst 제어 장치”로 보는 게 맞다는 의심 강화

## v26: hardened absolute score 1차 시도

목적:
- topN을 버리고, 안정화된 score 절대 기준으로 잘라보기
- wick/body 폭주를 ATR 보정과 bounded weighted sum으로 줄이기

기준선:
- official_top200_reference
  - final_return_pct 1120.69995
  - pf 1.2199649
  - mdd_pct -36.03441
  - max_conc 271

절대 score 컷 후보 중 비교적 근접한 것:
- score_l16_s18
  - final_return_pct 1088.0037
  - pf 1.2195171
  - mdd_pct -40.79565
  - max_conc 386
- score_l16_s20_shortheavy는 v26에는 없고 v27에서 주요 후보가 됨

해석:
- 절대 score 컷은 아직 공식 기준선을 넘지 못함
- hardened score 방향성은 유지 가능하지만, 절대 컷만으로는 부족
- clip/ATR stabilization은 이번 라운드에서 결정적 효과 없음

## v27: top200 제거 대체 시도

목적:
- 공식 기준선과 비교하되, 신규 후보는 전부 top200 없이 싸우게 함
- “top200 제거 상태에서 버틸 수 있는가”를 검증

핵심 결과:
- official_top200_reference
  - final_return_pct 1120.69995
  - pf 1.2199649
  - mdd_pct -36.03441
  - max_conc 271
- score_l16_s20_shortheavy
  - final_return_pct 1089.0657
  - pf 1.2242424
  - mdd_pct -41.06885
  - max_conc 386
- score_l16_s18
  - final_return_pct 1088.0037
  - pf 1.2195171
  - mdd_pct -40.79565
  - max_conc 386
- asym_guard_score_l16_s20_shortheavy
  - final_return_pct 1027.1190
  - pf 1.2416775
  - mdd_pct -39.53297
  - max_conc 379

해석:
- top200 제거 대체는 아직 실패
- 그중 가장 근접한 대체 축은 `score_l16_s20_shortheavy`
- asym guard는 PF 개선에는 도움되지만 수익 손실이 큼
- fail-fast는 계속 약했음

## 전체 요약

- v22: revalidation으로 판이 뒤집힘
- v23: baseline_top200이 공식 기준선으로 승격
- v24: topN 우세, MDD 방어형 후보 발굴
- v25: top200은 희귀 burst 시점 장치라는 의심 강화
- v26: hardened absolute score 1차 시도 실패
- v27: top200 제거 대체 1차 시도 실패, 최선 후보는 score_l16_s20_shortheavy
