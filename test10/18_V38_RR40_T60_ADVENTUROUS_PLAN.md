v38 목적

새 기준선은 rr40_t60이다.
이번 라운드는 미세 조정이 아니라, rr40 + timeout60 + rr_only + earlyreduce 코어 위에서 완전히 다른 축을 다시 흔드는 라운드다.

기준선 성과
- 최대 수익률 2848.9979%
- MDD -34.5016%
- 최대 보유 포지션 388
- 승률 22.0711%
- cd_value 1932.7986

핵심 철학
- rr_only, 큰 RR, 긴 timeout, earlyreduce는 현재 최강 코어 후보
- fail-fast 제거, timeout 추가 연장, RR 추가 확대, stop 철학 변경, direction split, guard 결합을 한 번에 다시 본다
- 이미 죽은 cooldown과 wick_only는 제외

실험 축
1. 코어 분해
- rr40_t60_no_failfast
- rr40_t60_no_earlyreduce

2. 시간 확대
- rr40_t100

3. RR 확대
- rr50_t60
- rr50_t100

4. stop 철학 변경
- rr40_t60_ema_or_rr
- rr40_t60_wick_or_atr
- rr40_t60_asym_both_wick_or_atr

5. guard 결합
- rr40_t60_asym_short_s22
- rr40_t60_asym_both_balanced

6. 방향 분해
- rr40_t60_long_only
- rr40_t60_short_only

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

핵심 질문
- timeout60보다 100이 더 유리한가
- rr40보다 rr50이 더 강한가
- fail-fast는 여전히 필요 없는가
- 큰 RR 구조에서 stop 철학을 바꾸면 MDD가 개선되는가
- short/asym guard가 큰 수익 훼손 없이 MDD를 더 줄일 수 있는가
