# START HERE

이 파일은 새로운 대화창의 어시스턴트가 가장 먼저 읽어야 하는 시작점이다.
현재 대화 환경에서는 기존 00_INDEX.md를 직접 업데이트하지 못해, 이 파일을 사실상 상위 인덱스 역할로 추가한다.

## 1. 가장 먼저 이해해야 할 것
이 프로젝트는 단발성 답변 프로젝트가 아니다.
반복 루프형 전략 개발 프로젝트다.

반복 루프는 아래와 같다.
1) 어시스턴트가 저장소와 기준선을 참고해 새 long/short 전략을 제안
2) 사용자가 자신의 로컬 Python 환경에서 백테스트 실행
3) 사용자가 전략 코드와 결과를 GitHub 저장소에 업로드
4) 어시스턴트가 업로드된 파일을 읽고 성과를 해석
5) 어시스턴트가 summary 파일과 기준선/카탈로그 반영사항을 정리
6) 다시 다음 전략을 설계

즉, 실행은 사용자 로컬에서 하고, 해석/기록/비교/다음 설계는 어시스턴트가 맡는다.

## 2. 현재 공식 목표
- MDD 5% 미만 전략만 유효 후보
- 그중 cd_value 최대 전략 추구
- long-only와 short-only를 분리 관리
- 신규 실험은 반드시 각 side의 공식 1위와 비교

cd_value 공식:
- cd_value = 100 * (1 - abs(mdd_pct)/100) * (1 + final_return_pct/100)

## 3. 절대 먼저 확인해야 하는 현재 공식 기준선
### LONG_ONLY_OFFICIAL_1
- strategy_name: long_hybrid_wick_bridge_halfhalf
- family: long_only_hybrid_wick_bridge
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
- result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
- summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/summary.json
- final_return_pct: 9.9603
- mdd_pct: -1.0456
- cd_value: 108.8106

### SHORT_ONLY_OFFICIAL_1
- strategy_name: short_beh_dd_brake
- family: short_only_behavioral_guards
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
- final_return_pct: 311.5456
- mdd_pct: -4.7589
- cd_value: 391.9606

공식 source of truth:
- state/global_top_reference_under_mdd5_cd.json
- CORE_SUMMARY/10_BASELINE_PATCH_2026-04-16.md
- CORE_SUMMARY/11_RESULTS_CATALOG_SEED_2026-04-16.md
- CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md

## 4. 새 대화창에서의 첫 행동 순서
새 대화창의 어시스턴트는 아래 순서로 행동한다.

1) 이 파일을 먼저 읽는다
2) state/global_top_reference_under_mdd5_cd.json을 확인한다
3) CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md를 읽는다
4) CORE_SUMMARY/10_BASELINE_PATCH_2026-04-16.md를 읽는다
5) CORE_SUMMARY/11_RESULTS_CATALOG_SEED_2026-04-16.md를 읽는다
6) 그 다음에 기존 CORE_SUMMARY의 다른 문서들을 읽는다
7) 사용자가 방금 업로드한 새 결과가 있다면 그 결과부터 우선 해석한다
8) 없으면 다음 long/short 전략을 설계한다

## 5. 사용자가 새 결과를 업로드했을 때 반드시 처리할 것
- 코드 파일 경로 확인
- 결과 폴더 경로 확인
- summary.json 확인
- master_summary.json 또는 txt 확인
- 같은 side 공식 1위 대비 delta 계산
- MDD 5% 미만 여부 확인
- cd_value 우위 여부 확인
- summary에 추가/수정/기록할 항목 정리
- 다음 실험 아이디어 제안

## 6. 현재 대전제
- GitHub Actions 중심 운영으로 되돌리지 않는다
- 로컬 Python 백테스트 + GitHub 기록 저장소 체계를 유지한다
- 실패 전략도 삭제하지 않고 누적한다
- path와 수치를 함께 기록한다
- 우선순위가 바뀌더라도 재해석 가능하도록 원시 핵심 수치를 남긴다

## 7. 현재 파일 구조에서의 의미
- 00_START_HERE.md: 새 대화창 시작점
- 09_NEXT_CHAT_MANUAL.md: 전체 운영 매뉴얼
- 10_BASELINE_PATCH_2026-04-16.md: 현재 공식 기준선 보정
- 11_RESULTS_CATALOG_SEED_2026-04-16.md: 결과 원장 초기 seed

## 8. 한 줄 핵심
이 저장소는 사용자가 로컬에서 백테스트한 결과를 어시스턴트가 이어받아 비교/기록/개선하는 반복형 전략 연구 저장소다.
