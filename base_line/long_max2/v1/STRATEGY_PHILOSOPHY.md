# LONG_MAX2 V1 STRATEGY PHILOSOPHY

## 전략 정체성
LONG_MAX2 V1은 기존 long_max 철학에서 방향을 전환하여 만들어진 두 번째 롱 기준선이다.

핵심은:
- reversal entry 유지
- exit 구조 공격적 개선
- 빠른 생존 판정
- 살아남는 반등을 강하게 보호

이다.

## 이전 철학과 차이
기존 long_max 계열:
- 반등을 오래 보유
- stop 보호 시점이 느림
- 살아남는지 판정이 늦음

LONG_MAX2 V1:
- 초반 2 bars 안에 생존 여부 판정
- 살아남으면 +0.15R 보호
- 죽는 트레이드는 매우 빠르게 제거
- 살아남는 반등은 공격적으로 유지

## 핵심 구조
entry:
- child::orig_V09_extreme_vol18::tp03
- reversal 기반 진입 유지

exit:
- time_reduce_bars = 2
- time_reduce_to_risk_frac = 0.15

즉:
- 진입 후 2 bars 경과 시
- stop을 +0.15R 수준으로 상향 보호

## 실험 과정
V14:
- 3 bars → +0.10R
- CD 약 890.97

V28:
- 2 bars → +0.10R
- CD 약 1004.40

V29/V30:
- 2 bars → +0.15R
- CD 약 1120.94

## 현재 해석
롱 반등은:
- 살아남는 놈은 생각보다 훨씬 강하게 움직인다.
- 따라서 보호를 너무 보수적으로 하면 큰 수익을 놓친다.
- 반대로 보호가 너무 느리면 죽는 트레이드를 오래 끌게 된다.

현재 기준 최적 균형:
- 빠른 보호 시점
- 약간 공격적인 positive stop protection

## 현재 공식 값
- final_return_pct: 1027.8680633622162
- max_drawdown_pct: 0.646528687970449
- official_cd_value: 1120.9401886015664
