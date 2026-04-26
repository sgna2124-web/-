8V2_LONG100_REVIEWED 장단점 추가 기록

이 문서는 8V2_LONG100_REVIEWED 결과를 바탕으로, 8V1과는 다른 신규 long family 100개를 검증한 결과를 다음 생성 규칙으로 남기기 위한 addendum이다.

1. 배치 요약
- batch best: 8V2_L31_V01_core_relaunch | final_return_pct 1.6503 | max_return_pct 1.7448 | max_drawdown_pct 0.3516 | cd_value 101.2929 | trades 107
- next: 8V2_L31_V08_shockage_window | final_return_pct 1.6124 | max_return_pct 1.6856 | max_drawdown_pct 0.3302 | cd_value 101.2769 | trades 73
- next: 8V2_L36_V02_extreme_reclaim | final_return_pct 2.0943 | max_return_pct 2.3498 | max_drawdown_pct 0.9835 | cd_value 101.0902 | trades 507
- strongest upside in batch was still weak: 8V2_L36_V05_prevhigh_rearm | final_return_pct 2.4436 | max_return_pct 3.0428 | max_drawdown_pct 1.9631 | cd_value 100.4325 | trades 2553
- conclusion: 8V2의 신규 family 100개는 8V1보다 아주 약간 나아졌지만, 여전히 이전 L09/L07 reversal family와 비교할 raw upside가 전혀 없었다. 기준선 도전과는 거리가 멀다.

2. 장점

2-1. L31 core_relaunch / shockage_window 계열은 방어형 구조로는 의미가 있다.
- L31_V01, L31_V08, L31_V03은 MDD를 0.33~1.12 수준으로 억제했다.
- 즉 relaunch + shockage_window 조합은 손실 억제형 보조 아이디어로는 참고 가치가 있다.

2-2. L36 extreme_reclaim / prevhigh_rearm은 그나마 수익 잠재력이 있었다.
- L36_V02와 L36_V05는 batch 상단권에 위치했고, max_return_pct 2~3 수준까지는 만들어냈다.
- 8V2 family 중에서는 그나마 “아예 죽어 있지 않은” 축으로 본다.

2-3. 일부 family는 거래 수 폭증 없이도 신호가 발생했다.
- L31, L36, L37 상단 전략들은 trades 39~580 수준으로 제한되면서도 완전히 0트레이드로 죽지는 않았다.
- 즉 신호 구조를 너무 넓게 만들지 않고도 발화는 가능했다.

3. 단점

3-1. 가장 큰 문제는 여전히 raw upside 부재다.
- batch best조차 max_return_pct 1.7448, cd_value 101.2929 수준이다.
- 이는 7V계열에서 보였던 raw reversal edge와 전혀 다른 수준이며, 현재 공식 기준선 도전력은 없다고 봐야 한다.

3-2. L32, L33, L40 계열은 구조적으로 붕괴했다.
- L32_V04~V10, L33_V04~V10, L40_V04~V10 일부는 trades 20만~92만 회대로 폭증했고, MDD 93~99.99% 구간까지 무너졌다.
- 따라서 이 축은 broad overtrading failure로 분류하고 현 형태로는 폐기 대상이다.

3-3. L39 일부와 L38 계열도 확대 시 급격히 무너진다.
- L39_V04~V10과 L38_V01/V04/V05/V07/V08/V09는 trades 수천~수만 회대로 늘며 MDD가 크게 악화됐다.
- 즉 prevhigh_rearm, cluster_pressure, firstfire_quality, shockage_window 같은 태그를 아무 family에나 붙인다고 엣지가 생기지 않는다.

3-4. zero-trade 또는 극소수 trade도 의미 있는 승격 후보가 아니다.
- L35_V01, L35_V02, L37_V02는 0트레이드였다.
- L31_V02, L34_V02, L35_V08 같은 극소수 trade 전략도 결과상 재현성 있는 후보로 볼 수 없다.

4. 다음 생성 규칙
- 8V2 family들(L31~L40)은 현재 단계에서 long 주력 신규 family로 승격하지 않는다.
- 특히 L32, L33, L40은 broad overtrading failure로 분류하고 현 형태로는 폐기 우선순위가 높다.
- L31 relaunch와 L36 extreme_reclaim은 보조 태그/보조 필터 차원에서만 제한적으로 참고한다.
- shockage_window, extreme_reclaim, relaunch 같은 태그는 보조축으로만 저장 가치가 있다.
- 다음 주력은 다시 L09 beartrap family와 L07 wick family 중심으로 돌아간다.

5. 한 줄 결론
- 8V2는 8V1보다 전략 수와 다양성은 더 컸지만, 새로운 edge를 만들지 못했다.
- 다음 단계는 다시 L09/L07 중심으로 돌아가고, 8V2에서는 relaunch/shockage_window/extreme_reclaim 정도만 보조 태그로 제한적으로 참고한다.
