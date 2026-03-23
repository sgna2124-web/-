# 파이썬 구현 메모

## 구현해야 하는 핵심 전략 로직
대상: 숏 전용

### 5분봉 조건
1. RSI(high, 14)가 직전 봉에서 70 초과, 현재 봉에서 70 이하
2. upper_wick > body * 1.5
3. upper_wick > lower_wick
4. close_pos < 0.35
5. recent_uptrend = close > close.shift(8)
6. trend_exhausted = ADX < 25 and ADX < ADX.shift(3) and ema_spread_pct < 0.025
7. high_update_ok = 현재 high <= 직전 8봉 최고 high

### 1시간 필터
- 5분봉 12개로 1시간봉 합성
- 현재 5분봉에서는 직전 완료 1시간봉만 사용
- 1시간 EMA20 > EMA50
- EMA20 slope 현재값 < 직전 slope

### HA 컨펌
- setup 발생 후 pending 저장
- 10봉 이내에 HA strong bear 나오면 진입
- HA strong bear = 현재 HA bearish AND 직전 HA bearish AND 현재 HA close < 직전 HA close

## 구현 시 반드시 지킬 것
1. datetime 오름차순 정렬
2. 중복 datetime 제거
3. 1시간 필터는 merge_asof가 아니라 hour_bucket map 방식 권장
4. setup과 entry를 분리
5. print, plt, 엑셀 저장 구조는 건드리지 말 것
6. DEBUG_MODE에서 조건별 통과 개수/샘플 출력

## 실제로 고쳤던 대표 오류
1. MYX/USDT만 고정해서 테스트하던 줄이 있었음
2. 시간 정렬 누락
3. 1시간 필터 결합 방식 불안정
4. high_update_ok를 너무 강하게 해석
5. fillna(False) FutureWarning 처리 필요

## high_update_ok 해석 주의
잘못된 해석:
- 최근 8봉 전체에 breakout 흔적이 있으면 금지
올바른 해석:
- 현재 봉이 직전 8봉 최고 high를 넘고 있으면 금지
즉, 현재 신호봉이 아직 돌파 진행 중인 자리인지 여부를 걸러야 한다.

## 중요한 현실
현재 구현은 구조적으로는 동작하지만,
이 구현 자체가 과거의 좋은 결과를 재현하지 못한다.
즉 지금은 구현 안정화는 되었으나, 전략이 검증된 것은 아니다.