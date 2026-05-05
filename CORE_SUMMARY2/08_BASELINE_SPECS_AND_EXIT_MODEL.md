08_BASELINE_SPECS_AND_EXIT_MODEL

이 문서는 기준선 4개 전략의 live clone 감사에 필요한 최소 실행 모델을 보존한다.
기존 CORE_SUMMARY를 완전히 대체할 경우, 이 문서 또는 별도 REFERENCE_CODE 폴더가 없으면 새 대화창은 기준선 조건을 정확히 복원할 수 없다.

중요
이 문서는 기준선 원형 재현용이다.
기준선 live clone에는 TP03을 추가하지 않는다.
기준선 live clone에는 수수료 0.04%, POS_FRAC 0.01, 전체 데이터, 캔들 제한 없음만 적용한다.
개선안에는 TP03을 기본 조건으로 추가한다.

현재 확인된 기준선 reference
long_main
name: 6V2_L01_doubleflush_core
side: long
reference trades: 592
reference max_return_pct: 23.919060
reference max_drawdown_pct: 1.751183
reference official_cd_value: 121.749029

long_max
name: 8V4_V51_V002_core_rare22_c1
side: long
reference trades: 2276
reference max_return_pct: 44.266371
reference max_drawdown_pct: 6.758722
reference official_cd_value: 134.515867

short_main
name: short_beh_dd_brake
side: short
reference trades: 28017
reference max_return_pct: 311.812150
reference max_drawdown_pct: 4.758886
reference official_cd_value: 392.214469

short_max
name: short_only_reference_1x
side: short
reference trades: 36505
reference max_return_pct: 394.614496
reference max_drawdown_pct: 7.779240
reference official_cd_value: 456.137449

기준선 Spec 핵심값

long_main: 6V2_L01_doubleflush_core
side: long
stop_atr: 1.04
rr: 1.85
hold: 18
cooldown: 10
atrp_min: 0.0030
atrp_max: 0.070
range20_max: 0.180
vol_min: 1.35
body_min: 0.34
ret3_floor: -0.036
ret5_floor: -0.052
ret10_floor: -0.070
ret20_floor: -0.110
close_pos_min: 0.72
wick_min: 0.15
upper_wick_max: 0.82
reclaim_buffer: 0.0000
low_buffer: 0.0000
require_green: True
require_reclaim: True
require_rare22: False
require_lowanchor: False
require_strict: False
require_shocklow: True
ema_guard: soft
be_r: 999.0
trail_r: 999.0
trail_atr: 1.80
fail_bars: 6
fail_pnl: -0.35
post_loss_after: 999
post_loss_bars: 0
sym_dd_pct: 999.0
sym_dd_bars: 0
shock_lb: 0
shock_ret5: -0.070
shock_range: 0.100
shock_close_pos: 0.22

long_max: 8V4_V51_V002_core_rare22_c1
side: long
stop_atr: 1.10
rr: 2.05
hold: 22
cooldown: 6
atrp_min: 0.0035
atrp_max: 0.095
range20_max: 0.240
vol_min: 1.35
body_min: 0.32
ret3_floor: -0.038
ret5_floor: -0.055
ret10_floor: -0.075
ret20_floor: -0.115
close_pos_min: 0.70
wick_min: 0.00
upper_wick_max: 0.92
reclaim_buffer: 0.0000
low_buffer: 0.0000
require_green: True
require_reclaim: True
require_rare22: True
require_lowanchor: False
require_strict: False
require_shocklow: False
ema_guard: none
be_r: 999.0
trail_r: 999.0
trail_atr: 1.80
fail_bars: 999
fail_pnl: -999.0
post_loss_after: 999
post_loss_bars: 0
sym_dd_pct: 999.0
sym_dd_bars: 0
shock_lb: 0
shock_ret5: -0.095
shock_range: 0.125
shock_close_pos: 0.18

short_main: short_beh_dd_brake
side: short
stop_atr: 1.8975
rr: 6.00
hold: 200
cooldown: 0
atrp_min: 0.0018
atrp_max: 0.110
range20_max: 0.500
vol_min: 0.0
body_min: 0.0
dev_short: 0.033
rsi_short_min: 77.0
close_pos_short_max: 1.00
wick_short_min: 1.30
ret3_ceil: 0.250
ret5_ceil: 0.360
ret10_ceil: 0.520
ret20_ceil: 0.760
require_upper_sweep: False
require_ema_reject: False
be_r: 999.0
trail_r: 999.0
trail_atr: 2.10
fail_bars: 10
fail_pnl: -999.0
post_loss_after: 999
post_loss_bars: 0
sym_dd_pct: 999.0
sym_dd_bars: 0
shock_lb: 0
shock_ret5: 0.115
shock_range: 0.165
shock_close_pos: 0.92
dd_brake_trigger_pct: 0.03
dd_brake_freeze_steps: 5

short_max: short_only_reference_1x
side: short
stop_atr: 1.8975
rr: 6.00
hold: 200
cooldown: 0
atrp_min: 0.0018
atrp_max: 0.110
range20_max: 0.500
vol_min: 0.0
body_min: 0.0
dev_short: 0.032
rsi_short_min: 76.0
close_pos_short_max: 1.00
wick_short_min: 1.30
ret3_ceil: 0.250
ret5_ceil: 0.360
ret10_ceil: 0.520
ret20_ceil: 0.760
require_upper_sweep: False
require_ema_reject: False
be_r: 999.0
trail_r: 999.0
trail_atr: 2.40
fail_bars: 10
fail_pnl: -999.0
post_loss_after: 999
post_loss_bars: 0
sym_dd_pct: 999.0
sym_dd_bars: 0
shock_lb: 0
shock_ret5: 0.140
shock_range: 0.190
shock_close_pos: 0.95

공통 진입 필터
atrp_min <= atrp <= atrp_max
range20p <= range20_max
volr >= vol_min
body_atr >= body_min

주의
기준선 clone에서는 TP03 공통 필터를 추가하지 않는다.
개선안에서는 expected_tp = stop_atr * rr * atrp >= 0.003 조건을 추가한다.

롱 진입 모델
공통 필터 통과
require_green이면 close > open
ret3 >= ret3_floor
ret5 >= ret5_floor
ret10 >= ret10_floor
ret20 >= ret20_floor
close_pos >= close_pos_min
lw_body >= wick_min
uw_body <= upper_wick_max
require_reclaim이면 close >= ll20 * (1 + reclaim_buffer)
require_rare22이면 low <= ll22 * (1 + max(low_buffer, 0.0005))
require_lowanchor이면 low <= ll50 * 1.012
require_strict이면 close_pos >= max(close_pos_min, 0.74) and body_atr >= max(body_min, 0.34)
require_shocklow이면 low <= ll20 * 1.006 또는 ret5 <= -0.018
ema_guard soft이면 close >= ema20 * 0.965 또는 close >= ema50 * 0.940
ema_guard hard이면 close >= ema20 * 0.985
shock_lb > 0이고 shock 조건이면 진입 금지

숏 진입 모델
공통 필터 통과
dev = high / ema50 - 1.0
dev >= dev_short
rsi >= rsi_short_min
close_pos <= close_pos_short_max
uw_body >= wick_short_min
ret3 <= ret3_ceil
ret5 <= ret5_ceil
ret10 <= ret10_ceil
ret20 <= ret20_ceil
require_upper_sweep이면 high >= hh20 * 0.997
require_ema_reject이면 close <= ema20 * 1.020
shock_lb > 0이고 shock 조건이면 진입 금지

손익절 설정 모델
진입 가격은 신호 캔들의 close다.
risk = stop_atr * ATR
long stop = entry - risk
long tp = entry + rr * risk
short stop = entry + risk
short tp = entry - rr * risk
max_exit_bar = entry_index + hold

즉, 이 엔진은 진입 직후 손절가와 익절가를 동시에 산출하는 bracket 성격이다.
다만 실제 거래소 주문을 동시에 넣는다는 뜻이 아니라, 백테스트 엔진 안에서 다음 캔들부터 high/low로 stop 또는 tp 도달 여부를 검사한다.

청산 우선순위
각 다음 캔들에서 다음 순서로 검사한다.

롱
1. runup_r 계산
2. be_r 조건 충족 시 dyn_stop을 entry 이상으로 올림
3. trail_r 조건 충족 시 dyn_stop을 high - trail_atr * ATR로 올림
4. low <= dyn_stop이면 dyn_stop에서 청산
5. high >= tp이면 tp에서 청산
6. fail_bars 조건이 있고 fail_pnl 이하이면 close에서 청산
7. 아무것도 안 맞으면 hold 만료 시 close에서 청산

숏
1. runup_r 계산
2. be_r 조건 충족 시 dyn_stop을 entry 이하로 내림
3. trail_r 조건 충족 시 dyn_stop을 low + trail_atr * ATR로 내림
4. high >= dyn_stop이면 dyn_stop에서 청산
5. low <= tp이면 tp에서 청산
6. fail_bars 조건이 있고 fail_pnl 이하이면 close에서 청산
7. 아무것도 안 맞으면 hold 만료 시 close에서 청산

비용 적용
공식 수수료는 0.04%다.
기존 코드의 COST_PCT = 0.10은 감사 대상이며 공식값이 아니다.
다음 live clone에서는 공식 수수료를 코드상 명확한 변수명으로 바꿔야 한다.
권장:
FEE_PCT_PER_SIDE = 0.04
ROUND_TRIP_FEE_PCT = 0.08
pnl 계산에서 비용을 어떻게 차감하는지 로그에 표시한다.
