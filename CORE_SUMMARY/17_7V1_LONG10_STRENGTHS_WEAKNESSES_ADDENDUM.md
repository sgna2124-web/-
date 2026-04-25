7V1_LONG10_REVIEWED 장단점 추가 기록

이 문서는 7V1_LONG10_REVIEWED 결과를 바탕으로, 신규 long reversal family의 구조적 장단점을 다음 전략 생성 규칙으로 남기기 위한 addendum이다.

1. batch 요약
- 최고 raw upside: 7V1_L10_shock_reversal_balance | final_return_pct 51.0204 | max_return_pct 56.5963 | max_drawdown_pct 15.1033 | cd_value 128.2113 | trades 33481
- 차점: 7V1_L04_engulf_panic_retake | final_return_pct 34.2567 | max_return_pct 36.4517 | max_drawdown_pct 7.9660 | cd_value 123.5618 | trades 5071
- 그 다음: 7V1_L09_beartrap_close_drive | final_return_pct 21.1251 | max_return_pct 21.8769 | max_drawdown_pct 7.6741 | cd_value 111.8298 | trades 4778
- low-MDD 최고: 7V1_L06_deep_ema20_retake | final_return_pct 0.9083 | max_return_pct 0.9889 | max_drawdown_pct 0.6282 | cd_value 100.2744 | trades 332
- 결론: 승격은 없었지만, 6V5 이후 죽어 있던 raw upside가 신규 reversal family에서 다시 살아났다. 다만 같은-bar 반전 신호를 넓게 허용하면 과다거래와 MDD 재팽창이 즉시 재현된다.

2. 장점

2-1. shock / panic / beartrap / climax wick 계열의 raw edge 존재
- L10, L04, L09, L07, L01, L02는 모두 MDD 기준을 넘었지만, 단순 low-MDD 소멸형 전략과 달리 실제 max_return_pct 13.5125~56.5963 구간까지 뻗었다.
- 이는 7V1에서 도입한 신규 reversal family가 완전히 무의미한 아이디어가 아니라, 전체 종목 풀 5분봉에서도 반전 에너지 자체는 포착하고 있음을 뜻한다.
- 특히 5V2_L01_capitulation_reclaim이 보여줬던 raw upside의 성격이, 이번에는 same-bar shock / panic / beartrap 캔들 계열에서도 다시 확인됐다.

2-2. 반전 코어는 broad continuation보다 분명한 이벤트 중심 구조다
- 7V1 상위권은 단순 눌림/리테스트/압축보다, 충격 캔들 직후의 비정상 복귀나 beartrap close drive처럼 사건성이 있는 캔들에서 성능이 나왔다.
- 이는 generic continuation보다 event-driven reversal이 여전히 long 신규 family 후보로 더 가치가 크다는 점을 재확인해 준다.

2-3. 제한형 버전은 MDD 통제력이 있다
- L06, L05, L03, L08은 수익은 약했지만 MDD가 0.4819~1.9005로 유지됐다.
- 즉 reversal family 자체가 반드시 고위험인 것은 아니고, 선택도를 높이면 방어력 자체는 확보 가능하다.

3. 단점

3-1. same-bar 반전 조건을 넓게 켜면 즉시 과다거래와 MDD 팽창으로 무너진다
- L10 trades 33481, L04 5071, L09 4778, L01 9885, L02 2944, L07 2118로 모두 거래 수가 높아졌고, MDD도 5.5953~15.1033으로 상승했다.
- 이는 새 family의 raw edge가 존재해도, rarity suppression 없이 쓰면 결국 5V2 broad family 실패를 다른 이름으로 반복하게 된다는 뜻이다.

3-2. 너무 강한 제한형 버전은 edge를 거의 소거한다
- L03, L05, L06, L08은 trades 45~671 수준으로 억제됐지만 final_return_pct가 -0.7596~0.9083에 머물렀다.
- 즉 단순히 거래 수를 줄이는 것만으로는 충분하지 않고, 신호를 줄이더라도 남는 신호가 실제로 강한 확장 후보가 되도록 설계해야 한다.

3-3. engulf / hammer / wick / outside bar 자체는 충분한 선택 조건이 아니다
- 캔들 모양만으로는 전체 종목 풀에서 여전히 너무 자주 켜진다.
- 따라서 캔들 패턴 명칭 자체를 전략 핵심으로 삼기보다, 직전 shock 강도, prior exhaustion, 위치 편차, recent-fire suppression 같은 구조적 희소성 조건을 같이 묶어야 한다.

4. 다음 전략 생성 규칙
- 7V1 상위권 family는 폐기하지 않는다. 오히려 다음 long 신규 배치의 주력 코어 후보로 유지한다.
- 단, same-bar raw reversal은 단독 조건으로 다시 내지 않는다.
- 다음 배치에서는 아래 요소를 기본 내장한다.
  1) recent-fire suppression: 직전 N봉 내 동일 이벤트 재발 금지
  2) shockfresh / exhaustion age: 충격 직후 첫 번째 또는 제한된 횟수의 반전만 허용
  3) location compression: deep extension 이후 첫 reclaim, 또는 prior low undercut 이후 close recovery처럼 위치를 더 좁힐 것
  4) spacing/cooldown: 동일 종목 연속 반전 난사 차단
  5) follow-through quality: 단순 종가 복귀보다 reclaim 이후 body/drive/close quality를 추가 확인
- 반대로 outside flush, deep ema20 retake, rangefloor pop 같은 저위험-저수익 버전은 단독 family로 확장하지 않는다. 이들은 필요하면 보조 필터나 하위 브랜치로만 사용한다.

5. 한 줄 결론
- 7V1은 승격 실패 라운드지만, long 신규 family 탐색이라는 관점에서는 유의미한 전진이다.
- 핵심 학습은 명확하다. 새 reversal family는 살아 있다. 다만 raw same-bar 반전을 넓게 허용하면 실패하고, 선택적 rarity control과 spacing을 얹어야만 공식 기준선 도전이 가능하다.
