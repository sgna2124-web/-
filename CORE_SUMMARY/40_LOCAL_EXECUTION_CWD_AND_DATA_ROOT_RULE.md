로컬 실행 위치와 데이터 루트 보존 규칙

작성 배경
8V23 실행에서 wrapper가 subprocess.run(..., cwd=REPO_ROOT)로 생성 실행 파일을 실행했다. 그 결과 원본 백테스트가 상대 경로로 찾던 데이터 루트가 사용자의 실제 실행 환경이 아니라 저장소 접근 경로 아래로 바뀌었다.

발생한 오류
FileNotFoundError: data root not found: C:\Users\user\Documents\GitHub\-\코인\Data\time

정확한 해석
C:\Users\user\Documents\GitHub\- 는 저장소 접근 경로다.
이 경로는 파이썬 실행 위치가 아니다.
OHLCV 데이터 루트는 사용자의 실제 실행 위치 또는 기존 로컬 백테스트 환경을 기준으로 찾아야 한다.
저장소 접근 경로를 cwd로 강제하면 데이터 루트가 잘못 해석된다.

필수 규칙
1. wrapper 또는 생성형 실행 파일은 subprocess.run에서 cwd를 저장소 접근 경로로 강제하지 않는다.
2. subprocess 실행 cwd는 사용자가 wrapper를 실행한 launch_cwd를 유지한다.
3. 저장소 접근 경로는 원본 기준 파일 읽기, 생성 파일 저장, local_results 결과 저장에만 사용한다.
4. 결과 저장 경로는 C:\Users\user\Documents\GitHub\-\local_results\{BATCH} 로 강제한다.
5. 데이터 루트는 launch_cwd 기준으로 자동 탐색하거나, 사용자가 --data-root로 명시한 경로를 우선한다.
6. 실행 로그에는 [LAUNCH_CWD], [DATA_ROOT], [RESULTS_DIR]를 모두 출력한다.
7. 결과 저장 경로와 데이터 루트를 동시에 강제할 때도 기준선 조건, base_spec, BASELINES, entry/exit 엔진, parent gate는 수정하지 않는다.

권장 데이터 루트 탐색 후보
- launch_cwd / 코인 / Data / time
- launch_cwd.parent / Data / time
- launch_cwd.parent / 코인 / Data / time
- launch_cwd.parent.parent / 코인 / Data / time
- C:\Users\user\Desktop\LCD\파이썬\코인\Data\time

적용 기준
8V24 이후 wrapper는 launch_cwd를 유지하고, 데이터 루트는 LOB_FORCE_DATA_ROOT 또는 자동 탐색 결과를 generated 파일에 주입한다.
