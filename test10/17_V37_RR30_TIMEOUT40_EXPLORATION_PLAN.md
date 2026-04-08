v37 목적

새 기준선은 rrcore_timeout40_rr30이다.
이번 라운드는 미세 조정이 아니라, rr30 + timeout40 + rr_only + earlyreduce 코어 위에서 어떤 구조를 더 얹거나 빼면 더 나아지는지 보는 라운드다.

기준선 성과
- 최대 수익률 2040.3289%
- MDD -36.6257%
- 최대 보유 포지션 387
- 승률 25.4323%
- cd_value 1357.3273

핵심 철학
- rr_only, rr30, timeout40, earlyreduce10/0.05는 현재 최강 코어 후보
- fail-fast 제거, timeout 연장, RR 확대, guard 결합, 방향 분해를 새로 시도
- 이미 약했던 wick_only와 cooldown 단독은 제외

실험 축
1. 코어 분해
- rr30_t40_no_failfast

2. 시간 확대
- rr30_t60
- rr30_t60_asym_short_s22

3. RR 확대/축소
- rr40_t40
- rr40_t60
- rr25_t40

4. guard 결합
- rr30_t40_asym_short_s22
- rr30_t40_asym_both_balanced
- rr30_t40_asym_short_s22_no_failfast

5. 방향 분해
- rr30_t40_long_only
- rr30_t40_short_only

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

핵심 질문
- timeout40이 더 길어질수록 더 유리한가
- rr30보다 rr40이 더 강한가
- fail-fast는 여전히 불필요한가
- short/asym guard가 수익을 덜 해치면서 MDD를 더 줄일 수 있는가
- 방향 분해 시 short-only가 여전히 방어형 극단값을 만드는가
