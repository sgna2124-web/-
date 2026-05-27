short_main v15 공식 기준선 기록

전략명
SM42_mdd10_aggr_v01_single_retest

축
short_main

이전 기준선
base_line/short_main/v14
smv12_topmix2_07_mix2_07_top1_reduce_frac000

갱신 사유
short_main v14 이후 신규 진입축 실험에서 MDD 10% 미만 고 CD 후보를 탐색했고, SM41_mdd10_aggr_v01_mdd10_new_axis가 압도적인 1위로 도출되었다.
해당 후보를 환경 잠금 단독 리테스트한 결과 SM42_mdd10_aggr_v01_single_retest에서 원본 탐색 결과와 완전히 같은 수치가 재현되었다.
수수료, 레버리지, 자산 분할 환경은 정상이다.
2025년 4분기 특이점 의존성 점검에서도 2025 Q4를 제외한 구간의 official_cd_value가 기존 v14 기준선을 넘었다.
따라서 short_main은 v15부터 기존 EMA/RSI/윗꼬리 점수형 기준선이 아니라, 넓은 과열/급등/거래량/윗꼬리 클라이맥스 축을 공식 기준선으로 사용한다.

선택 기준
MDD 10% 미만 후보 중 official_cd_value 최대.
단, 기존 v14의 MDD 5% 미만 안정형 기준보다 MDD 허용폭이 커졌으므로 v15는 고 CD 확장형 short_main 기준선으로 기록한다.

공식 결과 출처
local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_SINGLE_RETEST_V4_2_ENVLOCKED/summary_compact.csv

공식 리테스트 러너
base_line/short_main/v15/frozen_reproduce_runner.py
원본 개발 러너: short_main_mdd10_aggr_v01_single_retest_v4_2_envlocked.py

공식 성과
trades: 140827
wins: 11167
losses: 129660
win_rate_pct: 7.9295873660590654
final_return_pct: 25200.7456885644
max_return_pct: 25200.7456885644
max_drawdown_pct: 5.524791831439535
official_cd_value: 23902.932157469306
profit_factor: 1.7005605337643628
generated_signals: 239776
executed_entries: 140827
blocked_entries: 0
max_conc: 361
same_bar_trades: 10412
active_leftover: 0
pending_leftover: 0
load_errors: 0

이전 short_main v14 대비
v14 strategy: smv12_topmix2_07_mix2_07_top1_reduce_frac000
v14 official_cd_value: 6736.755883567657
v15 official_cd_value: 23902.932157469306
delta_cd_vs_v14: +17166.17627390165
v14 max_return_pct: 6864.507074601753
v15 max_return_pct: 25200.7456885644
delta_max_return_vs_v14: +18336.23861396265
v14 max_drawdown_pct: 3.2701695697124222
v15 max_drawdown_pct: 5.524791831439535
delta_mdd_vs_v14: +2.254622261727113
v14 trades: 66572
v15 trades: 140827
delta_trades_vs_v14: +74255
v14 profit_factor: 2.190937542731158
v15 profit_factor: 1.7005605337643628
delta_pf_vs_v14: -0.490377008966795

핵심 전략 해석
v15는 v14의 close/EMA20 과열 + 윗꼬리 + RSI 점수 구조와 다른 신규축이다.
핵심은 넓은 과열 숏 진입이다.
강한 rejection만 골라잡는 구조가 아니라, EMA20 대비 과열, 12캔들 급등, 3캔들 단기 가속, 거래량 과열, 윗꼬리 비중, 종가 위치, 고점 근접성, EMA20 slope 제한을 느슨하게 조합한다.
진입 정밀도는 v14보다 낮고 profit_factor도 낮지만, 거래 수와 수익 확장력이 크게 증가하여 official_cd_value가 크게 상승했다.

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
climax_score_min: 2.8

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
11. climax_score >= 2.8

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
atr_stop_mult: 2.20
rr_mult: 6.20
risk = atr14 * 2.20
stop = entry + risk
target = entry - 6.20 * risk

time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
bars_held >= 3이고 mfe_r > 0이면 stop = min(stop, entry + risk * 0.00)

fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
bars_held >= 12이고 mfe_r < 0.1이고 close > entry이면 해당 close에서 청산한다.

timeout_bars: 270
bars_held >= 270이면 해당 close에서 청산한다.

DD brake
mode: edge_current
dd_brake_trigger_pct: 0.070
dd_brake_freeze_steps: 3
현재 equity가 peak_equity 대비 -7.0% 이하로 처음 내려갈 때 다음 timestamp부터 신규 진입을 3 step 차단한다.

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

2025년 4분기 특이점 점검
결과 출처: local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_Q4_REGIME_CHECK_V4_3
자동 판정: GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14
FULL_TRAIN_TO_2025_END official_cd_value: 23902.932157469306
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 6891.0141
2025_Q4_ONLY official_cd_value: 329.1503
판정: Q4가 후반 복리 증폭에 기여했지만, Q4를 제외해도 기존 v14 official_cd_value 6736.755883567657을 넘는다. 따라서 Q4 특이점만으로 만들어진 전략은 아니다.

재현 주의사항
외부 json config를 참조하지 않는다.
외부 runner를 import하지 않는다.
2026 데이터는 지표 계산 전 제외해야 한다.
수수료는 편도 0.04%다.
레버리지는 1.0이다.
자산 분할 진입은 1%다.
백테스트 결과 비교는 탐색 결과가 아니라 환경 잠금 단독 리테스트 v4.2 결과를 공식값으로 사용한다.
short_main v15는 MDD 10% 미만 고 CD 기준을 만족하여 승격된 기준선이다.
