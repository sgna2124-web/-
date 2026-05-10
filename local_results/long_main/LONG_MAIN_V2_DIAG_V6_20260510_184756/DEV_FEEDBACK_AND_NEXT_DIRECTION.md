# LONG_MAIN_V2_DIAG_V6 피드백 및 다음 개발 방향

## 1. 결론

v6는 공식 long_main v2 기준선의 거래 단위 진단 목적을 달성했다.

기준선 복원은 성공했다.

- strategy: `LM6_000_LONG_MAIN_V2_EXACT_EMBEDDED`
- trades: 557
- wins: 333
- losses: 224
- win_rate_pct: 59.7845601436
- final_return_pct: 23.9514570645
- max_return_pct: 24.1477253403
- max_drawdown_pct: 1.3005547461
- official_cd_value: 122.3394005068
- pf: 3.8956015265

공식 기준선은 아직 유지한다.

- `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`

v6는 기준선 갱신용 공식 백테스트가 아니라 손실 거래 구조를 찾기 위한 진단 배치다.

---

## 2. 실행 조건

- batch_label: `LONG_MAIN_V2_TRADE_DIAGNOSTICS_V6`
- csv_files: 597
- round_trip_cost_bps: 8.0
- position_fraction: 0.01
- errors: 없음
- path_policy: 외부 하드코딩 경로 없음

---

## 3. 손실 거래 구조 핵심

win/loss feature 비교에서 손실 거래는 다음 특성이 강했다.

### 3.1 약한 하락 압축 구간에서 손실이 많다

수익 거래는 진입 전 하락이 더 깊고, 손실 거래는 상대적으로 덜 빠진 상태에서 들어간다.

- ret20 win_mean: -0.1781
- ret20 loss_mean: -0.1155
- ret10 win_mean: -0.1606
- ret10 loss_mean: -0.1106
- ret5 win_mean: -0.1448
- ret5 loss_mean: -0.0961
- ret3 win_mean: -0.1182
- ret3 loss_mean: -0.0646

해석:

- long_main v2는 급락 후 반전 구조에서 더 강하다.
- 덜 빠진 구간의 reclaim은 반등 폭이 약하거나 stop으로 이어질 가능성이 높다.

### 3.2 손실 거래는 RSI가 높다

- rsi14 win_mean: 22.3441
- rsi14 loss_mean: 27.0010

해석:

- 과매도 압력이 약한 상태에서 진입하면 기대 반등이 작아진다.
- 단, 기존 RSI 하한은 실패했으므로 v7에서는 RSI 상한을 아주 약하게만 테스트한다.

### 3.3 수익 거래는 더 깊은 저점 이탈과 높은 거래량을 보인다

- low_break_atr win_mean: 1.4073
- low_break_atr loss_mean: 0.9452
- vol_ratio win_mean: 3.5398
- vol_ratio loss_mean: 3.1880

해석:

- 저점을 더 확실히 찌르고 거래량을 동반한 reclaim이 더 좋다.
- 하지만 v5에서 real_break 단독 추가는 실패했으므로, 단독 조건보다 ret20/RSI와 결합한 약한 후보로 검증해야 한다.

### 3.4 손실 거래는 close_pos가 낮고 upper wick이 높다

- close_pos win_mean: 0.9332
- close_pos loss_mean: 0.8995
- upper_wick_ratio win_mean: 0.0668
- upper_wick_ratio loss_mean: 0.1005

해석:

- v2 기준선 안에서도 마감 품질이 약한 거래가 손실 쪽에 많다.
- 다만 이전 upper wick guard는 실질 필터로 작동하지 않았으므로 더 강한 조건을 바로 쓰기보다 다른 조건과 결합해야 한다.

### 3.5 손실 거래는 MFE가 매우 작다

- mfe_pct win_mean: 10.9890
- mfe_pct loss_mean: 2.4524
- mae_pct win_mean: -0.9508
- mae_pct loss_mean: -7.1263

해석:

- 손실 거래는 진입 후 반등이 거의 나오지 않고 빠르게 손실 구간으로 밀린다.
- 청산 조정보다 진입 품질 필터가 우선이다.

---

## 4. shadow filter 진단

주의:

- shadow_filter_screen.csv는 기준선 거래 집합에서 사후적으로 일부 거래를 제거한 진단이다.
- entry/cooldown 재시뮬레이션이 없으므로 공식 성과로 쓰면 안 된다.
- 단, v7 후보 설계에는 사용할 수 있다.

사후 진단상 유망한 방향:

1. MFE/MAE 기반은 성과가 매우 좋지만 미래 정보라서 실전 진입 조건으로 사용할 수 없다.
2. ret20 상단 제거가 유망하다.
   - `KEEP_RET20_LE_Q80`: cd 123.6443
   - `KEEP_RET20_LE_Q90`: cd 123.1393
3. RSI 상단 제거가 약하게 유망하다.
   - `KEEP_RSI14_LE_Q90`: cd 122.5998
4. ret10 상단 제거가 약하게 유망하다.
   - `KEEP_RET10_LE_Q90`: cd 122.5912
5. reclaim_atr 상단 제거가 약하게 유망하다.
   - `KEEP_RECLAIM_ATR_LE_Q90`: cd 122.4139
6. shock_recency <= 3은 거의 기준선과 비슷하지만 약간 개선 가능성이 있다.
   - `KEEP_SHOCK_RECENCY_LE_Q90`: cd 122.3555

---

## 5. v7 실제 백테스트 후보 방향

v7은 v6 shadow screen에서 나온 후보를 공식 백테스트로 재검증해야 한다.

단, 다음 원칙을 지킨다.

- MFE/MAE는 미래 정보이므로 사용 금지
- 사후 screen 결과를 공식 성과로 해석 금지
- v2 exact baseline을 반드시 먼저 재현
- 조건은 v2 기준선 위에 추가하는 방식으로 구성
- 미세 파라미터 조정이 아니라 구조형 후보로 구성

추천 후보:

1. v2 + ret20 not weak enough 제거
   - 목적: 덜 빠진 상태의 reclaim 제거
   - 예: ret20 <= -0.08 부근

2. v2 + ret20/ret10 압축 확인
   - 목적: 단기와 중기 하락 압력이 모두 존재하는 경우만 진입
   - 예: ret20 <= -0.08 AND ret10 <= -0.06 부근

3. v2 + RSI 상단 제한
   - 목적: 과매도 압력이 약한 거래 제거
   - 예: rsi14 <= 34 부근

4. v2 + reclaim_atr 과확장 제한
   - 목적: 이미 너무 멀리 회복한 종가 추격 제거
   - 예: reclaim_atr <= 1.77 부근

5. v2 + shock_recency <= 3
   - 목적: 너무 오래된 shock 기반 진입 제거

6. v2 + ret20 + RSI 복합
   - 목적: 덜 빠지고 RSI도 높은 약한 반전 제거

7. v2 + ret20 + reclaim_atr 복합
   - 목적: 덜 빠졌는데 reclaim만 과확장된 거래 제거

---

## 6. v7에서 반복 금지할 방향

v5에서 실패한 조건은 반복하지 않는다.

- range_atr <= 2.40
- body/range balance
- body_atr <= 1.45
- lower wick >= 1.34 단독
- real_break >= 0.05 단독
- shock recent 4/6 단독
- reclaim extension <= 1.10 ATR

기존 후순위 조건도 유지한다.

- ret1 상한
- ATRP 상한
- RSI 하한
- EMA50 gap
- EMA50 slope
- trend floor
- quiet ratio
- ret20 floor
- shock_count >= 2

---

## 7. 최종 판단

v6는 기준선 갱신 배치가 아니라 진단 배치로 성공이다.

공식 기준선은 유지한다.

- `LONG_MAIN_V2_LM4_014_ATTACK_BODY_NOT_HUGE`

다음 v7은 v2 기준선 위에 다음 구조형 조건을 공식 백테스트로 검증한다.

- ret20 상단 제한
- ret10/ret20 복합 하락 압력 확인
- RSI14 상단 제한
- reclaim_atr 상단 제한
- shock_recency <= 3
- ret20 + RSI
- ret20 + reclaim_atr
