# short_main v9 기준선

## 상태

공식 기준선 갱신 완료.

이 버전은 `short_main v8`의 actual bar engine과 핵심 위험관리 구조를 그대로 유지하면서, v2.3 조합 실험에서 short_main 기준을 통과한 1위 후보 `SM23_D02_wick120_dev03475_timeout215`를 승격한 버전이다.

완전히 새로운 전략이 아니다. v8 기준선의 진입 조건과 청산 조건을 작은 폭으로 개발한 short_main 기준선이다.

## 기준선 이름

- strategy: `short_main_v9_wick120_dev03475_timeout215_actual_bar_engine`
- axis: `short_main`
- baseline_version: `short_main/v9`
- source_candidate: `SM23_D02_wick120_dev03475_timeout215`
- parent_strategy: `short_main_v8_wick125_actual_bar_engine`
- previous_baseline: `short_main/v8`
- engine: `actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231`
- data_scope: `train_only_until_2025_12_31_end`
- train_end: `2025-12-31 23:59:59`
- holdout_start: `2026-01-01 00:00:00`

## 공식 성과

2025-12-31 23:59:59까지의 train 구간 결과다. 2026 데이터는 검증용 holdout으로 남기며, 지표 계산 전부터 제외했다.

- trades: 36,791
- wins: 5,171
- losses: 31,620
- win_rate_pct: 14.055067815498356
- final_asset: 1294.9206565723089
- final_return_pct: 1194.9206565723089
- peak_asset: 1295.2759019740386
- max_return_pct: 1195.2759019740386
- max_drawdown_pct: 4.770262221769094
- official_cd_value: 1233.487844954492
- profit_factor: 1.5698636647889879
- max_conc: 287
- max_conc_unique_symbols: 287
- same_bar_trades: 3,354
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 56
- generated_entry_candidates: 36,847
- executed_entries: 36,791
- load_errors: 0

## v8 기준선 대비

v8 기준선:

- strategy: `short_main_v8_wick125_actual_bar_engine`
- trades: 35,803
- max_return_pct: 1156.1081244457819
- max_drawdown_pct: 4.612307655489422
- official_cd_value: 1198.1725532607445
- profit_factor: 1.5763819188582828
- max_conc: 285
- same_bar_trades: 3,246

v9 개선폭:

- delta_trades: +988
- delta_max_return_pct: +39.16777752825669
- delta_max_drawdown_pct: +0.1579545662796722
- delta_official_cd_value: +35.31529169374744
- delta_same_bar_trades: +108
- delta_max_conc: +2

## 공식 성과 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

## 핵심 환경

- csv_files: 597
- loaded_symbols: 597
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008
- use_rsi_gate: false
- dd_brake_mode: edge_current
- runtime_external_path_reference: false
- no_candle_limit: true
- train_only_until_2025: true
- holdout_2026_reserved: true

## 핵심 파라미터

v9에서 v8 대비 바뀐 값은 3개다.

- short_wick_mult: 1.25 -> 1.20
- short_dev: 0.035 -> 0.03475
- timeout_bars: 210 -> 215

나머지 값은 v8 기준선과 동일하다.

- ema_period: 20
- rsi_period: 14
- atr_period: 14
- short_dev: 0.03475
- short_rsi_min: 77.0
- use_rsi_gate: false
- short_wick_mult: 1.20
- score_min_short: 2.35
- score_dev_weight: 1.0
- score_rsi_weight: 0.8
- score_wick_weight: 0.7
- score_dev_cap: 2.0
- score_rsi_cap: 2.0
- score_wick_cap: 2.5
- wick_atr_floor_mult: 0.2
- atr_stop_mult: 1.8975
- rr_mult: 5.75
- min_expected_tp: 0.003
- timeout_bars: 215
- time_reduce_bars: 8
- time_reduce_to_risk_frac: 0.05
- fail_fast_bars: 10
- fail_fast_min_progress_r: 0.1
- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5

## actual bar engine 규칙

5분봉 timestamp가 `12:00`이면 해당 캔들은 `12:00:00 ~ 12:04:59` 구간이다. 따라서 `12:00` 캔들 내부의 TP/SL 청산 결과를 `12:00 open` 신규 진입 판단에 사용하면 안 된다.

공식 처리 순서:

1. `t` open에서는 `t-1` close에서 확정된 pending entry만 진입한다.
2. `t` 캔들의 high/low/close로 청산을 평가한다.
3. `t` 캔들 내부 청산 결과는 `t+1` open부터 equity와 slot에 반영한다.
4. `t` close에서 새 신호가 나오면 `t+1` open pending entry가 된다.
5. same-bar TP/SL은 허용한다.
6. DD brake는 `t` 캔들 종료 후 발생한 drawdown edge를 `t+1`부터 적용한다.
7. 백테스트 종료 시 남은 포지션은 마지막 close로 forced_end 청산한다.

## 기준선 판정

short_main v9은 short_main 공식 기준선으로 승격한다.
이후 short_main 개선은 이 버전을 기준으로 한다.

주의: v9은 v8 대비 MDD가 상승한 수익 확장형 기준선이다. 다만 MDD가 5% 미만이고 official_cd_value가 뚜렷하게 개선되어 short_main 기준선으로 승격한다.
