# short_main v12 전략 문서

## 공식 기준선

- strategy: smv10_dev1_01_v10_stop210_rr550
- axis: short_main
- baseline_version: short_main/v12
- 이전 기준선: short_main/v11, smv9_topcombo1_01_tr4_stop205_rr550
- 승격 사유: MDD 5% 미만에서 기존 short_main v11보다 official_cd_value가 높고, MDD도 낮다.
- 결과 출처: local_results/short_max/short_max_v10_dev_1h_candidates_v1_results/summary_compact.csv

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

## 전략 구조

short_main v12는 short_max v11과 같은 전략 조건을 사용한다. 축(axis)만 short_main으로 기록한다. 이유는 이 전략이 MDD 4.38893845928694로 short_main식 MDD 5% 미만 조건을 만족하면서 기존 short_main v11의 official_cd_value를 초과했기 때문이다.

## v11 대비 핵심 변경

- atr_stop_mult: 2.05 -> 2.10
- rr_mult: 5.5 유지
- time_reduce_bars: 4 유지
- 진입 조건은 기존 short_main v11과 동일

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

- dev_score = min(max((close / ema20 - 1) / 0.032, 0), 2.0)
- rsi_score = min(max((rsi14 - 77.0) / 10, 0), 2.0)
- wick_score = min(log1p(max(0, upper_wick / max(abs(body), atr14 * 0.2, 1e-12))), 2.5)

## 진입 가격과 TP/SL

- entry_price: 다음 캔들 open
- risk: atr14 * 2.10
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

- trades: 64128
- wins: 7022
- losses: 57106
- win_rate_pct: 10.9499750499002
- final_return_pct: 3942.1044355472736
- max_return_pct: 3942.1044355472736
- max_drawdown_pct: 4.38893845928694
- official_cd_value: 3864.6989594109964
- profit_factor: 1.7555392280496656
- max_conc: 310
- max_conc_unique_symbols: 310
- same_bar_trades: 3696
- active_leftover: 0
- pending_leftover: 0
- blocked_by_guard: 151
- generated_entry_candidates: 64279
- executed_entries: 64128
- load_errors: 0

## v11 대비 변화

- previous_strategy: smv9_topcombo1_01_tr4_stop205_rr550
- previous_trades: 64339
- previous_max_return_pct: 3689.4315334640614
- previous_max_drawdown_pct: 4.629389056231814
- previous_official_cd_value: 3614.004004760479
- previous_profit_factor: 1.726703002070718
- delta_cd_vs_previous: +250.6949546505175
- delta_mdd_vs_previous: -0.24045059694487403
- delta_trades_vs_previous: -211

## 장점

- short_main식 MDD 5% 미만을 만족한다.
- 기존 short_main v11보다 official_cd_value가 상승했다.
- 기존 short_main v11보다 MDD가 낮아졌다.
- profit_factor가 개선되었다.

## 단점과 리스크

- win_rate는 10.9499%로 낮다. 다수 손실과 소수 target 수익에 의존한다.
- max_conc 310으로 동시 포지션 수가 많다.
- stop 폭을 넓힌 구조이므로 급등 손실 포지션의 체류 시간이 길어질 수 있다.
- 2025 train 기준 결과이므로 2026 holdout 검증은 별도로 필요하다.

## 재현 주의사항

- 반드시 frozen_reproduce_runner.py를 사용한다.
- 외부 runner import나 외부 json config를 사용하지 않는다.
- 같은 OHLCV 5분봉 CSV 597개 데이터셋을 사용한다.
- --data-dir는 실제 CSV 폴더를 직접 지정한다.
- BASELINE_GATE_FAILED_DO_NOT_USE.txt가 생성되면 해당 결과는 공식 재현 실패다.
- summary_compact.csv의 gate 기준값이 이 문서의 공식 결과와 일치해야 한다.
