# long_main v4 결과 요약

## 1. 갱신 판정

long_main 기준선을 v3 `LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08`에서 v4 `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`으로 갱신한다.

v4는 v3 기준선의 진입 조건을 바탕으로 `body_atr` 상한만 완화한 기준선 기반 개선안이다.

---

## 2. 개발 결과 원천

- 결과 폴더: `local_results/long_main/LONG_MAIN_DEV_V8_20260511_101823`
- 개발 배치: `LONG_MAIN_DEV_V8_V3_BASELINE_STRUCTURAL_TEST`
- 후보명: `LM8_021_LOOSER_BODY_GUARD_220`
- 후보 설명: v3 기준선에서 body_atr 상한을 1.60에서 2.20으로 완화
- 기준선 entry source: `raw_l01_cap_reclaim + double_flush_ok`

---

## 3. v3 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V3_LM7_070_ATTACK_REMOVE_CP_WITH_RET20_08 |
| trades | 469 |
| wins | 303 |
| losses | 166 |
| win_rate_pct | 64.6055437100 |
| final_return_pct | 24.6575066055 |
| max_return_pct | 24.9228703822 |
| max_drawdown_pct | 1.0181358195 |
| official_cd_value | 123.3883238790 |
| profit_factor | 4.6238644584 |

---

## 4. v4 갱신 기준선 결과

| 항목 | 값 |
|---|---:|
| strategy | LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220 |
| source_variant | LM8_021_LOOSER_BODY_GUARD_220 |
| trades | 479 |
| wins | 310 |
| losses | 169 |
| win_rate_pct | 64.7181628392 |
| final_return_pct | 24.9404780954 |
| max_return_pct | 25.2063735035 |
| max_drawdown_pct | 1.0904624350 |
| official_cd_value | 123.5780610685 |
| profit_factor | 4.5655373148 |
| verdict | baseline_win |

---

## 5. v3 대비 변화

| 항목 | v3 | v4 | 변화 |
|---|---:|---:|---:|
| trades | 469 | 479 | +10 |
| wins | 303 | 310 | +7 |
| losses | 166 | 169 | +3 |
| win_rate_pct | 64.6055 | 64.7182 | +0.1126 |
| final_return_pct | 24.6575 | 24.9405 | +0.2830 |
| max_return_pct | 24.9229 | 25.2064 | +0.2835 |
| max_drawdown_pct | 1.0181 | 1.0905 | +0.0723 |
| official_cd_value | 123.3883 | 123.5781 | +0.1897 |
| profit_factor | 4.6239 | 4.5655 | -0.0583 |

---

## 6. 해석

v4는 v3보다 거래를 10건 더 허용했다.

추가된 거래의 순효과는 긍정적이다.

- wins: +7
- losses: +3
- final_return_pct: +0.2830
- max_return_pct: +0.2835
- official_cd_value: +0.1897

다만 MDD는 1.0181에서 1.0905로 소폭 증가했다. profit_factor도 소폭 낮아졌다.

따라서 v4의 성격은 다음과 같다.

- v3보다 약간 더 공격적이다.
- 수익성과 max_return을 개선한다.
- MDD는 약간 높아진다.
- cd_value 기준으로는 v3보다 우위다.

프로젝트의 기준선 갱신 원칙인 “갱신 가능하면 조금씩 발전”에 따라 v4를 공식 기준선으로 채택한다.

---

## 7. 실행 조건

- csv_files: 597
- position_fraction: 0.01
- round_trip_cost_bps: 8.0
- fee_per_side 해석값: 0.0004
- round_trip_fee 해석값: 0.0008
- TP03: 개선안 규칙에 따라 적용

---

## 8. 기준선 갱신 결론

v4는 다음 이유로 long_main 공식 기준선으로 갱신한다.

1. v3의 핵심 진입 구조를 유지했다.
2. 변경점이 `body_atr <= 1.60`에서 `body_atr <= 2.20`으로 명확하다.
3. v3 대비 final_return, max_return, win_rate, official_cd_value가 개선되었다.
4. 거래 수 증가가 과도하지 않다.
5. MDD는 증가했지만 제한적이다.

따라서 앞으로 long_main 개발의 기준은 `LONG_MAIN_V4_LM8_021_LOOSER_BODY_GUARD_220`다.
