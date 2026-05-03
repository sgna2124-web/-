캔들 제한 금지 및 동일 환경 비교 규칙

작성 배경
8V26 wrapper에서 1시간 예산을 맞추기 위해 --max-bars 기본값을 주입했다. 이는 공식 기준선과 이전 백테스트 결과가 캔들 제한 없는 전체 데이터 환경에서 나온 결과라는 점을 훼손한다. 시간 단축을 위해 비교 기준 자체를 바꾸면 기준선 대비 성과 비교가 무의미해진다.

필수 규칙
1. 공식 기준선 또는 기준선 비교용 개선 배치는 캔들 제한을 걸지 않는다.
2. --max-bars, --max_bars, max-bars 기본값 주입을 금지한다.
3. 시간이 오래 걸릴 때는 캔들 수를 줄이지 말고 개선안 수, 축 수, 후보 수를 줄인다.
4. 기준선과 개선안은 같은 데이터 범위, 같은 캔들 환경, 같은 실행 조건에서 비교한다.
5. 이전 공식 결과와 비교해야 하는 실험에서는 전체 데이터 기준을 유지한다.
6. 1시간 예산형 실험도 캔들 제한 없이 설계한다. 시간은 개선안 개수와 축 선택으로만 조절한다.
7. wrapper가 사용자 입력으로 --max-bars 또는 --max_bars를 받더라도 비교용 실행에서는 이를 제거하거나 실행 전 경고해야 한다.
8. 결과 로그에 [CANDLE_LIMIT] disabled 또는 no candle limit 상태를 명시한다.
9. 저장소 접근 경로와 실행 위치는 계속 분리한다. C:\Users\user\Documents\GitHub\- 는 저장소 접근 경로이며 subprocess cwd로 강제하지 않는다.
10. 기준선 조건, base_spec, BASELINES, entry/exit 엔진, parent gate는 계속 보존한다.

8V27 적용
- BATCH: 8V27_TP03_NO_CANDLE_LIMIT_FAST1H_NO_BASELINE_TOUCH
- 캔들 제한 없음
- 기본 개선안: 각 축 1개, 총 4개
- 시간 목표: 캔들 제한 없이 약 1시간 내외
- 시간 조절 방식: max-bars가 아니라 개선안 수와 fast-axis 선택

다음 개선 파일 작성 시 체크리스트
- 코드 안에 --fast-max-bars 인자가 없어야 한다.
- 코드가 --max-bars를 자동 삽입하지 않아야 한다.
- forward_args에 들어온 --max-bars 계열 인자를 제거하거나 거부해야 한다.
- 결과 저장 경로는 C:\Users\user\Documents\GitHub\-\local_results\{BATCH} 를 유지한다.
- 실행 cwd는 launch_cwd를 유지한다.
