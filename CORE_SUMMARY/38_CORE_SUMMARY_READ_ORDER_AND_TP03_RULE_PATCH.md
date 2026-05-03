CORE_SUMMARY 전체 읽기 순서 및 TP 0.3% 필수 규칙 패치

새 대화창은 CORE_SUMMARY/00_START_HERE.md를 읽은 직후 이 문서를 읽는다.

핵심 규칙 0: 읽기 루프 방지
00_START_HERE와 이 문서는 진입점 문서다.
따라서 00_START_HERE > 이 문서 > CORE_SUMMARY 전체 .md 읽기 순서로 한 번만 진입한다.
CORE_SUMMARY 전체 .md를 읽는 단계에서 00_START_HERE와 이 문서를 다시 만나더라도 이미 읽은 파일로 표시하고 재실행하지 않는다.
즉 전체 읽기는 재귀 호출이 아니라 1회성 목록 순회다.
동일 파일은 한 세션에서 한 번만 읽는다.

핵심 규칙 1: CORE_SUMMARY 폴더 안의 모든 .md 문서는 읽기 대상이다.
기존 09_NEXT_CHAT_MANUAL의 선별 목록만 따르면 일부 최신 문서가 누락될 수 있다.
따라서 새 대화창은 00_START_HERE 이후 CORE_SUMMARY 전체를 탐색하고, 모든 .md 문서를 번호순으로 읽는다.
단, 이미 읽은 00_START_HERE와 이 문서는 다시 읽지 않고 건너뛴다.
최신 번호 addendum은 마지막에 다시 역순으로 훑어 현재 판단이 바뀐 부분이 없는지 확인한다.
이 역순 확인도 이미 읽은 내용을 재귀적으로 실행하는 것이 아니라 최신 판단만 재확인하는 1회성 검토다.

핵심 규칙 2: 신규 백테스트 개선안은 TP 기대값이 0.3% 이상일 때만 진입한다.
코드 기준은 min_expected_tp >= 0.003 또는 동등한 expected TP 필터다.
이 조건은 모든 신규 long 개선안, short 개선안, main 후보, max 후보, 4축 개선안, 파라미터 조정형 개선안에 적용한다.
기준선 복제 검증은 원본 보존을 우선하지만, 기준선 위에 개선 조건을 붙이는 순간부터 TP 0.3% 필터를 반드시 적용한다.

핵심 규칙 3: 읽기 누락 위험이 있던 문서도 반드시 읽는다.
특히 35_ASSISTANT_RESPONSE_AND_CODE_RULES.md, 36_LOCAL_BACKTEST_ENVIRONMENT_RULE.md, 37_8V14_FULLDATA_RUNTIME_STALL_FIX.md, 35_8V14_4AXIS_50_EACH_STREAMSAFE_ADDENDUM.md, 36_8V13_MAINMAX_4AXIS_400_DIFFERENT_FLOW_ADDENDUM.md, 36_8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE_ADDENDUM.md, 33_CURRENT_NEXT_STEP_AFTER_8V10.md, 30_CD_VALUE_FORMULA_CORRECTION_8V6_8V7_RERANK.md는 누락하지 않는다.

핵심 규칙 4: 문서 충돌 시 최신 명시 규칙을 우선한다.
우선순위는 최신 addendum, 이 문서, 35_ASSISTANT_RESPONSE_AND_CODE_RULES.md, 09_NEXT_CHAT_MANUAL.md, 00_START_HERE.md, 과거 실험 기록 순서다.

한 줄 결론: CORE_SUMMARY 일부만 읽고 다음 단계를 진행하지 말고, 모든 .md 문서를 1회성 목록 순회 방식으로 읽은 뒤 신규 개선안에는 TP 기대값 0.3% 이상 진입 조건을 반드시 넣는다.
