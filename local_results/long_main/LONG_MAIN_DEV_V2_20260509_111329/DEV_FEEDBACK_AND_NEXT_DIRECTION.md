# LONG_MAIN_DEV_V2 피드백 및 다음 개발 방향

## 1. 문서 목적

이 문서는 `LONG_MAIN_DEV_V2_20260509_111329` 결과 폴더 안에서 이번 롱 메인 개발 시도에 대한 판단, 장점, 단점, 보완할 점, 다음 개발 방향을 남기기 위한 기록이다.

다음 개선안을 만드는 작업자는 이 폴더의 `summary.csv`, `manifest.json`, `errors.csv`와 함께 이 문서를 먼저 읽어야 한다.

이번 v2의 핵심 의미는 “롱 메인 기준선의 진입 조건을 실제로 내장한 상태에서 개발이 가능해졌는가”를 검증한 것이다.

결론은 다음과 같다.

- 기준선 복원: 성공
- 기준선 대체 개선안 발굴: 실패
- 다음 개발 방향: close_pos 중심의 정밀 조정 및 약한 조합 필터

---

## 2. 기준선 복원 결과

이번 v2에서 가장 중요한 후보는 다음이다.

- `LM2_000_BASELINE_EXACT_EMBEDDED`
- 설명: exact embedded 6V2_L01_doubleflush_core entry; no added filter
- 목적: `base_line/6V2_long10_reviewed.py`의 롱 메인 기준선 진입 조건을 코드 내부에 내장한 뒤, 기준선 결과가 그대로 재현되는지 확인

결과는 다음과 같다.

- trades: 592
- wins: 346
- losses: 246
- win_rate_pct: 58.4459459459
- final_return_pct: 23.8426079030
- max_return_pct: 24.0623399724
- max_drawdown_pct: 1.7279904306
- official_cd_value: 121.7026194894
- verdict: baseline_win

manifest의 공식 기준선 값은 다음이다.

- restored_trades: 592
- restored_max_return_pct: 24.0623
- restored_max_drawdown_pct: 1.728
- restored_official_cd_value: 121.7026

따라서 v2의 기준선 내장은 성공으로 본다.

앞으로 롱 메인 개발 파일은 반드시 이 기준을 먼저 통과해야 한다.

통과 조건:

- baseline exact 후보가 trades 592를 재현해야 한다.
- max_return_pct는 약 24.0623 근처여야 한다.
- max_drawdown_pct는 약 1.728 근처여야 한다.
- official_cd_value는 약 121.7026 근처여야 한다.

이 값이 다르면 개선안 평가로 넘어가면 안 된다. 먼저 기준선 진입식, 수수료, 포지션 크기, 데이터 매칭, warmup, cooldown, 청산 로직을 확인해야 한다.

---

## 3. 이번 v2의 장점

### 3.1 기준선 진입 조건을 실제로 내장했다

v1에서는 기준선 설명을 바탕으로 proxy 진입식을 만들어 과다 진입이 발생했다. v2에서는 `base_line/6V2_long10_reviewed.py`의 핵심 구조를 내장했다.

기준 구조:

- `raw_l01_cap_reclaim`
- `double_flush_ok`
- 최종 기준선 진입: `raw_l01_cap_reclaim[i] and double_flush_ok(raw, f, i, lookback=10)`

이 구조가 정확히 복원되었기 때문에, 앞으로는 이 파일 구조를 롱 메인 개발의 기본 틀로 삼을 수 있다.

### 3.2 v1의 핵심 실패를 바로잡았다

v1은 60만~100만 건 수준의 과다 진입이 발생했다. 이는 롱 메인 기준선 592건과 비교할 수 없는 수준이었다.

v2는 기준선 진입 수 592건을 정확히 복원했다.

따라서 다음 개발에서 절대 해서는 안 되는 방식이 명확해졌다.

금지:

- 기준선 문서 설명만 보고 비슷한 proxy 진입식을 새로 만드는 것
- 롱 메인 기준선의 희소성을 재현하지 않은 상태에서 조건을 추가하는 것
- 기준선 exact 후보 없이 곧바로 개선 후보를 대량 생성하는 것

### 3.3 결과 비교가 명확해졌다

모든 후보가 기준선 대비 trade_ratio, ref_trades, ref_max_return_pct, ref_mdd, ref_cd를 함께 저장한다.

따라서 다음 개발자는 후보가 기준선을 이겼는지, 단순히 거래 수만 줄였는지, MDD 방어 후보인지 바로 판단할 수 있다.

### 3.4 errors.csv가 비어 있다

`errors.csv`에는 header만 있고 실제 에러가 없다. 597개 CSV 처리 자체는 정상으로 본다.

---

## 4. 이번 v2의 단점

### 4.1 기준선을 확실히 이긴 후보는 없다

이번 v2에서 기준선보다 official_cd_value가 높은 후보는 없다.

기준선:

- official_cd_value: 121.7026194894

가장 근접한 후보:

- `LM2_002_ADD_CLOSEPOS_080`
- official_cd_value: 121.6968401220

차이는 약 0.0057793674로 매우 작지만, 엄밀히 보면 기준선 대체 성공은 아니다.

### 4.2 일부 필터는 아무 효과가 없었다

다음 후보들은 기준선과 결과가 완전히 동일했다.

- `LM2_001_BASE_PLUS_TP03`
- `LM2_012_ADD_UPPER_REJECT_070`
- `LM2_013_ADD_RECLAIM_BUFFER_001`
- `LM2_018_VAR_RAW_CLOSEPOS_073`
- `LM2_019_VAR_DF_LOW_10015`

해석:

- 해당 조건들은 기준선의 592개 진입 중 어떤 거래도 제거하지 못했다.
- 같은 강도의 조건을 반복해도 의미가 없다.
- 다음 개발에서는 조건 강도를 더 세분화하거나, 해당 조건을 다른 필터와 조합해야 한다.

### 4.3 EMA, quiet, ret20 floor 계열은 롱 메인과 맞지 않았다

성능이 크게 훼손된 후보들:

- `LM2_007_ADD_RET20_FLOOR`
  - trades: 314
  - win_rate_pct: 45.5414
  - final_return_pct: 1.6053
  - official_cd_value: 100.3915

- `LM2_008_ADD_EMA50_GAP`
  - trades: 65
  - win_rate_pct: 29.2308
  - final_return_pct: -0.6470
  - official_cd_value: 98.5222

- `LM2_009_ADD_EMA50_SLOPE`
  - trades: 69
  - win_rate_pct: 33.3333
  - final_return_pct: -0.5703
  - official_cd_value: 98.7087

- `LM2_010_ADD_TREND_FLOOR`
  - trades: 54
  - win_rate_pct: 31.4815
  - final_return_pct: -0.5582
  - official_cd_value: 98.6983

- `LM2_011_ADD_QUIET_095`
  - trades: 0

해석:

롱 메인 기준선은 안정적인 추세장이나 quiet regime을 먹는 전략이 아니다. 급락, flush, reclaim, 강한 반전 캔들을 먹는 전략이다. EMA50 gap/slope, trend floor, quiet ratio, ret20 floor를 강하게 넣으면 전략의 핵심 진입 구간이 사라진다.

다음 개발에서는 이 계열을 우선 제외한다.

---

## 5. 가장 유망했던 후보

### 5.1 LM2_002_ADD_CLOSEPOS_080

기준선에 `close_pos >= 0.80`을 추가한 후보다.

결과:

- trades: 547
- trade_ratio_vs_ref: 0.9239864865
- wins: 332
- losses: 215
- win_rate_pct: 60.6946983547
- final_return_pct: 23.1593743609
- max_return_pct: 23.3543884304
- max_drawdown_pct: 1.1875135340
- official_cd_value: 121.6968401220
- verdict: baseline_fail

기준선 대비:

- 거래 수: 592 → 547, 감소
- 승률: 58.4459% → 60.6947%, 개선
- final_return_pct: 23.8426% → 23.1594%, 하락
- max_return_pct: 24.0623% → 23.3544%, 하락
- MDD: 1.7280% → 1.1875%, 크게 개선
- official_cd_value: 121.7026 → 121.6968, 아주 근소하게 하락

판정:

- 기준선 대체 후보는 아니다.
- 그러나 방어형 후보로는 가치가 있다.
- 다음 개발은 close_pos 구간을 더 촘촘히 쪼개야 한다.

### 5.2 close_pos 계열의 의미

`close_pos >= 0.80`은 반전 캔들이 봉의 상단에서 마감되는 품질을 요구한다.

이번 결과상 close_pos 강화는 다음 효과가 있었다.

- 승률 상승
- MDD 감소
- 수익률 일부 감소

따라서 close_pos는 “공격력 증가 조건”이 아니라 “진입 품질 및 MDD 방어 조건”에 가깝다.

다음 v3에서는 close_pos를 단독으로 더 세밀하게 테스트해야 한다.

추천 구간:

- 0.76
- 0.77
- 0.78
- 0.79
- 0.80
- 0.81
- 0.82
- 0.83
- 0.84

목표:

- cd_value가 121.7026을 초과하는 지점 찾기
- 또는 cd_value를 거의 유지하면서 MDD를 1.2% 이하로 낮추는 방어형 후보 찾기

---

## 6. 조건별 해석

### 6.1 TP03

`LM2_001_BASE_PLUS_TP03`은 기준선과 동일했다.

이유:

- 기준선의 atrp_min이 이미 0.003이다.
- atr_stop 1.05, rr_target 2.5 기준 expected_tp는 최소 `1.05 * 2.5 * 0.003 = 0.007875`다.
- 이는 0.7875%로, TP03 기준인 0.3%를 이미 충분히 넘는다.

따라서 현재 롱 메인 기준선에서는 TP03이 추가 필터로 기능하지 않는다.

다만 프로젝트 규칙상 개선안에는 TP03을 유지한다.

### 6.2 volume 강화

`LM2_016_VAR_RAW_VOL_150`

- trades: 583
- win_rate_pct: 58.8336
- final_return_pct: 23.7810
- max_drawdown_pct: 1.7653
- official_cd_value: 121.5959

`LM2_004_ADD_VOL_160`

- trades: 572
- win_rate_pct: 59.2657
- final_return_pct: 23.6264
- max_drawdown_pct: 1.6862
- official_cd_value: 121.5419

해석:

- volume 강화는 승률을 약간 올릴 수 있다.
- 하지만 수익률을 깎는다.
- raw volume 1.50 단독 변형은 기준선을 넘지 못했다.
- vol 1.60 추가 필터도 기준선을 넘지 못했다.

다음 개발에서는 volume을 단독 강화하기보다 close_pos와 약하게 조합한다.

추천:

- close_pos 0.78 + vol 1.45
- close_pos 0.79 + vol 1.45
- close_pos 0.80 + vol 1.45
- close_pos 0.78 + vol 1.50

### 6.3 body 강화

`LM2_017_VAR_RAW_BODY_038`

- trades: 557
- win_rate_pct: 59.7846
- final_return_pct: 21.9553
- max_drawdown_pct: 1.4270
- official_cd_value: 120.2149

`LM2_005_ADD_BODY_040`

- trades: 533
- win_rate_pct: 60.2251
- final_return_pct: 21.6910
- max_drawdown_pct: 1.4410
- official_cd_value: 119.9375

해석:

- body_atr 강화는 승률을 올리지만 수익률 감소가 크다.
- body_atr 0.38 또는 0.40은 강하다.
- 다음 개발에서는 body_atr 0.36~0.37 정도의 약한 조정만 시도한다.

### 6.4 wick 강화

`LM2_020_VAR_DF_WICK_145`

- trades: 508
- win_rate_pct: 59.8425
- final_return_pct: 21.8278
- max_drawdown_pct: 1.1995
- official_cd_value: 120.3664

`LM2_003_ADD_WICK_150`

- trades: 488
- win_rate_pct: 60.0410
- final_return_pct: 20.8696
- max_drawdown_pct: 1.1367
- official_cd_value: 119.4957

해석:

- wick 강화는 MDD 방어에는 좋다.
- 하지만 수익률 손실이 크다.
- wick 1.45~1.50은 너무 강한 편이다.
- 다음 개발에서는 1.32~1.42 범위의 미세 조정이 더 낫다.

### 6.5 double-flush lookback

`LM2_014_VAR_DF_LOOKBACK_8`

- trades: 589
- final_return_pct: 23.7554
- max_drawdown_pct: 1.8587
- official_cd_value: 121.4551

`LM2_015_VAR_DF_LOOKBACK_12`

- trades: 597
- final_return_pct: 23.6209
- max_drawdown_pct: 1.8523
- official_cd_value: 121.3311

해석:

- lookback 10이 현재 가장 균형이 좋다.
- 8과 12는 모두 기준선보다 MDD가 커졌다.
- 다음 개발에서 lookback은 우선 고정한다.

---

## 7. 다음 v3 개발 방향

### 7.1 1순위: close_pos 정밀 분해

가장 먼저 해야 할 작업은 close_pos 단독 구간 분해다.

추천 후보:

- baseline + close_pos >= 0.76
- baseline + close_pos >= 0.77
- baseline + close_pos >= 0.78
- baseline + close_pos >= 0.79
- baseline + close_pos >= 0.80
- baseline + close_pos >= 0.81
- baseline + close_pos >= 0.82
- baseline + close_pos >= 0.83
- baseline + close_pos >= 0.84

목표:

- 기준선보다 cd_value가 높은 지점 찾기
- 또는 cd_value 거의 동률 + MDD 대폭 감소 후보 찾기

### 7.2 2순위: close_pos + 약한 volume 조합

volume 단독 강화는 기준선을 넘지 못했지만, close_pos와 약하게 결합하면 승률과 MDD 균형을 개선할 가능성이 있다.

추천 후보:

- close_pos 0.77 + vol_ratio >= 1.45
- close_pos 0.78 + vol_ratio >= 1.45
- close_pos 0.79 + vol_ratio >= 1.45
- close_pos 0.80 + vol_ratio >= 1.45
- close_pos 0.78 + vol_ratio >= 1.50
- close_pos 0.79 + vol_ratio >= 1.50

주의:

- vol 1.60은 강하다.
- 수익률을 깎는 경향이 있으므로 1.45~1.50 사이만 우선 테스트한다.

### 7.3 3순위: close_pos + 약한 body 조합

body 0.38~0.40은 너무 강했다.

추천 후보:

- close_pos 0.77 + body_atr >= 0.36
- close_pos 0.78 + body_atr >= 0.36
- close_pos 0.79 + body_atr >= 0.36
- close_pos 0.80 + body_atr >= 0.36
- close_pos 0.78 + body_atr >= 0.37

### 7.4 4순위: close_pos + 약한 wick 조합

wick 1.45~1.50은 너무 강했다.

추천 후보:

- close_pos 0.77 + lower_wick_body_ratio >= 1.34
- close_pos 0.78 + lower_wick_body_ratio >= 1.34
- close_pos 0.79 + lower_wick_body_ratio >= 1.34
- close_pos 0.80 + lower_wick_body_ratio >= 1.34
- close_pos 0.78 + lower_wick_body_ratio >= 1.38
- close_pos 0.79 + lower_wick_body_ratio >= 1.38

### 7.5 제외 권장 조건

다음 조건들은 v3에서 우선 제외한다.

- EMA50 gap
- EMA50 slope
- trend floor
- quiet ratio
- ret20 floor
- double-flush lookback 8 또는 12
- body_atr 0.38 이상 단독 강화
- wick 1.45 이상 단독 강화
- volume 1.60 이상 단독 강화

---

## 8. 다음 개발 파일 작성 규칙

다음 파일은 `run_long_main_dev_v3.py` 형태가 적합하다.

필수 규칙:

1. 기준선 전략 진입 조건을 기본 세팅으로 내장한다.
2. `LM3_000_BASELINE_EXACT_EMBEDDED`를 반드시 포함한다.
3. `LM3_000`이 v2의 기준선 값과 일치하지 않으면 개선안 결과를 해석하지 않는다.
4. 모든 개선 후보는 기준선 진입 조건 통과 후 추가 필터 또는 미세 변형만 적용한다.
5. 외부 절대경로를 코드에 넣지 않는다.
6. 결과는 현재 파이썬 파일 실행 위치 기준 `./local_results/long_main/LONG_MAIN_DEV_V3_날짜시간/`에 생성한다.
7. 개선안에는 TP03 체크를 유지하되, 현재 구조에서는 실질 필터가 아닐 수 있음을 인지한다.
8. EMA/quiet/trend floor 계열은 v3에서 제외한다.

---

## 9. 판정 기준

기준선:

- trades: 592
- max_return_pct: 24.0623
- max_drawdown_pct: 1.7280
- official_cd_value: 121.7026

개선 후보의 성공 기준:

1. 공격형 성공

- official_cd_value > 121.7026
- max_return_pct >= 24.0623 근처 또는 초과
- MDD가 기준선보다 크게 악화되지 않을 것

2. 방어형 성공

- official_cd_value가 기준선과 거의 동률
- MDD가 기준선보다 의미 있게 낮을 것
- 예: MDD 1.20% 이하, cd_value 121.6 이상

3. 폐기 기준

- trade 수가 기준선 대비 지나치게 감소
- max_return이 크게 감소
- MDD가 증가하면서 수익률도 감소
- EMA/quiet류처럼 전략 본질을 훼손

---

## 10. 최종 요약

v2는 기준선 복원 성공이라는 점에서 중요한 전환점이다.

v1의 문제는 기준선 원본이 아닌 proxy 진입식을 사용한 것이었고, v2는 이를 바로잡았다.

이번 결과에서 기준선을 이긴 개선안은 없지만, `LM2_002_ADD_CLOSEPOS_080`은 MDD를 크게 낮추면서 cd_value를 거의 유지했다. 따라서 다음 v3는 close_pos 중심의 정밀 조정으로 가는 것이 가장 합리적이다.

다음 작업자는 이 문서를 읽고 다음 원칙을 지켜야 한다.

- 기준선 exact 복원부터 확인한다.
- 기준선 진입식 위에만 조건을 추가한다.
- close_pos 중심으로 세밀하게 탐색한다.
- EMA, quiet, ret20 floor 계열은 우선 제외한다.
- 기준선을 이기지 못해도 MDD 방어형 후보는 별도 가치가 있다.
