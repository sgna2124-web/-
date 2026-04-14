# 최근 저장소 파일 맵과 시도 이력

이 문서는 최근 대화에서 생성되었거나 직접 언급된 파일들을 정리한 것이다.
다음 어시스턴트는 이 목록을 보고 무엇이 기존 성공 자산이고, 무엇이 최근 실패 시도인지 구분해야 한다.

## 1. 기존에 의미 있었던 기반 파일들

### 숏 계열 핵심 기반

- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v78_short_lane_governor.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v80_short_lane_governor_refine.py`
- `experiments/v80_short_base.json`
- `experiments/v80_short_combinations.json`
- `.github/workflows/v80_short_lane_governor_refine.yml`

의미:

- v80 계열은 숏 쪽 최근 실험의 기반 축으로 자주 참조되었다
- lane governor, hot/quiet, prior signal, reentry/entry gap 관련 실험의 기반이다

### 롱 계열 핵심 기반

- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v57_long_only_hybrid_guards_and_entry_modes.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v81_long_preserve_prior_no_reentry.py`
- `experiments/v81_long_base.json`
- `experiments/v81_long_combinations.json`

의미:

- v81 계열은 롱 쪽 최근 실험의 핵심 기반이다
- preserve prior, no reentry, hybrid guard, entry mode 조합의 축이다

## 2. 최근 실패/혼선이 있었던 파일들

### 2-1. v82, v83 계열

사용자 보고 에러:

- v82: `v56mod.run_batch` 없음
- v83: `v57mod.run_batch` 없음

의미:

- wrapper 설계가 잘못되었고, 하위 모듈 API를 추측으로 호출한 흔적이다

### 2-2. v84, v85 관련 새 시도들

최근 대화 중 아래 파일들이 새로 만들어졌거나 시도되었다.

- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v84_short_lane_governor_reclaim.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v85_long_preserve_reclaim.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v84_short_lane_governor_reclaim_fixed.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v85_long_preserve_reclaim_fixed.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v84_short_lane_governor_reclaim_runnable.py`
- `scripts/run_backtest_batch_json_only_timeout18_time_reduce_v85_long_preserve_reclaim_runnable.py`

관련 workflow 시도 파일:

- `.github/workflows/v84_short_lane_governor_reclaim_runnable.yml`
- `.github/workflows/v85_long_preserve_reclaim_runnable.yml`
- `.github/workflows/wf84_short_lane_governor_reclaim_runnable.yml`
- `.github/workflows/wf85_long_reclaim_run.yml`

주의:

- 위 파일들 중 일부는 개념 실험용이거나, 잘못된 구조를 교정하려는 중간 산물일 수 있다
- 다음 어시스턴트는 이 파일들을 곧바로 신뢰하지 말고 반드시 열어본 뒤, 실제 실행 구조와 경로를 검증해야 한다

## 3. 최근 시도의 의도 자체는 무엇이었나

### 숏 v84 의도

숏 쪽은 다음 아이디어를 시험하려 했다.

- hot 구간 reclaim 강화
- prior signal 요구 수 조정
- quiet 이후 첫 진입 제어
- dense timestamp 스킵 강화
- symbol cap 완화 또는 stacking 허용

즉, 단순 threshold 튜닝이 아니라 진입 허용 상태를 재구성하려는 시도였다.

### 롱 v85 의도

롱 쪽은 다음 아이디어를 시험하려 했다.

- preserve prior 구조 유지
- prior signal 1개/2개 요구 비교
- entry gap 축소 또는 유지
- quiet 이후 첫 진입 바 제어
- dense timestamp 상황에서 더 보수적으로 동작

즉, 롱은 숏처럼 공격적 확장이 아니라 release logic 조절 중심이었다.

## 4. 다음 작업자가 파일을 볼 때 판단 기준

### 그대로 써도 되는 가능성이 높은 것

- 과거에 실제 결과를 냈던 v78, v80, v57, v81 기반 파일들
- 기존에 성공적으로 동작했던 workflow 템플릿

### 검증 없이 쓰면 위험한 것

- 최근 급하게 만든 wrapper
- 최근 급하게 만든 workflow
- fixed, runnable 같은 이름이 붙은 중간 산물
- 새로 만든 조합/기반 JSON

## 5. 권장 정리 방식

다음 어시스턴트는 아래처럼 정리하면 된다.

1. 기존 성공 기반 파일을 기준본으로 지정
2. 실패 시도 파일은 전부 `실험 초안`으로 취급
3. 실제 복구는 기존 성공본을 복사하여 최소 수정으로 재구성
4. 새 workflow는 한 번에 하나만 만들고 즉시 파싱 가능 여부 확인

중요한 점은 버전 번호를 늘리는 것보다, 무엇이 검증된 토대인지 먼저 구분하는 것이다.
