새 대화창의 어시스턴트 행동 순서

1. 가장 먼저 CORE_SUMMARY/00_START_HERE.md 를 읽는다.
2. 그 다음 CORE_SUMMARY/03_CURRENT_BASELINES.md 를 읽어 현재 공식 기준선을 확인한다.
3. 그 다음 CORE_SUMMARY/06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md 를 읽어 현재 백테스트 고정 환경을 확인한다.
4. 그 다음 CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 읽어 현재 유효 결과만 파악한다.
5. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 를 읽어 최근 전략군의 구조적 장단점을 파악한다.
6. 최신 addendum인 CORE_SUMMARY/24_8V4_LONG400_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/25_8V5_LONG300_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/26_8V6_TOP3_300_STRENGTHS_WEAKNESSES_ADDENDUM.md 를 읽는다.
7. CORE_SUMMARY/27_NEXT_STEP_AFTER_8V6.md 를 읽고 다음 실험 방향을 확인한다.
8. 이후 사용자 요청에 맞춰 전략 설계, 결과 해석, 문서 갱신을 진행한다.

새 대화창에서 반드시 확인할 현재 전제
공식 판정은 cd_value와 MDD 기준이다.
cd_value는 max_return_pct / max_drawdown_pct 기준으로 계산한다.
기존 문서의 121.5300, 132.7352 같은 값은 legacy_equity_cd_value 성격이 섞여 있을 수 있다.
공식 ratio 비교는 반드시 max_return_pct / max_drawdown_pct로 재계산한다.
현재 long 공식 기준선 6V2_L01_doubleflush_core의 공식 ratio는 23.9191 / 1.7512 = 13.6587이다.
자산 진입 비중은 1%다.
수수료는 0.04%다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
결과 요약에는 max_return_pct가 반드시 포함되어야 한다.

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
cd_value가 max_return_pct / max_drawdown_pct로 해석되었는가
legacy_equity_cd_value와 공식 ratio를 혼동하지 않았는가

반드시 해야 되는 일 목록
1. 사용자가 결과를 저장소에 올렸다면 local_results 또는 해당 결과 폴더를 먼저 확인한다.
2. 결과를 기존 공식 long-only / short-only 기준선과 비교한다.
3. 단순 수치 비교로 끝내지 말고, 왜 성과가 나왔는지 장점과 단점을 함께 정리한다.
4. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
5. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 또는 별도 addendum을 갱신한다.
6. 승격이 발생하면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 같이 갱신한다.
7. 지표 정의 충돌이 발견되면 현재 공식 정의인 cd_value = max_return_pct / max_drawdown_pct를 기준으로 다른 문서를 정정한다.
8. 결과를 확인만 하고 문서 업데이트를 빼먹지 않는다.
9. 각 신규 배치 결과를 반영할 때, 배치 내 최고 후보를 max_return_pct, max_drawdown_pct, official_ratio 기준으로 명시한다.
10. 전 전략이 탈락한 배치라도 과다거래, 방향 필터 부족, 진입 지연, 추세 위치 오류, edge 희석 같은 구조적 실패 원인을 문장으로 남긴다.
11. 압축 사다리, midband tag, wick accumulation처럼 거래 수가 비정상적으로 치솟는 구조를 발견하면, 재사용 금지 또는 추가 방향 필터 필요 여부를 명시한다.
12. 다음 전략을 제안하기 전에 방금 갱신한 장단점 기록을 다시 읽고, 그 항목을 실제 생성 규칙으로 반영한다.
13. 새 전략을 설명할 때는 최근 장단점 문서의 어떤 항목을 반영했는지 근거를 함께 적는다.
14. MDD 초과 전략은 아이디어 보관 대상일 수는 있어도 공식 후보로 승격하지 않는다.
15. 0트레이드 전략은 구조 검증 실패로 간주하고 별도 표시한다.

최근 상태 인식
현재 공식 long 기준선은 6V2_L01_doubleflush_core다.
공식 ratio는 13.6587이다.
현재 공식 short 기준선은 short_beh_dd_brake다.
8V4와 8V5를 거치며 V51 microbase_pop 계열이 clear 최우선 long 코어가 되었다.
8V5의 핵심 후보는 다음과 같다.
- 8V5_V51P_V002_core_rare22_c1 | max_return_pct 42.1517 | max_drawdown_pct 6.3109 | official_ratio 6.6792 | trades 2277
- 8V5_V51P_V001_core_base | max_return_pct 41.4900 | max_drawdown_pct 6.2801 | official_ratio 6.6066 | trades 2277
- 8V5_V51P_V012_strict_rare22_c1 | max_return_pct 19.7596 | max_drawdown_pct 2.7359 | official_ratio 7.2223 | trades 1040
8V6은 8V5 상위 3개를 각 100개씩 개선했으나 no_promotion이다.
- 8V6 best: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 | max_return_pct 5.2510 | max_drawdown_pct 2.1312 | official_ratio 2.4639 | trades 652
8V6의 핵심 학습은 MDD 압축은 가능하지만, 전단 필터로 진입을 줄이면 V51 edge가 먼저 죽는다는 점이다.

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
목표는 V51 core_base/core_rare22_c1의 trades를 8V5의 2277에 최대한 가깝게 유지하면서 MDD를 6.28~6.31에서 4.9대로 낮추는 것이다.
8V6처럼 500~700 trades까지 잘라내는 방식은 피한다.
전단 entry filter보다 사후 drawdown brake, 손실 군집 회피, 변동성 폭발 직후 일시 회피, exit/hold/stop 재조정을 우선한다.
strict/lowanchor는 safe branch 핵심 축이지만 전면 필터가 아니라 부분 브레이크로 사용하는 것이 우선이다.
shocklow는 단독 부모가 아니라 위험 구간 보조 커버로 사용한다.

환경 오류 발생 시 처리
환경 오류가 확인되면 그 실험군은 invalid_env로 처리한다.
invalid_env 실험은 보존형 실패 기록이 아니라 제거 대상이다.