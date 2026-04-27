8V3_LONG100_REVIEWED 장단점 추가 기록

이 문서는 8V3_LONG100_REVIEWED 결과를 바탕으로, 8V1/8V2의 신규 family 실패 이후 다시 L09 beartrap family 60개와 L07 wick family 40개로 회귀한 결과를 다음 생성 규칙으로 남기기 위한 addendum이다.

1. 배치 요약
- batch best: 8V3_L09_V51_microbase_pop | verdict=candidate_cd_win_mdd_fail | final_return_pct 41.5097 | max_return_pct 42.0017 | max_drawdown_pct 6.3144 | cd_value 132.5742 | trades 2277
- next candidate_cd_win_mdd_fail: 8V3_L09_V27_failed_break_pivot | final_return_pct 39.4890 | max_return_pct 40.2473 | max_drawdown_pct 11.4314 | cd_value 123.5435 | trades 7656
- next candidate_cd_win_mdd_fail: 8V3_L09_V09_cluster_pressure | final_return_pct 38.1414 | max_return_pct 38.9188 | max_drawdown_pct 11.3164 | cd_value 122.5087 | trades 6869
- next candidate_cd_win_mdd_fail: 8V3_L09_V28_refire_block | final_return_pct 41.4101 | max_return_pct 42.3732 | max_drawdown_pct 14.0253 | cd_value 121.5769 | trades 6347
- best under MDD<5: 8V3_L09_V41_exhaustion_recover | final_return_pct 19.4175 | max_return_pct 19.7022 | max_drawdown_pct 3.0952 | cd_value 115.7213 | trades 1126
- next under MDD<5: 8V3_L09_V01_shockfresh_quality | final_return_pct 17.7347 | max_return_pct 17.9117 | max_drawdown_pct 4.3807 | cd_value 112.5770 | trades 3045
- next under MDD<5: 8V3_L09_V02_extreme_synergy | final_return_pct 14.9064 | max_return_pct 15.0841 | max_drawdown_pct 2.3521 | cd_value 112.2037 | trades 729
- next under MDD<5 best L07: 8V3_L07_V28_shockwindow_rearm | final_return_pct 16.7009 | max_return_pct 16.8848 | max_drawdown_pct 3.9351 | cd_value 112.1086 | trades 1315
- conclusion: 8V3는 L09/L07 회귀가 맞는 방향이었음을 확인했다. 특히 L09 안에서 candidate_cd_win_mdd_fail가 4개로 늘었고, MDD<5 최고권도 115.7213까지 올라와 7V4보다 진전했다. 다만 아직 공식 기준선 121.5300을 넘는 MDD<5 전략은 없다.

2. 장점

2-1. L09 beartrap family가 더 강해졌다.
- 8V3_L09_V51_microbase_pop은 cd 132.5742까지 올라가 7V4의 candidate 후보보다도 더 높은 raw/cd 잠재력을 보였다.
- 8V3_L09_V27, V09, V28도 모두 candidate_cd_win_mdd_fail로 남았다.
- 즉 L09 family는 더 이상 단순 유망 수준이 아니라, 공식 기준선의 raw edge를 이미 넘어선 축으로 봐야 한다. 현재 과제는 오직 MDD 억제다.

2-2. MDD<5 구간에서도 L09가 개선됐다.
- 8V3_L09_V41_exhaustion_recover는 cd 115.7213으로 이전 L09 최고권 112.8990보다 한 단계 올라왔다.
- shockfresh_quality, extreme_synergy도 여전히 112대 cd를 유지했다.
- 즉 L09 family는 raw 후보뿐 아니라 공식 승격 후보군 자체도 전진했다.

2-3. L07 wick family도 보조 축으로 충분히 유효하다.
- 8V3_L07_V28_shockwindow_rearm, V02_drive_reclaim, V40_trap_relaunch, V27_bodydrive_reclaim, V03_extreme_synergy, V34_hold_then_drive가 모두 MDD<5에서 110~112대 cd를 유지했다.
- 따라서 L07은 계속 비교군이자 안정형 보조 축으로 보관 가치가 높다.

2-4. 8V1/8V2보다 훨씬 낫다.
- 완전 신규 family 150개 실험보다, 결국 검증된 L09/L07 family 안에서 조건을 더 세분화한 쪽이 훨씬 강했다.
- 이는 앞으로의 실험 자원을 broad 신규 family보다 강한 family 심화에 우선 배치해야 한다는 뜻이다.

3. 단점

3-1. L09 top 후보는 여전히 MDD 장벽을 넘지 못한다.
- V51, V27, V09, V28은 모두 기준선 이상 cd를 기록했지만 MDD 6.3~14.0 구간이라 공식 승격이 안 된다.
- 특히 V51은 6.3144까지 낮아져 가장 근접했지만 아직 5% 아래로는 못 들어왔다.

3-2. cluster_pressure와 lowanchor/failed-break류는 raw edge는 강하지만 MDD를 같이 키운다.
- V09, V27, V03은 모두 높은 수익 잠재력을 만들지만, 발화 밀도가 높아질수록 손실도 함께 커진다.
- 즉 이 축은 edge source는 맞지만 그대로 두면 승격용 구조가 아니다.

3-3. 일부 보조 태그는 여전히 edge를 죽인다.
- closehold_retake, volcrush_reclaim, reclaim_stack, shockage_mid, lowrange_quality, ultraselective, open_reclaim류는 대부분 수익을 희석하거나 음수화했다.
- 이 계열은 다음 라운드 주력 확장 우선순위를 낮춘다.

3-4. prevhigh_drive와 relaunch_window는 기대 대비 약했다.
- 8V3_L09_V04_prevhigh_drive, V21_relaunch_window, L07_V21_relaunch_window 등은 핵심 축이 되지 못했다.
- 따라서 prevhigh/relaunch는 메인 트리거보다 보조 조건에 더 가깝다.

4. 다음 생성 규칙

4-1. family 우선순위 재확정
1) L09 beartrap family
2) L07 wick family
3) L10 balance family
4) L04 engulf family
- 8V1/8V2에서 신규 family를 크게 벌려도 엣지가 없었고, 8V3에서 다시 L09/L07로 돌아오자 즉시 성과가 좋아졌다.

4-2. 1차 개선 대상
- 8V3_L09_V51_microbase_pop
- 8V3_L09_V27_failed_break_pivot
- 8V3_L09_V09_cluster_pressure
- 8V3_L09_V28_refire_block
이 네 개는 candidate_cd_win_mdd_fail 우선 대상이다. 특히 V51은 MDD 6.3144로 가장 근접했다.

4-3. MDD<5 승격 후보 보관 대상
- 8V3_L09_V41_exhaustion_recover
- 8V3_L09_V01_shockfresh_quality
- 8V3_L09_V02_extreme_synergy
- 8V3_L07_V28_shockwindow_rearm
- 8V3_L07_V02_drive_reclaim
이 다섯 개는 공식 승격 후보군으로 계속 보관한다.

4-4. 다음 라운드에서 유지할 것
- same-bar raw reversal core는 유지한다.
- recent-fire suppression, same-symbol refractory spacing은 기본 장치로 둔다.
- exhaustion_recover, shockfresh_quality, shockwindow_rearm, trap_relaunch, bodydrive_reclaim 같은 태그는 재사용 가치가 높다.
- microbase_pop은 8V3에서 처음 강하게 뜬 신규 핵심 태그이므로 다음 라운드 최우선 실험 대상이다.

4-5. 다음 라운드에서 낮출 것
- closehold_retake, reclaim_stack, volcrush_reclaim, shockage_mid, lowrange_quality, ultraselective, open_reclaim은 주력 확장 우선순위를 낮춘다.
- prevhigh_drive, relaunch_window는 hard gate보다 보조 score/tie-break로만 다룬다.

5. 한 줄 결론
- 8V3는 공식 승격 실패 라운드지만, 방향은 완전히 맞았다.
- L09/L07 회귀는 성공했고, 특히 L09 안에서 기준선보다 훨씬 높은 cd를 가진 후보가 4개로 늘었다.
- 다음 단계는 새 family 탐색이 아니라, 8V3_L09_V51을 포함한 high-cd 후보들의 MDD를 5% 아래로 끌어내리는 것이다.
