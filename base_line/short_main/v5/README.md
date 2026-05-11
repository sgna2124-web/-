# short_main v5 기준선

## 공식 기준선명

SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge

## 원본 전략명

SM16_C05_remove_no_rsi_dev035

## 승격 배경

short_main v4는 `SM16_C05_remove_no_rsi_dev035`의 원본 결과행을 기준으로 기록되어 있었다. 이후 같은 전략을 base_line에 기록된 실행 가능한 `strategy_code.py` 해석에 맞춰 단독 리테스트했더니 기존 v4보다 더 높은 결과가 재현되었다.

이 리테스트는 후보 전체 실행이 아니라 1위 전략 단독 재검증이다. baseline gate에서 모든 기준값이 완전히 일치했으므로 short_main v5 기준선으로 승격한다.

## 기준선 계보

- short_main v3: SM15_B10_rr575_tr8_f005
- short_main v4: SM16_C05_remove_no_rsi_dev035, 원본 결과행 기준
- short_main v5: SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge, 단독 리테스트 재현 기준

## v4 대비 핵심 차이

파라미터 이름은 동일하지만 실행 해석을 명확히 고정했다.

1. score_min_short 2.35를 entry mask 내부에 포함한다.
2. RSI 직접 gate는 사용하지 않는다.
3. RSI는 short_score 내부에서만 사용한다.
4. dd_brake는 포트폴리오 단계에서 edge_current 방식으로 적용한다.
5. same-bar 거래는 같은 timestamp에서 진입 직후 즉시 청산한다.

## 공식 테스트 환경

- 결과 폴더: `local_results/short_max/short_max_v5_v3_top1_retest_results`
- 실행 파일: `run_short_max_v5_v3_top1_retest_v2.py`
- 데이터: 597 CSV
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- side: short only
- entry: signal candle i 다음 캔들 open
- runtime_external_path_reference: false
- active_leftover: 0
- errors: 0

## 공식 성과

- trades: 34,005
- win_rate_pct: 14.406704896338773
- final_return_pct: 898.4999401921407
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984
- profit_factor: 1.555465134190124
- max_conc: 277
- max_conc_unique_symbols: 277
- same_bar_trades: 3,115
- active_leftover: 0
- blocked_by_guard: 39
- generated_trades_before_score_filter: 34,044
- errors: 0

## short_main v4 대비 개선폭

short_main v4:

- trades: 31,798
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361

short_main v5:

- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

개선폭:

- trades: +2,207
- max_return_pct: +77.0226457438133
- max_drawdown_pct: -0.119324442086676
- official_cd_value: +74.6113206547623

## short_main 승격 판정

short_main 기준은 MDD 5% 미만에서 official_cd_value를 개선하는 것이다.

이 전략은 max_drawdown_pct가 4.559023920452521로 5% 미만을 유지하면서 official_cd_value가 953.4644856111984로 기존 v4의 878.8531649564361을 초과한다.

따라서 short_main v5 기준선으로 채택한다.

## 핵심 진입 구조

```python
short_dev = 0.035
short_rsi_min = 77.0
use_rsi_gate = False
short_wick_mult = 1.3
score_min_short = 2.35
score_dev_weight = 1.0
score_rsi_weight = 0.8
score_wick_weight = 0.7
atr_stop_mult = 1.8975
rr_mult = 5.75
min_expected_tp = 0.003
timeout_bars = 200
time_reduce_bars = 8
time_reduce_to_risk_frac = 0.05
fail_fast_bars = 10
fail_fast_min_progress_r = 0.1
dd_brake_trigger_pct = 0.03
dd_brake_freeze_steps = 5
dd_brake_mode = "edge_current"
```

## 핵심 해석

이 전략은 RSI 직접 gate를 제거한 전략이다. 그러나 RSI를 버린 전략은 아니다. RSI14는 short_score 내부에서 가산점으로만 사용한다.

즉 `rsi14 > 77`을 직접 진입 필수 조건으로 쓰지 않는다. 대신 `rsi14 - 77`이 양수일 때 rsi_score가 올라가고, 이 점수가 short_score에 반영된다.

## 다음 개발 기준

앞으로 short_main 개발은 이 v5 기준선을 부모 전략으로 삼는다.

우선 탐색할 주변값:

- short_dev: 0.0345, 0.0350, 0.0355, 0.0360
- score_min_short: 2.30, 2.35, 2.40, 2.45
- rr_mult: 5.65, 5.75, 5.85
- time_reduce_bars: 7, 8, 9
- dd_brake_trigger_pct: 0.025, 0.030, 0.035
- dd_brake_freeze_steps: 3, 5, 7

## 재현 필수 규칙

- 수수료는 fee_per_side 0.0004를 유지한다.
- 자산 분할은 position_fraction 0.01을 유지한다.
- entry는 next bar open이다.
- score_min_short는 entry mask 내부에 포함한다.
- RSI 직접 gate는 false로 둔다.
- RSI는 score 내부에서만 사용한다.
- dd_brake는 포트폴리오 단계 edge_current로 적용한다.
- same-bar 거래는 진입 직후 같은 timestamp에서 즉시 청산한다.
- active_leftover는 0이어야 한다.
