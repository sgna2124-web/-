8V4_LONG400_REVIEWED 장단점 추가 기록

이 문서는 8V4_LONG400_REVIEWED 결과를 바탕으로, 8V3에서 추린 L09 핵심 4개(V51, V27, V09, V28)를 대규모로 파생한 결과를 다음 생성 규칙으로 남기기 위한 addendum이다.

1. 배치 요약
- batch best candidate_cd_win_mdd_fail: 8V4_V51_V002_core_rare22_c1 | final_return_pct 43.6673 | max_return_pct 44.2664 | max_drawdown_pct 6.7587 | cd_value 133.9572 | trades 2276
- next: 8V4_V51_V001_core_base | final_return_pct 43.2929 | max_return_pct 43.8091 | max_drawdown_pct 6.7547 | cd_value 133.6139 | trades 2277
- next: 8V4_V51_V032_shocklow_rare22_c1 | final_return_pct 42.0892 | max_return_pct 42.6508 | max_drawdown_pct 6.7352 | cd_value 132.5192 | trades 2275
- next: 8V4_V51_V031_shocklow_base | final_return_pct 41.7279 | max_return_pct 42.2024 | max_drawdown_pct 6.7353 | cd_value 132.1821 | trades 2276
- strongest V28 candidate: 8V4_V28_V001_core_base | final_return_pct 41.7051 | max_return_pct 42.4223 | max_drawdown_pct 10.2193 | cd_value 127.2238 | trades 6355
- strongest V09 candidate: 8V4_V09_V031_shocklow_base | final_return_pct 38.2949 | max_return_pct 39.0677 | max_drawdown_pct 10.9209 | cd_value 123.1919 | trades 6160
- best under MDD<5 overall: 8V4_V51_V022_lowanchor_rare22_c1 | final_return_pct 21.2903 | max_return_pct 21.5445 | max_drawdown_pct 3.0752 | cd_value 117.5603 | trades 1040
- next under MDD<5: 8V4_V51_V021_lowanchor_base | final_return_pct 20.9035 | max_return_pct 21.1577 | max_drawdown_pct 3.1165 | cd_value 117.1355 | trades 1040
- next under MDD<5: 8V4_V51_V012_strict_rare22_c1 | final_return_pct 20.5903 | max_return_pct 20.8352 | max_drawdown_pct 2.9942 | cd_value 116.9796 | trades 1040
- conclusion: 8V4는 공식 승격은 없었지만, V51 계열이 분명한 최우선 코어로 부상했다. raw/cd는 8V3보다 더 강해졌고, MDD<5 구간의 상위권도 116~117대 cd까지 올라왔다. 다음 단계는 V51의 MDD를 5 아래로 내리는 데 집중하는 것이다.

2. 장점

2-1. V51이 clear #1 코어다.
- top 4가 모두 V51이고, cd는 132~134대에 도달했다.
- 특히 V51 계열은 trades가 약 2275 수준으로 V27/V28/V09보다 낮으면서도 더 높은 수익 잠재력을 유지했다.
- 즉 V51은 현재 가장 강한 raw edge와 상대적으로 더 낮은 firing density를 동시에 가진다.

2-2. V51은 MDD<5 구간에서도 가장 강하다.
- V51_V022, V021, V012, V011이 모두 cd 116~117대까지 올라왔다.
- 이는 단지 raw candidate가 강한 것이 아니라, 승격권에 가까운 공식 후보군도 V51이 제일 앞선다는 뜻이다.

2-3. rare22_c1, strict, lowanchor 계열이 V51에서 잘 작동했다.
- core/ shocklow 계열에서는 rare22_c1이 소폭 개선을 주었고, lowanchor와 strict 계열은 MDD<5 구간의 최상단을 형성했다.
- 따라서 V51에서는 rare22_c1, lowanchor, strict가 재사용 가치가 높다.

2-4. V27/V28/V09는 비교군으로는 여전히 의미가 있다.
- V28 core_base/core_rare22_c1/core_microguard는 여전히 candidate_cd_win_mdd_fail권이다.
- V09 shocklow_base도 cd 123.1919로 강하다.
- 다만 현재는 V51보다 후순위다.

3. 단점

3-1. V51의 문제는 이제 사실상 MDD 하나다.
- top V51들은 max_drawdown_pct 6.73~6.76 구간에 몰려 있다.
- 즉 수익 잠재력과 cd는 충분히 넘었고, 다음 단계는 firing density 또는 손실 구간 제어로 MDD를 1~2포인트만 더 내리는 문제로 압축된다.

3-2. V28과 V09는 여전히 MDD가 높다.
- V28 core_base는 cd 127.2238이지만 MDD 10.2193이다.
- V09 shocklow_base는 cd 123.1919지만 MDD 10.9209다.
- 즉 V28/V09는 raw edge는 있지만, 현재 시점에서는 V51보다 승격 가능성이 낮다.

3-3. softscore/quality_hold/microguard 다수는 엣지를 희석했다.
- quality_hold 계열, 일부 softscore, microguard 다수는 trades는 줄이지만 수익도 함께 줄어 100~105대 cd 수준으로 내려갔다.
- 즉 억제 장치를 많이 붙일수록 좋은 것이 아니라, edge source를 너무 죽이지 않는 최소 억제가 중요하다.

3-4. ema_mid, prevhigh, vol18 일부는 과도하게 죽는다.
- 상단 일부를 제외하면 ema_mid, prevhigh, vol18 다수 파생은 trades가 1~20 수준 혹은 수익이 지나치게 얕았다.
- 따라서 이런 조건은 hard gate보다 보조 score/tie-break 쪽이 맞다.

4. 다음 생성 규칙

4-1. 최우선 코어 전환
- 이제 L09 family 안에서도 V51을 명확한 최우선 코어로 본다.
- 우선순위는 다음과 같이 재정렬한다.
  1) V51 microbase_pop family
  2) V28 refire_block family
  3) V09 cluster/shocklow family
  4) V27 failed_break_pivot family

4-2. 다음 라운드 1차 개선 대상
- 8V4_V51_V002_core_rare22_c1
- 8V4_V51_V001_core_base
- 8V4_V51_V032_shocklow_rare22_c1
- 8V4_V51_V031_shocklow_base
- 8V4_V51_V022_lowanchor_rare22_c1
- 8V4_V51_V021_lowanchor_base
이 여섯 개가 다음 주력이다.

4-3. 다음 라운드에서 유지할 것
- rare22_c1
- lowanchor
- strict
- shocklow
- core base
이 다섯 태그는 V51 안에서 재사용 가치가 높다.

4-4. 다음 라운드에서 낮출 것
- quality_hold 다수
- 과도한 microguard
- ema_mid 계열
- prevhigh 다수
- vol18 다수
이들은 주력 확장 우선순위를 낮춘다.

4-5. 다음 목표
- V51 상위 후보의 MDD를 6.7대에서 5 아래로 내린다.
- 공식 MDD<5 최고권도 117대에서 121.53 이상으로 끌어올린다.
- 새 family 탐색은 중단하고, V51 중심 국소 최적화에 집중한다.

5. 한 줄 결론
- 8V4는 승격 실패지만, 현재까지 가장 중요한 전진이다.
- V51은 이미 기준선보다 훨씬 높은 cd를 만들었고, 이제 남은 문제는 MDD 1~2포인트를 더 내리는 것이다.
