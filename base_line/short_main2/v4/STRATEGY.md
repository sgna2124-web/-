short_main2 v4 공식 기준선 기록

전략명
V3MIX07_N02_stop255_rr630_t375

축
short_main2

기준선 버전
base_line/short_main2/v4

이전 기준선
base_line/short_main2/v3
MIX05_A02_A03_failfast14_rr630

갱신 사유
V3MIX07은 topmix2 v1.2에서 1위 후보로 확인되었다.
단독 리테스트에서 topmix2 결과와 동일 수치로 재현되었다.
Q4 의존도 점검에서도 Q4 단독 몰빵이 아닌 일반 구간 엣지가 확인되었다.
Q4 제외 구간에서도 v3 기준선보다 official_cd_value, realized MDD, profit_factor, mtm_worstbar_cd_value, mtm_worstbar_max_drawdown_pct가 모두 개선되었다.

선택 기준
1. short_main2/v3 진입 조건을 유지한 개발형 후보일 것.
2. 2025 train 기준 realized MDD 10% 미만일 것.
3. official_cd_value가 v3 기준선보다 높을 것.
4. 단독 리테스트에서 topmix2 기대값과 동일하게 재현될 것.
5. Q4 의존성 점검에서 Q4 단독 몰빵 전략이 아닐 것.
6. Q4 제외 구간에서도 v3 기준선보다 우위일 것.
7. 실전형 actual bar engine 규칙을 유지할 것.
8. 전체 거래 로그 같은 무거운 결과 파일을 기본 저장하지 않을 것.

공식 결과 출처
local_results/short_main/SHORT_MAIN2_V3MIX07_SINGLE_RETEST_Q4_V1_3/v3mix07_single_q4_summary_compact.csv

개발 후보 출처
local_results/short_main/SHORT_MAIN2_V3_TOPMIX2_V1_2_INDEPENDENT_BASELINE/v3_topmix2_summary_compact.csv

공식 리테스트 및 Q4 점검 러너
short_main2_v3_V3MIX07_single_retest_q4_v1_3.py

공식 기준 성과, no slippage, 2025 train
trades: 149151
wins: 10603
losses: 138548
win_rate_pct: 7.108903057974804
max_return_pct: 113147.92211118022
max_drawdown_pct: 5.540389442518634
official_cd_value: 106973.54619066067
profit_factor: 1.9543969406097241
generated_signals: 267412
executed_entries: 149151
blocked_entries: 0
same_bar_trades: 7479
max_conc: 364
max_conc_unique_symbols: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0

실전성 MTM 참고 결과
mtm_close_max_drawdown_pct: 14.803514321510857
mtm_worstbar_max_drawdown_pct: 14.046920216852365
mtm_worstbar_cd_value: 97353.0658974033

이전 short_main2/v3 대비
v3 strategy: MIX05_A02_A03_failfast14_rr630
v3 trades: 150791
v3 max_return_pct: 86520.8367663832
v3 max_drawdown_pct: 5.879344393880359
v3 official_cd_value: 81528.0994560266
v3 profit_factor: 1.882073174356906
v3 mtm_worstbar_cd_value: 74307.00038895881
v3 mtm_worstbar_max_drawdown_pct: 14.233064755345204

v4 trades: 149151
v4 max_return_pct: 113147.92211118022
v4 max_drawdown_pct: 5.540389442518634
v4 official_cd_value: 106973.54619066067
v4 profit_factor: 1.9543969406097241
v4 mtm_worstbar_cd_value: 97353.0658974033
v4 mtm_worstbar_max_drawdown_pct: 14.046920216852365

delta_cd_vs_v3: +25445.446734634068
delta_mdd_vs_v3: -0.3389549513617247
delta_trades_vs_v3: -1640
delta_pf_vs_v3: +0.07232376625281822
delta_mtm_worstbar_cd_vs_v3: +23046.065508444488
delta_mtm_worstbar_mdd_vs_v3: -0.1861445384928384

핵심 전략 해석
short_main2 v4는 v3의 과열 숏 진입 필터를 바꾸지 않는다.
V3MIX07의 핵심은 v3보다 stop을 더 넓히고, rr은 유지 또는 소폭 낮춘 상태에서 timeout과 dd brake 여유를 늘려 추세 지속 구간을 더 길게 잡는 것이다.
realized MDD는 v3보다 낮고, official_cd_value와 profit_factor는 크게 개선되었다.
MTM worstbar MDD도 v3보다 낮으며, mtm_worstbar_cd_value는 크게 개선되었다.

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
atr_stop_mult: 2.55
rr_mult: 6.30
risk = atr14 * 2.55
stop = entry + risk
target = entry - 6.30 * risk

time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
bars_held >= 3이고 mfe_r > 0이면 stop = min(stop, entry + risk * 0.00)

fail_fast_bars: 15
fail_fast_min_progress_r: 0.1
bars_held >= 15이고 mfe_r < 0.1이고 close > entry이면 해당 close에서 청산한다.

timeout_bars: 375
bars_held >= 375이면 해당 close에서 청산한다.

DD brake
mode: edge_current
dd_brake_trigger_pct: 0.088
dd_brake_freeze_steps: 3
현재 equity가 peak_equity 대비 -8.8% 이하로 처음 내려갈 때 다음 timestamp부터 신규 진입을 3 step 차단한다.

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

장점
1. v3보다 official_cd_value가 +25445.446734634068 높다.
2. v3보다 realized MDD가 -0.3389549513617247%p 낮다.
3. v3보다 profit_factor가 +0.07232376625281822 높다.
4. v3보다 mtm_worstbar_cd_value가 +23046.065508444488 높다.
5. Q4 제외 구간에서도 v3보다 우위다.
6. 진입 조건은 유지하고 청산·보유 구조만 개선했기 때문에 개발 연속성이 좋다.

단점 및 주의
1. win_rate는 7.1089%로 낮다. 구조상 낮은 승률과 큰 payoff에 의존한다.
2. realized MDD는 5.5404%지만 mtm_close MDD는 약 14.8035%, mtm_worstbar MDD는 약 14.0469%다.
3. max_conc가 364로 높다. 포지션 수 제한이 없는 공식 조건에서는 정상이나 실거래 배치에서는 자산 분할과 동시 포지션 관리가 중요하다.
4. 슬리피지 0 기준 결과다. 수수료 0.04%는 반영되어 있으나 추가 슬리피지 비용 스트레스는 별도 보조 검증으로 관리한다.
5. 전체 거래 로그를 기본 저장하지 않는다. 결과 파일은 summary 중심으로 유지한다.

판정
V3MIX07_N02_stop255_rr630_t375를 short_main2 v4 공식 기준선으로 갱신한다.
이후 short_main2 개선은 v4 기준으로 진행한다.
