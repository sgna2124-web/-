# 37_8V14_FULLDATA_RUNTIME_STALL_FIX

## 상황

8V14 fast full-data numba 실행본에서 첫 50개 심볼은 약 100초 내 정상 진행되었으나, 이후 8시간 동안 추가 진행 로그가 나오지 않는 정체 현상이 보고되었다.

## 판단

이 정체는 단순한 max_bars 제한 해제 때문으로 보지 않는다. 사용자는 기존에도 전체 데이터 길이를 활용해 백테스트했고, 대체로 30분~1시간 30분 안에 완료되었다. 이번 정체는 현재 8V14 fast full-data 코드의 실행 구조와 메모리 구조가 겹친 문제일 가능성이 높다.

핵심 의심 지점은 다음과 같다.

1. 기존 fast 파일은 ProcessPoolExecutor에 전체 심볼 작업을 한 번에 submit한다. 전체 데이터 + 400개 전략 + 다중 프로세스에서는 큐와 피클링 부담이 커진다.
2. 기본 workers가 CPU-1에 가까워질 수 있어, 각 워커가 대형 OHLCV CSV와 feature pack을 동시에 들고 있으면 메모리 스와핑이 발생할 수 있다.
3. worker 결과가 전략별 거래 리스트를 Python tuple 리스트 형태로 반환한다. full data에서 신호가 조밀한 전략이면 수백만 개 Python 객체가 누적되어 메인 프로세스가 급격히 무거워질 수 있다.
4. 기존 진행 출력은 완료된 future 기준이므로, 일부 심볼/워커가 오래 걸리거나 스와핑 상태가 되면 실제로 어느 심볼에서 막혔는지 알 수 없다.

## 수정 방향

대화창에 새 파일로 `run_8v14_fast_full_data_numba_safe.py`를 제공했다. 이 파일은 기존 전략 400개와 기준선 비교 로직은 유지하되 실행 안정성을 강화한 버전이다.

주요 변경점:

1. workers 기본값을 CPU-1이 아니라 최대 4개로 제한한다.
2. 전체 future를 한 번에 submit하지 않고, inflight queue 방식으로 worker 수만큼 제한 제출한다.
3. 진행 로그를 기본 1개 심볼마다 출력한다.
4. 일정 시간 동안 완료 심볼이 없으면 HEARTBEAT 로그를 출력해 현재 실행 중인 심볼, 경과 시간, 파일 크기를 확인할 수 있게 했다.
5. 파일 처리 순서를 기본 `size_desc`로 바꿔 큰 CSV를 먼저 처리한다. 끝부분에 거대 심볼이 몰려 전체 진행이 멈춘 것처럼 보이는 현상을 줄인다.
6. 거래 결과 저장 구조를 Python tuple 리스트에서 numpy array chunk 구조로 바꿨다. 전체 거래 이벤트 수가 많을 때 메모리 부담을 크게 줄인다.
7. `--max-tasks-per-child` 옵션을 추가해 필요 시 워커를 주기적으로 재시작할 수 있게 했다.

## 실행 권장값

우선 아래처럼 실행한다.

```bash
python run_8v14_fast_full_data_numba_safe.py --workers 4 --progress-every 1 --heartbeat-sec 60 --inflight-per-worker 1 --file-order size_desc
```

만약 HEARTBEAT가 반복되고 컴퓨터 메모리 사용률이 높으면 다음 단계로 낮춘다.

```bash
python run_8v14_fast_full_data_numba_safe.py --workers 2 --progress-every 1 --heartbeat-sec 60 --inflight-per-worker 1 --file-order size_desc
```

특정 심볼 하나가 계속 오래 걸리는지 확인해야 할 때는 HEARTBEAT 로그의 `symbol`, `age`, `size`를 본다. 특정 대형 심볼 또는 데이터 이상 심볼이 확인되면 그 심볼을 별도로 단독 실행해 원인을 분리한다.

## 다음 인수인계 규칙

1. full data 테스트에서 임의 max_bars 제한을 다시 넣지 않는다.
2. 속도 문제를 해결할 때는 데이터 제한이 아니라 실행 구조, 메모리 구조, 로그 구조를 먼저 점검한다.
3. 400개 전략군처럼 결과 이벤트가 폭증할 수 있는 실험은 Python tuple 리스트 누적을 피하고 numpy array chunk 또는 스트리밍 집계 구조를 우선 고려한다.
4. 장시간 백테스트 파일은 반드시 심볼 단위 진행 로그와 heartbeat 로그를 포함시킨다.
5. 기준선 비교 출력 원칙은 유지한다. 기준선 1위가 갱신되지 않았으면 불필요한 기준선 비교 출력은 하지 않는다.
