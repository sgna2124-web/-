# short_main v4 재현 노트

전략명: SM16_C05_remove_no_rsi_dev035
부모 기준선: SM15_B10_rr575_tr8_f005
검증 실행 파일: short_main_v3_entry_dev_v1_6.py
결과 폴더: local_results/short_main/SHORT_MAIN_V3_ENTRY_DEV_V1_6
결과 파일: short_main_v3_entry_dev_v1_6_summary.csv
manifest 파일: short_main_v3_entry_dev_v1_6_manifest.json

1. 반드시 지켜야 할 실행 환경

initial_asset: 100.0
position_fraction: 0.01
fee_per_side: 0.0004
round_trip_fee: 0.0008
csv_file_count: 597
min_csv_files: 100
allow_small_data: false
ignore_non_ohlcv_csv: false
entry 방식: signal candle i -> next bar open i+1

2. 데이터 폴더

v1.6 실행 당시 data_dir:
C:\\Users\\user\\Desktop\\LCD\\파이썬\\코인\\Data\\time

다만 기준선 코드에서는 외부 경로를 고정 참조하지 않는다.
백테스트 파일을 만들 때는 스크립트 위치 기준 ../Data/time 또는 실행 인자로 받은 data_dir를 사용한다.
GitHub 저장소 경로, 외부 json, 외부 runner는 참조하지 않는다.

3. v4 기준선 행

summary.csv에서 아래 전략 행을 기준으로 한다.

strategy: SM16_C05_remove_no_rsi_dev035
parent: SM15_B10_rr575_tr8_f005
family: entry_remove_soften
description: RSI gate 제거 + dev/score 강화

성과:
trades: 31798
wins: 4638
losses: 27160
win_rate_pct: 14.585823007736334
final_return_pct: 821.5165864710646
max_return_pct: 821.9869251730971
max_drawdown_pct: 4.6783483625391975
official_cd_value: 878.8531649564361
pf: 1.5778442611030818
max_conc: 275
same_bar_trades: 4559
active_leftover: 0
raw_trades_generated: 61818
errors: 0

4. v4 기준선 파라미터

short_dev: 0.035
short_rsi_min: 77.0
use_rsi_gate: false
short_wick_mult: 1.3
score_min_short: 2.35
dd_brake_trigger_pct: 0.03
dd_brake_freeze_steps: 5
atr_stop_mult: 1.8975
rr_mult: 5.75
min_expected_tp: 0.003
timeout_bars: 200
fail_fast_bars: 10
fail_fast_min_progress_r: 0.1
time_reduce_bars: 8
time_reduce_to_risk_frac: 0.05

5. 진입 조건 재현 체크리스트

다음 조건을 모두 만족해야 한다.

1. close / ema20 - 1 >= 0.035
2. upper_wick >= 1.3 * body
3. score >= 2.35
4. expected_tp >= 0.003
5. i+1 open으로 진입

다음 조건은 직접 gate로 사용하지 않는다.

rsi14 > 77

6. score 재현 체크리스트

score 계산에는 RSI가 여전히 들어간다.

raw_dev = max(0, close / ema20 - 1)
raw_rsi = max(0, rsi14 - 77.0)
dev_score = clip(raw_dev / 0.035, 0, 2.0)
rsi_score = clip(raw_rsi / 10, 0, 2.0)
wick_ratio = upper_wick / max(abs(body), atr * 0.2, 1e-12)
wick_score = clip(log1p(wick_ratio), 0, 2.5)
score = 1.0 * dev_score + 0.8 * rsi_score + 0.7 * wick_score

7. 청산 재현 체크리스트

숏 포지션 기준:
risk = atr * 1.8975
stop = entry + risk
target = entry - 5.75 * risk

같은 캔들에서 stop과 target이 동시에 닿으면 stop 우선.
청산 순서:
1. stop
2. target
3. fail_fast
4. timeout

8. time_reduce 재현 체크리스트

bars_held >= 8 이고 MFE가 양수이면 stop을 entry + risk * 0.05 쪽으로 줄인다.
숏 기준으로 stop은 낮아질수록 위험이 줄어든다.

9. fail_fast 재현 체크리스트

bars_held >= 10
MFE < 0.1R
close > entry

위 조건을 만족하면 close로 청산한다.

10. dd_brake 재현 체크리스트

포트폴리오 평가 단계에서 현재 drawdown이 -3% 이하이면 5 timestamp 동안 신규 진입을 멈춘다.
개별 트레이드 생성 단계에서 후보 자체를 제거하면 안 된다.

11. 기준선 승격 판단 기준

v4는 다음 기준을 모두 만족해 승격한다.

MDD 5% 미만
trades 20000 이상
active_leftover 0
errors 0
v3 official_cd_value 초과
수수료 0.04% 적용
자산 1% 분할 진입 적용
next bar open 진입 적용

12. 다음 개발 시 주의

다음 v5 개발은 반드시 이 v4 조건을 부모로 삼는다.
이전 v3 조건인 rsi14 > 77 직접 gate를 다시 기본값으로 넣으면 안 된다.
RSI는 score 내부 요소로만 기본 유지한다.
진입 조건을 새 전략으로 완전히 바꾸는 것이 아니라, v4 조건에서 추가, 제거, 변형을 진행한다.
