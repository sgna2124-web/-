7V3_LONG40_REVIEWED 장단점 추가 기록

이 문서는 7V3_LONG40_REVIEWED 결과를 바탕으로, 7V2에서 확인된 신규 reversal family를 더 압축한 결과를 다음 long 생성 규칙으로 고정하기 위한 addendum이다.

1. 배치 요약
- batch raw-upside best: 7V3_L09_V09_beartrap_cluster_pressure | final_return_pct 41.1544 | max_return_pct 42.1291 | max_drawdown_pct 11.2133 | cd_value 125.3264 | trades 6863
- next raw-upside: 7V3_L09_V03_beartrap_lowanchor_drive | final_return_pct 39.3617 | max_return_pct 40.1602 | max_drawdown_pct 11.9139 | cd_value 122.7583 | trades 7664
- best under MDD<5: 7V3_L09_V02_beartrap_extreme_synergy | final_return_pct 15.8330 | max_return_pct 16.0180 | max_drawdown_pct 2.5330 | cd_value 112.8990 | trades 730
- next under MDD<5: 7V3_L07_V02_wick_drive_reclaim | final_return_pct 15.6410 | max_return_pct 16.0068 | max_drawdown_pct 3.2136 | cd_value 111.9247 | trades 1443
- next under MDD<5: 7V3_L07_V03_wick_extreme_synergy | final_return_pct 14.3090 | max_return_pct 14.5280 | max_drawdown_pct 3.3181 | cd_value 110.5161 | trades 754
- 결론: 7V2의 방향이 유지되었고, L09 beartrap과 L07 wick 계열이 여전히 신규 family의 최우선 축임이 재확인되었다. 다만 공식 long 기준선 121.5300을 넘는 MDD<5 전략은 여전히 부재하다.

2. 장점

2-1. L09 beartrap family가 가장 유망하다.
- raw upside best도 L09였고, MDD<5 최고도 L09였다.
- 즉 이 family는 high-upside와 selective control 둘 다에서 가장 균형이 좋다.
- 다음 long 신규 배치의 최우선 family는 L09 beartrap 계열로 고정한다.

2-2. L07 wick family도 안정적 2순위다.
- 7V3_L07_V02와 7V3_L07_V03은 7V2와 유사하게 MDD<5에서 110대 cd를 유지했다.
- trades 754~1443 수준으로 sample 수가 너무 죽지도 않았고, raw upside는 L09보다 약하지만 통제가 더 쉬운 편이다.
- L07은 2순위 family로 유지한다.

2-3. L04 engulf family는 제한형 일부만 보조 가치가 있다.
- 7V3_L04_V07_engulf_volcap_drive는 MDD 4.8202에서 cd 102.4061까지 왔다.
- 하지만 나머지 engulf 파생은 대부분 MDD 초과이거나 엣지가 약했다.
- 따라서 L04는 주력 family보다 보조 아이디어 저장 대상에 가깝다.

2-4. 속도 개선은 실제 성과다.
- 사용자 보고 기준으로 7V3의 40전략 배치는 이전 40전략 배치보다 백테스트 시간이 크게 단축되었다.
- 이 점은 결과 못지않게 중요하다. 다음 대규모 배치도 7V3의 실행 구조를 유지해야 한다.

3. 단점

3-1. L09/L10 raw reversal은 여전히 과다거래와 MDD 재팽창이 문제다.
- L09_V09, L09_V03, L10_V03, L10_V02는 cd가 높아도 trades가 6863~18191, MDD가 9~12% 수준으로 커진다.
- 즉 raw same-bar 반전의 edge는 확인됐지만, 아직도 firing density 제어가 충분하지 않다.

3-2. ultraselective / lowanchor_singlefire 계열은 edge를 과하게 죽인다.
- L04_V10, L09_V10, L10_V10, L07_V10, L04_V03 등은 MDD는 낮추지만 수익이 너무 줄거나 음수화된다.
- 즉 과도한 단발성/초선택화는 6V3, 6V4 때와 같은 문제를 반복한다.

3-3. prevhigh/midflip/ema20 류는 여전히 hard gate로 약하다.
- L10_V04_balance_prevhigh_drive, L09_V04_beartrap_prevhigh_retake, L10_V07_balance_midflip_reclaim, L04_V08_engulf_prevhigh_drive, L07_V05_wick_prevhigh_drive를 보면, 설명력은 있지만 주력 성능 개선으로 이어지지 못했다.
- 따라서 이 계열은 다음부터 진입 필수 조건보다 score/tie-break로만 다룬다.

3-4. volcap/cluster_pressure는 단독으로는 충분하지 않다.
- 일부 경우 거래 수를 줄이는 데는 도움이 되지만, 그것만으로 승격 후보까지는 끌어올리지 못했다.
- 즉 이 장치들은 core edge를 대체하는 것이 아니라 보조 장치다.

4. 다음 생성 규칙

4-1. family 우선순위 고정
1) L09 beartrap family
2) L07 wick family
3) L10 balance family
4) L04 engulf family

4-2. 다음 라운드에 반드시 유지할 구조
- 공통 feature/raw를 심볼당 한 번만 계산하고 재사용한다.
- same-bar raw reversal은 유지하되, recent-fire suppression과 refractory spacing을 기본 장치로 둔다.
- prevhigh, ema20, midflip, trendfloor는 hard gate보다 soft score나 tie-break로 사용한다.
- volcap, cluster, shockfresh age는 보조 억제 장치로 쓰되, core family를 대체하지 않는다.

4-3. 다음 라운드에서 피할 것
- ultraselective, maxselective, lowanchor_singlefire 같은 과선택화 브랜치의 과도한 확장
- same-bar raw reversal을 아무 suppression 없이 넓게 허용하는 구조
- prevhigh/midflip/ema20을 필수 진입 트리거로 승격하는 구조

5. 한 줄 결론
- 7V3는 승격 실패지만, 7V2의 결론을 더 강하게 굳혔다.
- 다음 long 신규 배치는 L09 1순위, L07 2순위 중심으로 가고, 7V3의 속도 개선 실행 구조는 유지한다.
