# 6V2_LONG10_REVIEWED STRENGTHS AND WEAKNESSES ADDENDUM

이 문서는 6V2_LONG10_REVIEWED 결과를 CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md에 바로 반영하기 전까지, 최신 long 전용 학습을 별도로 고정하기 위한 보조 문서다.
핵심 목적은 다음 long 전략 생성 시 6V2 라운드의 장점을 재사용하고, 실패 패턴을 반복하지 않도록 규칙으로 남기는 것이다.

## 1. double flush + cap reclaim 코어 계열

장점
- 이번 배치의 핵심 승자는 6V2_L01_doubleflush_core 였다. trades 592, win_rate_pct 58.1081, final_return_pct 23.6961, max_return_pct 23.9191, max_drawdown_pct 1.7512, cd_value 121.5300으로 공식 long 기준선을 교체했다.
- 이 결과는 5V2_L01_capitulation_reclaim의 장점이었던 강한 확장 잠재력을 유지하면서, 가장 큰 약점이었던 과도한 MDD를 크게 줄였다는 점에서 중요하다.
- 즉 급락 후 즉시 반등이라는 아이디어 자체는 맞았고, 여기에 double flush 식의 재차 흔들기와 선택적 회수 구조를 얹으면 전체 종목 풀에서도 방어력과 확장성을 동시에 잡을 수 있다.
- 거래 수가 수백 회 단위로 유지된 것도 중요하다. 지나치게 넓게 켜지는 과다거래형 전략도 아니고, 너무 드물게만 발생하는 0트레이드형 전략도 아니었다.

단점
- raw capitulation reclaim처럼 너무 단순한 급락 회수 구조로 돌아가면 다시 MDD가 커질 위험이 있다.
- 따라서 이후 개선은 core를 버리는 방향이 아니라, core를 유지한 채 더 좋은 자리만 고르는 방향이어야 한다.
- 특히 추세 한복판의 무리한 칼날 잡기, 회수 강도가 약한 저품질 복귀, 추세 재개가 없는 일회성 반등은 계속 경계해야 한다.

## 2. extreme close quality 강화형 계열

장점
- 6V2_L04_doubleflush_extremeclose는 trades 442, win_rate_pct 61.3122, final_return_pct 19.2086, max_return_pct 19.4782, max_drawdown_pct 1.0102, cd_value 118.0043을 기록했다.
- 이는 L01의 코어가 우연히 한 번 맞은 것이 아니라, 종가 품질을 더 엄격히 요구해도 여전히 강하게 작동한다는 뜻이다.
- 특히 MDD 1.0102는 매우 우수하다. 즉 종가 품질 필터는 double flush 코어의 방어력을 더 끌어올릴 수 있는 유효한 보조 게이트다.

단점
- 다만 수익 확장과 cd_value는 L01보다 낮았다.
- 즉 extreme close는 주력 코어 자체라기보다, 코어의 품질을 올리는 옵션형 모듈로 보는 편이 낫다.
- 이후 개선에서 extreme close를 너무 강하게 쓰면 좋은 초기 진입까지 삭제할 위험이 있으므로, 필수 조건보다 선택형 보조 조건으로 다루는 것이 더 적절하다.

## 3. trend floor / second push / delayed confirmation 계열

장점
- 아이디어 차원에서는 나쁘지 않다. 급락 회수 이후 구조적 바닥 확인이나 2차 밀어올림을 기다리면, 직관적으로는 더 안전해 보인다.
- 실제로 거래 수를 줄이는 데는 일정 부분 성공한다.

단점
- 6V2_L02_doubleflush_trendfloor는 trades 54, final_return_pct -0.5371, max_return_pct 0.0000, max_drawdown_pct 0.7739, cd_value 98.6931에 그쳤다.
- 6V2_L05_doubleflush_secondpush는 trades 354, win_rate_pct 21.1864, final_return_pct -2.3852, max_drawdown_pct 2.3852, cd_value 95.2866으로 더 나빴다.
- 핵심 문제는 반등의 핵심 에너지가 이미 지나간 뒤 너무 늦게 들어간다는 점이다. 급락 회수 계열의 엣지는 초반 복귀 에너지에서 나오는데, trend floor나 second push를 과도하게 기다리면 좋은 파동을 버리고 뒤늦은 약한 구간만 사게 된다.
- 따라서 delayed confirmation은 진입 강화의 기본 축으로 쓰지 않는다. 필요하더라도 진입 자체를 늦추는 용도가 아니라, 이미 선택된 코어의 품질 보조 확인 수준으로만 제한한다.

## 4. quiet / absorb / contraction / 과선택 필터 계열

장점
- 이 계열의 존재 이유는 분명하다. 노이즈를 더 줄이고, 더 정제된 상황만 거래하려는 목적이다.
- 이론적으로는 MDD를 더 낮추는 데 도움이 될 수 있다.

단점
- 이번 배치에서는 과선택화의 부작용이 명확했다.
- 6V2_L03_doubleflush_quiet, 6V2_L06_doubleflush_absorbbreak, 6V2_L08_quiet_reclaim_secondpush는 모두 0트레이드였다.
- 6V2_L10_contraction_flush_break는 trades 3, final_return_pct 0.1384, max_return_pct 0.1484, max_drawdown_pct 0.0099, cd_value 100.1285였다. 숫자만 보면 깔끔해 보일 수 있으나 재현성 있는 주력 전략으로 보기 어렵다.
- 즉 quiet, absorb, contraction 류 필터를 무분별하게 얹으면 전략을 개선하는 것이 아니라 전략을 지워버릴 수 있다.
- 따라서 이후 규칙은 명확하다. 추가 필터는 항상 거래 수 소실 위험과 함께 봐야 하며, 0트레이드 또는 극소수 트레이드가 나오는 조합은 주력 후보에서 제외한다.

## 5. 6V2 라운드에서 확정된 생성 규칙

1. 다음 long 전략의 출발점은 double flush + cap reclaim 코어다.
2. extreme close quality는 재사용 가치가 높지만, 필수 메인 코어가 아니라 선택형 품질 게이트다.
3. trend floor, delayed second push, 과도한 구조 확인은 초반 반등 에너지를 죽일 수 있으므로 메인 진입 조건으로 승격하지 않는다.
4. quiet, absorb, contraction 류 필터는 0트레이드 위험이 높으므로, 거래 수 하한 검증 없이 반복 실험하지 않는다.
5. broad continuation이나 generic retest 계열보다 selective shock-reclaim 계열이 현재 long 쪽에서 훨씬 우세하다.
6. 다음 개선 방향은 core를 버리고 새 계열로 도망가는 것이 아니라, L01 코어 위에 위치 필터와 품질 필터를 얇게 추가해 MDD를 더 줄이거나 cd_value를 더 높이는 쪽이다.

## 6. 실전 해석 한 줄 요약
- 5V2는 잠재력은 컸지만 위험 압축에 실패했다.
- 6V2는 그 잠재력을 double flush 코어로 정제해 공식 long 승격까지 만들었다.
- 앞으로의 long 설계는 이 코어를 중심으로 얇고 선택적인 보조 게이트를 붙이는 방향이 맞다.
