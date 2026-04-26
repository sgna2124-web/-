7V4_LONG40_REVIEWED 장단점 추가 기록

이 문서는 7V4_LONG40_REVIEWED 결과를 바탕으로, 7V2~7V3에서 확인된 L09/L07 신규 reversal family를 다음 long 생성 규칙으로 더 구체화하기 위한 addendum이다.

1. 배치 요약
- candidate_cd_win_mdd_fail 1위: 7V4_L09_V09_beartrap_cluster_pressure | final_return_pct 41.1544 | max_return_pct 42.1291 | max_drawdown_pct 11.2133 | cd_value 125.3264 | trades 6863
- candidate_cd_win_mdd_fail 2위: 7V4_L09_V03_beartrap_lowanchor_drive | final_return_pct 39.3617 | max_return_pct 40.1602 | max_drawdown_pct 11.9139 | cd_value 122.7583 | trades 7664
- best under MDD<5: 7V4_L09_V02_beartrap_extreme_synergy | final_return_pct 15.8330 | max_return_pct 16.0180 | max_drawdown_pct 2.5330 | cd_value 112.8990 | trades 730
- next under MDD<5: 7V4_L07_V02_wick_drive_reclaim | final_return_pct 15.6410 | max_return_pct 16.0068 | max_drawdown_pct 3.2136 | cd_value 111.9247 | trades 1443
- 다음 under MDD<5: 7V4_L07_V19_wick_drive_after_pause | final_return_pct 16.1279 | max_return_pct 16.4648 | max_drawdown_pct 4.0259 | cd_value 111.4526 | trades 1327
- 결론: 7V4는 공식 승격은 없었지만, L09 family 안에 기준선보다 높은 cd를 가진 개선 후보가 실제로 존재한다는 점을 고정한 라운드다.

2. 장점

2-1. L09 beartrap family가 clear 1순위다.
- candidate_cd_win_mdd_fail 1위와 2위가 모두 L09다.
- MDD<5 최고도 L09_V02다.
- 즉 L09 family는 현재 long 신규 family 중 가장 강한 upside와 가장 현실적인 승격 가능성을 동시에 가진다.

2-2. L07 wick family는 안정적 2순위다.
- L07_V02, L07_V19, L07_V03이 모두 MDD<5 안에서 cd 110대 전후를 유지했다.
- raw upside는 L09보다 약하지만, 제어가 더 쉬운 편이다.
- 따라서 L07은 L09의 보조 축이자 비교군으로 유지 가치가 높다.

2-3. drive_reclaim, after_pause, extreme_synergy 계열은 재사용 가치가 있다.
- L09_V02, L09_V03, L09_V09와 L07_V02, L07_V19, L07_V03을 보면, 단순 패턴보다 drive/reclaim/quality/after_pause 류가 상대적으로 우수했다.
- 즉 다음 라운드에서 유지할 유망 패턴 태그는 drive, reclaim, extreme_synergy, after_pause다.

3. 단점

3-1. cluster_pressure는 raw cd를 높이지만 MDD 팽창이 크다.
- L09_V09는 candidate_cd_win_mdd_fail로 남을 가치가 있지만, MDD 11.2133이 여전히 너무 높다.
- 즉 cluster_pressure는 core edge를 보여주는 raw 후보이지, 현재 상태로는 승격용 구조가 아니다.

3-2. lowanchor_drive도 비슷한 문제를 가진다.
- L09_V03은 cd가 기준선보다 높지만, MDD가 11.9139로 높다.
- 따라서 lowanchor는 edge source일 수는 있어도, 현 단계에서는 suppression 없이 쓰면 MDD를 같이 끌어올린다.

3-3. ultraselective, closehold, reclaim_stack, volcrush 계열은 edge를 과하게 죽인다.
- L09_V10, L09_V15, L09_V11, L09_V18과 L07_V10, L07_V15, L07_V11, L07_V18을 보면 대부분 trades가 너무 적고 수익 곡선이 얕다.
- 이런 계열은 다음 주력 배치에서 우선순위를 낮춘다.

3-4. prevhigh, shockage_mid, discount_quality, lowrange_quality는 hard gate보다 보조 판단에 가깝다.
- 성과를 결정적으로 끌어올리지 못했고, 일부는 edge를 약화시켰다.
- 따라서 이 조건들은 다음부터 tie-break, score bonus, ranking 요소로만 다룬다.

4. 다음 생성 규칙

4-1. 다음 family 우선순위
1) L09 beartrap family
2) L07 wick family
3) L10 balance family
4) L04 engulf family

4-2. 다음 라운드에 유지할 것
- same-bar raw reversal core는 유지한다.
- recent-fire suppression, same-symbol refractory spacing, shockfresh age는 기본 장치로 둔다.
- reclaim quality, drive quality, after_pause는 재사용 가치가 높다.

4-3. 다음 라운드에서 낮출 것
- cluster_pressure와 lowanchor는 단독 강신호로 두지 말고, firing density를 더 줄일 수 있는 보조 억제 장치와 같이 쓴다.
- ultraselective, closehold, reclaim_stack, volcrush 계열은 주력 확장 우선순위를 낮춘다.
- prevhigh, shockage_mid, discount_quality, lowrange_quality는 hard gate 대신 score/tie-break로 이동한다.

4-4. 개선 우선순위
- 1차 개선 대상: 7V4_L09_V09_beartrap_cluster_pressure
- 2차 개선 대상: 7V4_L09_V03_beartrap_lowanchor_drive
- 3차 비교군: 7V4_L09_V02_beartrap_extreme_synergy, 7V4_L07_V02_wick_drive_reclaim, 7V4_L07_V19_wick_drive_after_pause

5. 한 줄 결론
- 7V4는 공식 승격 실패 라운드지만, L09 family 안에 기준선보다 높은 cd를 가진 개선 후보가 실제로 존재한다는 것을 확정했다.
- 다음 단계는 L09의 high-cd raw 후보 두 개의 MDD를 낮추는 것이다.
