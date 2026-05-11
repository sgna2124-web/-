# short_max v6 기준선

## 공식 기준선명

SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge

## 원본 전략명

SM16_C05_remove_no_rsi_dev035

## 승격 배경

short_max v5는 short_main v4에서 발견된 `SM16_C05_remove_no_rsi_dev035`의 원본 결과행을 기준으로 기록되어 있었다. 이후 같은 전략을 단독 리테스트한 결과, base_line strategy_code 해석인 exact-entry-mask와 edge_current dd_brake 구조에서 더 높은 official_cd_value가 재현되었다.

short_max 기준은 official_cd_value 1위이므로, 리테스트에서 재현된 953.4644856111984를 short_max v6 기준선으로 승격한다.

## 기준선 계보

- short_max v4: short_max_v4_combo_rsi755_timeout280
- short_max v5: SM16_C05_remove_no_rsi_dev035, 원본 short_main 결과행 기준
- short_max v6: SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge, 단독 리테스트 재현 기준

## 공식 테스트 환경

- 결과 폴더: `local_results/short_max/short_max_v5_v3_top1_retest_results`
- 실행 파일: `run_short_max_v5_v3_top1_retest_v2.py`
- 데이터: 597 CSV
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- side: short only
- entry: next bar open
- score_min_short 적용 위치: entry mask 내부
- dd_brake_mode: edge_current
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

## short_max v5 대비 개선폭

short_max v5:

- trades: 31,798
- max_return_pct: 821.9869251730971
- max_drawdown_pct: 4.6783483625391975
- official_cd_value: 878.8531649564361

short_max v6:

- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

개선폭:

- trades: +2,207
- max_return_pct: +77.0226457438133
- max_drawdown_pct: -0.119324442086676
- official_cd_value: +74.6113206547623

## short_max 승격 판정

short_max 기준은 official_cd_value 1위다. v6는 기존 v5보다 official_cd_value가 높고, MDD도 낮다. active_leftover와 errors도 0이다.

따라서 short_max v6 기준선으로 채택한다.

## 핵심 파라미터

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

이 전략은 RSI 직접 gate 제거 전략이다. RSI가 없는 전략이 아니라, RSI를 score 내부 보조 점수로만 사용하는 전략이다.

`score_min_short >= 2.35`는 entry mask 내부에 포함한다. 이 적용 위치가 v6 재현의 핵심이다.

## 다음 개발 기준

앞으로 short_max 개발은 이 v6 기준선을 부모 전략으로 삼는다.

우선 개선 범위:

- short_dev 0.0345~0.0360
- score_min_short 2.30~2.45
- short_wick_mult 1.2~1.4
- rr_mult 5.65~6.00
- timeout_bars 180~220
- time_reduce_bars 7~9
- dd_brake_trigger_pct 0.025~0.035
- dd_brake_freeze_steps 3~7

## 재현 필수 규칙

- external path 참조 금지
- 수수료 fee_per_side 0.0004 유지
- position_fraction 0.01 유지
- next bar open 진입 유지
- score_min_short는 entry mask 내부 적용
- RSI 직접 gate false 유지
- RSI score 내부 기여 유지
- dd_brake edge_current 유지
- same-bar 즉시 청산 유지
- active_leftover 0 유지
