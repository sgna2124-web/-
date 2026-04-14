# 다음 단계 플레이북

이 문서는 다음 어시스턴트가 실제로 어떤 순서로 복구하고, 그 다음 어떤 전략 실험을 재개해야 하는지 단계별로 정리한 것이다.

## 1. 1차 목표: 실행 구조 안정화

전략 개발보다 먼저 아래를 수행한다.

### Step 1. 기준본 선택

숏은 아래 기준본에서 시작한다.

- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v80_short_lane_governor_refine.py`
- `.github/workflows/v80_short_lane_governor_refine.yml`

롱은 아래 기준본에서 시작한다.

- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v81_long_preserve_prior_no_reentry.py`
- 기존에 실제로 동작했던 롱 계열 workflow

### Step 2. 공개 API 확인

새 wrapper를 만들기 전에 원본 파일을 열어서 아래를 확인한다.

- `run_batch` 같은 export 함수가 실제로 있는가
- 아니면 단순 실행형 스크립트인가
- base/combinations JSON을 어떤 형식으로 기대하는가
- 결과 디렉터리를 어디로 쓰는가

### Step 3. workflow는 최소 변경만 수행

새 workflow를 만들 경우 아래 원칙만 따른다.

1. 기존 성공 workflow를 그대로 복사
2. `name`, 실행 파일 경로, artifact path만 수정
3. 요약 단계, heredoc, 부가 출력, 복잡한 shell 조건문은 넣지 않음
4. 사용자 규칙에 맞게 workflow 이름은 숫자부터 시작

### Step 4. 조합 파일 또는 그룹 구조 검증

새 조합을 외부 JSON으로 둘 경우, 기존 성공 사례의 형식을 그대로 복사한다.
가장 안전한 방법은 기존 성공 JSON의 shape를 바꾸지 않고, 실험 이름과 override 내용만 바꾸는 것이다.

### Step 5. 한 번에 하나만 실행

실행 복구 단계에서는 여러 workflow를 동시에 만들지 않는다.
하나를 정상 실행시킨 다음 다음 하나로 넘어간다.

## 2. 2차 목표: 전략 개발 재개

실행 구조가 안정화되면 그 다음부터 전략 개발을 재개한다.

### 숏 전략 재개 방향

숏은 다음 순서가 적절하다.

1. 시간 세션 기반 governor를 그대로 반복하지 말고, 변동성 상태 기반 governor로 전환
2. hot/quiet를 시간대 대신 아래 상태값으로 치환 검토
   - 최근 ATR 확장률
   - wick burst 빈도
   - dense signal cluster 여부
   - 직전 N bars 내 signal arrival density
3. reclaim 허용 여부를 시간대가 아니라 상태 조합으로 판별
4. prior signal 요구와 stacking 허용을 상태별로 다르게 적용

숏의 핵심 질문:

- 과열/과확산 상태에서 표준 진입은 죽이고 reclaim만 받게 할 수 있는가
- dense cluster 구간에서 overtrade를 억제하면서 peak return을 유지할 수 있는가

### 롱 전략 재개 방향

롱은 다음 순서가 적절하다.

1. preserve prior 구조 유지
2. 진입 조건보다 `재진입 해제 시점`을 상태 기반으로 재설계
3. quiet 이후 첫 진입 허용 조건을 시간 기반 대신 상태 기반으로 바꿔보기
4. dense timestamp나 동시 신호 밀집 구간에서 더 보수적인 release logic 적용

롱의 핵심 질문:

- 신호를 더 많이 잡는 것보다, 어떤 상태에서 잠금을 풀어야 MDD를 지키며 cd_value를 높일 수 있는가

## 3. 결과 보고 규칙

결과가 나오면 아래처럼만 보고한다.

1. 전체 숏 1위 갱신 여부
2. 전체 롱 1위 갱신 여부
3. 갱신 실패 시 왜 실패했는지 구조적으로 설명
4. 다음 실험은 기존 실패 이유를 반영해서 제안

상위 여러 개를 길게 나열하지 않는다. 사용자는 현재 `전체 1위 기준 비교`만 원한다.

## 4. 절대 금지 사항

1. 단순 파라미터 튜닝으로 버전 수만 늘리는 것
2. 사용자가 이미 반박한 시간 세션 논리를 그대로 반복하는 것
3. wrapper의 공개 함수 존재를 확인하지 않고 추측으로 호출하는 것
4. YAML workflow에 복잡한 요약/후처리 로직을 넣는 것
5. 실행 검증 없이 새 버전을 여러 개 동시에 만드는 것

## 5. 권장 실행 순서 요약

가장 안전한 실제 작업 순서는 아래와 같다.

1. 기준본 workflow 1개 선택
2. 기준본 script 1개 선택
3. export 함수/입력 형식/결과 경로 확인
4. 최소 수정판 1개만 생성
5. workflow 파싱 및 실행 확인
6. 그 다음에만 새 전략 조합 적용
7. 결과는 전체 롱/숏 1위와만 비교

이 순서를 지키면 최근 반복된 실행 계층 실패를 크게 줄일 수 있다.
