이 파일은 새 대화창의 첫 진입점이다.
새 대화창의 어시스턴트는 다른 요약 문서보다 먼저 이 파일을 읽고 현재 프로젝트 상태를 복원한다.

CORE_SUMMARY 읽기 순서
새 대화창은 CORE_SUMMARY 폴더 안의 .md 문서를 파일명 숫자 기준으로 00번부터 끝까지 차례대로 1회 읽는다.
특정 문서로 먼저 점프하지 않는다.
00_START_HERE를 읽은 뒤에는 01, 02, 03 순서로 계속 읽고, 38번 문서는 순서가 왔을 때 읽는다.
동일 파일은 한 세션에서 한 번만 읽는다.
최신 addendum은 전체 순회가 끝난 뒤 현재 판단 보정용으로만 다시 확인한다.
신규 백테스트 개선안은 TP 기대값이 0.3% 이상일 때만 진입해야 하며, 코드상 min_expected_tp >= 0.003 또는 동등한 필터를 반드시 포함한다.

현재 프로젝트 목표
코인/주식 차트 전략 중 MDD 5% 미만 전략을 우선 후보로 보고, 그중 공식 cd_value가 가장 높은 전략을 찾는다.
롱 전용 전략 1위와 숏 전용 전략 1위를 별도 기준으로 유지하며, 앞으로의 모든 백테스트 결과는 이 기준과 비교한다.

성과 판단 기준
공식 판단 기준은 cd_value와 max_drawdown_pct(MDD)다.
max_return_pct는 단독 판단 지표는 아니지만 cd_value 산출에 반드시 포함된다.
final_return_pct는 참고 지표로 기록하되, 공식 우선순위는 MDD 5% 미만 통과 여부 -> 공식 cd_value -> max_return_pct/trades/재현성 보조 판단이다.

cd_value 공식 정의
현재 프로젝트의 공식 cd_value는 사용자가 정의한 자산 기준 계산식으로 고정한다.

cd_value = (base_asset * (1 - (abs(max_drawdown_pct) / 100))) * (1 + (max_return_pct / 100))

기본 base_asset은 100으로 둔다.
따라서 실무 계산식은 다음과 같다.

cd_value = 100 * (1 - (abs(max_drawdown_pct) / 100)) * (1 + (max_return_pct / 100))

해석:
1) 기초 자산 100에 MDD를 먼저 적용한다.
2) MDD 적용 후 남은 자산에 max_return_pct를 적용한다.
3) final_return_pct는 공식 cd_value 계산에 사용하지 않는다.
4) max_return_pct / max_drawdown_pct 방식은 폐기된 비공식 ratio이며 앞으로 공식 cd_value로 쓰지 않는다.
5) 기존 문서의 official_ratio, current_cd_value_ratio, legacy_equity_cd_value 표기는 혼동 가능성이 있으므로 신규 결과 해석에서는 official_cd_value 또는 cd_value만 사용한다.

예시:
base_asset = 100, max_drawdown_pct = 10, max_return_pct = 10이면
cd_value = 100 * (1 - 0.10) * (1 + 0.10) = 99

고정 백테스트 환경
자산 진입 비중은 1%다.
수수료는 0.04%다.
공식 판정은 전체 종목 풀 백테스트 기준이다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
백테스트 결과 요약에는 max_return_pct를 반드시 포함한다.
신규 개선안은 TP 기대값 0.3% 이상 진입 조건을 반드시 포함한다.

무효 실험 처리 규칙
정상 환경에서 실패한 전략은 기록으로 남긴다.
하지만 환경 설정 오류, 엔진 설정 오류, 자산 비중 오류, 수수료 오류, 비교 불가능한 실험은 invalid_env로 간주한다.
invalid_env 실험은 실패 전략 기록으로 보존하지 않고, 비교 체계 오염 방지를 위해 결과와 카탈로그에서 제거한다.

현재 방향성 요약
현재 공식 long 기준선은 6V2_L01_doubleflush_core 이다.
공식 cd_value는 121.7490이다.
계산: 100 * (1 - 0.017512) * (1 + 0.239191) = 121.7490

7V1~7V4 구간에서는 신규 reversal family 실험을 통해 L09 beartrap family와 L07 wick family가 가장 유망한 long 신규 축으로 확인되었다.
8V1과 8V2에서 completely new family를 대규모로 시도했지만 새로운 엣지는 확인되지 않았다. 따라서 long 주력 개발은 다시 L09/L07 중심으로 회귀했다.
8V3에서는 이 회귀가 성공했고, L09 안에서 candidate_cd_win_mdd_fail 풀이 4개로 늘어났다. 특히 8V3_L09_V51_microbase_pop은 max_return_pct 42.0017, max_drawdown_pct 6.3144까지 올라와 가장 근접한 고잠재력 후보가 되었다.
8V4에서는 이 방향이 더 강화되었다. V51 microbase_pop 계열이 clear 최우선 코어로 부상했다.
8V5에서는 V51만 300개를 세 그룹으로 확장했다.
- batch best candidate_cd_win_mdd_fail: 8V5_V51P_V002_core_rare22_c1 | final_return_pct 41.6763 | max_return_pct 42.1517 | max_drawdown_pct 6.3109 | official_cd_value 133.1863 | trades 2277
- next: 8V5_V51P_V001_core_base | final_return_pct 41.0096 | max_return_pct 41.4900 | max_drawdown_pct 6.2801 | official_cd_value 132.6036 | trades 2277
- best under MDD<5 overall: 8V5_V51P_V012_strict_rare22_c1 | final_return_pct 19.5333 | max_return_pct 19.7596 | max_drawdown_pct 2.7359 | official_cd_value 116.4858 | trades 1040
이 결과는 두 가지를 의미한다.
1) V51 top candidate의 MDD는 8V4의 6.75대에서 8V5의 6.28~6.31대로 실제 개선되었다.
2) 반면 safe branch의 최고 official_cd_value는 공식 long 기준선 121.7490을 넘지 못했다.

8V6에서는 8V5 상위 3개 전략을 각 100개씩 개선했다.
- batch best: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V001_core_base | final_return_pct 3.0599 | max_return_pct 5.2510 | max_drawdown_pct 2.1312 | official_cd_value 103.0070 | trades 652
- next: 8V6_P2_CORE_BASE_I050_mdd_compress_mdd15 | parent 8V5_V51P_V001_core_base | final_return_pct 2.2944 | max_return_pct 3.7822 | max_drawdown_pct 1.5658 | official_cd_value 102.1572 | trades 501
- next: 8V6_P3_SHOCKLOW_RARE22_C1_I088_hybrid_cover_hyb18 | parent 8V5_V51P_V032_shocklow_rare22_c1 | final_return_pct 2.7986 | max_return_pct 5.1129 | max_drawdown_pct 2.2018 | official_cd_value 102.7978 | trades 666
8V6 판정은 no_promotion이다.
공식 MDD 조건은 통과했지만, max_return_pct가 8V5의 41~42%대에서 3~5%대로 줄어 V51 raw edge가 과도하게 손실되었다.
즉 현재는 진입을 더 줄이는 방향이 아니라, V51 core_base/core_rare22_c1의 진입 밀도를 유지하면서 사후 브레이크, 손실 군집 회피, exit/hold/stop 재조정으로 MDD를 5 아래로 내려야 한다.

8V7은 8V6 후보를 200개 개선했으나 no_promotion이다.
- batch best: 8V7_AB_BEST_I070_post_loss_brake_plb20 | final_return_pct 1.1655 | max_return_pct 1.3290 | max_drawdown_pct 0.2122 | official_cd_value 101.1140 | trades 93
8V7의 핵심 학습은 post_loss_brake와 soft_safe_mix가 MDD 압축 도구로는 유효하지만, 이미 희소화된 8V6 후보 위에 얹으면 edge가 완전히 죽는다는 점이다.

현재 우선순위는 다음과 같이 재정렬한다.
1) V51 core_base / core_rare22_c1 edge 보존형 MDD 압축
2) V51 strict_base / strict_rare22_c1 safe branch 복원
3) V51 lowanchor_base / lowanchor_rare22_c1 safe branch 복원
4) V51 shocklow_base / shocklow_rare22_c1 보조 커버 조건화
5) V28 refire_block family
6) V09 cluster/shocklow family
7) V27 failed_break_pivot family
8) L07 wick family

장단점 기록 사용 규칙
CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 는 단순 보관 문서가 아니다.
새 전략을 설계하기 전에 반드시 이 문서를 읽고, 최근 실패 패턴과 살아남은 구조를 다음 전략 생성 규칙에 반영해야 한다.
즉 장단점 기록은 사후 회고가 아니라 사전 생성 규칙이다.
같은 실패 패턴의 재생산을 막고, 유망 구조만 조합적으로 재사용하는 것이 목적이다.
최근 라운드의 세부 보정 사항은 최신 addendum을 함께 본다.
특히 8V7 이후에는 CORE_SUMMARY/29_8V7_AB_BEST_200_STRENGTHS_WEAKNESSES_ADDENDUM.md 와 CORE_SUMMARY/28_BASELINE_AND_IMPROVEMENT_CANDIDATE_RULES.md 를 반드시 본다.

결과 해석 보정 규칙
거래 수가 0인 전략, 극단적으로 적은 거래만 발생한 전략, 혹은 구조적으로 재현성이 낮은 전략은 cd_value 숫자가 높아 보여도 승격 후보로 보지 않는다.
MDD 초과 전략은 공식 기준선으로 승격하지 않는다.
다만 MDD가 5%를 넘더라도 공식 cd_value가 배치 내 전체 1위라면 raw_cd_candidate_any_mdd로 기록하고 다음 개선 시도의 후보로 보관한다.
공식 cd_value가 현 공식 기준선보다 높고 MDD만 초과하면 candidate_cd_win_mdd_fail로 강하게 표시한다.

역할 분담
사용자는 로컬 컴퓨터에서 백테스트를 실행하고, 전략 코드와 결과 요약 파일을 저장소에 업로드한다.
어시스턴트는 업로드된 결과를 검토하고, 통합 요약/결과 카탈로그/장단점 문서/다음 단계 매뉴얼을 갱신하며, 다음 실험 전략을 설계한다.

결과 업로드 후 반드시 할 일
1. 업로드된 local_results 또는 결과 폴더를 확인한다.
2. 공식 long-only / short-only 기준선과 비교한다.
3. MDD 5% 미만 중 official_cd_value 1위와 MDD 관계없는 전체 official_cd_value 1위를 각각 확인한다.
4. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
5. 장단점 문서를 갱신한다.
6. 승격이면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 갱신한다.
7. 결과만 보고 끝내지 말고, 왜 그런 결과가 나왔는지 장점과 단점을 남긴다.
8. 다음 전략 설계 전에 방금 추가한 장단점 기록을 다시 읽고, 생성 규칙으로 반영한다.
9. 신규 개선안의 진입 조건에 TP 기대값 0.3% 이상 필터가 들어갔는지 확인한다.

다음으로 읽을 문서
CORE_SUMMARY 폴더 안의 .md 파일을 파일명 숫자 기준으로 00번부터 끝까지 차례대로 읽는다.
이미 읽은 파일은 다시 읽지 않는다.
특정 문서로 점프하지 않는다.
파일명이 같은 번호로 시작하는 경우에는 파일명 전체의 오름차순으로 읽는다.
전체 순회를 마친 뒤 최신 번호 addendum만 현재 판단 보정용으로 다시 확인한다.
