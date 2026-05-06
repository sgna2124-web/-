기준선 진입 조건과 청산 조건

작성 목적
기준선 전략을 재현하거나 기준선 위에 개선안을 붙일 때, 어떤 조건이 전략의 원형인지 명확히 남긴다.

공통 실행 조건
initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
min_bars: 120
entry_on_next_bar_open: true
allow_long: false
allow_short: true

공통 지표
ema_period: 20
rsi_period: 14
atr_period: 14
ATR 계산: true range를 EWM alpha=1/period, adjust=False로 평균
RSI 계산: 상승/하락분을 EWM alpha=1/period, adjust=False로 평균
EMA 계산: pandas ewm span=period, adjust=False

숏 신호 기본식
short_signal = close / ema20 - 1 >= short_dev
그리고 rsi14 > short_rsi_min
그리고 upper_wick >= short_wick_mult * body

진입가
entry = next_bar_open
즉 신호 캔들 i가 조건을 만족하면 i+1 캔들의 open으로 진입한다.

스탑/타겟
side = short
atr_stop = entry + atr[i] * atr_stop_mult
stop_mode = atr_only 이므로 stop = atr_stop
target_mode = rr_only 이므로 target = entry - rr_mult * (stop - entry)
min_expected_tp = 0.003
진입 조건 통과에는 (entry - target) / entry >= 0.003 조건이 포함된다.

청산 우선순위
숏 포지션에서는 같은 캔들에서 stop을 먼저 검사한다.
1. high[i] >= stop 이면 stop 청산
2. 아니면 low[i] <= target 이면 target 청산
3. 아니면 fail_fast 조건 또는 timeout 조건에서 close 청산

time reduce 보호
protect_mode: time_reduce
time_reduce_bars: 10
time_reduce_to_risk_frac: 0.05
진입 후 10봉 이상 지났고 MFE가 양수이면, 숏 기준 dynamic stop을 entry + risk * 0.05 쪽으로 축소한다.

fail fast
fail_fast_bars: 10
fail_fast_min_progress_r: 0.1
숏 기준 진입 후 10봉 이상 지났고 MFE가 0.1R 미만이며 close > entry이면 close 청산한다.

timeout
timeout_bars: 200
진입 후 200봉 이상 지나면 close 청산한다.

score 계산
short raw_dev = max(0, close / ema20 - 1)
short raw_rsi = max(0, rsi14 - short_rsi_min)
dev_score = clip(raw_dev / short_dev, 0, score_dev_cap)
rsi_score = clip(raw_rsi / 10, 0, score_rsi_cap)
wick_ratio = upper_wick / max(abs(body), atr * wick_atr_floor_mult, 1e-12)
wick_score = clip(log1p(wick_ratio), 0, score_wick_cap)
score = score_dev_weight * dev_score + score_rsi_weight * rsi_score + score_wick_weight * wick_score

score 기본 파라미터
score_dev_weight: 1.0
score_rsi_weight: 0.8
score_wick_weight: 0.7
score_dev_cap: 2.0
score_rsi_cap: 2.0
score_wick_cap: 2.5
wick_atr_floor_mult: 0.2

1. short_only_reference_1x 조건
축: short_max
short_dev: 0.032
short_rsi_min: 76
short_wick_mult: 1.3
atr_stop_mult: 1.8975
rr_mult: 6.0
min_expected_tp: 0.003
timeout_bars: 200
score_min_short: 2.0
cooldown_bars_same_symbol_same_side: 0
dd_brake_trigger_pct: 없음
dd_brake_freeze_steps: 0
평가 엔진: strict_time_axis_revalidated_hardened_absolute_score 계열

2. short_beh_dd_brake 조건
축: short_main
short_dev: 0.033
short_rsi_min: 77
short_wick_mult: 1.3
atr_stop_mult: 1.8975
rr_mult: 6.0
min_expected_tp: 0.003
timeout_bars: 200
score_min_short: 2.2
cooldown_bars_same_symbol_same_side: 0
dd_brake_trigger_pct: 0.03
dd_brake_freeze_steps: 5
평가 엔진: strict_time_axis_behavioral_guards 계열

short_beh_dd_brake의 dd_brake 의미
포트폴리오 평가 중 현재 drawdown이 -3% 이하로 처음 내려가면 5 timestamp 동안 신규 진입을 멈춘다.
이 조건은 개별 트레이드 생성 조건이 아니라 포트폴리오 실행 단계의 신규 진입 제어다.

주의 사항
1. 신호 캔들 close 진입으로 바꾸면 원본 숏 기준선과 달라진다.
2. fee_per_side 0.0004를 누락하면 성과가 과대평가된다.
3. position_fraction 0.01을 고정 금액으로 바꾸면 복리 경로가 달라진다.
4. short_beh_dd_brake의 dd_brake는 trade generation 단계가 아니라 portfolio evaluation 단계에서 작동한다.
5. 기준선 위에 개선안을 붙일 때는 먼저 이 조건으로 clone이 통과되는지 확인해야 한다.
