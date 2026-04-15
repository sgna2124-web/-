# 최근 에러 로그와 근본 원인

이 문서는 최근 대화에서 발생한 실행 실패들을 정리한 것이다.
다음 어시스턴트는 같은 에러를 반복하지 않기 위해 이 파일을 먼저 확인해야 한다.

## 1. v68, v69 계열 에러

에러 메시지:

`ModuleNotFoundError: No module named 'summarize_results_json_only_short_strict_cd'`

해석:

- workflow 또는 실행 스텝이 존재하지 않는 요약 모듈을 import 하거나 호출했다
- 결과 요약 모듈 경로/파일명/호출 방식 검증 없이 바로 연결한 것이 원인이다

교훈:

- workflow 후처리에서 외부 summarize 스크립트를 연결할 때는 실제 파일 존재 여부를 먼저 확인할 것
- 가장 안전한 방식은 workflow 내에서 최소한의 Python one-liner나 CSV 확인만 수행하는 것이다

## 2. v82 에러

에러 메시지:

`AttributeError: module 'v56mod' has no attribute 'run_batch'`

## 3. v83 에러

에러 메시지:

`AttributeError: module 'v57mod' has no attribute 'run_batch'`

해석:

- wrapper가 하위 모듈에 `run_batch`가 있을 것이라 가정했으나 실제로는 존재하지 않았다
- 즉, 기존 엔진을 감싼 새 스크립트를 만들 때 공개 API를 확인하지 않고 추측으로 호출했다

근본 원인:

1. 기존 스크립트가 함수 export를 하는지 직접 확인하지 않음
2. `if __name__ == '__main__'` 실행형 스크립트를 라이브러리처럼 잘못 취급함
3. 실제 실행 경로와 재사용 경로를 구분하지 않음

교훈:

- wrapper 설계 전 원본 스크립트의 진입점과 export 함수부터 확인할 것
- `run_batch`가 없으면 wrapper 안에서 base 로딩, experiment build, evaluation까지 직접 구성해야 한다
- 또는 원본 스크립트를 subprocess 방식으로 실행하는 편이 더 안전할 수 있다

## 4. 최근 v84, v85 시도에서 발생한 문제

최근에는 아래 문제가 겹쳤다.

### 4-1. 조합 파일 형식 불일치 위험

문제:

- 엔진은 보통 `group_name`, `experiments`, `overrides` 형식을 기대한다
- 새 조합 파일을 만들 때 이 구조를 벗어나면 build 단계에서 실패할 수 있다

교훈:

- 조합 JSON은 기존 성공 사례를 그대로 복사해 구조를 유지한 뒤 내용만 바꿀 것
- 새 형식을 발명하지 말 것

### 4-2. workflow YAML 문법 에러

사용자가 직접 보고한 메시지:

`Invalid workflow file`
`You have an error in your yaml syntax on line 32`

해석:

- heredoc 또는 run 블록 들여쓰기 문제로 YAML 파싱이 실패했을 가능성이 높다
- 단순한 shell 스텝을 넣었더라도 들여쓰기/문자열 처리 때문에 문법 오류가 날 수 있다

교훈:

- workflow는 최대한 단순하게 작성할 것
- run 블록 안에 heredoc를 넣지 말 것
- 되도록 한 줄 command 또는 별도 실행 스크립트를 사용할 것
- workflow 이름은 사용자의 규칙대로 숫자부터 시작할 것

### 4-3. 결과 경로 불일치 문제

문제:

- 실제 `results_dir`와 workflow에서 artifact/upload/summary 대상으로 지정한 경로가 일치하지 않으면 후처리 단계에서 실패하거나 결과를 못 찾는다

교훈:

- 새 전략 base를 만들 때 `results_dir`를 명시적으로 바꾸고,
- workflow artifact path도 정확히 동일하게 맞출 것

## 5. 최근 시도의 본질적 문제

중요한 점:

- 최근 실패는 전략 자체가 틀렸다기보다는 실행 계층을 검증 없이 덧대면서 생긴 문제였다
- 즉, 전략 연구보다 먼저 `실행 구조의 보수적 안정화`가 필요하다

## 6. 다음 작업자가 따라야 할 안전 규칙

1. 기존 성공 workflow 하나를 템플릿으로 복사한다
2. 이름, 실행 스크립트, artifact path만 최소 변경한다
3. heredoc, 복잡한 후처리, 불필요한 요약 단계는 넣지 않는다
4. wrapper 작성 전 원본 스크립트의 export 함수 존재를 직접 확인한다
5. 조합 파일 형식은 기존 성공 파일을 그대로 따른다
6. 새 workflow를 추가한 뒤엔 전략 내용보다 먼저 workflow 파싱 여부를 점검한다

이 6개를 지키지 않으면 같은 실패가 반복될 가능성이 높다.
