7V2_LONG40_REVIEWED 장단점 추가 기록

이 문서는 7V2_LONG40_REVIEWED 결과를 바탕으로, 7V1에서 드러난 신규 reversal family의 장단점을 더 정교하게 구조화해 다음 long 생성 규칙으로 남기기 위한 addendum이다.

1. 배치 요약
- 최고 raw upside: 7V2_L10_V02_balance_shockfresh_drive | final_return_pct 43.8072 | max_return_pct 47.1476 | max_drawdown_pct 9.1478 | cd_value 130.6520 | trades 18419
- 그다음 raw upside: 7V2_L10_V07_balance_closedrive | final_return_pct 43.4233 | max_return_pct 47.1152 | max_drawdown_pct 9.3596 | cd_value 129.9995 | trades 19328
- 3위 raw upside: 7V2_L10_V06_balance_shocklow_retake | final_return_pct 52.7194 | max_return_pct 58.9180 | max_drawdown_pct 18.5213 | cd_value 124.4338 | trades 30585
- best under MDD<5 but baseline fail: 7V2_L09_V09_beartrap_extreme_synergy | final_return_pct 15.8330 | max_return_pct 16.0180 | max_drawdown_pct 2.5330 | cd_value 112.8990 | trades 730
- next under MDD<5: 7V2_L07_V08_wick_closedrive | final_return_pct 15.3392 | max_return_pct 15.7100 | max_drawdown_pct 3.3512 | cd_value 111.4740 | trades 1439
- 다음 under MDD<5: 7V2_L07_V09_wick_extreme_synergy | final_return_pct 14.3090 | max_return_pct 14.5280 | max_drawdown_pct 3.3181 | cd_value 110.5161 | trades 754
- 결론: 7V1의 raw reversal family는 7V2에서 “선택적 억제”를 거치며 MDD<5 구간에서도 110대 cd까지 실제로 끌어올릴 수 있음이 확인됐다. 다만 아직 공식 기준선 121.5300을 넘는 MDD<5 후보는 나오지 않았다.

2. 장점

2-1. L10 balance 계열은 strongest raw upside family다.
- shockfresh_drive, closedrive, shocklow_retake 세 변형이 모두 cd_value 124~130대를 기록했다.
- 이는 same-bar shock reversal family 안에서도 L10 balance 계열이 가장 강한 확장성을 갖고 있음을 의미한다.
- 단, 지금 단계에서는 동일 family가 거래 수 1만~3만 회대로 너무 넓게 켜지며 MDD가 9~18%로 커진다. 즉 core family 자체는 유효하지만, gating이 아직 부족하다.

2-2. L09 beartrap 계열은 “승격에 가장 가까운 선택적 신규 family”다.
- 7V2_L09_V09_beartrap_extreme_synergy가 max_drawdown_pct 2.5330, cd_value 112.8990까지 올라왔다.
- 7V2_L09_V04_beartrap_deepdiscount도 max_drawdown_pct 4.2069, cd_value 103.1559로 생존했다.
- 즉 beartrap 계열은 raw upside도 있고, 선택도를 올렸을 때 MDD<5 안에서 성과를 남길 가능성이 가장 높다.

2-3. L07 wick 계열도 제한형으로는 꽤 강하다.
- 7V2_L07_V08_wick_closedrive와 7V2_L07_V09_wick_extreme_synergy는 trades 754~1439, MDD 3.31~3.35, cd 110대까지 올라왔다.
- 이는 wick reclaim family가 같은-bar reversal류 중에서도 상대적으로 제어가 쉬운 축임을 뜻한다.
- 특히 closedrive, extreme synergy처럼 “종가 품질”을 강화하는 쪽이 유효했다.

2-4. L04 engulf 계열은 raw drive는 있으나 품질 편차가 크다.
- 7V2_L04_V09_engulf_shocklow_retake는 cd 120.7161까지 올랐지만 MDD 7.7437로 탈락했다.
- 반면 7V2_L04_V03_engulf_lowanchor_singlefire는 MDD 2.4929로 낮췄지만 cd는 101.4679에 그쳤다.
- 즉 engulf 계열은 drive를 살리면 MDD가 커지고, MDD를 줄이면 edge가 옅어지는 전형적 trade-off가 확인됐다.

3. 단점

3-1. broad same-bar reversal을 그대로 쓰면 7V1과 똑같이 과다거래 + MDD 재팽창이 재현된다.
- L10 상위 3개와 L09 상위 raw 계열, L04 shocklow 계열 모두 trades가 수천~수만 회까지 늘었다.
- 따라서 신규 reversal family에서도 가장 먼저 넣어야 하는 것은 패턴 미세조정이 아니라 rarity control, event age suppression, refractory spacing이다.

3-2. firstshock_strict, trendfloor_deep, maxselective 계열은 이름과 달리 edge를 손상시키는 경우가 많았다.
- 예: 7V2_L10_V01_balance_firstshock_strict, 7V2_L10_V10_balance_maxselective, 7V2_L09_V10_beartrap_maxselective, 7V2_L04_V10_engulf_maxselective는 모두 성과가 무너졌다.
- 즉 “더 엄격하게 만들면 더 좋아질 것”이라는 가정은 이 family에서 자주 틀린다.
- 지나친 선택 조건은 강한 신호만 남기는 것이 아니라, 강한 파동의 초입도 함께 삭제한다.

3-3. EMA20/trendfloor/midflip 계열은 보조 요인으로는 의미가 있을 수 있으나 hard gate로는 약했다.
- L10_V03_balance_ema20_midflip, L07_V04_wick_trendfloor, L04_V04_engulf_drive_midflip, L09_V03_beartrap_ema20_trend 등은 대부분 수익을 강화하지 못했다.
- 따라서 이 계열은 다음부터 hard gate보다 score/tie-break/priority 용도로만 본다.

3-4. clusterban은 과다거래 억제에는 기여하지만 edge 보존이 부족했다.
- L09_V08_beartrap_clusterban, L10_V09_balance_clusterban, L04_V06_engulf_shock_clusterban, L07_V06_wick_clusterban을 보면 거래 수는 일부 줄었지만, 여전히 MDD가 높거나 수익이 약했다.
- 즉 clusterban 하나만으로는 부족하고, event rarity와 location discount까지 함께 들어가야 한다.

4. 다음 생성 규칙

4-1. 다음 long 신규 family 확장 우선순위
1) L09 beartrap family
2) L07 wick reclaim family
3) L10 balance shock family
4) L04 engulf family
- 이유는 L09와 L07이 MDD<5 구간에서 110대 cd까지 실제로 도달했기 때문이다.
- L10은 raw upside 최고지만 현재 형태로는 과다거래 억제가 더 어려워 후순위다.
- L04는 edge는 있으나 trade-off가 더 크므로 네 번째 우선순위다.

4-2. 다음 라운드에 반드시 넣을 공통 장치
- recent-fire suppression
- same-symbol refractory bars
- first-valid-event or capped-retrigger logic
- shockfresh age limit
- close quality or reclaim quality score
- 필요시 extreme/discount branch를 tie-break로 사용

4-3. 다음 라운드에서 피할 것
- same-bar reversal을 아무 context 없이 넓게 허용하는 구조
- firstshock_strict / maxselective / trendfloor_deep 류 hard gate를 과도하게 겹치는 구조
- ema20 / midflip / trendfloor를 필수 진입 조건으로 격상하는 구조

5. 한 줄 결론
- 7V2는 7V1보다 한 단계 진전했다.
- 새 reversal family는 단순 raw edge 수준을 넘어서, 제한형으로도 110대 cd까지 올라올 수 있음을 증명했다.
- 다음 목표는 명확하다. L09/L07을 중심으로 MDD<5를 유지한 채 121.53을 넘는 승격 후보를 만드는 것이다.
