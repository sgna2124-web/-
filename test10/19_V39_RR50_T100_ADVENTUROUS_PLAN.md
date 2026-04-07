v39 목적

새 기준선은 rr50_t100이다.
이번 라운드는 미세 조정이 아니라, rr50 + timeout100 + rr_only + earlyreduce 코어 위에서 완전히 다른 축을 다시 흔드는 라운드다.

기준선 성과
- 최대 수익률 2721.3486%
- MDD -29.7717%
- 최대 보유 포지션 386
- 승률 18.4008%
- cd_value 1982.7131

핵심 철학
- rr_only, 매우 큰 RR, 매우 긴 timeout, earlyreduce는 현재 최강 코어 후보
- fail-fast 제거, earlyreduce 제거, timeout 추가 연장, RR 추가 확대, stop 철학 변경, 방향 분해, guard 결합을 한 번에 다시 본다
- wick_only와 cooldown 단독은 제외

실험 축
1. 코어 분해
- rr50_t100_no_failfast
- rr50_t100_no_earlyreduce

2. 시간 확대
- rr50_t200

3. RR 확대
- rr60_t100
- rr60_t200

4. stop/target 철학 변경
- rr50_t100_ema_or_rr
- rr50_t100_wick_or_atr

5. guard 결합
- rr50_t100_asym_short_s22
- rr50_t100_asym_both_balanced

6. 방향 분해
- rr50_t100_long_only
- rr50_t100_short_only

판정 기준
- 최대 수익률
- MDD
- 최대 보유 포지션
- 승률
- cd_value

핵심 질문
- timeout100보다 200이 더 유리한가
- rr50보다 rr60이 더 강한가
- fail-fast는 여전히 필요 없는가
- earlyreduce를 빼면 다시 크게 무너지는가
- 큰 RR 구조에서 stop/target 철학을 바꾸면 더 좋아지는가
- direction split가 다시 극단값을 보여주는가
