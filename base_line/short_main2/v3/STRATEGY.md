short_main2 v3 공식 기준선 기록

전략명
MIX05_A02_A03_failfast14_rr630

축
short_main2

기준선 버전
base_line/short_main2/v3

이전 기준선
base_line/short_main2/v2
SM60_C03_stop240_score270_timeout315
C03_stop240_score270_timeout315

갱신 사유
short_main2/v2의 climax_exhaustion 진입 조건은 그대로 유지한다.
MIX05는 진입 조건을 새로 만든 전략이 아니라, v2 기준선의 청산·보유·방어 파라미터를 완만하게 변형한 개발형 후보다.
단독 리테스트에서 직전 topmix 결과와 동일 수치로 재현되었고, Q4 의존도 점검에서도 Q4 단독 몰빵이 아닌 일반 구간 엣지가 확인되었다.
Q4 제외 구간에서도 v2 기준선보다 official_cd_value, realized MDD, profit_factor, mtm_worstbar_cd_value가 모두 개선되었다.

선택 기준
1. short_main2/v2 진입 조건을 유지한 개발형 후보일 것.
2. 2025 train 기준 realized MDD 10% 미만일 것.
3. official_cd_value가 v2 기준선보다 높을 것.
4. 단독 리테스트에서 topmix 기대값과 동일하게 재현될 것.
5. Q4 의존성 점검에서 Q4 단독 몰빵 전략이 아닐 것.
6. Q4 제외 구간에서도 v2 기준선보다 우위일 것.
7. 실전형 actual bar engine 규칙을 유지할 것.
8. 전체 거래 로그 같은 무거운 결과 파일을 기본 저장하지 않을 것.

공식 결과 출처
local_results/short_main/SHORT_MAIN2_V2_MIX05_SINGLE_RETEST_V1_6_ENVLOCKED/single_retest_summary_compact.csv

Q4 의존도 점검 출처
local_results/short_main/SHORT_MAIN2_V2_MIX05_Q4_DEPENDENCY_CHECK_V1_7/q4_dependency_summary_compact.csv

개발 후보 출처
local_results/short_main/SHORT_MAIN2_V2_TOPMIX_DEV_V1_5_2_INDEPENDENT_BASELINE_MEMFIX/topmix_summary_compact.csv

공식 리테스트 러너
short_main2_v2_MIX05_single_retest_v1_6_envlocked.py

Q4 의존도 점검 러너
short_main2_v2_MIX05_q4_dependency_check_v1_7_REUPLOAD.py

공식 기준 성과, no slippage, 2025 train
trades: 150791
wins: 10980
losses: 139811
win_rate_pct: 7.281601687103342
max_return_pct: 86520.8367663832
max_drawdown_pct: 5.879344393880359
official_cd_value: 81528.0994560266
profit_factor: 1.882073174356906
generated_signals: 267412
executed_entries: 150791
blocked_entries: 0
same_bar_trades: 8370
max_conc: 364
max_conc_unique_symbols: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0

실전성 MTM 참고 결과
mtm_close_max_drawdown_pct: 15.015490588915748
mtm_worstbar_max_drawdown_pct: 14.233064755345204
mtm_worstbar_cd_value: 74307.00038895881

이전 short_main2/v2 대비
v2 strategy: SM60_C03_stop240_score270_timeout315
v2 candidate: C03_stop240_score270_timeout315
v2 trades: 152030
v2 max_return_pct: 73746.55353592646
v2 max_drawdown_pct: 5.888592725709996
v2 official_cd_value: 69498.03075622236
v2 profit_factor: 1.8286053579584032
v2 mtm_worstbar_cd_value: 63347.67993125091
v2 mtm_worstbar_max_drawdown_pct: 14.23277215250176

v3 trades: 150791
v3 max_return_pct: 86520.8367663832
v3 max_drawdown_pct: 5.879344393880359
v3 official_cd_value: 81528.0994560266
v3 profit_factor: 1.882073174356906
v3 mtm_worstbar_cd_value: 74307.00038895881
v3 mtm_worstbar_max_drawdown_pct: 14.233064755345204

delta_cd_vs_v2: +12030.068699804237
delta_mdd_vs_v2: -0.009248331829637024
delta_trades_vs_v2: -1239
delta_pf_vs_v2: +0.05346781639850273
delta_mtm_worstbar_cd_vs_v2: +10959.320457707901
delta_mtm_worstbar_mdd_vs_v2: +0.0002926028434444561

핵심 전략 해석
short_main2 v3는 v2의 과열 숏 진입 필터를 바꾸지 않는다.
MIX05의 핵심은 v2보다 stop과 timeout을 조금 넓히고 rr을 6.30으로 올리며 fail_fast를 14로 늦춰, 초반 흔들림을 조금 더 허용한 뒤 payoff를 키우는 것이다.
realized MDD는 v2보다 낮고, official_cd_value와 profit_factor는 크게 개선되었다.
MTM worstbar MDD는 v2와 거의 같은 수준이며, mtm_worstbar_cd_value는 크게 개선되었다.

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
atr_stop_mult: 2.45
rr_mult: 6.30
risk = atr14 * 2.45
stop = entry + risk
target = entry - 6.30 * risk

time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
bars_held >= 3이고 mfe_r > 0이면 stop = min(stop, entry + risk * 0.00)

fail_fast_bars: 14
fail_fast_min_progress_r: 0.1
bars_held >= 14이고 mfe_r < 0.1이고 close > entry이면 해당 close에서 청산한다.

timeout_bars: 345
bars_held >= 345이면 해당 close에서 청산한다.

DD brake
mode: edge_current
dd_brake_trigger_pct: 0.085
dd_brake_freeze_steps: 3
현재 equity가 peak_equity 대비 -8.5% 이하로 처음 내려갈 때 다음 timestamp부터 신규 진입을 3 step 차단한다.

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
1. v2보다 official_cd_value가 +12030.068699804237 높다.
2. v2보다 realized MDD가 -0.009248331829637024%p 낮다.
3. v2보다 profit_factor가 +0.05346781639850273 높다.
4. Q4 제외 구간에서도 v2보다 우위다.
5. 진입 조건은 유지하고 청산·보유 구조만 개선했기 때문에 개발 연속성이 좋다.

단점 및 주의
1. win_rate는 7.2816%로 낮다. 구조상 낮은 승률과 큰 payoff에 의존한다.
2. realized MDD는 5.8793%지만 mtm_close MDD는 약 15.0155%, mtm_worstbar MDD는 약 14.2331%다.
3. max_conc가 364로 높다. 포지션 수 제한이 없는 공식 조건에서는 정상이나 실거래 배치에서는 자산 분할과 동시 포지션 관리가 중요하다.
4. 슬리피지 0 기준 결과다. 수수료 0.04%는 반영되어 있으나 추가 슬리피지 비용 스트레스는 별도 보조 검증으로 관리한다.
5. 전체 거래 로그를 기본 저장하지 않는다. 결과 파일은 summary 중심으로 유지한다.

판정
MIX05_A02_A03_failfast14_rr630을 short_main2 v3 공식 기준선으로 갱신한다.
이후 short_main2 개선은 v3 기준으로 진행한다.
