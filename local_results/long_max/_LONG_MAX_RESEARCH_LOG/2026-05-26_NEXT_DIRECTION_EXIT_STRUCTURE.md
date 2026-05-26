# NEXT DIRECTION: EXIT STRUCTURE IMPROVEMENT

현재 상태:
- long_max 최상위는 reversal 기반.
- trend acceleration long 실패.
- trend pullback continuation long 실패.

객관적 해석:
- long 개선 병목은 entry보다 exit 구조일 가능성이 높음.
- short v12 계열도 exit 구조 개선이 성과에 큰 영향을 줌.

다음 우선 실험 후보:
1. fail_fast
- 초기 n봉 동안 기대 방향 진행 없으면 조기 종료.
- dead trade 제거 목적.

2. trailing stop
- 일정 RR 이상 도달 후 trailing.
- 고RR 구조 유지 목적.

3. time_reduce
- 시간 경과에 따라 stop tighten.
- 장시간 횡보 손실 감소 목적.

4. partial exit
- 일부 익절 후 나머지 RR 확장.
- variance 감소 목적.

5. dynamic RR
- volatility regime 따라 RR 가변.
- 과열/둔화 적응 목적.

6. DD brake for long
- 연속 손실 구간에서 진입 강도 감소.
- equity protection 목적.

현재 우선순위:
1. fail_fast
2. time_reduce
3. trailing stop
4. partial exit

배제 우선순위:
- breakout continuation long
- pure trend-follow long
- breakout chase long
