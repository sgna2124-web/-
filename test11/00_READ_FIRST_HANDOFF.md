TEST11 인수인계 문서

목적
- 이 폴더는 현재 대화창까지의 전략 탐색 과정을 다음 대화창의 어시스턴트가 빠르게 이어받기 위한 전용 인수인계 폴더다.
- 사용자는 이 파일들을 직접 읽기보다, 다음 어시스턴트가 읽고 이어서 실험을 진행하는 용도로 저장하라고 지시했다.
- 따라서 설명은 사람 친화적이면서도, 다음 어시스턴트가 즉시 행동할 수 있도록 구조화해두었다.

현재 프로젝트 운영 원칙
1. 현재 핵심 목표는 절대수익 극대화보다 MDD 통제다.
2. 레버리지 후보는 비레버리지 기준 MDD 10% 미만만 통과시킨다.
3. cd_value는 중요하지만 1차 필터가 아니라 2차 비교 지표다.
4. 현재는 롱 전용과 숏 전용 전략을 별도 개발한다.
5. 각각 개별적으로 저MDD 후보를 확보한 뒤, 나중에 포트폴리오처럼 결합한다.
6. 최근 사용자 요구: 파라미터 미세조정은 지양하고, 새로운 기준/새로운 철학/전혀 다른 전략처럼 보이는 시도를 더 많이 하길 원함.
7. 결과 보고 시 사용자가 선호하는 항목: 최대 수익률, MDD, 최대 보유 포지션, 승률, cd_value. 다만 최근 요약 스크립트(master_summary.csv)에는 cd_value가 자동 저장되지 않으므로, 필요 시 별도 계산 또는 요약 스크립트 보완이 필요함.

중요한 판단 변화
- 과거에는 cd_value 상위 전략을 먼저 보고 레버리지를 고려했다.
- 하지만 실제 실험 결과, 고수익/고MDD 전략에 레버리지를 얹는 것보다 저MDD 전략에 레버리지를 얹는 쪽이 훨씬 실전적이라는 결론에 도달했다.
- 따라서 현재 평가 체계는 다음 순서다.
  a. 비레버리지 기준 MDD 10% 미만 후보만 추림
  b. 그 안에서 수익, PF, max_conc, 나중에는 cd_value 순으로 비교
  c. 그 뒤 필요 시 레버리지 검토

레버리지 관련 주의사항
- v42는 잘못된 10배 모델이었다. position_fraction을 0.10으로 올려 실제 총노출이 크게 왜곡되었고, 현실형 10배 모델로 보기에 부적절했다.
- v43에서 300분할 기준 10배(= position_fraction 10/300)를 사용해 모델을 바로잡았다.
- 사용자 지시로 현재는 다시 100분할, 비레버리지 기준으로 돌아와 저MDD 전용 전략 탐색을 계속하고 있다.

현재까지의 큰 결론
- 숏 전용은 다수의 MDD 10% 미만 전략이 이미 확보되었다.
- 롱 전용은 오랫동안 실패했으나, 최근 라운드(v51, v53, v55)에서 MDD 10% 미만 후보들이 생기기 시작했다.
- 행동 브레이크(behavioral guards)와 진입 모드 변경(diverse entry modes)이 특히 중요했다.

매우 중요한 코드/해석 주의사항
1. v53 base config / baseline 해석 주의
- v53 baseline은 이전 v51의 베스트 구조를 그대로 계승한 기준선이 아니다.
- 따라서 v53 baseline 수치만 보고 롱 전략이 퇴화했다고 단정하면 안 된다.
- v53의 의미는 baseline보다, behavioral guard 조합에서 나온 후보들에 있다.

2. v54/v55 러너와 base config 필드 불일치 주의
- scripts/run_backtest_batch_json_only_timeout18_time_reduce_v54_short_only_diverse_entry_modes.py 와 이를 재사용한 v55 러너는 실제로 다음 필드만 사용한다.
  dd_brake_trigger_pct
  dd_brake_freeze_steps
  reentry_gap_after_close_bars
  entry_gap_same_symbol_bars
  require_prior_signals_same_symbol
  prior_signal_window_bars
  first_signal_after_quiet_bars
  allowed_entry_hours_utc
  skip_dense_ts_threshold
- 즉 max_active_cap, max_per_symbol, loss_streak_* 같은 behavioral guard 계열 필드는 diverse entry modes 러너에서 직접 쓰이지 않는다.
- 따라서 v55 baseline_lossbrake 같은 이름은 실제 동작과 불일치할 수 있다. 이 부분은 반드시 정리/수정해야 한다.

3. 현재 summary 스크립트 한계
- recent master_summary.csv에는 cd_value가 자동 포함되지 않는다.
- 사용자는 앞으로 결과 표기 시 cd_value도 함께 보고 싶어 한다.
- 따라서 다음 단계 중 하나로 요약 스크립트 개편이 필요하다.
  a. cd_value를 master_summary에 포함
  b. 별도 summary 확장 스크립트 생성

다음 어시스턴트가 당장 해야 할 우선순위
1. test11/01_CURRENT_TOP_CANDIDATES.md 를 먼저 읽고 현재 롱/숏 후보군을 파악한다.
2. test11/02_EXPERIMENT_TIMELINE_V41_TO_V55.md 를 읽고 어느 라운드에서 어떤 철학이 먹혔는지 파악한다.
3. test11/03_NEXT_STEP_PLAN.md 를 읽고 후속 실험 방향을 정한다.
4. test11/04_GUARDRAILS_AND_REPORTING.md 를 읽고 사용자 선호 보고 형식과 해석 주의점을 확인한다.
5. test11/05_MACHINE_STATE.json 을 사용해 기계적으로 현재 상태를 참조한다.

사용자 성향/요구 요약
- 반복 설명보다 즉시 실행을 선호한다.
- 미세 파라미터 조정보다 구조적/행동적/운용 철학 변화 같은 새로운 시도를 선호한다.
- topN, top200 같은 강한 랭킹 기준을 불신한다.
- 현재는 MDD 통제가 가장 중요하며, 그 안에서 수익과 cd_value를 본다.
- 보고 시에는 최대 수익률, MDD, 최대 보유 포지션, 승률, cd_value를 선호한다.

현재 가장 중요한 한 줄 요약
- 지금 프로젝트는 “롱/숏 전용 저MDD 전략군을 개별적으로 확립한 뒤, 나중에 결합하는 단계”이며, 최근 가장 큰 성과는 behavioral guards와 diverse entry modes가 실제로 새로운 저MDD 후보를 만들어냈다는 점이다.
