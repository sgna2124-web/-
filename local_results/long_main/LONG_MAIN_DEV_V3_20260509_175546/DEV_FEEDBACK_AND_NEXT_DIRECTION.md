# LONG_MAIN_DEV_V3 피드백 및 다음 개발 방향

## 1. 문서 목적

이 문서는 `LONG_MAIN_DEV_V3_20260509_175546` 결과 폴더 안에서 v3 롱 메인 개발 결과의 장점, 단점, 보완점, 다음 개발 방향을 기록하기 위한 문서다.

다음 개선안을 만드는 작업자는 이 폴더의 `manifest.json`, `summary.csv`, `errors.csv`와 함께 이 문서를 먼저 읽어야 한다.

v3의 목적은 v2 결과에서 가장 유망했던 close_pos 계열을 정밀 분해하고, close_pos와 약한 volume/body/wick 조합을 테스트하는 것이었다.

결론은 다음과 같다.

- 기준선 복원: 성공
- 기준선 개선 후보 발굴: 성공
- 최우수 후보: `LM3_020_CP077_VOL145`
- 다음 방향: `close_pos 0.77 + vol_ratio 1.45` 계열을 중심으로 추가 미세 조정

---

## 2. 기준선 복원 확인

v3의 기준선 감사 후보는 다음이다.

- `LM3_000_BASELINE_EXACT_EMBEDDED`

결과:

- trades: 592
- wins: 346
- losses: 246
- win_rate_pct: 58.4459459459
- final_return_pct: 23.8426079030
- max_return_pct: 24.0623399724
- max_drawdown_pct: 1.7279904306
- official_cd_value: 121.7026194894
- verdict: baseline_win

manifest의 공식 기준선 값:

- restored_trades: 592
- restored_max_return_pct: 24.0623
- restored_max_drawdown_pct: 1.728
- restored_official_cd_value: 121.7026

판정:

- v3에서도 기준선 내장은 정상이다.
- 개선안 결과를 해석해도 된다.

---

## 3. v3 최우수 후보

### LM3_020_CP077_VOL145

조건:

- 기준선 진입 조건 통과
- close_pos >= 0.77
- vol_ratio >= 1.45
- TP03 적용

결과:

- trades: 568
- trade_ratio_vs_ref: 0.9594594595
- wins: 340
- losses: 228
- win_rate_pct: 59.8591549296
- final_return_pct: 24.1323630760
- max_return_pct: 24.3289178035
- max_drawdown_pct: 1.4817728785
- official_cd_value: 122.2930033864
- pf: 3.8224552451
- verdict: baseline_win

기준선 대비:

- trades: 592 → 568, 24건 감소
- win_rate_pct: 58.4459% → 59.8592%, 개선
- final_return_pct: 23.8426% → 24.1324%, 개선
- max_return_pct: 24.0623% → 24.3289%, 개선
- max_drawdown_pct: 1.7280% → 1.4818%, 개선
- official_cd_value: 121.7026 → 122.2930, 개선

판정:

- v3 최우수 후보
- 공격형 개선 후보
- 기준선 대체 후보로 저장할 가치 있음

이 후보는 수익률, max_return, MDD, cd_value가 모두 기준선보다 좋아졌다. 단순 방어형 후보가 아니라 기준선 대체 후보로 볼 수 있다.

---

## 4. 기준선을 이긴 주요 후보

### 4.1 LM3_030_CP077_BODY036

조건:

- close_pos >= 0.77
- body_atr >= 0.36

결과:

- trades: 565
- win_rate_pct: 59.4690
- final_return_pct: 23.7323
- max_return_pct: 23.9282
- max_drawdown_pct: 1.4109
- official_cd_value: 121.9866
- verdict: baseline_win

해석:

- 수익률은 기준선보다 약간 낮다.
- MDD가 크게 낮아져 cd_value는 기준선을 넘었다.
- 방어형에 가까운 개선 후보.

### 4.2 LM3_011_CP_077

조건:

- close_pos >= 0.77

결과:

- trades: 574
- win_rate_pct: 59.2334
- final_return_pct: 23.8661
- max_return_pct: 24.0622
- max_drawdown_pct: 1.5259
- official_cd_value: 121.9759
- verdict: baseline_win

해석:

- close_pos 0.77 단독으로도 기준선을 이겼다.
- v2에서 close_pos 0.80이 방어형 후보였는데, v3에서 0.77이 더 균형 좋은 지점으로 확인됐다.
- close_pos는 너무 강하게 조이면 수익을 깎고, 0.77 부근이 현재 최적 균형점으로 보인다.

### 4.3 LM3_023_CP080_VOL145

조건:

- close_pos >= 0.80
- vol_ratio >= 1.45

결과:

- trades: 542
- win_rate_pct: 61.2546
- final_return_pct: 23.3425
- max_return_pct: 23.5378
- max_drawdown_pct: 1.1432
- official_cd_value: 121.9325
- verdict: baseline_win

해석:

- 수익률은 기준선보다 낮다.
- MDD가 1.1432%로 크게 낮다.
- 안정형/방어형 롱 메인 후보로 가치가 있다.

### 4.4 LM3_022_CP079_VOL145

조건:

- close_pos >= 0.79
- vol_ratio >= 1.45

결과:

- trades: 553
- win_rate_pct: 60.7595
- final_return_pct: 23.4698
- max_return_pct: 23.6653
- max_drawdown_pct: 1.3527
- official_cd_value: 121.7996
- verdict: baseline_win

해석:

- 기준선 대비 수익률은 낮지만 MDD 방어가 좋다.
- cd_value 기준으로는 기준선보다 높다.
- 방어형 후보로 의미 있음.

---

## 5. 방어형 후보

### LM3_014_CP_080

조건:

- close_pos >= 0.80

결과:

- trades: 547
- win_rate_pct: 60.6947
- final_return_pct: 23.1594
- max_return_pct: 23.3544
- max_drawdown_pct: 1.1875
- official_cd_value: 121.6968
- verdict: defensive_candidate

해석:

- v2에서 확인된 방어형 후보가 v3에서도 재현됐다.
- 기준선 cd_value보다 아주 근소하게 낮지만, MDD가 크게 낮다.
- 다만 v3에서는 `LM3_023_CP080_VOL145`가 같은 close_pos 0.80 계열에서 cd_value까지 기준선을 넘겼으므로, 단독 close_pos 0.80보다 `close_pos 0.80 + vol 1.45`가 더 낫다.

---

## 6. v3의 핵심 발견

### 6.1 close_pos 최적 구간은 0.77 근처다

close_pos 단독 후보 중 가장 좋은 것은 `LM3_011_CP_077`이었다.

- close_pos 0.76: 기준선보다 낮음
- close_pos 0.77: 기준선보다 높음
- close_pos 0.78 이상: 대체로 수익률 감소가 커짐

따라서 단독 close_pos 필터는 0.77이 현재 최적 구간으로 보인다.

### 6.2 close_pos 0.77 + vol 1.45가 가장 좋았다

`LM3_020_CP077_VOL145`는 수익률과 MDD가 동시에 개선된 유일한 최상위 후보다.

해석:

- close_pos 0.77은 반전 캔들의 마감 품질을 높인다.
- vol_ratio 1.45는 reclaim이 의미 있는 거래량을 동반했는지 확인한다.
- 두 조건의 조합이 기준선의 좋은 거래는 대부분 유지하면서 품질 낮은 거래를 제거한 것으로 보인다.

### 6.3 volume은 너무 강하면 수익을 깎는다

vol 1.45는 좋았지만, vol 1.50은 대체로 성능이 떨어졌다.

예:

- `LM3_023_CP080_VOL145`: cd 121.9325
- `LM3_026_CP080_VOL150`: cd 121.5097

해석:

- vol 1.45 부근이 더 적절하다.
- 다음 개발에서는 1.42, 1.44, 1.46, 1.48 같은 세밀한 분해가 필요하다.

### 6.4 body_atr 0.36은 방어형에는 유효하지만 공격형 최우수는 아니다

`LM3_030_CP077_BODY036`은 기준선을 이겼지만, 수익률은 기준선보다 낮다.

해석:

- body_atr 0.36은 MDD를 낮추는 데 유효하다.
- 하지만 max_return을 늘리는 핵심 조건은 아니었다.
- 다음 개발에서는 body를 단독 핵심축으로 두기보다 보조 필터로 제한한다.

### 6.5 wick 조합은 수익률을 많이 깎는다

wick 1.34 이상 조합은 승률과 MDD에는 도움이 되지만, 수익률 저하가 컸다.

해석:

- wick은 너무 강하게 쓰면 큰 반등 거래를 놓칠 수 있다.
- 다음 개발에서 wick은 우선순위가 낮다.
- 시도한다면 1.30~1.33 사이의 아주 약한 조건만 테스트한다.

---

## 7. 다음 v4 개발 방향

v4는 `LM3_020_CP077_VOL145`를 중심으로 미세 조정하는 것이 가장 합리적이다.

### 7.1 1순위: close_pos 0.765~0.785 세밀 분해

추천 후보:

- cp 0.765 + vol 1.45
- cp 0.770 + vol 1.45
- cp 0.775 + vol 1.45
- cp 0.780 + vol 1.45
- cp 0.785 + vol 1.45

목표:

- LM3_020보다 cd_value가 높은 지점 탐색
- 수익률과 MDD의 최적 균형 찾기

### 7.2 2순위: volume 1.40~1.48 세밀 분해

추천 후보:

- cp 0.77 + vol 1.40
- cp 0.77 + vol 1.42
- cp 0.77 + vol 1.44
- cp 0.77 + vol 1.45
- cp 0.77 + vol 1.46
- cp 0.77 + vol 1.48

보조 후보:

- cp 0.775 + vol 1.42
- cp 0.775 + vol 1.44
- cp 0.775 + vol 1.46

### 7.3 3순위: 청산 파라미터 소폭 조정

진입 조건에서는 v3가 이미 기준선을 이겼다. 다음에는 최우수 진입 후보인 `cp 0.77 + vol 1.45`를 기준으로 청산 파라미터를 소폭 조정해볼 수 있다.

추천 범위:

- atr_stop: 1.00, 1.03, 1.05, 1.07, 1.10
- rr_target: 2.35, 2.40, 2.45, 2.50, 2.55, 2.60
- max_hold_bars: 16, 18, 20
- cooldown_bars: 16, 18, 20

주의:

- 한 번에 너무 많은 축을 섞으면 해석이 어려워진다.
- v4에서는 진입 미세 조정 중심, v5에서 청산 조정으로 분리해도 된다.

### 7.4 4순위: 방어형 별도 관리

방어형 후보로는 다음이 유효하다.

- `LM3_023_CP080_VOL145`
- `LM3_014_CP_080`

방어형 기준:

- MDD 1.20% 이하
- cd_value 121.6 이상
- 거래 수 500건 이상

`LM3_023_CP080_VOL145`는 이 조건을 만족하며 cd_value도 기준선을 넘는다. 따라서 방어형 롱 메인 후보로 따로 관리할 가치가 있다.

---

## 8. 다음 파일 작성 규칙

다음 파일은 `run_long_main_dev_v4.py` 형태가 적합하다.

필수 규칙:

1. `LM4_000_BASELINE_EXACT_EMBEDDED`를 반드시 포함한다.
2. 기준선 exact 후보가 trades 592, max_return 약 24.0623, MDD 약 1.728, cd 약 121.7026을 재현해야 한다.
3. 최우수 v3 후보 `LM3_020_CP077_VOL145`와 같은 조건을 v4의 기준 개선 후보로 포함한다.
4. v4의 목적은 `cp 0.77 + vol 1.45` 주변 미세 조정이다.
5. EMA50 gap, EMA50 slope, trend floor, quiet ratio, ret20 floor는 여전히 제외한다.
6. wick 강화는 우선순위를 낮춘다.
7. 결과는 현재 파이썬 파일 실행 위치 기준으로 저장한다.
8. 기존 결과 파일은 수정하지 않고, 새 결과 폴더에 추가 기록만 남긴다.

---

## 9. 최종 판정

v3는 성공이다.

v2는 기준선 복원에 성공했지만 기준선을 이긴 후보가 없었다. v3는 기준선 복원을 유지하면서 기준선보다 좋은 후보를 발굴했다.

최우수 후보:

- `LM3_020_CP077_VOL145`

이 후보는 다음을 모두 만족한다.

- 기준선보다 final_return_pct 높음
- 기준선보다 max_return_pct 높음
- 기준선보다 MDD 낮음
- 기준선보다 official_cd_value 높음
- trades도 기준선 대비 95.95% 수준으로 과도하게 줄지 않음

따라서 다음 개발은 이 후보를 중심으로 진행한다.

v4 권장 방향:

- cp 0.765~0.785 미세 조정
- vol 1.40~1.48 미세 조정
- `cp 0.77 + vol 1.45`를 중심축으로 유지
- 방어형 후보 `cp 0.80 + vol 1.45`는 별도 관리
