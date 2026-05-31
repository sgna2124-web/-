short_main2 v2 공식 기준선 기록

전략명
SM60_C03_stop240_score270_timeout315

실행 전략명
SMAUD_C03_stop240_score270_timeout315_slip000000

후보 키
C03_stop240_score270_timeout315

축
short_main2

기준선 버전
base_line/short_main2/v2

이전 기준선
base_line/short_main2/v1
SM52_B04_stop230_score270_single_retest

갱신 사유
short_main2 v1의 climax_exhaustion 진입 조건을 그대로 유지한 상태에서 청산/방어 파라미터만 완만하게 변형했다.
C03은 v1 대비 atr_stop_mult를 2.30에서 2.40으로 확대하고, timeout_bars를 285에서 315로 늘리고, dd_brake_trigger_pct를 0.075에서 0.080으로 완화한 후보다.
rr_mult는 6.20으로 유지한다.
진입 조건 자체는 v1과 동일하다.

실전성 감사에서 C03은 C00 기준선보다 official_cd_value, mtm_worstbar_cd_value가 모두 높았고, realized MDD, mtm_close MDD, mtm_worstbar MDD도 기준선보다 약간 더 안정적이었다.
Q4 의존성 점검에서도 Q4 단독 몰빵 전략이 아니며 Q4 제외 구간에서도 기준선보다 높은 성과를 유지했다.
단독 리테스트 v1.3에서 기대값과 완전 일치 재현되었으므로 short_main2/v2 공식 기준선으로 승격한다.

선택 기준
1. short_main2 v1 진입 조건을 유지한 개발형 후보일 것.
2. 2025 train 기준 realized MDD 10% 미만일 것.
3. official_cd_value가 v1 기준선보다 높을 것.
4. 단독 리테스트에서 거래 수와 성과값이 기대값과 일치할 것.
5. Q4 의존성 점검에서 Q4 단독 몰빵 전략이 아닐 것.
6. 실전성 감사에서 mtm_close MDD, mtm_worstbar MDD를 함께 기록할 것.
7. 편도 0.05% 슬리피지 조건에서도 기준선보다 우위를 유지할 것.

공식 결과 출처
local_results/short_main/SHORT_MAIN2_V2_C03_SINGLE_RETEST_V1_3_ENVLOCKED/single_retest_summary_compact.csv

Q4 및 실전성 감사 출처
local_results/short_main/SHORT_MAIN2_V1_Q4_REALISM_RECHECK_V1_2_1_MEMFIX/q4_realism_summary_compact.csv

이전 실전성 감사 출처
local_results/short_main/SHORT_MAIN2_V1_REALISM_AUDIT_V1_1/audit_summary_compact.csv

공식 리테스트 러너
short_main2_v2_C03_single_retest_v1_3_envlocked.py

공식 기준 성과, no slippage, 2025 train
trades: 152030
wins: 11364
losses: 140666
win_rate_pct: 7.4748404920081555
max_return_pct: 73746.55353592646
max_drawdown_pct: 5.888592725709996
official_cd_value: 69498.03075622236
profit_factor: 1.8286053579584032
generated_signals: 267412
executed_entries: 152030
blocked_entries: 0
same_bar_trades: 8883
max_conc: 364
max_conc_unique_symbols: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0

실전성 감사 성과, no slippage, 2025 train
mtm_close_max_return_pct: 73855.85996080964
mtm_close_max_drawdown_pct: 15.017466599306728
mtm_close_cd_value: 62849.56339296499
mtm_worstbar_max_return_pct: 73760.00634635029
mtm_worstbar_max_drawdown_pct: 14.23277215250176
mtm_worstbar_cd_value: 63347.67993125091

이전 short_main2 v1 대비
v1 strategy: SM52_B04_stop230_score270_single_retest
v1 trades: 154015
v1 max_return_pct: 53676.46264218497
v1 max_drawdown_pct: 5.923149464550481
v1 official_cd_value: 50591.202383140204
v1 profit_factor: 1.7648350795085153

v2 trades: 152030
v2 max_return_pct: 73746.55353592646
v2 max_drawdown_pct: 5.888592725709996
v2 official_cd_value: 69498.03075622236
v2 profit_factor: 1.8286053579584032

delta_cd_vs_v1: +18906.828373082157
delta_mdd_vs_v1: -0.034556738840485046
delta_trades_vs_v1: -1985
delta_pf_vs_v1: +0.06377027844988792

단독 리테스트 기대값 대비 차이
delta_vs_target_expected_trades: 0
delta_vs_target_expected_max_return_pct: 0.0
delta_vs_target_expected_max_drawdown_pct: 0.0
delta_vs_target_expected_official_cd_value: 0.0
delta_vs_target_expected_profit_factor: 0.0
gate_target_exact_retest_pass: True

핵심 전략 해석
short_main2 v2는 v1의 진입 조건을 바꾸지 않는다.
C03의 핵심은 과열 숏 진입의 필터를 그대로 둔 채 손절폭과 보유시간을 약간 넓혀, 좋은 방향으로 진행되는 긴 숏 기회를 더 오래 허용하는 것이다.
atr_stop_mult가 2.40으로 넓어졌지만 realized MDD는 v1보다 약간 낮아졌다.
timeout_bars가 315로 늘어나 same_bar_trades가 감소했고, profit_factor와 official_cd_value가 개선되었다.

진입 조건
raw OHLCV는 2025-12-31 23:59:59까지만 사용한다.
2026-01-01 이후 데이터는 EMA, RSI, ATR, volume, return 지표 계산 전부터 제외한다.
EMA: 20
RSI: 14
ATR: 14
entry_mode: climax_exhaustion
precompute_signals: True
short_dev: 0.025
ret12_min: 0.030
ret3_min: 0.004
volume_spike_min: 0.75
upper_range_ratio_min: 0.16
close_position_max: 0.94
green_streak_min: 0
ema20_slope12_min: -0.025
ema20_slope12_max: 0.095
atr_pct_min: 0.0008
atr_pct_max: 0.135
range_spike_min: 0.0
dist_roll_high20_min: -0.08
climax_score_min: 2.7

진입 판정 핵심
1. close / ema20 - 1.0 >= 0.025
2. 12캔들 수익률 ret12 >= 0.030
3. 3캔들 수익률 ret3 >= 0.004
4. volume / volume_ma20 >= 0.75
5. upper_wick / candle_range >= 0.16
6. close_position <= 0.94
7. green_streak >= 0
8. -0.025 <= ema20_slope12 <= 0.095
9. atr_pct가 0.0008 이상 0.135 이하
10. close가 rolling high 20 대비 -8% 이상 위치
11. climax_score >= 2.7

climax_score 계산
climax_score = 1.05 * dev_component + 0.75 * ret_component + 0.15 * volume_component + 0.55 * wick_component + 0.10 * streak_component

dev_component = clamp((close / ema20 - 1.0) / short_dev, 0, 2.0)
ret_component = clamp(ret12 / 0.070, 0, 2.5)
volume_component = clamp(volume_spike / 2.0, 0, 2.0)
wick_component = clamp(upper_range_ratio / 0.38, 0, 2.5)
streak_component = clamp(green_streak / 4.0, 0, 1.5)

진입 가격
신호는 i번째 캔들 close 기준으로 확정한다.
실제 진입은 i+1번째 캔들 open에서 한다.
숏 진입 가격은 open[i+1]이다.
기간 시작 전 신호로 기간 첫 캔들에 진입하지 않는다.

청산 조건
atr_stop_mult: 2.40
rr_mult: 6.20
risk = atr14 * 2.40
stop = entry + risk
target = entry - 6.20 * risk

time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
bars_held >= 3이고 mfe_r > 0이면 stop = min(stop, entry + risk * 0.00)

fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
bars_held >= 12이고 mfe_r < 0.1이고 close > entry이면 해당 close에서 청산한다.

timeout_bars: 315
bars_held >= 315이면 해당 close에서 청산한다.

DD brake
mode: edge_current
dd_brake_trigger_pct: 0.080
dd_brake_freeze_steps: 3
현재 equity가 peak_equity 대비 -8.0% 이하로 처음 내려갈 때 다음 timestamp부터 신규 진입을 3 step 차단한다.

공식 엔진
actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231

엔진 규칙
1. t close에서 만들어진 신규 신호는 t+1 open 진입 후보가 된다.
2. t open에서는 t-1 close에서 확정된 pending entry만 진입한다.
3. t 캔들 내부 청산 결과는 t+1 open부터 equity와 slot에 반영한다.
4. 같은 timestamp에서 청산된 자리를 같은 timestamp 신규 진입에 재사용하지 않는다.
5. same-bar TP/SL은 허용한다.
6. same-bar에서 stop과 target이 동시에 닿으면 stop 우선으로 처리한다.
7. DD brake는 t 캔들 청산 후 발생한 edge를 t+1부터 적용한다.
8. train 종료 시 남은 active position은 마지막 close로 forced_end 청산한다.
9. 2026 데이터는 지표 계산 전 제외한다.

환경
initial_asset: 100.0
position_fraction: 0.01
leverage: 1.0
fee_per_side: 0.0004
round_trip_fee: 0.0008
csv_file_count: 597
loaded_symbols: 597
load_errors: 0
data_dir: C:/Users/user/Desktop/LCD/파이썬/코인/Data/time
train_end: 2025-12-31 23:59:59
holdout_start: 2026-01-01 00:00:00

2025년 4분기 특이점 및 실전성 점검
FULL_TRAIN_TO_2025_END official_cd_value: 69498.03075622236
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 16979.64262769056
2025_Q4_ONLY official_cd_value: 390.894405739309
auto q4_dependency_flag: GENERAL_EDGE_CONFIRMED

편도 0.05% 슬리피지 점검
FULL_TRAIN_TO_2025_END official_cd_value: 15177.194065003236
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 4617.4606705665265
2025_Q4_ONLY official_cd_value: 310.33515316809167
FULL_TRAIN_TO_2025_END mtm_worstbar_cd_value: 14001.429941017343

장점
1. v1보다 official_cd_value가 +18906.828373082157 높다.
2. v1보다 realized MDD가 -0.034556738840485046%p 낮다.
3. v1보다 profit_factor가 +0.06377027844988792 높다.
4. Q4 제외 구간에서도 기준선보다 official_cd_value가 높다.
5. 편도 0.05% 슬리피지에서도 기준선보다 우위가 유지된다.
6. 단독 리테스트에서 기대값과 완전히 일치했다.
7. active_leftover와 pending_leftover가 0이다.

단점 및 주의점
1. realized MDD는 5.8886%지만 MTM 기준 MDD는 14~15% 영역이다.
2. mtm_close_max_drawdown_pct는 15.017466599306728이다.
3. mtm_worstbar_max_drawdown_pct는 14.23277215250176이다.
4. 승률은 7.47% 수준으로 낮다.
5. max_conc가 364로 높아 실거래에서는 동시 포지션과 증거금 사용량을 반드시 고려해야 한다.
6. 2026 holdout 검증은 별도 검증용으로 남긴다.

재현 주의사항
외부 json config를 참조하지 않는다.
외부 runner를 import하지 않는다.
2026 데이터는 지표 계산 전 제외해야 한다.
수수료는 편도 0.04%다.
레버리지는 1.0이다.
position_fraction은 0.01이다.
포지션 수 제한은 없다.
actual bar engine과 no same timestamp reentry 규칙을 반드시 사용한다.
탐색 결과가 아니라 단독 리테스트 v1.3 결과를 공식값으로 사용한다.
