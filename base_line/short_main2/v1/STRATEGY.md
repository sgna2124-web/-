short_main2 v1 공식 기준선 기록

전략명
SM52_B04_stop230_score270_single_retest

원 탐색 전략명
SM50_B04_stop230_score270

축
short_main2

이전 기준선
base_line/short_main/v15
SM42_mdd10_aggr_v01_single_retest

갱신 사유
short_main v15 기준선의 climax_exhaustion 신규축을 기준으로 주변값을 개발했다.
그중 B04_stop230_score270 후보가 전체 1위로 나왔다.
B04는 v15 대비 climax_score_min을 2.8에서 2.7로 완화하고, atr_stop_mult를 2.20에서 2.30으로 확대하고, timeout_bars를 270에서 285로 늘린 변형이다.
rr_mult는 6.20으로 유지했다.
이 후보는 전체 탐색에서 official_cd_value 50591.2024를 기록했고, Q4 의존성 점검에서 2025년 4분기 몰빵 전략이 아님을 확인했다.
이후 단독 리테스트 v5.2에서 원 탐색 결과와 사실상 동일하게 재현되었다.
따라서 short_main2/v1 공식 기준선으로 승격한다.

선택 기준
MDD 10% 미만 후보 중 official_cd_value 최대.
단독 리테스트 재현 통과.
2025년 4분기 특이점 의존성 점검 통과.
수수료, 레버리지, 자산 분할 환경 잠금 통과.

공식 결과 출처
local_results/short_main/SHORT_MAIN_V15_B04_SINGLE_RETEST_V5_2_ENVLOCKED/summary_compact.csv

Q4 점검 결과 출처
local_results/short_main/SHORT_MAIN_V15_B04_Q4_REGIME_CHECK_V5_1/period_summary_compact.csv

공식 리테스트 러너
short_main_v15_B04_single_retest_v5_2_envlocked.py

공식 기준 성과
trades: 154015
wins: 11824
losses: 142191
win_rate_pct: 7.6771743012044285
max_return_pct: 53676.46264218497
max_drawdown_pct: 5.923149464550481
official_cd_value: 50591.202383140204
profit_factor: 1.7648350795085153
generated_signals: 267412
executed_entries: 154015
blocked_entries: 0
same_bar_trades: 9995
max_conc: 364
active_leftover: 0
pending_leftover: 0
load_errors: 0

이전 short_main v15 대비
v15 strategy: SM42_mdd10_aggr_v01_single_retest
v15 official_cd_value: 23902.932157469306
short_main2 v1 official_cd_value: 50591.202383140204
delta_cd_vs_v15: +26688.270225670898
v15 max_return_pct: 25200.7456885644
short_main2 v1 max_return_pct: 53676.46264218497
delta_max_return_vs_v15: +28475.71695362057
v15 max_drawdown_pct: 5.524791831439535
short_main2 v1 max_drawdown_pct: 5.923149464550481
delta_mdd_vs_v15: +0.398357633110946
v15 profit_factor: 1.7005605337643628
short_main2 v1 profit_factor: 1.7648350795085153
delta_pf_vs_v15: +0.0642745457441525
v15 trades: 140827
short_main2 v1 trades: 154015
delta_trades_vs_v15: +13188

원 탐색 결과 대비 단독 리테스트 차이
delta_vs_source_official_cd_value: -0.000016859798
delta_vs_source_max_return_pct: +0.000042184969
delta_vs_source_max_drawdown_pct: +0.000049464550
delta_vs_source_trades: 0
delta_vs_source_profit_factor: +0.000035079508
해석: 원 탐색 결과가 소수 4자리로 기록되어 생긴 반올림 차이다. 거래 수는 완전 일치하고 성과값도 사실상 동일 재현이다.

gate 결과
gate_retest_match_strict: True
gate_retest_match_loose: True
gate_mdd10_search_pass: True
gate_short_main_improve_vs_v15: True
gate_v16_candidate: True
short_main2_v1_candidate: True

핵심 전략 해석
short_main2 v1은 v15의 climax_exhaustion 계열을 유지한다.
다만 v15보다 진입 score를 약간 완화하고, 손절폭과 보유시간을 넓혀 더 많은 과열 숏 기회를 받아들이는 구조다.
기존 v15 대비 거래 수, max_return_pct, profit_factor가 동시에 증가했다.
MDD는 5.52%에서 5.92%로 조금 증가했지만 여전히 10% 미만이다.
따라서 이 기준선은 고 CD 확장형 short_main2 기준선이다.

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
atr_stop_mult: 2.30
rr_mult: 6.20
risk = atr14 * 2.30
stop = entry + risk
target = entry - 6.20 * risk

time_reduce_bars: 3
time_reduce_to_risk_frac: 0.00
bars_held >= 3이고 mfe_r > 0이면 stop = min(stop, entry + risk * 0.00)

fail_fast_bars: 12
fail_fast_min_progress_r: 0.1
bars_held >= 12이고 mfe_r < 0.1이고 close > entry이면 해당 close에서 청산한다.

timeout_bars: 285
bars_held >= 285이면 해당 close에서 청산한다.

DD brake
mode: edge_current
dd_brake_trigger_pct: 0.075
dd_brake_freeze_steps: 3
현재 equity가 peak_equity 대비 -7.5% 이하로 처음 내려갈 때 다음 timestamp부터 신규 진입을 3 step 차단한다.

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
FULL_TRAIN_TO_2025_END official_cd_value: 50591.2024
EXCL_2025_Q4_ALL_BEFORE_2025_10_01 official_cd_value: 12736.7326
2025_Q4_ONLY official_cd_value: 378.1772
자동 판정: GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14
판정: 2025년 Q4를 제거해도 기존 short_main v15 이전 기준선보다 높고, Q4 단독 CD는 전체 성과를 설명할 정도로 크지 않다. 따라서 Q4 몰빵 전략이 아니다.

장점
1. short_main v15 대비 official_cd_value가 약 2.12배로 증가했다.
2. profit_factor가 v15보다 상승했다.
3. 거래 수가 늘어 복리 확장력이 좋아졌다.
4. Q4를 제외해도 official_cd_value가 12736.7326으로 강하다.
5. 단독 리테스트에서 탐색 결과가 재현됐다.
6. active_leftover와 pending_leftover가 0이다.

단점 및 주의점
1. MDD가 v15보다 0.398%p 증가했다.
2. 승률은 7.68% 수준으로 낮다.
3. 거래 수가 많아 실거래에서는 체결 품질, 슬리피지, 동시 포지션 관리가 중요하다.
4. max_conc가 364로 높다.
5. 2026 holdout 검증은 다른 대화창에서 별도 수행한다.

재현 주의사항
외부 json config를 참조하지 않는다.
외부 runner를 import하지 않는다.
2026 데이터는 지표 계산 전 제외해야 한다.
수수료는 편도 0.04%다.
레버리지는 1.0이다.
자산 분할 진입은 1%다.
백테스트 결과 비교는 탐색 결과가 아니라 환경 잠금 단독 리테스트 v5.2 결과를 공식값으로 사용한다.
short_main2 v1은 MDD 10% 미만 고 CD 기준을 만족하여 승격된 기준선이다.
