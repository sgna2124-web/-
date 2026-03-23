# 현재 디버그 구현 스냅샷

이 문서는 현재 재현 가능한 파이썬 디버그 구현의 핵심만 보관한다.
전체 실행 파일은 대화 중 사용자에게 직접 전달된 버전을 기준으로 삼고, 여기서는 다음 작업자가 핵심 로직을 빠르게 확인하도록 요약만 남긴다.

## 목적
- 5분봉만으로 합성 1시간봉 필터를 만든다.
- 직전 완료 1시간봉만 사용한다.
- 단일 종목 디버그에서 조건별 통과 개수를 출력한다.
- 현재 구현이 실제로 어떤 전략을 실행하는지 텍스트로 고정한다.

## 핵심 함수
1. calc_rsi(series, 14)
- high 기준 RSI 계산

2. calc_adx(df, 14)
- up_move / down_move
- plus_dm / minus_dm
- TR -> ATR
- plus / minus -> DX -> ADX

3. calc_heikin_ashi(df)
- ha_close = (open + high + low + close) / 4
- ha_open은 재귀적으로 계산

4. build_closed_1h_filter_from_5m(df)
- datetime.floor('1h')로 hour_bucket 생성
- 5분봉 12개를 묶어 1시간 OHLCV 합성
- 1시간 EMA20, EMA50, EMA20 slope 계산
- mid_filter_1h_raw = EMA20 > EMA50 and EMA20_slope < EMA20_slope_prev
- mid_filter_1h_closed = mid_filter_1h_raw.shift(1, fill_value=False)
- 원본 5분봉의 hour_bucket에 map

## 현재 구현 전략 정의
대상: 숏 전용

### 5분봉 조건
- short_cross = rsi_high.shift(1) > 70 and rsi_high <= 70
- wick_cond = upper_wick > body * 1.5 and upper_wick > lower_wick
- close_cond = close_pos < 0.35
- recent_uptrend = close > close.shift(8)
- trend_exhausted = adx < 25 and adx < adx.shift(3) and ema_spread_pct < 0.025
- high_update_ok = high <= high.shift(1).rolling(8).max() or rolling value is na
- mid_filter_1h = 직전 완료 1시간봉 기준 중간 필터

### setup
short_setup = short_cross and wick_cond and close_cond and recent_uptrend and trend_exhausted and high_update_ok and mid_filter_1h

### HA 컨펌
- ha_bear = ha_close < ha_open
- ha_strong_bear = ha_bear and ha_bear.shift(1, fill_value=False) and ha_close < ha_close.shift(1)
- setup 발생 후 pending 저장
- 10봉 이내 ha_strong_bear가 나오면 진입

### 손익절
- signal high를 기본 손절 후보로 저장
- move_ratio에 따라 RR 1.0 / 1.5 / 2.0
- move_ratio >= 0.5면 하이브리드 SL 적용

## 단일 종목 검증 결과
### KAIA/USDT
- short_setup 1
- 실제 진입 1
- 익절 1

### CGPT/USDT
- short_setup 0
- 실제 진입 0

## 전체 종목 재실행 결과
- 총 거래 수 31
- 승 11 / 패 20
- 승률 35.48%
- PF 0.75
- 최대 동시 포지션 수 1

## 중요 해석
- 현재 구현은 재현 가능하지만 아직 수익 전략이 아니다.
- 과거 고수익 수치와 현재 구현은 일치하지 않는다.
- 다음 작업자는 이 구현을 기준으로 사용자 대용량 백테스트 결과와 먼저 대조해야 한다.