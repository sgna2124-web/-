# NEXT CHAT MANUAL

이 파일은 새로운 대화창의 어시스턴트가 이 프로젝트의 현재 상태와 자신의 역할을 즉시 복원할 수 있도록 만드는 운영 매뉴얼이다.

## 1. 프로젝트의 핵심 목표
사용자는 코인/주식 차트를 이용해 돈을 벌 전략을 찾고 있다.
현재 공식 목표는 다음과 같다.

- MDD 5% 미만 전략만 유효 후보로 인정
- 그중 cd_value가 가장 높은 전략을 찾는다
- cd_value 공식:
  - cd_value = 100 * (1 - abs(mdd_pct)/100) * (1 + final_return_pct/100)
- long-only와 short-only를 분리해서 관리한다
- 앞으로의 신규 백테스트는 long 공식 1위, short 공식 1위와 각각 비교한다

## 2. 역할 분담
사용자 역할:
- 자신의 컴퓨터 파이썬 환경에서 백테스트를 직접 실행
- 신규 전략 코드, 결과, summary.json, master_summary 등을 GitHub 저장소에 직접 업로드

어시스턴트 역할:
- 저장소의 과거 실험들을 참고해 새로운 long/short 전략 아이디어를 제안
- 사용자가 업로드한 코드/결과를 읽고 성과를 해석
- 어떤 항목을 CORE_SUMMARY에 기록해야 하는지 정리
- 공식 기준선이 바뀌면 baseline 문서와 results catalog를 갱신
- 다음 대화창에서도 같은 실수를 반복하지 않도록 운영 규칙을 유지

즉, 백테스트 실행은 사용자가 하고, 요약/기록/비교/다음 전략 설계는 어시스턴트가 맡는다.

## 3. 반드시 먼저 읽을 파일 순서
새 대화창의 어시스턴트는 아래 순서로 읽는다.

1) CORE_SUMMARY/00_INDEX.md
2) CORE_SUMMARY/01_PROJECT_OVERVIEW.md
3) CORE_SUMMARY/02_STRATEGY_FAMILIES_AND_HISTORY.md
4) CORE_SUMMARY/03_CURRENT_BASELINES.md
5) CORE_SUMMARY/04_HARD_RULES_AND_BANS.md
6) CORE_SUMMARY/05_EXPERIMENT_UPDATE_PROTOCOL.md
7) CORE_SUMMARY/06_LONG_ONLY_TRACK.md
8) CORE_SUMMARY/07_SHORT_ONLY_TRACK.md
9) CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md
10) CORE_SUMMARY/09_NEXT_CHAT_MANUAL.md
11) state/global_top_reference_under_mdd5_cd.json
12) summary_upload_draft/summary_upload_draft/04_현재기준_TOP1_참조.md

주의:
- 03_CURRENT_BASELINES.md, 08_ALL_RESULTS_CATALOG.md는 과거 내용이 남아 있을 수 있으므로,
  반드시 state/global_top_reference_under_mdd5_cd.json과 최신 summary.json을 함께 대조한다.
- 이 파일(09_NEXT_CHAT_MANUAL.md)은 대화 운영 방식의 source of truth 역할을 한다.

## 4. 현재 공식 비교 기준선
현재 저장소 기준 공식 비교선은 다음과 같다.

### LONG_ONLY_OFFICIAL_1
- strategy_name: long_hybrid_wick_bridge_halfhalf
- family: long_only_hybrid_wick_bridge
- version_reference: legacy_v67
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge.json
- result_path: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/
- summary_file: results_json_only_timeout18_time_reduce_v67_long_only_hybrid_wick_bridge/long_hybrid_wick_bridge_halfhalf/summary.json
- final_return_pct: 9.9603
- mdd_pct: -1.0456
- cd_value: 108.8106
- pf: 1.3033
- win_rate_pct: 54.9859
- max_conc: 50

### SHORT_ONLY_OFFICIAL_1
- strategy_name: short_beh_dd_brake
- family: short_only_behavioral_guards
- version_reference: legacy_v52
- code_path: scripts/run_backtest_batch_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.py
- config_path: experiments/base_config_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- combinations_path: experiments/combinations_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards.json
- result_path: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/
- summary_file: results_json_only_timeout18_time_reduce_v52_short_only_behavioral_guards/short_beh_dd_brake/summary.json
- final_return_pct: 311.5456
- mdd_pct: -4.7589
- cd_value: 391.9606
- pf: 1.4457
- win_rate_pct: 15.0623
- max_conc: 286

## 5. 앞으로의 대화 루프
새 대화창에서 어시스턴트는 기본적으로 아래 루프를 따른다.

1) 저장소 요약과 기준선을 확인한다
2) long 전략 1개 이상, short 전략 1개 이상을 제안한다
3) 사용자가 로컬 파이썬에서 백테스트를 실행한다
4) 사용자가 코드/결과를 GitHub에 업로드한다
5) 어시스턴트는 업로드된 결과를 읽고 다음을 수행한다
   - 공식 기준선과 비교
   - cd_value, MDD, final_return, PF, max_conc 해석
   - 승급 여부 판정
   - CORE_SUMMARY에 추가할 항목 정리
   - 다음 개선 포인트 제안
6) 다시 다음 전략을 설계한다

## 6. 새 실험을 제안할 때의 규칙
- 무조건 long-only / short-only를 분리해서 생각한다
- 결과 비교는 각 side의 공식 1위와 비교한다
- 단순 파라미터 튜닝만 반복하지 않는다
- 구조적으로 다른 진입/청산/필터/리스크 제어 아이디어를 섞는다
- 사용자가 원하면 완전히 다른 계열 전략도 제안한다
- 새 워크플로우/버전명은 사용자가 지정한 규칙을 따른다
  - 예: 1V2로 시작, 다음은 2V2

## 7. 새 결과를 받았을 때 반드시 해야 하는 일
사용자가 새 결과를 업로드한 뒤 어시스턴트는 아래 체크리스트를 따른다.

### 7-1. 결과 확인
- summary.json 위치 확인
- master_summary.json 또는 master_summary.txt 확인
- 코드 파일 경로 확인
- 실험 설명이 있으면 해당 설명도 같이 확인

### 7-2. 핵심 지표 추출
최소한 아래를 기록한다.
- strategy_name
- family
- version tag
- code_path
- config_path
- result_path
- summary_file
- final_return_pct
- mdd_pct
- cd_value
- pf
- win_rate_pct
- max_conc
- total_trades 가능하면 같이 기록
- verdict (promote / keep as candidate / reject / archive)

### 7-3. 비교 분석
- 같은 side의 공식 1위와 delta 계산
- MDD 5% 미만인지 먼저 확인
- MDD 조건 통과 시 cd_value 우열을 최우선 평가
- max_conc가 지나치게 크면 별도 경고
- 성과가 높아도 과최적화/특수구간 편향 의심이 있으면 note에 남김

### 7-4. 기록 갱신
가능하면 아래 파일들을 갱신한다.
- CORE_SUMMARY/03_CURRENT_BASELINES.md
- CORE_SUMMARY/06_LONG_ONLY_TRACK.md
- CORE_SUMMARY/07_SHORT_ONLY_TRACK.md
- CORE_SUMMARY/08_ALL_RESULTS_CATALOG.md
- state/global_top_reference_under_mdd5_cd.json (공식 1위가 바뀐 경우)

현재 일부 대화에서는 GitHub update_file 액션이 비정상일 수 있다.
그 경우에는 새 patch 파일을 만들어 기록을 남긴다.
예:
- CORE_SUMMARY/10_BASELINE_PATCH_YYYY-MM-DD.md
- CORE_SUMMARY/11_RESULTS_CATALOG_SEED_YYYY-MM-DD.md

## 8. 금지 수칙
- 사용자가 이미 백테스트를 로컬에서 돌리겠다고 정한 상태에서, GitHub Actions 전제 방식으로 다시 되돌리지 않는다
- LFS가 막혀 있는 저장소 상황을 무시하고 Actions 실행을 전제로 설계하지 않는다
- long/short/mixed를 뒤섞어 공식 비교선을 오염시키지 않는다
- MDD 5% 미만 필터를 무시하고 수익률만으로 승급시키지 않는다
- 실패 전략도 삭제 대상으로 보지 않는다. 실패한 흔적도 카탈로그에 남긴다
- 같은 실수와 같은 제안을 반복하지 않는다
- 사용자가 저장소에 업로드한 파일 경로와 실제 수치를 함께 기록하는 원칙을 무시하지 않는다

## 9. 현재 저장소 운영 원칙
- 모든 전략 결과는 성공/실패와 관계없이 저장소에 남긴다
- 어시스턴트는 그것들을 취합해 summary 파일에 반영한다
- 우선순위가 바뀔 수 있으므로, 결과 원장에는 path와 수치를 함께 남긴다
- 현재의 공식 우선순위는 “MDD 5% 미만 전략 중 cd_value 최대”다
- 다만 이후 목표가 바뀌더라도 과거 결과를 다시 재해석할 수 있도록 원본 수치를 남겨야 한다

## 10. 다음 대화창의 첫 행동
새 대화창의 어시스턴트는 아래처럼 행동하면 된다.

1) 먼저 CORE_SUMMARY와 state/global_top_reference_under_mdd5_cd.json을 읽는다
2) 현재 long/short 공식 1위를 명시한다
3) 사용자가 방금 업로드한 새 결과가 있으면 그 파일부터 읽는다
4) 없으면 다음 long 전략과 short 전략을 바로 제안한다
5) 제안 시 기존 1위 대비 어떤 구조를 개선하려는지 분명히 설명한다

## 11. 핵심 한 줄 요약
이 프로젝트는 “사용자가 로컬에서 백테스트를 실행하고 GitHub에 결과를 올리면, 어시스턴트가 그 결과를 해석/기록/비교/다음 전략 설계를 수행하는 반복 루프”다.
