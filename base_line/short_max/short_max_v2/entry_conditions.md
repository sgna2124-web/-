# short_max 기준선 진입 조건과 청산 조건

전략명: short_only_reference_1x
축: short_max
목적: 숏 전용 수익 극대화 기준선

1. 공통 실행 조건

initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
min_bars: 120
entry_on_next_bar_open: true
allow_long: false
allow_short: true

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

short_signal 조건:
close / ema20 - 1 >= short_dev
rsi14 > short_rsi_min
upper_wick >= short_wick_mult * body
score >= score_min_short
expected_tp >= min_expected_tp

short_max 파라미터:
short_dev: 0.032
short_rsi_min: 76
short_wick_mult: 1.3
score_min_short: 2.0
atr_stop_mult: 1.8975
rr_mult: 6.0
min_expected_tp: 0.003
timeout_bars: 200

4. 캔들 구조

body = abs(close - open)
upper_wick = high - max(open, close)
raw_dev = max(0, close / ema20 - 1)
raw_rsi = max(0, rsi14 - short_rsi_min)

5. score 계산

dev_score = clip(raw_dev / short_dev, 0, 2.0)
rsi_score = clip(raw_rsi / 10, 0, 2.0)
wick_ratio = upper_wick / max(abs(body), atr * 0.2, 1e-12)
wick_score = clip(log1p(wick_ratio), 0, 2.5)
score = 1.0 * dev_score + 0.8 * rsi_score + 0.7 * wick_score

score_min_short: 2.0

6. 진입가

신호 캔들 i에서 조건을 만족하면 i+1 캔들의 open으로 숏 진입한다.
close 진입으로 바꾸면 기준선이 아니다.

entry = open[i + 1]

7. 스탑과 타겟

side: short
risk = atr[i] * atr_stop_mult
stop = entry + risk
target = entry - rr_mult * risk
expected_tp = (entry - target) / entry

expected_tp가 0.003 미만이면 진입하지 않는다.

8. 청산 우선순위

숏 포지션에서 같은 캔들에 stop과 target이 동시에 닿으면 stop을 먼저 적용한다.

청산 순서:
1. high >= stop 이면 stop 청산
2. 아니면 low <= target 이면 target 청산
3. 아니면 fail_fast 조건이면 close 청산
4. 아니면 timeout 조건이면 close 청산

9. time_reduce 보호

time_reduce_bars: 10
time_reduce_to_risk_frac: 0.05

진입 후 10봉 이상 지났고 MFE가 양수이면 dynamic_stop을 entry + risk * 0.05 쪽으로 줄인다.

10. fail_fast

fail_fast_bars: 10
fail_fast_min_progress_r: 0.1

진입 후 10봉 이상 지났고 MFE가 0.1R 미만이며 close > entry이면 close로 청산한다.

11. timeout

timeout_bars: 200

진입 후 200봉 이상 지나면 close로 청산한다.

12. dd_brake

short_max 기준선에는 dd_brake가 없다.

dd_brake_trigger_pct: 없음
dd_brake_freeze_steps: 0

즉 포트폴리오 drawdown이 커져도 신규 진입을 계속 허용한다. 이 구조가 short_max의 높은 수익성과 높은 MDD를 동시에 만든다.

13. short_max 개선 시 금지 사항

신호 캔들 close 진입으로 변경 금지
fee_per_side 0.0004 누락 금지
position_fraction 0.01 복리 구조 변경 금지
기준선 진입 조건을 완전히 새 전략으로 대체 금지
수익 극대화 축인데 거래 수를 과도하게 줄이는 필터 금지

14. 개선 실험 허용 범위

short_dev 소폭 조정
short_rsi_min 소폭 조정
short_wick_mult 소폭 조정
score_min_short 소폭 조정
rr_mult 5.5~6.2 부근 조정
time_reduce_bars와 time_reduce_to_risk_frac 조정
fail_fast_bars 조정
약한 dd_brake 또는 loss-streak guard 추가 실험
max_conc 완화 필터 실험

15. short_main과의 차이

short_max는 short_main보다 조건이 느슨하다.
short_dev: 0.032 vs 0.033
short_rsi_min: 76 vs 77
score_min_short: 2.0 vs 2.2
dd_brake: 없음 vs 3% drawdown 시 5 timestamp freeze

따라서 short_max는 더 많은 거래와 더 높은 수익률을 목표로 하고, short_main은 더 낮은 MDD를 목표로 한다.
