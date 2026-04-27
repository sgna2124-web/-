새 대화창의 어시스턴트 행동 순서

1. 가장 먼저 CORE_SUMMARY/00_START_HERE.md 를 읽는다.
2. 그 다음 CORE_SUMMARY/03_CURRENT_BASELINES.md 를 읽어 현재 공식 기준선을 확인한다.
3. 그 다음 CORE_SUMMARY/06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md 를 읽어 현재 백테스트 고정 환경을 확인한다.
4. 그 다음 CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 읽어 현재 유효 결과만 파악한다.
5. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 를 읽어 최근 전략군의 구조적 장단점을 파악한다.
6. 최신 addendum인 CORE_SUMMARY/24_8V4_LONG400_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/25_8V5_LONG300_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/26_8V6_TOP3_300_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/29_8V7_AB_BEST_200_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/30_8V8_LONG_DUAL_BEST_200_UNTRIED_ADDENDUM.md 를 읽는다.
7. CORE_SUMMARY/27_NEXT_STEP_AFTER_8V6.md 는 과거 참고로만 읽고, 최신 판단은 30번 addendum을 우선한다.
8. CORE_SUMMARY/28_BASELINE_AND_IMPROVEMENT_CANDIDATE_RULES.md 를 읽고 기준선 및 개선 후보 선정 규칙을 확인한다.
9. 이후 사용자 요청에 맞춰 전략 설계, 결과 해석, 문서 갱신을 진행한다.

새 대화창에서 반드시 확인할 현재 전제
공식 판정은 cd_value와 MDD 기준이다.
현재 프로젝트의 공식 cd_value는 사용자가 정의한 자산 기준 계산식으로 고정한다.

cd_value = 100 * (1 - (abs(max_drawdown_pct) / 100)) * (1 + (max_return_pct / 100))

해석:
1) 기초 자산 100에 MDD를 먼저 적용한다.
2) MDD 적용 후 남은 자산에 max_return_pct를 적용한다.
3) final_return_pct는 공식 cd_value 계산에 사용하지 않는다.
4) max_return_pct / max_drawdown_pct 방식은 폐기된 비공식 ratio이며 앞으로 공식 cd_value로 쓰지 않는다.

현재 long 공식 기준선 6V2_L01_doubleflush_core의 공식 cd_value는 121.7490이다.
계산: 100 * (1 - 0.017512) * (1 + 0.239191) = 121.7490
자산 진입 비중은 1%다.
수수료는 0.04%다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
결과 요약에는 max_return_pct가 반드시 포함되어야 한다.

기준선 및 개선 후보 선정 규칙
공식 기준선은 MDD 5% 미만 전략 중 공식 cd_value 1위다.
개선 후보는 매 배치마다 최대 2개를 뽑는다.
후보 A는 MDD 5% 미만 중 공식 cd_value 1위 전략이다.
후보 B는 MDD와 관계없이 전체 공식 cd_value 1위 전략이다.
후보 A와 후보 B가 같으면 중복 후보로 기록한다.
MDD가 5%를 넘더라도 전체 공식 cd_value 1위라면 다음 개선 후보로 올린다.
official_cd_value가 현재 공식 기준선보다 높고 MDD만 초과한 전략은 candidate_cd_win_mdd_fail로 강하게 표시한다.

V2 실험군 처리 원칙
V2 실험군은 환경 전제 오류가 있었으므로 실패 전략으로 해석하지 않는다.
4V2R1을 제외한 V2 전략과 결과는 제거되었다.
새 대화창의 어시스턴트는 삭제된 V2 실험군을 비교 기준이나 실패 사례로 인용하면 안 된다.

사용자와 어시스턴트의 역할
사용자는 로컬 백테스트를 실행하고 결과와 코드를 저장소에 올린다.
어시스턴트는 그 결과를 분석하고, 결과 카탈로그와 통합 요약을 갱신하며, 다음 전략을 제안한다.

결과 해석 전 점검 체크
자산 1% 진입이 반영되었는가
수수료 0.04%가 반영되었는가
FAST 예비검사가 개입되지 않았는가
결과 파일에 max_return_pct가 포함되었는가
공식 비교가 전체 종목 풀 백테스트 기준인가
거래 수가 0이거나 지나치게 적은 전략을 숫자만 보고 승격 후보로 착각하지 않았는가
cd_value가 사용자 정의 공식인 100 * (1 - abs(MDD)/100) * (1 + max_return_pct/100)로 계산되었는가
max_return_pct / max_drawdown_pct 비공식 ratio를 공식 cd_value로 착각하지 않았는가

반드시 해야 되는 일 목록
1. 사용자가 결과를 저장소에 올렸다면 local_results 또는 해당 결과 폴더를 먼저 확인한다.
2. 결과를 기존 공식 long-only / short-only 기준선과 비교한다.
3. MDD 5% 미만 중 official_cd_value 1위와 MDD 관계없는 전체 official_cd_value 1위를 각각 확인한다.
4. 두 후보가 같으면 중복 후보로 기록한다.
5. 단순 수치 비교로 끝내지 말고, 왜 성과가 나왔는지 장점과 단점을 함께 정리한다.
6. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
7. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 또는 별도 addendum을 갱신한다.
8. 승격이 발생하면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 같이 갱신한다.
9. 지표 정의 충돌이 발견되면 현재 공식 정의인 사용자 정의 cd_value를 기준으로 다른 문서를 정정한다.
10. 결과를 확인만 하고 문서 업데이트를 빼먹지 않는다.
11. 각 신규 배치 결과를 반영할 때, 배치 내 최고 후보를 max_return_pct, max_drawdown_pct, official_cd_value 기준으로 명시한다.
12. 전 전략이 탈락한 배치라도 과다거래, 방향 필터 부족, 진입 지연, 추세 위치 오류, edge 희석 같은 구조적 실패 원인을 문장으로 남긴다.
13. 압축 사다리, midband tag, wick accumulation처럼 거래 수가 비정상적으로 치솟는 구조를 발견하면, 재사용 금지 또는 추가 방향 필터 필요 여부를 명시한다.
14. 다음 전략을 제안하기 전에 방금 갱신한 장단점 기록을 다시 읽고, 그 항목을 실제 생성 규칙으로 반영한다.
15. 새 전략을 설명할 때는 최근 장단점 문서의 어떤 항목을 반영했는지 근거를 함께 적는다.
16. MDD 초과 전략은 공식 기준선으로 승격하지 않는다. 다만 전체 official_cd_value 1위라면 개선 후보로 기록한다.
17. 0트레이드 전략은 구조 검증 실패로 간주하고 별도 표시한다.

최근 상태 인식
현재 공식 long 기준선은 6V2_L01_doubleflush_core다.
official_cd_value는 121.7490이다.
현재 공식 short 기준선은 short_beh_dd_brake다.
8V4와 8V5를 거치며 V51 microbase_pop 계열이 clear 최우선 long 코어가 되었다.
8V5의 핵심 후보는 다음과 같다.
- 8V5_V51P_V002_core_rare22_c1 | max_return_pct 42.1517 | max_drawdown_pct 6.3109 | official_cd_value 133.1863 | trades 2277
- 8V5_V51P_V001_core_base | max_return_pct 41.4900 | max_drawdown_pct 6.2801 | official_cd_value 132.6036 | trades 2277
- 8V5_V51P_V012_strict_rare22_c1 | max_return_pct 19.7596 | max_drawdown_pct 2.7359 | official_cd_value 116.4858 | trades 1040
8V6은 8V5 상위 3개를 각 100개씩 개선했으나 no_promotion이다.
- 8V6 best: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | max_return_pct 5.2510 | max_drawdown_pct 2.1312 | official_cd_value 103.0070 | trades 652
8V6의 후보 A와 후보 B는 모두 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 이다.
8V6의 핵심 학습은 MDD 압축은 가능하지만, 전단 필터로 진입을 줄이면 V51 edge가 먼저 죽는다는 점이다.
8V7은 8V6 후보를 200개 개선했으나 no_promotion이다.
- 8V7 best: 8V7_AB_BEST_I070_post_loss_brake_plb20 | max_return_pct 1.3290 | max_drawdown_pct 0.2122 | official_cd_value 101.1140 | trades 93
8V7의 후보 A와 후보 B는 모두 8V7_AB_BEST_I070_post_loss_brake_plb20 이다.
8V7의 핵심 학습은 post_loss_brake와 soft_safe_mix가 MDD 압축 도구로는 유효하지만, 이미 희소화된 8V6 후보 위에 얹으면 edge가 완전히 죽는다는 점이다.
8V8은 저장소 내 long 전략 중 MDD 5% 미만 cd 1위와 MDD 무관 cd 1위를 각각 100개씩 개선했으나 no_promotion이다.
- 8V8 best: 8V8_RAWV51_I080_raw_official_conversion_r080 | parent 8V4_V51_V002_core_rare22_c1 | max_return_pct 9.6311 | max_drawdown_pct 3.5251 | official_cd_value 105.766560 | trades 1027
8V8의 후보 A와 후보 B는 모두 8V8_RAWV51_I080_raw_official_conversion_r080 이다.
8V8의 핵심 학습은 V51 raw를 MDD 5% 미만으로 변환하는 것은 가능하지만, hard conversion은 max_return_pct를 10% 미만으로 낮춰 기준선 초과 가능성을 죽인다는 점이다.

다음 우선순위
1. V51 core_base / core_rare22_c1의 edge 보존형 MDD 압축
2. V51 strict_base / strict_rare22_c1 safe branch 복원
3. V51 lowanchor_base / lowanchor_rare22_c1 safe branch 복원
4. V51 shocklow_base / shocklow_rare22_c1 보조 커버 조건화
5. V28 refire_block family
6. V09 cluster/shocklow family
7. V27 failed_break_pivot family
8. L07 wick family

다음 전략 설계 방향
새로운 family 탐색보다 V51 심화가 우선이다.
8V7 top 전략이나 8V8 top 전략을 직접 부모로 쓰지 않는다.
목표는 8V5 V51 core_base/core_rare22_c1의 trades를 최소 1500 이상, 가능하면 2000 내외로 최대한 유지하면서 MDD를 6.28~6.31에서 4.9대로 낮추는 것이다.
8V6처럼 500~700 trades까지 잘라내거나 8V7처럼 100 trades 안팎으로 잘라내는 방식은 피한다.
8V8처럼 1000 trades 수준까지는 버틸 수 있으나 max_return_pct가 10% 아래로 내려가는 hard conversion은 피한다.
전단 entry filter보다 사후 drawdown brake, 손실 군집 회피, 변동성 폭발 직후 일시 회피, exit/hold/stop 재조정을 우선한다.
strict/lowanchor는 safe branch 핵심 축이지만 전면 필터가 아니라 부분 브레이크로 사용하는 것이 우선이다.
shocklow는 단독 부모가 아니라 위험 구간 보조 커버로 사용한다.
post_loss_brake, soft_safe_mix, raw_official_conversion은 유효성이 확인됐지만 hard filter가 아니라 부분 모듈로만 이식한다.

환경 오류 발생 시 처리
환경 오류가 확인되면 그 실험군은 invalid_env로 처리한다.
invalid_env 실험은 보존형 실패 기록이 아니라 제거 대상이다.