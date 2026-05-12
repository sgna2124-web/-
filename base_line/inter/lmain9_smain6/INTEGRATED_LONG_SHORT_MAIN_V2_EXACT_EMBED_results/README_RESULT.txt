INTEGRATED_LONG_MAIN_V9_SHORT_MAIN_V6_V2_EXACT_EMBED

기준선 내장 방식:
- long_main: frozen long runner 구조를 내장하고 v9 rr_target=3.50 적용
- short_main: base_line/short_main/v6/strategy_code.py 구조 내장
- 런타임 외부 기준선 파일 import/read 없음

long_strategy: 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20__DEV13_risk_stop_110__DEV14_risk_rr_320__DEV16_risk_rr_350
short_strategy: short_main_v6_timeout210
fee_per_side: 0.0004
position_fraction: 0.00125
max_total_positions: 800
symbol_files: 597
raw_long_candidates: 126615
raw_short_candidates: 52481
trades: 90720
long_trades: 57035
short_trades: 33685
wins: 25240
losses: 65480
win_rate_pct: 27.821869488536155
final_return_pct: 56.09996246187716
max_return_pct: 56.109478762906576
max_drawdown_pct: 1.8993854561222674
official_cd_value: 153.14435802765564
max_conc: 445
same_bar_trades: 19837
blocked_by_cap: 0
blocked_by_cooldown: 88376
blocked_by_short_dd_brake: 0
errors: 0

v2 수정 핵심:
- long cooldown 판정을 entry_i가 아니라 frozen runner와 같은 signal_i 기준으로 수정했다.
- 전략 조건 함수 내부는 통합을 위해 새로 해석하지 않았다.
- 통합 포트폴리오 레벨에서만 1/800 분할, 800 cap, 롱/숏 동시 보유를 적용한다.