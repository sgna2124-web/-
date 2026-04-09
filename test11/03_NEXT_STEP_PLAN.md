다음 단계 실행 계획

핵심 원칙
- 앞으로도 미세 파라미터 조정보다 새로운 기준, 새로운 운용 철학, 전혀 다른 전략처럼 보이는 시도를 우선한다.
- 다음 단계는 숫자 미세조정이 아니라 전략 철학의 추가 확장이어야 한다.

현재 유효한 큰 축
1. behavioral guards
- loss streak 브레이크
- drawdown 브레이크
- max active cap
- per symbol 제한

2. diverse entry modes
- confirmation 계열
- quiet-after-first 계열
- reentry gap 계열
- dense timestamp skip 계열
- 시간대 분리형

3. 기존 저MDD 구조 자체
- 숏: s22 계열, rr30_t40 계열, dd_brake 계열
- 롱: more_block 계열, lossbrake 계열, confirmation_plus_reentry 계열

다음 대화창에서 추천 실행 순서

1단계: v52/v54 교배 실험, 숏 전용
목표
- behavioral guard와 diverse entry mode를 교배해 새로운 숏 전용 전략군 생성

권장 실험 방향
- short_beh_dd_brake + dense_skip30
- short_beh_conservative_combo + reentry_gap48
- short_div_dense_skip30 + loss_streak_brake
- short_div_first_after_quiet48 + dd_brake
- short_div_reentry_gap48 + max_active_cap

핵심 질문
- 과밀 회피와 행동 브레이크를 동시에 넣으면 MDD 2% 이하 후보가 더 좋아질 수 있는가
- 수익 훼손 없이 max_conc를 더 낮출 수 있는가

2단계: v53/v55 교배 실험, 롱 전용
목표
- behavioral guard와 diverse entry mode를 결합해 롱 전용 메인형 강화

권장 실험 방향
- long_beh_max50_plus_lossbrake + confirmation_plus_reentry
- long_beh_conservative_combo + dense_skip30_confirm
- long_div_confirmation_plus_reentry + max_active_cap 50
- long_div_dense_skip30_confirm + loss_streak_brake
- long_push_u10_ema_rr_more_block + confirmation_plus_reentry

핵심 질문
- 롱 전용에서 PF 1.3 이상, MDD 10% 미만, 수익 70~100% 수준을 동시에 만족시키는 조합이 가능한가

3단계: delayed entry 또는 observed entry 실험
목표
- 신호가 뜨는 즉시 들어가지 않고, 몇 봉 관찰한 뒤 진입하는 다른 진입 철학 실험

권장 실험 아이디어
- 신호 후 1봉 대기 후 진입
- 신호 후 2봉 동안 반대 방향 과도 반등 또는 반락이 없을 때만 진입
- 신호 후 종가 기준으로 여전히 조건 유지 시 진입
- 신호 후 고점 또는 저점 재돌파 시 진입
- 신호 후 EMA20 재접촉 또는 이탈 확인 후 진입

4단계: reporting pipeline 정비
필수 작업
- cd_value를 master_summary에 포함하도록 요약 스크립트 보완
- 결과 표기 템플릿 통일
  최대 수익률
  MDD
  최대 보유 포지션
  승률
  PF
  cd_value
- baseline 해석 오류 가능성이 있는 라인, v53와 v55, 이름 정리

5단계: MDD 10% 미만 후보군만 별도 정리
목표
- 롱 전용과 숏 전용 전략 중 MDD 10% 미만인 후보들만 모아 cd_value 순으로 정리

권장 형태
- long_candidates_under10.csv
- short_candidates_under10.csv
- combined_under10_rank.md

현재 추천 우선 실행 대상
숏 전용
1. short_beh_dd_brake
2. short_div_dense_skip30
3. short_beh_conservative_combo
4. short_div_reentry_gap48

롱 전용
1. long_beh_max50_plus_lossbrake
2. long_div_confirmation_plus_reentry
3. long_beh_conservative_combo
4. long_div_dense_skip30_confirm

사용자 응답 시 권장 방식
- 질문이 없으면 바로 새 실험을 만들고 action 실행 준비까지 끝낸다.
- 결과가 나오면 상위 3개 또는 요청한 범위만 간단히 비교한다.
- 사용자가 원하면 다음 실험도 바로 이어간다.

한 줄 요약
- 숫자 조금 만지지 말고, v52/v54 숏 교배와 v53/v55 롱 교배, 그리고 delayed entry 계열을 우선적으로 확장한다.
