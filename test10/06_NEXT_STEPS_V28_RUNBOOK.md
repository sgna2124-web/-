# 다음 단계 실행 가이드 (v28 권장)

## 1. 핵심 목표

다음 단계의 최우선 목표는 이것이다.

`top200 없이도 official_top200_reference에 근접하거나 대체 가능한 구조를 찾는 것`

즉 다음 버전은 “성능 최고 기준선 유지”가 아니라,
“설명 가능하고 실거래 구현 가능한 구조로 top200을 대체”하는 데 초점을 둔다.

## 2. v28 권장 주축

### 주축 A: score_l16_s20_shortheavy
현재 top200 없는 후보 중 가장 근접.

최근 수치(v27):
- final_return_pct 1089.0657
- pf 1.2242424
- mdd_pct -41.06885
- max_conc 386

왜 주축인가:
- 수익 보존율 최고 수준
- 숏을 더 엄격하게 자르는 방향이 가장 유망함을 보여줌

### 주축 B: asym_guard_score_l16_s20_shortheavy
PF 강화형 보조 후보.

최근 수치(v27):
- final_return_pct 1027.1190
- pf 1.2416775
- mdd_pct -39.53297
- max_conc 379

왜 같이 보나:
- 수익은 더 낮지만 PF가 좋음
- 대체형이 아니라 방어형 보조 축으로 의미가 있음

## 3. v28에서 조정할 변수 (권장 순서)

### 1순위: short threshold 미세 조정
현재 시사점:
- short-heavy가 가장 유망

권장 탐색 예시:
- long 1.6 고정 / short 1.9
- long 1.6 고정 / short 2.0
- long 1.6 고정 / short 2.1
- long 1.55 / short 2.0
- long 1.65 / short 2.0

목적:
- 수익 보존을 최대한 유지하면서 숏 쪽 불필요 진입만 더 억제

### 2순위: quality guard 약하게 결합
asym guard가 PF에는 도움됨.
다만 너무 강하면 수익 손실이 커질 수 있음.

권장 방식:
- soft asym guard
- long side는 거의 유지
- short side만 살짝 더 까다롭게

### 3순위: score 가중치 재조정
현재 기본값:
- dev_weight 1.0
- rsi_weight 0.8
- wick_weight 0.7

권장 탐색:
- wick_weight 약화: 0.5 ~ 0.6
- rsi_weight 강화: 0.9 ~ 1.1
- dev_weight는 1.0 유지 or 0.9 ~ 1.1 소폭 범위

의도:
- wick 항이 여전히 과도한 영향력을 주는지 확인
- 좀 더 안정적인 score로 만들기

### 4순위: wick normalization 강도
현재 핵심 파라미터:
- wick_atr_floor_mult
- score_wick_cap

권장 탐색:
- wick_atr_floor_mult: 0.15, 0.20, 0.25
- score_wick_cap: 1.8, 2.0, 2.2

의도:
- 도지/작은 body에서 wick score 폭주를 더 줄이기

## 4. v28에서 우선 제외하거나 후순위로 둘 것

- fail-fast 주력화: 후순위
- top250/top300 등 topN 재확장: 후순위
- wick_or_atr 주력화: 후순위
- 강한 score floor 단독 구조: 후순위

## 5. v28 설계 예시

라인 1: short-heavy 중심
- score_l16_s19_shortheavy
- score_l16_s20_shortheavy
- score_l16_s21_shortheavy
- score_l155_s20_shortheavy
- score_l165_s20_shortheavy

라인 2: short-heavy + asym guard
- asym_guard_score_l16_s19_shortheavy
- asym_guard_score_l16_s20_shortheavy
- asym_guard_score_l16_s21_shortheavy

라인 3: short-heavy + score weight 변화
- score_l16_s20_shortheavy_wick05
- score_l16_s20_shortheavy_rsi10
- score_l16_s20_shortheavy_wick05_rsi10

라인 4: short-heavy + wick normalization 변화
- score_l16_s20_shortheavy_atr020
- score_l16_s20_shortheavy_atr025
- score_l16_s20_shortheavy_cap20

## 6. 다음 대화창에서의 우선 평가 기준

1. official_top200_reference 대비 수익 보존율
2. MDD가 얼마나 줄었는지 혹은 덜 나빠졌는지
3. max_conc가 억제되는지
4. PF가 개선되는지
5. top200 제거 상태에서 실제로 공식 기준선에 얼마나 가까워졌는지

## 7. 최종 목표를 잊지 말 것

다음 어시스턴트는 다음 문장을 계속 기억할 것.

- 공식 기준선은 지금도 top200이다.
- 그러나 사용자는 top200 같은 cross-sectional cap을 최종 규칙으로 쓰는 것에 거부감이 있다.
- 따라서 우리의 일은 top200을 방어하는 것이 아니라, top200 없이도 그에 근접하는 설명 가능한 구조를 만드는 것이다.
