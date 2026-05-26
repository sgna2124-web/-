short_main v14 공식 기준선 기록

전략명
smv12_topmix2_07_mix2_07_top1_reduce_frac000

축
short_main

이전 기준선
base_line/short_main/v13
smv11_topcombo1_03_combo03_stop215_rr540_tr4_top1_plus_rr540

갱신 사유
short_max v12 상위 조합 2차 1위 후보를 단독 리테스트했고 gate를 통과했다.
MDD가 3.2701695697124222%로 short_main 기준인 5% 미만을 충분히 통과한다.
기존 short_main v13보다 official_cd_value, max_return_pct, max_drawdown_pct, profit_factor가 모두 개선되었다.

공식 결과 출처
local_results/short_max/short_max_v12_topmix2_07_retest_v2_results/summary_compact.csv

공식 리테스트 러너
run_short_max_v12_topmix2_07_retest_v2.py

공식 성과
trades: 66572
wins: 5664
losses: 60908
win_rate_pct: 8.508081475695487
final_return_pct: 6864.507074601753
max_return_pct: 6864.507074601753
max_drawdown_pct: 3.2701695697124222
official_cd_value: 6736.755883567657
profit_factor: 2.190937542731158
max_conc: 305
max_conc_unique_symbols: 305
same_bar_trades: 3524
forced_end_trades: 12
active_leftover: 0
pending_leftover: 0
load_errors: 0

이전 short_main v13 대비
v13 official_cd_value: 4136.12683229544
v14 official_cd_value: 6736.755883567657
delta_cd_vs_v13: +2600.629051272217
v13 max_drawdown_pct: 4.260534220480682
v14 max_drawdown_pct: 3.2701695697124222
delta_mdd_vs_v13: -0.9903646507682602
v13 trades: 63863
v14 trades: 66572
delta_trades_vs_v13: +2709
v13 profit_factor: 1.7783712609125915
v14 profit_factor: 2.190937542731158
delta_pf_vs_v13: +0.4125662818185667

핵심 전략 해석
진입 조건은 short_main v13과 동일한 short_max v12 계열 진입 조건을 유지한다.
이번 갱신의 본질은 청산/방어 구조 개선이다.
time_reduce_bars를 3으로 두고, time_reduce_to_risk_frac를 0.00으로 낮춰 유리한 움직임이 나온 포지션의 손실 허용폭을 거의 본전선까지 축소한다.
timeout_bars를 240으로 늘려 좋은 포지션의 목표가 도달 시간을 확보한다.
DD brake는 0.035 / freeze 4로 약간 느슨하게 해 수익 기회를 덜 막는다.
fail_fast_bars는 12다.

진입 조건
raw OHLCV는 2025-12-31 23:59:59까지만 사용한다.
2026-01-01 이후 데이터는 EMA, RSI, ATR 계산 전부터 제외한다.
EMA: 20
RSI: 14
ATR: 14
short_dev: 0.032
use_rsi_gate: False
short_rsi_min: 77.0
short_wick_mult: 1.3
score_min_short: 2.35
score_dev_weight: 1.3
score_rsi_weight: 0.8
score_wick_weight: 0.7
score_dev_cap: 2.0
score_rsi_cap: 2.0
score_wick_cap: 2.5
wick_atr_floor_mult: 0.2
min_expected_tp: 0.003

진입 판정
close / ema20 - 1.0 >= 0.032
upper_wick >= 1.3 * body
score >= 2.35
use_rsi_gate가 False이므로 RSI는 점수에는 들어가지만 단독 필터로는 쓰지 않는다.

score 계산
score = 1.3 * dev_score + 0.8 * rsi_score + 0.7 * wick_score

dev_score = clamp((close / ema20 - 1.0) / short_dev, 0, 2.0)
rsi_score = clamp((rsi14 - 77.0) / 10.0, 0, 2.0)
wick_score = clamp(log1p(upper_wick / max(abs(body), atr14 * 0.2, 1e-12)), 0, 2.5)

진입 가격
신호는 i번째 캔들 close 기준으로 확정한다.
실제 진입은 i+1번째 캔들 open에서 한다.
숏 진입 가격은 open[i+1]이다.

청산 조건
atr_stop_mult: 2.15
rr_mult: 5.4
risk = atr14 * 2.15
stop = entry + risk
target = entry - 5.4 * risk

time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
bars_held >= 3이고 mfe_r > 0이면 stop = min(stop, entry + risk * 0.00)

fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
bars_held >= 12이고 mfe_r < 0.1이고 close > entry이면 해당 close에서 청산한다.

timeout_bars: 240
bars_held >= 240이면 해당 close에서 청산한다.

DD brake
mode: edge_current
dd_brake_trigger_pct: 0.035
dd_brake_freeze_steps: 4
현재 equity가 peak_equity 대비 -3.5% 이하로 처음 내려갈 때 다음 timestamp부터 신규 진입을 4 step 차단한다.

공식 엔진
actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231

엔진 규칙
1. t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
2. t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
3. t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
4. 같은 timestamp에서 청산된 자리를 같은 timestamp 신규 진입에 재사용하지 않는다.
5. same-bar TP/SL은 유지한다.
6. DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
7. train 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.

환경
initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
csv_file_count: 597
loaded_symbols: 597
load_errors: 0
data_dir: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
train_end: 2025-12-31 23:59:59
holdout_start: 2026-01-01 00:00:00

재현 주의사항
외부 json config를 참조하지 않는다.
외부 runner를 import하지 않는다.
2026 데이터는 지표 계산 전 제외해야 한다.
수수료는 편도 0.04%다.
자산 분할 진입은 1%다.
백테스트 결과 비교는 탐색 결과가 아니라 단독 리테스트 v2 결과를 공식값으로 사용한다.
short_main v14는 short_max v13과 동일한 전략을 사용하되 short_main식 MDD 5% 미만 기준을 만족하여 승격된 기준선이다.
