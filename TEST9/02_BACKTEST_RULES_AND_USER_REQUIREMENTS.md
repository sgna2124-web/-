백테스트 규칙과 사용자 요구사항

사용자 목표
- 차트 기반 전략을 지속적으로 개선한다.
- 수익성과 MDD를 함께 보며 더 나은 구조를 찾는다.
- 다음 대화창에서도 같은 흐름으로 바로 실험을 이어간다.

사용자 고정 요구사항
- 동시 진입 제한은 하지 않는다.
- 최대 포지션 보유수는 신경 쓰지 않는다.
- 상위 N개 시그널 제한 방식은 선호하지 않는다.
- 전략 조건과 구조를 개선해서 성과를 높이는 방식으로 간다.
- 개선안이 있으면 되묻지 말고 저장소에 반영하고 백테스트 가능한 상태로 만들어야 한다.

현재 백테스트 기본 가정
- initial_asset = 100.0
- position_fraction = 0.01
- fee_per_side = 0.0004
- leverage = 1
- entry_on_next_bar_open = true
- allow_long = true
- allow_short = true
- cooldown_bars_same_symbol_same_side = 0
- top_n_per_timestamp = null

정렬과 평가 원칙
- 최우선 정렬 기준은 cd_value다.
- 중복 전략은 제거해서 정렬한다.
- cd_value 정의:
  - cd_value = 100 * (1 + mdd_pct / 100) * (1 + peak_growth_pct / 100)
  - 초기 자산 100에 먼저 MDD를 적용한 뒤 peak_growth를 반영한 값이다.
- final_return_pct, peak_growth_pct, pf, mdd_pct를 함께 본다.

현재 데이터와 실행 방식
- repo_assets_5m 아래 data_manifest.json + monthly csv.gz 자산을 사용한다.
- 각 workflow는 repo asset 압축을 풀어 DATA_DIR에 배치한 뒤 백테스트를 수행한다.
- 결과는 results_json_only_timeout18_* 계열 폴더 아래 master_summary.csv/json/txt, 실험별 summary.json 으로 저장된다.

판단 메모
- 같은 1위가 유지되고 MDD 개선이 없으면 다시 새로운 개선안을 찾아야 한다.
- 수익이 올라가고 MDD도 같이 좋아지는 조합을 매우 높게 평가한다.
- 안정형 후보도 의미 있지만, 현재 주 흐름은 상단 성과를 계속 밀어올리는 쪽이다.
- 다음 대화창에서는 시스템 전체 설계로 튀지 말고, 현재 이기고 있는 전략군을 더 개선하는 실험을 이어가야 한다.
