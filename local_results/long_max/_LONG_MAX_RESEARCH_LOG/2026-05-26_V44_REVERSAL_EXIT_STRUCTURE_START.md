# V44 REVERSAL EXIT STRUCTURE START

실험 배치 예정:
- LONG_MAX_V25_2025_REVERSAL_EXIT_DEV_V44_STANDALONE

목적:
- V42 trend acceleration 실패.
- V43 trend pullback 실패.
- 따라서 기존 long_max 최상위 reversal entry를 유지하고 exit 구조만 개선한다.

기준 진입:
- entry_key: child::orig_V09_extreme_vol18::tp03
- body_atr_min: 0.48
- atr_stop: 1.30
- rr_target: 7.75
- max_hold_bars: 17
- cooldown_bars: 32

공식 참조 성과:
- final_return_pct: 533.1034733807187
- max_drawdown_pct: 1.0889127793824005
- official_cd_value: 627.2845620812368

실험 후보:
- fail_fast only
- time_reduce only
- trailing only
- fail_fast + time_reduce
- time_reduce + trailing
- fail_fast + time_reduce + trailing

후보 수:
- 32 total including V35 baseline and V38 reference

보수적 체결 규칙:
- trailing/time_reduce stop은 현재 캔들의 high가 아니라 이전 캔들까지의 high 기준으로만 상향한다.
- same-bar target/stop 충돌은 stop first 유지.

성공 판정:
- baseline reproduction true
- errors 0
- ruined false
- MDD < 5%
- V38 reference CD 627.2845620812368 초과

중요:
- 이 실험은 진입 철학 변경이 아니다.
- short_max v12처럼 entry 유지 + exit 개선이 long_max에도 먹히는지 확인하는 단계다.
