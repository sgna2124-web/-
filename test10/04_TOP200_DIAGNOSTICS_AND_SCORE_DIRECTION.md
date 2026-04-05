# top200 의심 근거 / score 재정의 방향

## 1. 왜 top200을 의심하게 되었는가

사용자 관점의 핵심 문제제기:
- 실거래 프로그램매매 관점에서 topN은 구현이 번거롭다.
- 전 종목 후보를 한 번에 모아 정렬해야 한다.
- 과열 시점에서 topN이 손실을 자르는지, 수익을 자르는지 설명이 약하다.
- 차라리 신호 자체를 단단하게 정의하고 절대 score 기준으로 자르는 편이 논리적으로 더 낫다.

이 문제제기는 타당하다.

## 2. v25 진단 결과 핵심

### 후보 수 분포
- timestamps_with_candidates = 47,282
- mean_candidates = 1.9084
- median_candidates = 1
- p90_candidates = 2
- p95_candidates = 3
- max_candidates = 386
- timestamps_over_200 = 13
- share_over_200 = 0.000274946

해석:
- top200은 거의 항상 비활성이다.
- 극히 드문 burst 시점에서만 실제로 작동한다.
- 따라서 top200은 일반 규칙이라기보다 희귀 burst 시점 제어 장치로 해석하는 게 더 맞다.

### 선택/탈락 거래 품질 비교(200 초과 시점 기준)
- selected_when_over200
  - count 2600
  - mean_return 0.0001315
  - win_rate 0.4315
  - pf 1.00896
- rejected_when_over200
  - count 582
  - mean_return 0.0002627
  - win_rate 0.4966
  - pf 1.01538

해석:
- top200이 “나쁜 거래만 잘랐다”는 증거가 약하다.
- 오히려 개별 거래만 보면 탈락 거래가 특별히 더 나쁘지 않다.
- top200의 개선 효과는 거래 질 선택이라기보다 포트폴리오 경로/노출 구조를 바꾼 효과일 가능성이 크다.

### rank bucket 품질
- rank_201_250: mean_return 플러스
- rank_251_plus: mean_return 마이너스

해석:
- 200이라는 숫자 자체가 특별한 경계라는 증거가 약하다.
- 251 이상부터 품질 악화가 더 뚜렷한 그림이다.

## 3. 현재 top200에 대한 최종 해석

현재 단계에서 가장 정확한 해석:
- top200은 완전히 허상이라고 보긴 어렵다.
- 하지만 구조적 정답 규칙이라고 부를 수준도 아니다.
- 현재는 “희귀한 과열 시점에서 포트폴리오 노출을 제한하는 임시 안전장치”로 보는 것이 가장 적절하다.

즉:
- 성과 기준선으로는 유지 가능
- 최종 배포 규칙으로는 아직 신뢰 부족

## 4. score 재정의가 필요한 이유

기존 raw score 문제:
- wick/body 비율이 body가 매우 작을 때 폭주 가능
- 일부 구간에서 score 극단값이 너무 커짐
- 절대 점수 컷 기준으로 쓰기에 불안정

따라서 score는 다음과 같이 재정의하기 시작했다.

### hardened score 설계 아이디어
- dev_score: EMA 이격을 threshold 대비 비율로 정규화 후 cap
- rsi_score: RSI 극단 정도를 10단위 등으로 정규화 후 cap
- wick_score: wick / max(body, ATR*floor) 형태로 안정화 후 log1p와 cap
- 최종 score = weighted sum

즉 절대 score를 “bounded weighted sum”으로 만들려는 방향이다.

## 5. v26 / v27이 보여준 hardened score 현실

### v26
- hardened absolute score 절대 컷 1차 시도
- top200 기준선을 넘지 못함
- 가장 가까운 쪽도 score_l16_s18 수준

### v27
- top200 없는 대체 시도
- 가장 가까운 후보는 score_l16_s20_shortheavy
- 그러나 still fail

해석:
- hardened score 방향성 자체는 유지할 가치가 있다.
- 그러나 현재 수식/threshold는 아직 top200 대체 수준이 아니다.
- 특히 long/short threshold 비대칭, short-heavy 접근이 더 유망하다.

## 6. 다음 score 방향

우선순위가 높은 조정 대상:
1. short threshold 세분화
   - long은 완만, short는 더 엄격한 구조 유지
2. quality guard 결합
   - asym guard를 가볍게 결합해 수익 손실을 과도하게 키우지 않는 선을 찾기
3. score 가중치 재조정
   - dev / rsi / wick 가중치 재탐색
4. wick normalization 강도 조정
   - ATR floor multiplier
   - wick cap
   - log 스케일링 강도
5. fail-fast는 후순위
   - 현재까지 기여도가 약함

## 7. 중요한 철학적 결론

다음 어시스턴트는 top200을 “증명된 원리”로 믿고 출발하면 안 된다.
지금은 다음처럼 이해해야 한다.

- top200 = 현재 최고 성과 기준선
- hardened score = 장기적으로 더 설명 가능하고 배포 친화적인 방향
- 현재 미션 = top200을 맹신하는 게 아니라, hardened score 기반 구조로 top200을 대체할 수 있는지 계속 검증하는 것
