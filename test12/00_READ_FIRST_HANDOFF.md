TEST12 최신 인수인계 문서

이 문서는 test12/00_READ_FIRST_V56_V57.md보다 최신 상태를 반영한 상위 인수인계 문서다.
다음 대화창의 어시스턴트는 이 문서부터 읽고, 이어서 test12/01_CURRENT_STATE_AND_TOP_CANDIDATES.md, test12/02_TIMELINE_V56_TO_V67.md, test12/03_WORKFLOW_ERRORS_AND_SAFE_PATTERN.md, test12/04_CD_VALUE_AND_REPORTING_RULES.md, test12/05_NEXT_STEP_PLAN.md, test12/06_MACHINE_STATE.json 순으로 참고하면 된다.

프로젝트 핵심 목표
- 롱 전용 전략과 숏 전용 전략을 따로 개발한다.
- 절대수익보다 먼저 MDD 통제를 본다.
- 현재 사용자는 단순 파라미터 조정을 원하지 않는다.
- 새로운 전략 철학, 새로운 진입 구조, 기존 전략 간의 구조적 결합을 선호한다.
- 장기 목표는 저MDD 전략에 레버리지를 얹어 실전형 수익을 만드는 것이다.

현재 평가 방식
1. 먼저 MDD가 낮은지 본다.
2. 그 안에서 수익률과 PF, max_conc를 본다.
3. 최근부터는 cd_value를 함께 기록/비교한다.
4. 사용자가 최근 직접 정의한 cd_value 계산식은 다음과 같다.
   cd_value = 초기자산 × (1 - |MDD|) × (1 + 최대수익률)
   실사용 계산은 퍼센트를 소수화해서 사용한다.
   예시: 100 × (1 - |mdd_pct|/100) × (1 + final_return_pct/100)

현재 가장 중요한 운영 원칙
- 롱 전용과 숏 전용을 합치지 말고 따로 평가한다.
- topN, top200 같은 강한 랭킹 컷은 사용자가 좋아하지 않는다.
- 같은 아이디어를 숫자만 미세하게 바꿔 반복하지 말고, 구조 자체를 바꾸거나 결합하는 시도를 우선한다.
- 보고 시에는 최소한 다음 수치를 같이 본다.
  최대 수익률, MDD, PF, max_conc, cd_value
- 결과 정렬 요청이 오면, 최근 사용자의 지시 기준은 다음과 같다.
  MDD 5% 미만 후보만 남기고, cd_value 내림차순으로 정렬

현재 최신 상태 한 줄 요약
- 숏은 이미 여러 계열이 성숙했고, 현재는 메인형/공격형/극방어형/초방어형으로 나뉜다.
- 롱은 아직 약하지만, 최근 65~67에서 극저MDD형과 bridge형이 생기기 시작했다.
- 다음 단계는 롱의 수익 엔진을 더 키우는 것과, 숏의 공격형을 너무 죽이지 않으면서 방어를 유지하는 것이다.

현재 최신 TOP 개념 정리
숏 메인형 축
- short_beh_dd_brake
- short_div_dense_skip30
- short_beh_conservative_combo

숏 공격형 축
- v62 split 계열에서 나온 pure_atr050_2bar, pure_atr025_1bar, pure_wick075_2bar 류
- 수익은 강하지만 max_conc가 너무 높았다.

숏 중간지대/bridge 축
- v66 short_balanced_bridge_atr050_prior1_24
- v66 short_balanced_bridge_wick075_dense30
- v66 short_balanced_bridge_wick075_prior1_24

롱 메인형 철학 축
- 과거 long_hybrid_symbol1_dd_confirmation 계열이 기준선 역할을 했다.
- 최근에는 v67 hybrid wick bridge family가 그 철학을 이어받아 재실험 중이다.

롱 극저MDD/bridge 축
- v65 guarded_wick_split 계열
- v67 hybrid_wick_bridge 계열
- 아직 수익이 약한 경우가 많지만, MDD는 매우 낮다.

다음 어시스턴트가 절대 놓치면 안 되는 점
1. 사용자는 같은 말을 반복하거나 요청을 벗어나는 답을 매우 싫어한다.
2. 새 전략을 추가하라는 요청이 아닐 때는 새 전략을 만들지 말고, 요청한 작업만 수행해야 한다.
3. workflow 문제는 최근에 여러 번 터졌으므로, 새 workflow를 만들 때는 test12/03_WORKFLOW_ERRORS_AND_SAFE_PATTERN.md의 안전 패턴을 따라야 한다.
4. 앞으로 summary는 cd_value를 자동 포함하는 새 스크립트를 우선 사용해야 한다.
5. 다음 라운드 번호는 v68, v69 이후로 가는 것이 자연스럽다. 이미 v66, v67까지 사용했다.

현재 다음 단계 핵심
- 그냥 지금까지 모든 전략을 참고해서 개선하면서 새로운 전략을 찾는 것이 사용자 의도다.
- 단, 단순 파라미터 조정은 금지다.
- 롱은 더 괜찮은 전략이 나올 때까지 계속 개발/개선 대상이다.
- 숏도 계속 개선하지만, 이미 확보된 강한 후보를 기준 삼아 새로운 철학을 붙이는 방식이 좋다.
