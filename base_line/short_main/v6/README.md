# short_main v6 기준선

## 공식 기준선명

short_main_v6_timeout210

## 부모 기준선

short_main v5: `SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge`

## 승격 전략

`timeout210`

## 승격 배경

short_max v6 기준선 후보 개발 중 `timeout210`이 short_main 기준에서 가장 좋은 결과를 기록했다.

`timeout210`은 부모 기준선의 진입 구조를 유지하면서 `timeout_bars`만 200에서 210으로 늘린 변형이다. 수익률이 증가했고 MDD는 오히려 낮아졌다.

## 공식 리테스트 결과

- 결과 폴더: `local_results/short_max/short_max_v6_top_candidates_retest_v1_results`
- 실행 파일: `run_short_max_v6_top_candidates_retest_v1.py`
- 데이터: 597 CSV
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- side: short only
- entry: next bar open
- use_rsi_gate: false
- score_min_short 적용 위치: entry mask 내부
- dd_brake_mode: edge_current
- runtime_external_path_reference: false

## 공식 성과

- strategy: timeout210
- description: RETEST short_main top1: timeout_bars 210
- trades: 33,989
- win_rate_pct: 14.213421989467182
- final_return_pct: 931.1433546380067
- max_return_pct: 931.6464095007982
- max_drawdown_pct: 4.506694290977831
- official_cd_value: 985.153259660748
- profit_factor: 1.5653897913886468
- max_conc: 277
- max_conc_unique_symbols: 277
- same_bar_trades: 3,112
- active_leftover: 0
- blocked_by_guard: 30
- generated_trades_before_score_filter: 34,019
- errors: 0

## v5 대비 개선폭

short_main v5 기준선:

- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

short_main v6:

- trades: 33,989
- max_return_pct: 931.6464095007982
- max_drawdown_pct: 4.506694290977831
- official_cd_value: 985.153259660748

개선폭:

- trades: -16
- max_return_pct: +32.636838583887766
- max_drawdown_pct: -0.05232962947469044
- official_cd_value: +31.68877404954958

## short_main 승격 판정

short_main 기준은 MDD 5% 미만에서 official_cd_value를 개선하는 것이다.

`timeout210`은 MDD가 4.506694290977831로 5% 미만이고, official_cd_value가 985.153259660748로 기존 v5보다 높다. 따라서 short_main v6 기준선으로 채택한다.

## 핵심 변경점

부모 기준선 대비 변경은 하나다.

```python
timeout_bars = 210
```

부모 기준선의 나머지 핵심 구조는 유지한다.

```python
short_dev = 0.035
short_rsi_min = 77.0
use_rsi_gate = False
short_wick_mult = 1.3
score_min_short = 2.35
score_dev_weight = 1.0
score_rsi_weight = 0.8
score_wick_weight = 0.7
dd_brake_trigger_pct = 0.03
dd_brake_freeze_steps = 5
dd_brake_mode = "edge_current"
atr_stop_mult = 1.8975
rr_mult = 5.75
min_expected_tp = 0.003
time_reduce_bars = 8
time_reduce_to_risk_frac = 0.05
fail_fast_bars = 10
fail_fast_min_progress_r = 0.1
```

## 재현 필수 규칙

- 외부 경로 참조 금지
- 수수료 fee_per_side 0.0004 유지
- position_fraction 0.01 유지
- initial_asset 100.0 유지
- next bar open 진입 유지
- RSI 직접 gate false 유지
- RSI는 short_score 내부에서만 사용
- score_min_short 2.35는 entry mask 내부 적용
- dd_brake는 포트폴리오 평가 단계에서 edge_current 방식으로 적용
- same-bar 즉시 청산 유지
- active_leftover 0 확인

## 다음 개발 방향

short_main v6은 구조 변경 폭이 작고 MDD도 낮아진 안정형 개선이다. 다음 개발은 timeout 주변값과 MDD 완화 조건을 중심으로 진행한다.

우선 후보:

- timeout_bars 205, 210, 215, 220
- time_reduce_bars 7, 8, 9
- score_min_short 2.35, 2.40
- short_dev 0.0350, 0.0355
- dd_brake_trigger_pct 0.025, 0.030, 0.035
