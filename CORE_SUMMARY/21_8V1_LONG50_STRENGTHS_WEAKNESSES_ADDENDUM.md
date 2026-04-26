8V1_LONG50_REVIEWED 장단점 추가 기록

이 문서는 8V1_LONG50_REVIEWED 결과를 바탕으로, 7V계열과 다른 신규 long family 50개를 검증한 결과를 다음 생성 규칙으로 남기기 위한 addendum이다.

1. 배치 요약
- batch best: 8V1_L25_V01_washout_squeeze_release | final_return_pct 1.2567 | max_return_pct 1.2888 | max_drawdown_pct 0.1903 | cd_value 101.0640 | trades 54
- next: 8V1_L25_V08_squeeze_shockage_window | final_return_pct 0.9310 | max_return_pct 0.9310 | max_drawdown_pct 0.4424 | cd_value 100.4845 | trades 222
- next: 8V1_L25_V02_squeeze_extreme_release | final_return_pct 0.2301 | max_return_pct 0.2302 | max_drawdown_pct 0.1133 | cd_value 100.1165 | trades 15
- best non-squeeze but still weak: 8V1_L22_V06_inside_lowanchor_pop | final_return_pct 1.7901 | max_return_pct 3.2382 | max_drawdown_pct 1.7176 | cd_value 100.0417 | trades 3372
- conclusion: 이번 8V1의 신규 family 50개는 이전 L09/L07 reversal family와 달리 raw upside 자체가 전반적으로 죽어 있었다. 공식 기준선 도전과는 거리가 매우 멀었다.

2. 장점

2-1. washout_squeeze_release 계열은 방어력은 있다.
- L25_V01, L25_V08, L25_V02는 MDD를 매우 낮게 유지했다.
- 즉 squeeze/washout 계열은 손실 억제형 아이디어로는 의미가 있다.

2-2. 일부 inside/microbase/absorb 파생은 거래 수는 충분했다.
- L22_V06, L21_V06, L23_V05 같은 전략은 trades가 수천 회까지도 나왔다.
- 즉 전략이 전혀 안 켜진 것은 아니고, 신호 밀도 자체는 존재했다.

3. 단점

3-1. 가장 치명적인 문제는 raw upside 부재다.
- 상위권조차 max_return_pct가 1~3 수준에 머물렀다.
- 이는 7V1~7V4에서 확인된 L09/L07/L10 계열과 달리, 이번 family들은 시장의 큰 반전 에너지나 재가속 구간을 잡지 못했다는 뜻이다.

3-2. holdpop family는 구조적으로 붕괴했다.
- L24_V09, L24_V04, L24_V05, L24_V06, L24_V10, L24_V07은 trades 5만~19만 회대까지 폭증하며 MDD 44~87% 구간으로 붕괴했다.
- 따라서 holdpop family는 현재 형태로는 폐기 대상이다.

3-3. absorb/inside/microbase 계열도 broad firing 위험이 크다.
- L21, L22, L23 일부 파생은 trades가 수천~2만 회대로 늘었지만 수익곡선은 대부분 약하거나 음수였다.
- 즉 이 family들은 broad continuation 실패 패턴을 다른 이름으로 반복했을 가능성이 높다.

3-4. squeeze family는 너무 안전하게 만들면 edge가 사라진다.
- L25가 상위권을 차지했지만, 이는 좋은 전략이라기보다 나머지가 더 나빴기 때문이다.
- MDD는 낮지만 수익과 max_return_pct가 너무 얕아 기준선 도전력은 거의 없다.

4. 다음 생성 규칙
- 8V1 family들(L21 shock_absorb, L22 inside, L23 microbase, L24 holdpop, L25 squeeze)은 현재 단계에서 long 주력 신규 family로 승격하지 않는다.
- 특히 L24 holdpop family는 폐기 우선순위가 높다.
- L25 squeeze family는 주력 코어가 아니라 보조 필터 또는 방어형 보조 조건으로만 저장 가치를 본다.
- 다음 주력은 다시 L09 beartrap family와 L07 wick family 중심으로 회귀한다.
- 8V1에서 재사용할 가치가 있는 것은 family 자체보다 after_pause, shockage_window, lowanchor_pop 같은 일부 보조 패턴 태그 정도다.

5. 한 줄 결론
- 8V1은 새로운 50개 family 실험이었지만, 현재 long 기준선에 도전할 만한 새로운 엣지를 전혀 만들지 못했다.
- 다음 단계는 다시 L09/L07 중심으로 돌아가되, 8V1에서 상대적으로 덜 나빴던 보조 태그만 선별적으로 참고하는 것이다.
