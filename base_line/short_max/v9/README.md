# short_max v9 기준선

## 상태

공식 기준선 갱신 완료.

이 버전은 `short_max v8`을 기반으로 한 mix2 상위 후보 `smv8_mix2_13_all_timereduce5`를 리테스트하여 승격한 버전이다.

## 기준선 이름

- strategy: `smv8_mix2_13_all_timereduce5`
- retest_strategy: `smv8_mix2_13_all_timereduce5__short_max_formula_top1_RETEST`
- axis: `short_max`
- baseline_version: `short_max/v9`
- source_old_baseline: `short_max/v8`
- origin: `short_max v8 derived mix2 candidate`
- selection_rule: `short_max formula, MDD under 10%, highest official_cd_value after retest`
- engine: `actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231`
- data_scope: `train_only_until_2025_12_31_end`
- holdout_start: `2026-01-01 00:00:00`

## 공식 성과

2025-12-31 23:59:59까지의 train 구간 결과다. 2026 데이터는 검증용 holdout으로 남기며, 지표 계산 전부터 제외했다.

- trades: 63,105
- wins: 7,297
- losses: 55,808
- win_rate_pct: 11.563267569923145
- final_asset: 2843.319336054713
- final_return_pct: 2743.319336054713
- peak_asset: 2843.3304850694603
- max_return_pct: 2743.3304850694603
- max_drawdown_pct: 5.686879318598392
- official_cd_value: 2681.6337117546423
- profit_factor: 1.5925867541542813
- max_conc: 307
- max_conc_unique_symbols: 307
- same_bar_trades: 4,197
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 363
- generated_entry_candidates: 63,468
- executed_entries: 63,105
- load_errors: 0

## short_max v8 대비

- previous_strategy: `short_max_v7_devw120_actual_bar_engine`
- previous_trades: 45,500
- previous_max_return_pct: 1424.4317435070927
- previous_max_drawdown_pct: 6.104584306764704
- previous_official_cd_value: 1431.3715225256192
- previous_profit_factor: 1.4976180824186338

차이:

- delta_cd_vs_v8: +1250.262189229023
- delta_mdd_vs_v8: -0.41770498816631196
- delta_trades_vs_v8: +17,605
- profit_factor: 1.4976180824186338 -> 1.5925867541542813

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

주의: `position_fraction = 0.01`은 포지션당 현재 equity의 1% 진입이다. 총 계좌 노출 1% 제한이 아니다. 이 전략은 최대 동시 포지션 307개를 기록했다.

## 핵심 파라미터

- ema_period: 20
- rsi_period: 14
- atr_period: 14
- short_dev: 0.032
- short_rsi_min: 77.0
- short_wick_mult: 1.3
- score_min_short: 2.35
- score_dev_weight: 1.3
- score_rsi_weight: 0.8
- score_wick_weight: 0.7
- score_dev_cap: 2.0
- score_rsi_cap: 2.0
- score_wick_cap: 2.5
- wick_atr_floor_mult: 0.2
- atr_stop_mult: 2.0
- rr_mult: 5.5
- min_expected_tp: 0.003
- timeout_bars: 200
- time_reduce_bars: 5
- time_reduce_to_risk_frac: 0.05
- fail_fast_bars: 10
- fail_fast_min_progress_r: 0.1
- atr_pct_min: 0.0
- atr_pct_max: 999.0
- close_position_min: -999.0
- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5

## 진입 조건 요약

- close가 EMA20보다 최소 3.2% 이상 위에 있어야 한다.
- upper wick이 body의 1.3배 이상이어야 한다.
- RSI 직접 gate는 사용하지 않는다.
- RSI는 `short_score` 내부 보조 점수로만 사용한다.
- `short_score >= 2.35`를 entry mask 내부에서 만족해야 한다.
- 기대 TP 비율은 최소 0.3% 이상이어야 한다.

## 청산 조건 요약

- stop: entry + ATR14 * 2.0
- target: entry - rr_mult * risk, rr_mult = 5.5
- time reduce: 진입 후 5봉 이상 지나고 유리한 진행이 있으면 stop을 entry + risk * 0.05 이하로 축소
- fail fast: 10봉 이상 경과, MFE가 0.1R 미만이고 close가 entry보다 위면 청산
- timeout: 200봉 경과 시 close 청산
- forced_end: train 구간 마지막 close에서 잔여 포지션 강제 정산

## 실제 바 엔진 규칙

- `t` open에서는 `t-1` close에서 확정된 pending entry만 진입한다.
- `t` 캔들 내부 청산 결과는 `t` open 신규 진입에 사용하지 않는다.
- `t` 캔들 청산 결과는 `t+1` open부터 equity와 slot에 반영한다.
- `t` close에서 새 신호가 나오면 `t+1` open pending entry가 된다.
- same-bar TP/SL은 허용한다.
- DD brake는 `t` 캔들 종료 후 발생한 drawdown edge를 `t+1`부터 적용한다.
- 백테스트 종료 시 남은 포지션은 마지막 close로 forced_end 청산한다.

## 장점

- short_max v8 대비 CD가 크게 상승했다.
- MDD가 v8보다 낮아졌고 profit factor도 상승했다.
- 단독 리테스트에서 mix2 결과와 동일한 성과를 재현했다.
- active_leftover, pending_leftover, load_errors가 모두 0이다.

## 단점과 주의사항

- 승률은 11.56%로 낮다.
- 거래 수가 v8보다 17,605개 증가해 2025 train 구간 과최적화 가능성은 반드시 점검해야 한다.
- 최대 동시 포지션이 307개로 높다.
- 2026 holdout 검증 전까지는 실전 일반화 여부를 확정하면 안 된다.

## 재현 source of truth

- 결과 출처: `local_results/short_max/short_max_v8_mix2_top_retest_v1_results/summary_compact.csv`
- 메타데이터: `local_results/short_max/short_max_v8_mix2_top_retest_v1_results/run_metadata.json`
- 공식 재현 코드: `base_line/short_max/v9/frozen_reproduce_runner.py`

## 기준선 판정

short_max v9은 short_max 공식 기준선으로 승격한다.
이후 short_max 개선은 이 버전을 기준으로 한다.
