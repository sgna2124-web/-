# short_main v4 진입 조건과 청산 조건

전략명: SM16_C05_remove_no_rsi_dev035
부모 기준선: SM15_B10_rr575_tr8_f005
축: short_main
목적: RSI 직접 gate를 제거하고 dev/score를 강화해 수익성을 크게 높인 short_main v4 기준선

1. 공통 실행 조건

initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
min_bars: 120
entry_on_next_bar_open: true
allow_long: false
allow_short: true
csv_file_count: 597

2. 지표

ema_period: 20
rsi_period: 14
atr_period: 14

EMA 계산:
pandas ewm(span=20, adjust=False).mean()

RSI 계산:
close diff를 상승분과 하락분으로 나누고, 각각 EWM alpha=1/14, adjust=False로 평균한다.
RSI = 100 - 100 / (1 + avg_gain / avg_loss)

ATR 계산:
true range = max(high-low, abs(high-prev_close), abs(low-prev_close))
ATR = true range의 EWM alpha=1/14, adjust=False 평균

3. 숏 진입 기본식

v4 short_signal 조건:
close / ema20 - 1 >= short_dev
upper_wick >= short_wick_mult * body
score >= score_min_short
expected_tp >= min_expected_tp

v4에서 사용하지 않는 직접 gate:
rsi14 > short_rsi_min

중요:
RSI gate는 제거되었지만 RSI 지표 자체는 제거하지 않는다.
score 계산에서 rsi_score를 만들 때 short_rsi_min 77.0을 그대로 사용한다.
따라서 RSI가 높으면 score가 더 좋아지지만, RSI가 77을 넘지 않아도 dev/wick/score 조건이 충분하면 진입할 수 있다.

4. v4 핵심 파라미터

short_dev: 0.035
short_rsi_min: 77.0
use_rsi_gate: false
short_wick_mult: 1.3
score_min_short: 2.35
atr_stop_mult: 1.8975
rr_mult: 5.75
min_expected_tp: 0.003
timeout_bars: 200
fail_fast_bars: 10
fail_fast_min_progress_r: 0.1
time_reduce_bars: 8
time_reduce_to_risk_frac: 0.05
dd_brake_trigger_pct: 0.03
dd_brake_freeze_steps: 5

5. 캔들 구조

body = abs(close - open)
upper_wick = high - max(open, close)
raw_dev = max(0, close / ema20 - 1)
raw_rsi = max(0, rsi14 - 77.0)

6. score 계산

dev_score = clip(raw_dev / 0.035, 0, 2.0)
rsi_score = clip(raw_rsi / 10, 0, 2.0)
wick_ratio = upper_wick / max(abs(body), atr * 0.2, 1e-12)
wick_score = clip(log1p(wick_ratio), 0, 2.5)
score = 1.0 * dev_score + 0.8 * rsi_score + 0.7 * wick_score

score_min_short: 2.35

7. v3 대비 진입 조건 변경

v3:
close / ema20 - 1 >= 0.033
rsi14 > 77
upper_wick >= 1.3 * body
score >= 2.2

v4:
close / ema20 - 1 >= 0.035
rsi14 직접 gate 없음
upper_wick >= 1.3 * body
score >= 2.35

해석:
v4는 RSI 직접 조건을 제거해 진입 기회를 넓힌다.
대신 short_dev를 0.035로 강화하고 score_min_short를 2.35로 올려 과도한 저품질 진입을 막는다.

8. 진입가

신호 캔들 i에서 조건을 만족하면 i+1 캔들의 open으로 숏 진입한다.
close 진입으로 바꾸면 기준선이 아니다.

entry = open[i + 1]

9. 스탑과 타겟

side: short
risk = atr[i] * atr_stop_mult
stop = entry + risk
target = entry - rr_mult * risk
expected_tp = (entry - target) / entry

v4 값:
atr_stop_mult: 1.8975
rr_mult: 5.75

expected_tp가 0.003 미만이면 진입하지 않는다.

10. 청산 우선순위

숏 포지션에서 같은 캔들에 stop과 target이 동시에 닿으면 stop을 먼저 적용한다.

청산 순서:
1. high >= stop 이면 stop 청산
2. 아니면 low <= target 이면 target 청산
3. 아니면 fail_fast 조건이면 close 청산
4. 아니면 timeout 조건이면 close 청산

11. time_reduce 보호

time_reduce_bars: 8
time_reduce_to_risk_frac: 0.05

진입 후 8봉 이상 지났고 MFE가 양수이면 dynamic_stop을 entry + risk * 0.05 쪽으로 줄인다.
숏 기준으로 stop은 낮아질수록 위험이 줄어든다.

12. fail_fast

fail_fast_bars: 10
fail_fast_min_progress_r: 0.1

진입 후 10봉 이상 지났고 MFE가 0.1R 미만이며 close > entry이면 close로 청산한다.

13. timeout

timeout_bars: 200

진입 후 200봉 이상 지나면 close로 청산한다.

14. dd_brake

dd_brake_trigger_pct: 0.03
dd_brake_freeze_steps: 5

포트폴리오 평가 중 현재 drawdown이 -3% 이하로 내려가면 5 timestamp 동안 신규 진입을 멈춘다.
이 조건은 개별 트레이드 생성 단계가 아니라 포트폴리오 실행 단계에서 작동한다.

15. 승격 기준 충족 여부

MDD 5% 미만: 충족. 4.6783483625391975
trades 20000 이상: 충족. 31798
active_leftover 0: 충족
errors 0: 충족
v3 CD 초과: 충족. 878.8531649564361 > 414.18780792249464
position_fraction 0.01: 충족
fee_per_side 0.0004: 충족
next bar open 진입: 충족

16. 향후 개선 시 금지 사항

v4를 부모로 하는 다음 개발에서는 아래를 지켜야 한다.

1. 외부 경로, 외부 json, 외부 runner 참조 금지
2. fee_per_side 0.0004 유지
3. position_fraction 0.01 유지
4. next bar open 진입 유지
5. dd_brake를 개별 트레이드 생성 단계로 이동 금지
6. RSI 직접 gate 제거 상태를 기준선으로 인식할 것
7. score 내부 RSI 기여와 RSI 직접 gate 제거를 혼동하지 말 것
8. v4 기준선 진입 조건을 완전히 다른 전략으로 대체하지 말 것

17. 다음 개선 허용 범위

short_dev: 0.0345~0.0360
score_min_short: 2.30~2.45
short_wick_mult: 1.2~1.4
rr_mult: 5.65~5.85
time_reduce_bars: 7~9
time_reduce_to_risk_frac: 0.04~0.06
fail_fast_bars: 8~12
dd_brake_trigger_pct: 0.025~0.035
dd_brake_freeze_steps: 3~7
