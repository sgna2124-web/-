v33 목적

이번 라운드는 미세 개선이 아니다.
대폭적인 조건 수정으로 결과 분산을 크게 만들어 보는 모험적 탐색 라운드다.
현재 기준선은 non_top200_reference_atr020이다.

기준선 성과
- 최대 수익률 1096.0061%
- MDD -40.9433%
- 최대 보유 포지션 386
- 승률 37.8582%
- cd_value 722.12695

핵심 철학
- 같은 축 미세조정 금지
- 조건 추가/제거를 동시에 수행
- long-only, short-only, cooldown, fail-fast, early reduce, stop/target mode 변경, 강한 quality guard를 한 번에 탐색
- 목표는 다양한 결과군을 의도적으로 만들어 다음 방향을 더 명확히 정하는 것

실험 축
1. 방향 제거
- adv_long_only
- adv_short_only

2. 거래 템포 제어
- adv_cooldown12
- adv_failfast12_r010
- adv_earlyreduce10_r005

3. 청산 구조 변경
- adv_ema_or_rr
- adv_rr_only
- adv_ema_or_rr_earlyreduce12_r010
- adv_rr_only_failfast10

4. stop 구조 변경
- adv_wick_only_asym_short_s22
- adv_wick_or_atr_asym_both_s22

5. 강한 진입 강화
- adv_balanced_l18_s24_asym_both
- adv_short_hard_s24_asym_both_cooldown12
- adv_asym_both_earlyreduce10_r005_cooldown12

우선순위
1순위
- adv_rr_only
- adv_wick_or_atr_asym_both_s22
- adv_short_hard_s24_asym_both_cooldown12

2순위
- adv_ema_or_rr_earlyreduce12_r010
- adv_asym_both_earlyreduce10_r005_cooldown12
- adv_failfast12_r010

3순위
- 나머지 전부

판정 기준
반드시 아래 5개를 같이 본다.
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

이번 라운드의 핵심 질문
- 특정 조건을 제거하거나 바꾸면 구조가 완전히 달라지는가
- long-only / short-only 중 어느 쪽이 문제 원인에 더 가깝나
- stop/target 구조 변경이 수익과 MDD를 동시에 크게 움직일 수 있나
- 강한 진입 강화가 max_conc를 실제로 줄일 수 있나
