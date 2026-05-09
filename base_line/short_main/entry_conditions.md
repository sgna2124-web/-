# short_main 기준선 진입 조건과 청산 조건

전략명: short_beh_dd_brake
축: short_main
목적: MDD 5% 미만을 유지하는 숏 메인 기준선

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

short_main 파라미터:
short_dev: 0.033
short_rsi_min: 77
short_wick_mult: 1.3
score_min_short: 2.2
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

score_min_short: 2.2

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
숏 기준으로 stop은 낮아질수록 위험이 줄어든다.

10. fail_fast

fail_fast_bars: 10
fail_fast_min_progress_r: 0.1

진입 후 10봉 이상 지났고 MFE가 0.1R 미만이며 close > entry이면 close로 청산한다.

11. timeout

timeout_bars: 200

진입 후 200봉 이상 지나면 close로 청산한다.

12. dd_brake

dd_brake_trigger_pct: 0.03
dd_brake_freeze_steps: 5

포트폴리오 평가 중 현재 drawdown이 -3% 이하로 내려가면 5 timestamp 동안 신규 진입을 멈춘다.
이 조건은 개별 트레이드 생성 단계가 아니라 포트폴리오 실행 단계에서 작동한다.

13. short_main 개선 시 금지 사항

신호 캔들 close 진입으로 변경 금지
fee_per_side 0.0004 누락 금지
position_fraction 0.01 복리 구조 변경 금지
dd_brake를 트레이드 생성 단계로 이동 금지
기준선 진입 조건을 완전히 새 전략으로 대체 금지

14. 개선 실험 허용 범위

short_dev 소폭 조정
short_rsi_min 소폭 조정
short_wick_mult 소폭 조정
score_min_short 소폭 조정
rr_mult 5.5~6.1 부근 조정
time_reduce_bars와 time_reduce_to_risk_frac 조정
fail_fast_bars 조정
dd_brake_trigger_pct와 dd_brake_freeze_steps 조정
기준선 진입 조건 위에 약한 품질 필터 추가
