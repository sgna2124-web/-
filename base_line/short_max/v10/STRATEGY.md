# short_max v10 전략 문서

## 공식 기준선

- strategy: smv9_topcombo1_01_tr4_stop205_rr550
- axis: short_max
- baseline_version: short_max/v10
- 이전 기준선: short_max/v9, smv8_mix2_13_all_timereduce5
- 승격 사유: short_max식 기준인 MDD 10% 미만에서 official_cd_value 1위 후보를 단독 리테스트하여 통과했다.
- 결과 출처: local_results/short_max/short_max_v9_topcombo1_01_retest_v2_results/summary_compact.csv

## 데이터 범위

- train_end: 2025-12-31 23:59:59
- holdout_start: 2026-01-01 00:00:00
- 2026 데이터는 기준선 산출에서 제외한다.
- 2026 데이터는 EMA, RSI, ATR 계산 전부터 제외한다.

## 공식 실행 환경

- data_dir: C:\Users\user\Desktop\LCD\파이썬\코인\Data\time
- CSV 파일 수: 597
- loaded_symbols: 597
- load_errors: 0
- initial_asset: 100.0
- position_fraction: 0.01
- fee_per_side: 0.0004
- round_trip_fee: 0.0008

position_fraction 0.01은 포지션당 현재 equity의 1% 진입이다. 전체 총노출 1% 제한이 아니다.

## 지표

- EMA period: 20
- RSI period: 14
- ATR period: 14
- ATR 계산: true range의 Wilder 계열 EWM, alpha=1/period, adjust=False
- EMA 계산: span=period, adjust=False
- RSI 계산: diff 기준 상승/하락 EWM, alpha=1/period, adjust=False

## 진입 조건

신호 캔들 i의 close에서 아래 조건을 모두 만족하면 다음 캔들 i+1의 open에 숏 pending entry를 건다.

필수 조건:

- close / ema20 - 1 >= 0.032
- upper_wick >= 1.3 * body
- score >= 2.35
- entry open > 0
- expected_tp >= 0.003

RSI hard gate는 사용하지 않는다.

- use_rsi_gate: False
- short_rsi_min: 77.0은 score 계산에는 사용하지만, 단독 필터로는 사용하지 않는다.

## score 계산

score = 1.3 * dev_score + 0.8 * rsi_score + 0.7 * wick_score

- dev_score = min(max((close / ema20 - 1) / short_dev, 0), 2.0)
- rsi_score = min(max((rsi14 - 77.0) / 10, 0), 2.0)
- wick_score = min(log1p(max(0, upper_wick / max(abs(body), atr14 * 0.2, 1e-12))), 2.5)

## 진입 가격과 TP/SL

- entry_price: 다음 캔들 open
- risk: atr14 * 2.05
- stop: entry_price + risk
- target: entry_price - 5.5 * risk
- min_expected_tp: 0.003

## 청산 조건

포지션 진입 후 각 캔들에서 아래 순서로 청산한다.

1. high >= stop이면 stop 청산
2. low <= target이면 target 청산
3. bars_held >= 10이고 mfe_r < 0.1이고 close > entry_price이면 fail_fast 청산
4. bars_held >= 200이면 timeout 청산
5. train 종료까지 남은 active position은 마지막 close로 forced_end 청산

## time reduce

- time_reduce_bars: 4
- time_reduce_to_risk_frac: 0.05
- bars_held >= 4이고 MFE가 0보다 크면 stop을 entry + risk * 0.05 이하로 낮춘다.

v9 대비 핵심 변화:

- time_reduce_bars: 5 -> 4
- atr_stop_mult: 2.0 -> 2.05
- rr_mult: 5.5 유지

해석: 유리하게 움직인 포지션은 더 빨리 방어하고, 손절 폭은 아주 조금 넓혀 불필요한 조기 손절을 줄인다.

## DD brake

- dd_brake_trigger_pct: 0.03
- dd_brake_freeze_steps: 5
- dd_brake_mode: edge_current

equity가 직전 peak 대비 -3% 이하로 내려가는 edge가 발생하면 다음 timestamp부터 5 step 동안 신규 진입을 막는다.

## 실제 바 엔진 규칙

- t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
- t 캔들 내부 청산 결과는 t open 신규 진입에 사용할 수 없다.
- t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영된 것으로 간주한다.
- t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
- same-bar TP/SL은 유지한다.
- DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
- 백테스트 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

## 공식 결과

- trades: 64339
- wins: 7025
- losses: 57314
- win_rate_pct: 10.918727365983308
- final_return_pct: 3689.4315334640614
- max_return_pct: 3689.4315334640614
- max_drawdown_pct: 4.629389056231814
- official_cd_value: 3614.004004760479
- profit_factor: 1.726703002070718
- max_conc: 309
- max_conc_unique_symbols: 309
- same_bar_trades: 3945
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 207
- generated_entry_candidates: 64546
- executed_entries: 64339
- load_errors: 0

## v9 대비 변화

- previous_strategy: smv8_mix2_13_all_timereduce5
- previous_trades: 63105
- previous_max_return_pct: 2743.3304850694603
- previous_max_drawdown_pct: 5.686879318598392
- previous_official_cd_value: 2681.6337117546423
- delta_cd_vs_previous: +932.3702930058366
- delta_mdd_vs_previous: -1.0574902623665787
- delta_trades_vs_previous: +1234

## 장점

- short_max 기준 공식 CD가 크게 개선되었다.
- max_drawdown_pct가 5% 미만으로 내려가 short_main식 조건도 만족한다.
- profit_factor가 1.5926에서 1.7267로 개선되었다.
- time_reduce 4와 stop 2.05 조합이 v9보다 방어와 수익 균형을 더 잘 만든다.

## 단점과 리스크

- win_rate는 10.9187%로 낮다. 다수 손실과 소수 큰 수익에 의존한다.
- max_conc 309로 동시 포지션 수가 많다.
- 2025 train 기준 결과이므로 2026 holdout 검증은 별도로 필요하다.
- same_bar_trades가 3945건 존재한다. same-bar TP/SL은 공식 엔진에서 허용하지만, 실거래 체결 정밀도와는 차이가 날 수 있다.

## 재현 주의사항

- 반드시 frozen_reproduce_runner.py를 사용한다.
- 외부 runner import나 외부 json config를 사용하지 않는다.
- 같은 OHLCV 5분봉 CSV 597개 데이터셋을 사용한다.
- --data-dir는 실제 CSV 폴더를 직접 지정한다.
- BASELINE_GATE_FAILED_DO_NOT_USE.txt가 생성되면 해당 결과는 공식 재현 실패다.
- summary_compact.csv의 gate 기준값이 이 문서의 공식 결과와 일치해야 한다.
