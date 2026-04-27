이 파일은 새 대화창의 첫 진입점이다.
새 대화창의 어시스턴트는 다른 요약 문서보다 먼저 이 파일을 읽고 현재 프로젝트 상태를 복원한다.

현재 프로젝트 목표
코인/주식 차트 전략 중 MDD 5% 미만 전략을 우선 후보로 보고, 그중 cd_value가 가장 높은 전략을 찾는다.
롱 전용 전략 1위와 숏 전용 전략 1위를 별도 기준으로 유지하며, 앞으로의 모든 백테스트 결과는 이 기준과 비교한다.

성과 판단 기준
공식 판단 기준은 cd_value와 max_drawdown_pct(MDD)이다.
max_return_pct는 단독 판단 지표는 아니지만 cd_value 산출에 반드시 포함된다.
final_return_pct는 참고 지표로 기록하되, 공식 우선순위는 MDD -> cd_value(max_return_pct 기반) -> final_return_pct 다.

cd_value 정의
cd_value는 max_return_pct / max_drawdown_pct 로 해석한다.
문서와 결과 해석에서 cd_value를 final_return_pct 기준으로 계산하면 안 된다.
현재 프로젝트에서 cd_value는 max_return_pct 기준이다.

고정 백테스트 환경
자산 진입 비중은 1%다.
수수료는 0.04%다.
공식 판정은 전체 종목 풀 백테스트 기준이다.
FAST 예비검사는 사용하지 않는다.
조기탈락 규칙은 사용하지 않는다.
거래 로그 파일은 필수가 아니다.
백테스트 결과 요약에는 max_return_pct를 반드시 포함한다.

무효 실험 처리 규칙
정상 환경에서 실패한 전략은 기록으로 남긴다.
하지만 환경 설정 오류, 엔진 설정 오류, 자산 비중 오류, 수수료 오류, 비교 불가능한 실험은 invalid_env로 간주한다.
invalid_env 실험은 실패 전략 기록으로 보존하지 않고, 비교 체계 오염 방지를 위해 결과와 카탈로그에서 제거한다.

현재 방향성 요약
현재 공식 long 기준선은 6V2_L01_doubleflush_core 이다.
7V1~7V4 구간에서는 신규 reversal family 실험을 통해 L09 beartrap family와 L07 wick family가 가장 유망한 long 신규 축으로 확인되었다.
8V1과 8V2에서 completely new family를 대규모로 시도했지만 새로운 엣지는 확인되지 않았다. 따라서 long 주력 개발은 다시 L09/L07 중심으로 회귀했다.
8V3에서는 이 회귀가 성공했고, L09 안에서 candidate_cd_win_mdd_fail 풀이 4개로 늘어났다. 특히 8V3_L09_V51_microbase_pop은 cd_value 132.5742, max_drawdown_pct 6.3144까지 올라와 가장 근접한 고잠재력 후보가 되었다.
8V4에서는 이 방향이 더 강화되었다.
- batch best candidate_cd_win_mdd_fail: 8V4_V51_V002_core_rare22_c1 | final_return_pct 43.6673 | max_return_pct 44.2664 | max_drawdown_pct 6.7587 | cd_value 133.9572 | trades 2276
- next: 8V4_V51_V001_core_base | final_return_pct 43.2929 | max_return_pct 43.8091 | max_drawdown_pct 6.7547 | cd_value 133.6139 | trades 2277
- best under MDD<5 overall: 8V4_V51_V022_lowanchor_rare22_c1 | final_return_pct 21.2903 | max_return_pct 21.5445 | max_drawdown_pct 3.0752 | cd_value 117.5603 | trades 1040
즉 현재는 L09 내부에서도 V51 microbase_pop 계열이 clear 최우선 코어다. raw/cd는 이미 기준선을 크게 넘었고, 공식 후보군도 117대까지 올라왔다. 남은 과제는 V51의 MDD를 6.7대에서 5 아래로 더 내리는 것이다.
현재 우선순위는 다음과 같이 재정렬한다.
1) V51 microbase_pop family
2) V28 refire_block family
3) V09 cluster/shocklow family
4) V27 failed_break_pivot family
5) L07 wick family

장단점 기록 사용 규칙
CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 는 단순 보관 문서가 아니다.
새 전략을 설계하기 전에 반드시 이 문서를 읽고, 최근 실패 패턴과 살아남은 구조를 다음 전략 생성 규칙에 반영해야 한다.
즉 장단점 기록은 사후 회고가 아니라 사전 생성 규칙이다.
같은 실패 패턴의 재생산을 막고, 유망 구조만 조합적으로 재사용하는 것이 목적이다.
최근 라운드의 세부 보정 사항은 CORE_SUMMARY/13_6V2_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md 부터 CORE_SUMMARY/24_8V4_LONG400_STRENGTHS_WEAKNESSES_ADDENDUM.md 까지를 함께 본다.

결과 해석 보정 규칙
거래 수가 0인 전략, 극단적으로 적은 거래만 발생한 전략, 혹은 구조적으로 재현성이 낮은 전략은 cd_value 숫자가 높아 보여도 승격 후보로 보지 않는다.
MDD 초과 전략은 아이디어 저장 대상으로는 남길 수 있지만 공식 후보로 승격하지 않는다.
추가로, MDD가 5%를 넘더라도 cd_value가 현 공식 기준선 이상이면 candidate_cd_win_mdd_fail로 기록하고 다음 개선 시도의 우선 후보로 보관한다.

현재 상태 요약
6V2_LONG10_REVIEWED에서는 6V2_L01_doubleflush_core가 max_return_pct 23.9191, max_drawdown_pct 1.7512, cd_value 121.5300으로 공식 long 1위가 되었다.
7V1~7V4 구간에서는 신규 reversal family를 집중 검증했고, L09 beartrap family와 L07 wick family가 가장 유망한 신규 축으로 살아남았다.
8V1과 8V2에서는 완전히 새로운 family를 각각 50개, 100개씩 시도했지만 새로운 엣지를 만들지 못했다.
8V3에서는 다시 L09/L07으로 회귀하자 즉시 성과가 회복되었다.
8V4에서는 그 흐름이 더 강화되었고, V51 microbase_pop이 clear 최우선 코어로 부상했다.
이번 구간의 핵심 학습은 다음과 같다.
1) 새 family 탐색보다 강한 family 심화가 훨씬 낫다.
2) 현재 최우선 문제는 V51의 MDD를 5 아래로 내리는 것이다.
3) lowanchor, strict, rare22_c1, shocklow는 V51 안에서 재사용 가치가 높다.
4) quality_hold 다수, 과도한 microguard, ema_mid, prevhigh, vol18 다수는 주력 확장 우선순위를 낮춘다.

역할 분담
사용자는 로컬 컴퓨터에서 백테스트를 실행하고, 전략 코드와 결과 요약 파일을 저장소에 업로드한다.
어시스턴트는 업로드된 결과를 검토하고, 통합 요약/결과 카탈로그/장단점 문서/다음 단계 매뉴얼을 갱신하며, 다음 실험 전략을 설계한다.

결과 업로드 후 반드시 할 일
1. 업로드된 local_results 또는 결과 폴더를 확인한다.
2. 공식 long-only / short-only 기준선과 비교한다.
3. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md 를 갱신한다.
4. 장단점 문서를 갱신한다.
5. 승격이면 CORE_SUMMARY/03_CURRENT_BASELINES.md 도 갱신한다.
6. 결과만 보고 끝내지 말고, 왜 그런 결과가 나왔는지 장점과 단점을 남긴다.
7. 다음 전략 설계 전에 방금 추가한 장단점 기록을 다시 읽고, 생성 규칙으로 반영한다.

다음으로 읽을 문서
1. CORE_SUMMARY/03_CURRENT_BASELINES.md
2. CORE_SUMMARY/06_LOCAL_BACKTEST_AND_GITHUB_POLICY.md
3. CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md
4. CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md
5. CORE_SUMMARY/13_6V2_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md
6. CORE_SUMMARY/14_6V3_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md
7. CORE_SUMMARY/15_6V4_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md
8. CORE_SUMMARY/16_6V5_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md
9. CORE_SUMMARY/17_7V1_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md
10. CORE_SUMMARY/18_7V2_LONG40_STRENGTHS_WEAKNESSES_ADDENDUM.md
11. CORE_SUMMARY/19_7V3_LONG40_STRENGTHS_WEAKNESSES_ADDENDUM.md
12. CORE_SUMMARY/20_7V4_LONG40_STRENGTHS_WEAKNESSES_ADDENDUM.md
13. CORE_SUMMARY/21_8V1_LONG50_STRENGTHS_WEAKNESSES_ADDENDUM.md
14. CORE_SUMMARY/22_8V2_LONG100_STRENGTHS_WEAKNESSES_ADDENDUM.md
15. CORE_SUMMARY/23_8V3_LONG100_STRENGTHS_WEAKNESSES_ADDENDUM.md
16. CORE_SUMMARY/24_8V4_LONG400_STRENGTHS_WEAKNESSES_ADDENDUM.md
17. CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md
