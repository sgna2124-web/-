# LONG_MAIN_RESEARCH_LOG_2026_05_26_A016_SERIES_V17_TO_V20_FINAL

## 목적
롱 메인 신규 탐색 중 v15에서 처음 반응이 나온 selloff_calm_reclaim 계열의 후속 연구(v17~v20)를 최종 기록한다.
다음 대화창에서 A016 계열을 기준선 대체 후보로 오해하거나, 같은 진입 조건 확장/출구 실험을 반복하지 않기 위한 append 로그다.

## 배경
v15 State Migration / Multi-Stage Qualification에서 유일하게 반응한 family는 selloff_calm_reclaim이었다.

v16에서는 selloff_calm_reclaim + failure test 구조로 정제했다.

v16 최고:
- SCRF_A_012
- cd: 66.300264
- max_return_pct: 2.137985
- MDD: 35.087555
- trades: 6504

v16은 v15 대비 MDD와 거래수는 줄고 max_return은 늘었지만, 기준선 후보로 보기에는 MDD가 너무 높았다.

## v17: SCRF_A_012 MDD Compression
파일:
run_long_scrf_a012_mdd_compress_v17_1h.py

결과 폴더:
local_results/long_main/LONG_SCRF_A012_MDD_COMPRESS_V17_1H

최고 후보:
- SCR17_A_016
- family: a012_core_tighten
- cd: 97.319011
- max_return_pct: 0.424831
- MDD: 3.092681
- trades: 395
- win_rate_pct: 38.481

판정:
A016 계열은 매우 낮은 MDD로 압축 가능함을 확인했다.
다만 max_return이 0.42% 수준으로 기준선 대비 성장성이 매우 약했다.

## v18: SCR17_A016 Retest + Local Refinement
파일:
run_long_scr17_a016_retest_refine_v18_1h.py

결과 폴더:
local_results/long_main/LONG_SCR17_A016_RETEST_REFINE_V18_1H

중요 결과:
- SCR18_EXACT_A016
- cd: 97.319011
- max_return_pct: 0.424831
- MDD: 3.092681
- trades: 395

판정:
SCR17_A_016 exact 재현 성공.
우연히 한 번 튄 후보는 아니었다.

v18 상위 후보들은 더 낮은 MDD가 나오긴 했지만 대부분 거래수가 너무 적었다.
예:
- SCR18_B_026: cd 99.372267, max 0.134707, MDD 0.761414, trades 103

실질 후보권:
- SCR18_E_084: cd 97.536821, max 0.421615, MDD 2.872682, trades 367
- SCR18_C_050: cd 97.457483, max 0.496251, MDD 3.023763, trades 391

## v19: SCR18/A016 Trade Count Expansion
파일:
run_long_scr18_tradecount_expand_v19_1h.py

결과 폴더:
local_results/long_main/LONG_SCR18_TRADECOUNT_EXPAND_V19_1H

목적:
A016 계열의 거래수를 600~2000 수준으로 늘릴 수 있는지 확인했다.

최고 후보:
- SCR19_D_056
- family: profit_expand
- cd: 97.042193
- max_return_pct: 0.680313
- MDD: 3.613537
- trades: 431
- win_rate_pct: 34.107

비교:
- v18 exact A016: max 0.424831, MDD 3.092681, trades 395
- v19 최고: max 0.680313, MDD 3.613537, trades 431

판정:
거래수 확장은 사실상 실패.
조건을 완화해도 trades가 600~2000으로 확장되지 않았고, max_return 증가도 제한적이었다.
A016 계열은 구조적으로 희소 진입 전략이다.

## v20: A016 Entry Fixed + Exit Structure Test
파일:
run_long_a016_exit_structure_v20_1h.py

결과 폴더:
local_results/long_main/LONG_A016_EXIT_STRUCTURE_V20_1H

목적:
A016 진입 조건은 고정하고 출구 구조만 실험했다.
테스트한 출구:
- RR 확장형
- 짧은 손절 + 긴 익절형
- hold 확장형
- fail exit 완화/제거형
- wide stop + big TP

금지 유지:
- trailing stop 없음
- break-even 없음
- dynamic TP 없음
- 진입 후 TP/SL 수정 없음

v20 최고 후보:
- A016_TS_028
- family: tight_stop_big_rr
- cd: 97.357118
- max_return_pct: 0.931102
- MDD: 3.541014
- trades: 431
- win_rate_pct: 30.626

max_return 최고권:
- A016_FAIL_069: max 1.197135, MDD 4.216342, trades 431
- A016_NOFAIL_089: max 1.289704, MDD 4.996495, trades 431

판정:
출구 구조 변경으로 max_return은 0.30~0.42 수준에서 1.29까지 개선됐다.
그러나 사전에 정한 기준인 max_return 3~5%에는 도달하지 못했다.
거래수도 431로 거의 증가하지 않았다.

## 최종 결론
A016 계열은 다음 특성을 가진다.

장점:
- 저MDD 특성은 재현됨
- exact retest 성공
- MDD 3~5% 이하 후보 다수 존재
- 출구 구조를 바꾸면 max_return은 소폭 개선 가능

한계:
- 거래수가 구조적으로 적다
- 진입 조건 완화로도 거래수 확장이 거의 되지 않는다
- max_return이 기준선 대비 너무 작다
- 출구 구조 실험 후에도 max_return 3~5% 기준에 도달하지 못했다
- 기준선 대체 후보로 보기 어렵다

## 최종 판정
A016 계열은 기준선 대체 후보에서 제외한다.

다만 완전 무효 전략은 아니다.
저MDD 보조 전략 또는 포트폴리오 보조축으로 참고할 수 있으나, 현재 롱 메인 기준선 개선의 주력 후보는 아니다.

## 반복 금지
다음은 반복하지 않는다.

1. A016 진입 조건 추가 완화
2. A016 진입 조건 주변 grid 반복
3. selloff_calm_reclaim + failure test 단독 확장
4. A016 fixed entry + RR/hold/stop/fail exit 단순 출구 실험
5. A016을 기준선 대체 후보로 재검토

## 다음 방향
다음 탐색은 A016 계열을 떠나 기준선 철학에 가까운 구조로 돌아간다.

핵심 방향:
- 희귀 패턴이 아니라 더 자주 발생하는 기대값 우위
- 낮은 MDD와 포트폴리오 효과 동시 추구
- 거래수와 성장성이 기준선과 비교 가능한 수준이어야 함

A016의 교훈:
- 단순히 MDD가 낮다는 것만으로는 좋은 기준선이 아니다.
- 기준선 대체 후보가 되려면 낮은 MDD뿐 아니라 충분한 거래수와 성장성이 필요하다.
