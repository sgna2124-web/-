CORE_SUMMARY 전체 읽기 순서 및 TP 0.3% 필수 규칙 패치

이 문서는 CORE_SUMMARY 전체 읽기 원칙과 TP 0.3% 필수 규칙을 정리한 보강 문서다.
새 대화창은 이 문서를 별도로 먼저 호출하지 않는다.
파일명 숫자 기준 순서가 왔을 때 읽는다.

핵심 규칙 0: 읽기 순서 단순화
CORE_SUMMARY 폴더 안의 .md 문서는 파일명 숫자 기준으로 00번부터 끝까지 차례대로 1회 읽는다.
특정 문서로 먼저 점프하지 않는다.
00_START_HERE를 읽은 뒤에는 01, 02, 03 순서로 계속 읽고, 이 문서는 38번 순서가 왔을 때 읽는다.
동일 파일은 한 세션에서 한 번만 읽는다.
파일명이 같은 번호로 시작하는 경우에는 파일명 전체의 오름차순으로 읽는다.
번호가 없는 .md 파일이 생기면 번호순 .md 전체 순회가 끝난 뒤 별도 예외 문서로 읽는다.
전체 읽기는 재귀 호출이 아니라 1회성 목록 순회다.

핵심 규칙 1: CORE_SUMMARY 폴더 안의 모든 .md 문서는 읽기 대상이다.
기존 09_NEXT_CHAT_MANUAL의 선별 목록만 따르면 일부 최신 문서가 누락될 수 있다.
따라서 새 대화창은 CORE_SUMMARY 전체를 탐색하고, 모든 .md 문서를 번호순으로 읽는다.
최신 번호 addendum은 전체 순회가 끝난 뒤 현재 판단 보정용으로만 다시 확인한다.
이 재확인은 문서 지시를 다시 실행하는 것이 아니라 최신 상태와 다음 단계 판단만 확인하는 검토다.

핵심 규칙 1-1: .py 파일 예외 처리
CORE_SUMMARY 안의 .py 파일은 .md 인수인계 문서가 아니므로 번호순 읽기 대상은 아니다.
하지만 최신 백테스트 코드 구조, 결과 저장 방식, 필수 필터 구현 방식 확인용으로 반드시 참조한다.
특히 run_*.py 파일은 신규 코드 생성 전 확인 대상이다.
현재 확인된 예외 파일 예시는 CORE_SUMMARY/run_8v20_embedded_parent_gate_4axis_50_each.py 이다.
이 파일은 전체 전략 인수인계 문서가 아니라 실행 코드 참조 대상이다.

핵심 규칙 2: 신규 백테스트 개선안은 TP 기대값이 0.3% 이상일 때만 진입한다.
코드 기준은 min_expected_tp >= 0.003 또는 동등한 expected TP 필터다.
이 조건은 모든 신규 long 개선안, short 개선안, main 후보, max 후보, 4축 개선안, 파라미터 조정형 개선안에 적용한다.
기준선 복제 검증은 원본 보존을 우선하지만, 기준선 위에 개선 조건을 붙이는 순간부터 TP 0.3% 필터를 반드시 적용한다.

핵심 규칙 3: 읽기 누락 위험이 있던 문서도 반드시 읽는다.
특히 35_ASSISTANT_RESPONSE_AND_CODE_RULES.md, 36_LOCAL_BACKTEST_ENVIRONMENT_RULE.md, 37_8V14_FULLDATA_RUNTIME_STALL_FIX.md, 35_8V14_4AXIS_50_EACH_STREAMSAFE_ADDENDUM.md, 36_8V13_MAINMAX_4AXIS_400_DIFFERENT_FLOW_ADDENDUM.md, 36_8V15_4AXIS_PARENT_PRESERVE_50_EACH_STREAMSAFE_ADDENDUM.md, 33_CURRENT_NEXT_STEP_AFTER_8V10.md, 30_CD_VALUE_FORMULA_CORRECTION_8V6_8V7_RERANK.md는 전체 번호순 읽기 과정에서 누락하지 않는다.

핵심 규칙 4: 문서 충돌 시 최신 명시 규칙을 우선한다.
우선순위는 최신 addendum, 이 문서, 35_ASSISTANT_RESPONSE_AND_CODE_RULES.md, 09_NEXT_CHAT_MANUAL.md, 00_START_HERE.md, 과거 실험 기록 순서다.

한 줄 결론: CORE_SUMMARY 안의 모든 .md 문서를 00번부터 끝까지 번호순으로 1회 읽고, run_*.py는 최신 실행 코드 참조 대상으로 확인하며, 신규 개선안에는 TP 기대값 0.3% 이상 진입 조건을 반드시 넣는다.
