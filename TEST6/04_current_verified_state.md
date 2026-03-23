# 현재 신뢰 가능한 상태

## 기준
현재 기준은 지금 디버그해서 맞춘 파이썬 구현이다.
이 기준에 맞지 않는 과거 수치는 기준점으로 사용하지 않는다.

## 단일 종목 검증

### KAIA/USDT
- 전체봉수: 114,424
- 체크 봉수: 114,135
- short_cross: 1,680
- wick_cond: 16,505
- close_cond: 43,739
- recent_uptrend: 53,320
- trend_exhausted: 40,699
- high_update_ok: 97,463
- mid_filter_1h: 25,752
- short_setup: 1
- ha_strong_bear: 31,974
- 실제 진입: 1
- 결과: 익절 1회

### CGPT/USDT
- 전체봉수: 109,749
- 체크 봉수: 109,460
- short_cross: 1,620
- wick_cond: 18,019
- close_cond: 40,764
- recent_uptrend: 52,994
- trend_exhausted: 39,126
- high_update_ok: 90,529
- mid_filter_1h: 25,975
- short_setup: 0
- ha_strong_bear: 32,840
- 실제 진입: 0

## 전체 종목 재검증
대상:
- CGPT_5m 242개
- UXLINK_5m 61개
- 총 303개 파일

현재 구현 결과:
- 총 거래 수: 31
- 승: 11
- 패: 20
- 승률: 35.48%
- 평균 R: 음수
- PF: 0.75
- 거래 발생 종목 수: 30
- 최대 동시 보유 포지션 수: 1

## 현재 상태 해석
- 현재 재현 가능한 구현 기준으로는 아직 수익 전략이 아니다.
- 과거 최적 전략 숫자와 현재 구현이 일치하지 않으므로,
  지금 단계는 전략 개선이 아니라 전략 복원/재탐색 단계다.