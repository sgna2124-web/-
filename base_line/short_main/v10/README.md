# short_main v10 기준선

## 상태

공식 기준선 갱신 완료.

이 버전은 `short_max v8` 기반 mix2 후보 중 short_main식 기준으로 1위를 기록한 `smv8_mix2_02_prev_mix18_top2_top3_timereduce6`를 리테스트하여 승격한 버전이다.

주의: 저장소에는 이미 `short_main/v8`, `short_main/v9`가 존재한다. 따라서 이번 갱신은 `short_main/v10`으로 기록한다.

## 기준선 이름

- strategy: `smv8_mix2_02_prev_mix18_top2_top3_timereduce6`
- retest_strategy: `smv8_mix2_02_prev_mix18_top2_top3_timereduce6__short_main_formula_top1_RETEST`
- axis: `short_main`
- baseline_version: `short_main/v10`
- source_old_baseline: `short_main/v9`
- origin: `short_max v8 derived mix2 candidate`
- selection_rule: `short_main formula, MDD under 5%, highest official_cd_value after retest`
- engine: `actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231`
- data_scope: `train_only_until_2025_12_31_end`
- holdout_start: `2026-01-01 00:00:00`

## 공식 성과

2025-12-31 23:59:59까지의 train 구간 결과다. 2026 데이터는 검증용 holdout으로 남기며, 지표 계산 전부터 제외했다.

- trades: 50,501
- wins: 6,382
- losses: 44,119
- win_rate_pct: 12.637373517356092
- final_asset: 2073.439096027405
- final_return_pct: 1973.4390960274047
- peak_asset: 2073.447230393373
- max_return_pct: 1973.4472303933733
- max_drawdown_pct: 4.814092666588577
- official_cd_value: 1973.629559329422
- profit_factor: 1.5675065791005796
- max_conc: 302
- max_conc_unique_symbols: 302
- same_bar_trades: 3,533
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 119
- generated_entry_candidates: 50,620
- executed_entries: 50,501
- load_errors: 0

## short_main v9 대비

- previous_strategy: `short_main_v9_wick120_dev03475_timeout215_actual_bar_engine`
- previous_official_cd_value: 1233.487844954492
- previous_max_drawdown_pct: 4.770262221769094
- previous_trades: 36,791

차이:

- delta_cd_vs_v9: +740.14171437493
- delta_mdd_vs_v9: +0.04383044481948275
- delta_trades_vs_v9: +13,710

## short_main v8 대비 참고

- previous_v8_strategy: `short_main_v8_wick125_actual_bar_engine`
- previous_v8_official_cd_value: 1198.1725532607445
- previous_v8_max_drawdown_pct: 4.612307655489422
- previous_v8_trades: 35,803

차이:

- delta_cd_vs_v8: +775.4570060686775
- delta_mdd_vs_v8: +0.20178501109915475
- delta_trades_vs_v8: +14,698

## short_main v7 대비 참고

- previous_v7_strategy: `short_main_v6_timeout210_actual_bar_engine`
- previous_v7_trades: 35,330
- previous_v7_max_return_pct: 1115.0033786152128
- previous_v7_max_drawdown_pct: 4.607649926423363
- previous_v7_official_cd_value: 1159.0202763344078
- previous_v7_profit_factor: 1.5743323511471792

차이:

- delta_cd_vs_v7: +814.6092829950142
- delta_mdd_vs_v7: +0.20644274016521358
- delta_trades_vs_v7: +15,171
- profit_factor: 1.5743323511471792 -> 1.5675065791005796

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

주의: `position_fraction = 0.01`은 포지션당 현재 equity의 1% 진입이다. 총 계좌 노출 1% 제한이 아니다. 이 전략은 최대 동시 포지션 302개를 기록했다.

## 핵심 파라미터

- ema_period: 20
- rsi_period: 14
- atr_period: 14
- short_dev: 0.035
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
- time_reduce_bars: 6
- time_reduce_to_risk_frac: 0.05
- fail_fast_bars: 10
- fail_fast_min_progress_r: 0.1
- atr_pct_min: 0.0
- atr_pct_max: 999.0
- close_position_min: -999.0
- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5

## 진입 조건 요약

- close가 EMA20보다 최소 3.5% 이상 위에 있어야 한다.
- upper wick이 body의 1.3배 이상이어야 한다.
- RSI 직접 gate는 사용하지 않는다.
- RSI는 `short_score` 내부 보조 점수로만 사용한다.
- `short_score >= 2.35`를 entry mask 내부에서 만족해야 한다.
- 기대 TP 비율은 최소 0.3% 이상이어야 한다.

## 청산 조건 요약

- stop: entry + ATR14 * 2.0
- target: entry - rr_mult * risk, rr_mult = 5.5
- time reduce: 진입 후 6봉 이상 지나고 유리한 진행이 있으면 stop을 entry + risk * 0.05 이하로 축소
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

- short_main v9 대비 CD가 크게 상승했다.
- MDD 5% 미만 기준을 유지한다.
- 단독 리테스트에서 mix2 결과와 동일한 성과를 재현했다.
- active_leftover, pending_leftover, load_errors가 모두 0이다.

## 단점과 주의사항

- short_main v9보다 MDD가 0.0438%p 높다.
- short_main v7보다 MDD가 0.2064%p 높고 profit factor는 소폭 낮다.
- 출처가 short_main 직접 개발 후보가 아니라 short_max v8 파생 후보다.
- 2026 holdout 검증 전까지는 실전 일반화 여부를 확정하면 안 된다.

## 재현 source of truth

- 결과 출처: `local_results/short_max/short_max_v8_mix2_top_retest_v1_results/summary_compact.csv`
- 메타데이터: `local_results/short_max/short_max_v8_mix2_top_retest_v1_results/run_metadata.json`
- 공식 재현 코드: `base_line/short_main/v10/frozen_reproduce_runner.py`

## 기준선 판정

short_main v10은 short_main 공식 기준선으로 승격한다.
이후 short_main 개선은 이 버전을 기준으로 한다.
