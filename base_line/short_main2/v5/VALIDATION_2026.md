short_main2 v5 2026 validation

대상 전략
V4R05_stop262_rr620_t390_ff15

비교 기준
short_main2/v4 공식 기준선
V3MIX07_N02_stop255_rr630_t375

검증 목적
2025 train과 2025 Q4 제외 검증을 통과한 V4R05가 2026 holdout 구간에서도 붕괴하지 않는지 확인한다.
2026 데이터는 기준선 갱신용 train으로 사용하지 않는다.
2026 결과는 validation 보조 근거로만 사용한다.

검증 결과 출처
local_results/short_main/SHORT_MAIN2_V4R05_2026_QUARTER_VALIDATION_V1_1_SKIP_EMPTY/v4r05_2026_quarter_summary_compact.csv

실행 조건
period_set: quarterly_2026_available
period_labels:
FULL_TO_2026_END
2026_YTD_ONLY
2026_Q1_ONLY

주의
현재 데이터 기준 2026_Q2_ONLY의 유효 심볼 수가 0개였으므로 Q2 이후는 검증하지 않았다.
2026_YTD_ONLY와 2026_Q1_ONLY 결과는 동일하다.

환경
initial_asset: 100.0
position_fraction: 0.01
leverage: 1.0
fee_per_side: 0.0004
round_trip_fee: 0.0008
position_limit: 없음
load_errors: 0

V4R05 2026 Q1 성과
trades: 1932
win_rate_pct: 9.834368530020704
max_return_pct: 11.532665439025624
max_drawdown_pct: 2.066572846244019
official_cd_value: 109.22776166037053
profit_factor: 1.977895137634963
mtm_worstbar_max_drawdown_pct: 1.640001421461712
mtm_worstbar_cd_value: 109.83100615462072

V3MIX07 2026 Q1 성과
trades: 1939
win_rate_pct: 10.00515729757607
max_return_pct: 10.768182866713595
max_drawdown_pct: 2.185877830413352
official_cd_value: 108.34692571427838
profit_factor: 1.8672855375829094
mtm_worstbar_max_drawdown_pct: 1.7939997795672125
mtm_worstbar_cd_value: 108.88990994812465

2026 Q1 v5 개선폭
delta_2026_q1_cd_vs_v4: +0.880835946092148
delta_2026_q1_mdd_vs_v4: -0.11930498416933277
delta_2026_q1_pf_vs_v4: +0.11060960005205356
delta_2026_q1_mtm_worstbar_cd_vs_v4: +0.94109620649607
delta_2026_q1_mtm_worstbar_mdd_vs_v4: -0.15399835810550044

V4R05 FULL_TO_2026_END 성과
trades: 150329
max_return_pct: 144134.75209844712
max_drawdown_pct: 5.692488096031778
official_cd_value: 136024.20600490208
profit_factor: 1.986529784284138
mtm_worstbar_cd_value: 124100.77993420625

V3MIX07 FULL_TO_2026_END 성과
trades: 151208
max_return_pct: 125236.0679256071
max_drawdown_pct: 5.540389442518634
official_cd_value: 118391.9616505888
profit_factor: 1.9345681018670302
mtm_worstbar_cd_value: 107838.06648044978

FULL_TO_2026_END v5 개선폭
delta_full_to_2026_cd_vs_v4: +17632.244354313283
delta_full_to_2026_mdd_vs_v4: +0.15209865351314367
delta_full_to_2026_pf_vs_v4: +0.05196168241710786
delta_full_to_2026_mtm_worstbar_cd_vs_v4: +16262.71345375647
delta_full_to_2026_mtm_worstbar_mdd_vs_v4: +0.012113713280760052

판정
2026 Q1 validation에서 V4R05는 V3MIX07보다 우수했다.
특히 2026 Q1에서는 CD, PF, MTM CD가 개선되었고 realized MDD와 MTM worstbar MDD도 더 낮았다.
현재 데이터 기준 Q2 이후는 검증 불가다.
2026 validation 결과는 v5 기준선 승격의 보조 근거로 기록한다.
