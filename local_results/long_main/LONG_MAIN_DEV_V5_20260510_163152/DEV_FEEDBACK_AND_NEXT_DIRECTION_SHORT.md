# LONG_MAIN_DEV_V5 피드백 요약

## 1. 결론

v5는 기준선 v2 복원에는 성공했지만, v2 기준선을 넘는 신규 개선 후보는 나오지 않았다.

공식 long_main 기준선은 그대로 유지한다.

- `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`

## 2. 기준선 복원

`LM5_000_LONG_MAIN_V2_EXACT_EMBEDDED`가 v2 기준선을 정상 재현했다.

- trades: 557
- wins: 333
- losses: 224
- win_rate_pct: 59.7845601436
- final_return_pct: 23.9514570645
- max_return_pct: 24.1477253403
- max_drawdown_pct: 1.3005547461
- official_cd_value: 122.3394005068
- profit_factor: 3.8956015265

따라서 v5 결과 해석은 유효하다.

## 3. v5 최고 결과

최고 결과는 v2 exact와 동일했다.

동일 결과 후보:

- `LM5_000_LONG_MAIN_V2_EXACT_EMBEDDED`
- `LM5_001_V2_NO_TP03_SANITY`
- `LM5_023_V2_RECLAIM_COMMITTED`

`LM5_023`은 reclaim extension >= 0.20 ATR 조건을 추가했지만 결과가 기준선과 완전히 같았다. 즉, v2의 557개 거래는 이미 이 조건을 만족한 것으로 보인다.

## 4. 근접 후보

`LM5_012_REMOVE_CP_ADDON`은 기준선 v2에 매우 근접했다.

- trades: 574
- final_return_pct: 24.0258276872
- max_return_pct: 24.2458848407
- max_drawdown_pct: 1.3656446744
- official_cd_value: 122.3320755765

해석:

- close_pos 0.77을 제거하면 수익성과 max_return은 증가한다.
- 하지만 MDD도 증가해 cd_value가 v2보다 아주 근소하게 낮다.
- 공격형 후보로 참고할 수 있으나 공식 기준선 대체는 아니다.

`LM5_010_REMOVE_BODY_GUARD`는 v3 공격형 anchor와 같은 결과다.

- trades: 568
- final_return_pct: 24.1323630760
- max_return_pct: 24.3289178035
- max_drawdown_pct: 1.4817728785
- official_cd_value: 122.2930033864

해석:

- body_atr <= 1.60은 MDD를 낮추는 데 유효하다.
- 제거하면 수익률은 올라가지만 MDD도 올라간다.

## 5. 실패한 방향

다음 방향은 v2 기준선 위에서 성능을 개선하지 못했다.

- shock recent 4 또는 6 추가
- real break >= 0.05 ATR 추가
- lower wick >= 1.34 추가
- reclaim extension <= 1.10 ATR
- range_atr <= 2.40
- body/range balance
- body_atr <= 1.45
- defense cp0.80 계열 추가 조합

특히 range_atr 제한과 body/range balance는 거래 수를 크게 줄이고 수익률을 크게 낮췄다.

## 6. 핵심 해석

v2 기준선은 이미 꽤 압축되어 있다.

v2 조건의 역할은 다음과 같다.

- close_pos >= 0.77: MDD를 낮추는 균형 조정
- vol_ratio >= 1.45: reclaim 품질 확인에 중요
- body_atr <= 1.60: 과도한 반전봉을 느슨하게 제거해 MDD 완화

v5에서 조건을 더 붙이는 방식은 대부분 수익 거래까지 제거했다.

## 7. 다음 방향

다음 단계는 추가 필터 대량 생성보다 v2 기준선 거래 진단이 적합하다.

추천 v6 방향:

- v2 exact 557개 거래의 entry feature snapshot 저장
- win/loss feature 분포 비교
- 손실 거래의 atrp, close_pos, vol_ratio, body_atr, ret5, ret10, ret20, shock recency 분석
- MAE/MFE 구조 분석
- 손실 거래가 특정 심볼이나 시간대에 몰리는지 확인

추천 파일명:

- `run_long_main_v2_trade_diagnostics_v6.py`

v6에서 진단 결과를 얻은 뒤, v7에서 그 결과를 기준으로 개선안을 만드는 것이 좋다.

## 8. 최종 판단

v5는 기준선 갱신 실패다.

현재 공식 long_main 기준선은 유지한다.

- `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`

다음 개발은 기준선 위에 조건을 계속 붙이기보다, 기준선의 손실 거래 구조를 먼저 분석하는 방향이 더 합리적이다.
