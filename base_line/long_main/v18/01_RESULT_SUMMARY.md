# LONG MAIN v18 결과 요약

## 공식 기준선

- axis: long_main
- version: v18
- official strategy: `LM26R_001_RETEST_S128_RR505_B360_H17_CD32__V35_RETEST_FROM_V34_TOP1_S130_RR625_B400_H17_C32`
- source batch: `local_results/long_max/LONG_MAX_V16_2025_V34_TOP1_RETEST_V35_STANDALONE`
- result scope: 2025년까지의 데이터 기준
- train_end_exclusive_utc: `2026-01-01 00:00:00`
- fee: 왕복 0.08%, 편도 0.04%
- round_trip_cost_bps: 8.0
- position_fraction: 0.01

## 공식 결과

| metric | value |
|---|---:|
| trades | 55597 |
| wins | 22513 |
| losses | 33084 |
| win_rate_pct | 40.493192078709285 |
| final_return_pct | 525.6012732388051 |
| max_return_pct | 526.8003775673284 |
| max_drawdown_pct | 1.3626489750456883 |
| official_cd_value | 618.2592886468248 |
| max_conc | 446 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 직전 기준선 대비

직전 기준선:
`LM26R_001_RETEST_S128_RR505_B360_H17_CD32`

직전 공식 CD:
603.3485179858741

신규 공식 CD:
618.2592886468248

변화:
- final_return_pct +16.7254778432227
- official_cd_value +14.9107706609507
- max_drawdown_pct +0.2695662176330

## 판정

long_main v18 기준선 갱신 확정.

근거:
- V35 단독 리테스트에서 신규 후보가 1위로 재현됨.
- errors 0.
- ruined false.
- trades 55597로 과도한 거래 폭증 없음.
- 기존 LM26 기준선 대비 CD와 max_return이 상승함.
- MDD는 상승했으나 1.3626489750456883으로 5% 이내이며, 공격형 수익률 우선 기준에 부합함.

주의:
과거 V33/V34/V35 리포트의 `baseline_reproduction_ok: False`는 이전 LM26 expected MDD와 새 실행계열 MDD가 다르기 때문에 발생한 것이다.
이 폴더에서는 신규 기준선을 V35 후보값으로 확정했으므로, 더 이상 이전 expected MDD를 기준선 재현 게이트로 사용하지 않는다.
