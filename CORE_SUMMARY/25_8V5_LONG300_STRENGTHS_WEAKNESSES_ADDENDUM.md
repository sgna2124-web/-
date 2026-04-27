8V5_LONG300_REVIEWED 장단점 추가 기록

이 문서는 8V5_LONG300_REVIEWED 결과를 바탕으로, V51만을 대상으로 300개를 세 그룹(파라미터 조정 100개, 장점 극대화 100개, 단점 커버 100개)으로 확장 검증한 결과를 다음 생성 규칙으로 남기기 위한 addendum이다.

1. 배치 요약
- batch best candidate_cd_win_mdd_fail: 8V5_V51P_V002_core_rare22_c1 | final_return_pct 41.6763 | max_return_pct 42.1517 | max_drawdown_pct 6.3109 | cd_value 132.7352 | trades 2277
- next: 8V5_V51P_V001_core_base | final_return_pct 41.0096 | max_return_pct 41.4900 | max_drawdown_pct 6.2801 | cd_value 132.1541 | trades 2277
- next: 8V5_V51P_V032_shocklow_rare22_c1 | final_return_pct 41.8220 | max_return_pct 42.3994 | max_drawdown_pct 7.2292 | cd_value 131.5694 | trades 2276
- next: 8V5_V51P_V031_shocklow_base | final_return_pct 41.4808 | max_return_pct 41.9799 | max_drawdown_pct 7.2419 | cd_value 131.2349 | trades 2276
- best under MDD<5 overall: 8V5_V51P_V012_strict_rare22_c1 | final_return_pct 19.5333 | max_return_pct 19.7596 | max_drawdown_pct 2.7359 | cd_value 116.2630 | trades 1040
- next under MDD<5: 8V5_V51P_V011_strict_base | final_return_pct 19.1976 | max_return_pct 19.4241 | max_drawdown_pct 2.6505 | cd_value 116.0383 | trades 1040
- next under MDD<5: 8V5_V51P_V022_lowanchor_rare22_c1 | final_return_pct 18.9851 | max_return_pct 19.2151 | max_drawdown_pct 2.8711 | cd_value 115.5689 | trades 1040
- conclusion: 8V5는 공식 승격은 없었지만, 8V4 대비 V51 top candidate의 MDD를 실제로 약 6.75 → 6.28 수준까지 낮추는 데 성공했다. 반면 MDD<5 최고권은 8V4의 117.5603보다 소폭 후퇴했다. 즉 파라미터 조정은 high-cd 후보를 더 근접하게 만들었지만, 안전권 후보를 더 강하게 만들지는 못했다.

2. 장점

2-1. 파라미터 조정 그룹(V51P)이 이번 라운드의 실질 승자다.
- top 4가 모두 V51P에서 나왔다.
- 특히 core_base / core_rare22_c1은 8V4 대비 MDD를 6.75대에서 6.28~6.31대로 낮추면서 cd 132대를 유지했다.
- 이는 V51 개선에서 단순 신규 태그 추가보다, 기존 강한 코어의 firing density와 gate 강도를 미세 조정하는 것이 실제 효과가 있음을 뜻한다.

2-2. strict branch가 MDD<5 구간에서 가장 강해졌다.
- 8V5에서는 lowanchor보다 strict가 더 높은 cd를 기록했다.
- V012 strict_rare22_c1, V011 strict_base가 각각 cd 116.2630, 116.0383으로 MDD<5 최상단을 형성했다.
- 즉 안전권 공식 후보군은 이제 lowanchor 단독보다 strict 계열을 더 우선 봐야 한다.

2-3. lowanchor도 여전히 유효하다.
- V022 lowanchor_rare22_c1, V021 lowanchor_base는 cd 115대 중반을 유지했다.
- strict 바로 아래 보조 축으로 계속 보관 가치가 높다.

2-4. spring/refire40 계열은 안정적인 중상단 방어 후보를 만든다.
- V062, V067, V061, V017, V037, V007 등은 trades 671~675 수준에서 cd 112대 전후를 유지했다.
- 즉 핵심 승격 후보는 아니지만, 지나친 MDD 상승 없이 구조적 안정성을 확인하는 비교군으로 유용하다.

3. 단점

3-1. 아직도 공식 승격은 없다.
- top candidate의 MDD가 6.2801~6.3109로 줄긴 했지만, 여전히 공식 장벽 5%를 넘는다.
- 즉 가장 강한 코어는 거의 다 왔지만, 아직 1단계가 더 필요하다.

3-2. shocklow branch는 top core보다 오히려 MDD가 더 높다.
- V032, V031은 cd 131대지만 MDD 7.23~7.24 구간이다.
- 따라서 shocklow는 raw edge source일 수는 있어도, 현재 시점에서는 core_base/rare22_c1보다 우선순위가 낮다.

3-3. 장점 극대화/단점 커버 그룹(C/E)의 상당수는 edge를 희석했다.
- quality_hold, softscore, hammer_outside, 일부 microguard는 대부분 cd 102~109대 수준에 머물렀다.
- 즉 보조 장치는 도움될 수 있지만, 과도하게 얹으면 V51 본래의 edge를 죽인다.

3-4. 과억제 계열은 0트레이드로 사라진다.
- noshock14, vol16_quiet, ema_mid 계열 다수는 0트레이드였다.
- 따라서 이 축은 hard gate로는 부적합하다.

4. 다음 생성 규칙

4-1. V51 내부 우선순위 재정렬
1) core_base / core_rare22_c1
2) strict_base / strict_rare22_c1
3) lowanchor_base / lowanchor_rare22_c1
4) shocklow_base / shocklow_rare22_c1
5) spring/refire40 보조군

4-2. 다음 라운드 1차 개선 대상
- 8V5_V51P_V002_core_rare22_c1
- 8V5_V51P_V001_core_base
- 8V5_V51P_V012_strict_rare22_c1
- 8V5_V51P_V011_strict_base
- 8V5_V51P_V022_lowanchor_rare22_c1
- 8V5_V51P_V021_lowanchor_base
이 여섯 개가 다음 주력이다.

4-3. 다음 라운드에서 유지할 것
- rare22_c1
- strict
- lowanchor
- core_base
- 제한적 refire40 비교군
- 일부 미세 파라미터 조정

4-4. 다음 라운드에서 낮출 것
- shocklow 우선순위
- quality_hold 다수
- softscore 다수
- hammer_outside 다수
- ema_mid 계열
- noshock14, vol16_quiet 계열
- 과도한 microguard

4-5. 다음 목표
- core_base/core_rare22_c1의 MDD를 6.28~6.31에서 5 아래로 더 내린다.
- strict/lowanchor의 MDD<5 후보군을 116대에서 121.53 이상으로 끌어올린다.
- 새 family 탐색은 하지 않고 V51 내부 국소 최적화에 집중한다.

5. 한 줄 결론
- 8V5는 승격 실패지만, V51 top candidate의 MDD를 실제로 낮춘 의미 있는 라운드다.
- 다음 단계는 core 축의 MDD를 더 낮추고, strict/lowanchor 안전권 후보군의 cd를 더 끌어올리는 것이다.
