# short_max v7 기준선

## 공식 기준선명

short_max_v7_devw120

## 부모 기준선

short_max v6: `SM16_C05_remove_no_rsi_dev035_exact_entrymask_ddedge`

## 승격 전략

`devw120`

## 승격 배경

short_max v6 기준선을 부모로 한 후보 개발 및 단독 리테스트에서 `devw120`이 short_max 기준 1위를 기록했다.

`devw120`은 부모 기준선의 진입 구조를 유지하면서 `score_dev_weight`만 1.0에서 1.2로 높인 변형이다. 즉 EMA20 대비 과열 이격이 강한 신호를 더 높게 평가하는 방식이다.

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

- strategy: devw120
- description: RETEST short_max top1: score_dev_weight 1.20
- trades: 43,681
- win_rate_pct: 13.827522263684438
- final_return_pct: 1221.3299878755902
- max_return_pct: 1221.9746135454966
- max_drawdown_pct: 5.6636954922983485
- official_cd_value: 1247.1019969487918
- profit_factor: 1.5021526593629504
- max_conc: 295
- max_conc_unique_symbols: 295
- same_bar_trades: 3,694
- active_leftover: 0
- blocked_by_guard: 152
- generated_trades_before_score_filter: 43,833
- errors: 0

## v6 대비 개선폭

short_max v6 기준선:

- trades: 34,005
- max_return_pct: 899.0095709169104
- max_drawdown_pct: 4.559023920452521
- official_cd_value: 953.4644856111984

short_max v7:

- trades: 43,681
- max_return_pct: 1221.9746135454966
- max_drawdown_pct: 5.6636954922983485
- official_cd_value: 1247.1019969487918

개선폭:

- trades: +9,676
- max_return_pct: +322.96504262858616
- max_drawdown_pct: +1.1046715718458273
- official_cd_value: +293.6375113375934

## short_max 승격 판정

short_max 기준은 official_cd_value 1위다. v7은 기존 v6보다 official_cd_value가 크게 높고, MDD도 10% 미만이다. active_leftover와 errors도 0이다.

따라서 `devw120`을 short_max v7 기준선으로 채택한다.

## short_main 사용 여부

이 전략은 short_main 기준선으로는 사용하지 않는다.

이유:

- short_main 기준은 MDD 5% 미만이다.
- devw120의 MDD는 5.6636954922983485로 5%를 초과한다.

따라서 이 전략은 short_max 전용 고수익형 기준선이다.

## 핵심 변경점

부모 기준선 대비 변경은 하나다.

```python
score_dev_weight = 1.2
```

부모 기준선의 나머지 핵심 구조는 유지한다.

```python
short_dev = 0.035
short_rsi_min = 77.0
use_rsi_gate = False
short_wick_mult = 1.3
score_min_short = 2.35
score_rsi_weight = 0.8
score_wick_weight = 0.7
dd_brake_trigger_pct = 0.03
dd_brake_freeze_steps = 5
dd_brake_mode = "edge_current"
atr_stop_mult = 1.8975
rr_mult = 5.75
min_expected_tp = 0.003
timeout_bars = 200
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

short_max v7은 dev score 가중치를 키우면서 수익률을 크게 끌어올린 전략이다. 다음 개선은 score_dev_weight 주변값과 MDD 완화 방향을 중심으로 진행한다.

우선 후보:

- score_dev_weight 1.15, 1.20, 1.25
- score_min_short 2.35, 2.40, 2.45
- short_dev 0.0350, 0.0355, 0.0360
- max_active_cap 280~295
- dd_brake_trigger_pct 0.025~0.035
- timeout_bars 190~210
- time_reduce_to_risk_frac 0.04~0.05
