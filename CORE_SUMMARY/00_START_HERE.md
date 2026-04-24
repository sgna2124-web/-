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
파이썬 로컬 백테스트 전환 이후 long 쪽에서 처음으로 공식 승격이 발생했고, 그 기준선은 현재도 유지되고 있다.
현재 공식 long 기준선은 6V2_L01_doubleflush_core 이며, selective double flush + cap reclaim 코어가 broad continuation류보다 훨씬 유효하다는 것이 확인되었다.
6V3_LONG10_REVIEWED에서는 post-signal 패턴 강화형 변형 10개가 전부 승격에 실패했다.
6V4_LONG10_REVIEWED에서는 상태 필터형 개선을 시도했지만, core 위에 얹은 hard gate는 과선택화로 무너졌고, 신규 전략은 cooldown과 rarity guard가 부족해 과다거래로 붕괴했다.
6V5_LONG10_REVIEWED에서는 soft score + spacing 구조로 과다거래와 0/1 trade 문제를 상당 부분 정리했지만, 최고 전략조차 6V5_L05_core_score_shockfresh | max_return_pct 4.3842 | max_drawdown_pct 1.0476 | cd_value 102.8241에 그쳐 6V2 기준선을 크게 밑돌았다.
7V1_LONG10_REVIEWED에서는 신규 family 개발로 전환한 뒤 처음으로 raw upside는 다시 살아났다. 특히 7V1_L10_shock_reversal_balance, 7V1_L04_engulf_panic_retake, 7V1_L09_beartrap_close_drive, 7V1_L07_climax_wick_reclaim은 max_return_pct 17.8515~56.5963 구간까지 뻗으며 새 family 자체의 확장성은 확인했다.
하지만 동시에 같은-bar shock reversal / engulf / beartrap 계열을 넓게 켜면 거래 수가 2118~33481까지 늘고, MDD도 5.5953~15.1033으로 다시 무너진다는 점도 확인됐다.
반대로 outside flush / deep ema20 retake / rangefloor pop / beartrap midflip처럼 거래를 과도하게 줄인 버전은 MDD는 낮지만 수익이 거의 남지 않았다.
즉 다음 long 개선 방향은 다시 broad continuation류로 회귀하는 것이 아니라, 7V1에서 확인된 새 reversal family의 raw edge는 유지하되, 6V2/6V5에서 배운 spacing·shockfresh·rarity control을 더 강하게 결합해 과다거래를 줄인 선택적 반전 family로 재구성하는 것이다.
반면 숏 측은 기존 높은 기준선이 여전히 유지되므로, 당분간 우선순위는 새 long 기준선을 찾는 것이다.

장단점 기록 사용 규칙
CORE_SUMMARY/12_STRATEGY_STRENGTHS_WEAKNESSES.md 는 단순 보관 문서가 아니다.
새 전략을 설계하기 전에 반드시 이 문서를 읽고, 최근 실패 패턴과 살아남은 구조를 다음 전략 생성 규칙에 반영해야 한다.
즉 장단점 기록은 사후 회고가 아니라 사전 생성 규칙이다.
같은 실패 패턴의 재생산을 막고, 유망 구조만 조합적으로 재사용하는 것이 목적이다.
최근 라운드의 세부 보정 사항은 CORE_SUMMARY/13_6V2_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/14_6V3_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/15_6V4_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/16_6V5_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md, CORE_SUMMARY/17_7V1_LONG10_STRENGTHS_WEAKNESSES_ADDENDUM.md 를 함께 본다.

결과 해석 보정 규칙
거래 수가 0인 전략, 극단적으로 적은 거래만 발생한 전략, 혹은 구조적으로 재현성이 낮은 전략은 cd_value 숫자가 높아 보여도 승격 후보로 보지 않는다.
MDD 초과 전략은 아이디어 저장 대상으로는 남길 수 있지만 공식 후보로 승격하지 않는다.
결과가 저조한 배치도 반드시 왜 실패했는지 구조적으로 기록하고 다음 배치 설계에 반영한다.

현재 상태 요약
V2 실험군은 환경 전제 오류가 있었으므로 4V2R1을 제외하고 전부 제거했다.
새 대화창의 어시스턴트는 기존 V2 결과를 비교 근거로 사용하면 안 된다.
4V2R14 ~ 4V2R16 결과는 신규 조건 탐색의 한계와 롱 전략 부진을 보여주는 참고 구간으로 남아 있다.
5V2_COMBO10_REVIEWED에서는 5V2_L01_capitulation_reclaim이 높은 수익 잠재력을 보였지만 MDD 13.7240으로 승격에 실패했다.
6V2_LONG10_REVIEWED에서는 6V2_L01_doubleflush_core가 max_return_pct 23.9191, max_drawdown_pct 1.7512, cd_value 121.5300으로 공식 long 1위가 되었고, 6V2_L04_doubleflush_extremeclose도 cd_value 118.0043으로 함께 살아남았다.
6V3_LONG10_REVIEWED에서는 새 후속 패턴 게이트 10개가 전부 실패했다. best는 6V3_L04_core_redtogreen 이었지만 trades 9, cd_value 100.2439로 기준선에 못 미쳤고, L03은 0트레이드, L05는 늦은 hold-break 추격 구조로 악화됐다.
6V4_LONG10_REVIEWED에서는 state hard gate 쪽은 0트레이드/1트레이드로 과선택화가 발생했고, 신규 전략 쪽은 trades가 1701 ~ 1644460까지 치솟는 과다거래 붕괴가 발생했다.
6V5_LONG10_REVIEWED에서는 soft score + spacing으로 과다거래는 제거했고 대부분 전략을 61~337 trades 범위, 1.05% 이하 MDD로 안정화했지만, 수익 엣지는 크게 희석되었다. best인 6V5_L05_core_score_shockfresh도 cd_value 102.8241에 그쳤다.
7V1_LONG10_REVIEWED에서는 신규 반전 family 10개를 처음으로 일괄 검증했다.
- raw upside 최고: 7V1_L10_shock_reversal_balance | final_return_pct 51.0204 | max_return_pct 56.5963 | max_drawdown_pct 15.1033 | cd_value 128.2113 | trades 33481
- low-MDD but weak edge: 7V1_L06_deep_ema20_retake | final_return_pct 0.9083 | max_return_pct 0.9889 | max_drawdown_pct 0.6282 | cd_value 100.2744 | trades 332
- broad same-bar reversal 계열인 L10/L04/L09/L07/L01/L02는 raw edge는 있었지만 모두 MDD 5% 초과로 실패했다.
- 반대로 거래 수를 45~671 수준으로 강하게 누른 L03/L05/L06/L08은 방어력은 좋았지만 수익 곡선이 너무 얕았다.
이번 구간의 핵심 학습은 새 reversal family 자체는 살아 있지만, same-bar 반전 코어를 넓게 켜면 5V2식 broad overtrading이 다시 재현된다는 점이다.
따라서 다음 단계는 신규 family 개발을 계속하되, 7V1 상위권의 reversal edge를 6V2식 선택도와 6V5식 spacing/score로 압축하는 방향이 적절하다.

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
10. CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md
