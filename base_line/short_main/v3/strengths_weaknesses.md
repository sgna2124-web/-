# short_main v3 기준선 장단점

전략명: SM15_B10_rr575_tr8_f005
부모 기준선: short_beh_dd_brake
축: short_main
상태: v1.5 SM24 주변값 개발 결과 기준 short_main 1위 후보

1. 현재 성과

trades: 28313
wins: 4136
losses: 24177
win_rate_pct: 14.608130540741001
final_asset: 431.06426729450357
final_return_pct: 331.06426729450357
peak_asset: 431.3434403627648
max_return_pct: 331.3434403627648
max_drawdown_pct: 3.9772559021280185
official_cd_value: 414.18780792249464
pf: 1.4757306514967135
max_conc: 286
max_conc_unique_symbols: 286
same_bar_trades: 3359
active_leftover: 0
gross_profit: 1026.9712185345038
gross_loss: 695.9069512400048
raw_trades_generated: 34107
errors: 0

2. 핵심 장점

1. MDD가 4% 미만이다.
기존 short_main v2의 MDD는 4.4066%였고, v3는 3.9773%다. short_main의 방어 목적에 더 잘 맞는다.

2. 수익률도 동시에 개선됐다.
max_return_pct가 322.7577%에서 331.3434%로 상승했다. 단순 방어형 개선이 아니라 수익성과 방어력이 동시에 좋아졌다.

3. official_cd_value가 의미 있게 개선됐다.
v2 official_cd_value는 404.1284였고, v3는 414.1878이다. 개선폭은 +10.0594다.

4. 거래 수가 거의 유지됐다.
v2 trades는 28308이고, v3 trades는 28313이다. 진입 조건을 훼손하지 않았기 때문에 main 축의 표본 수가 유지됐다.

5. active_leftover가 0이다.
백테스트 종료 시 미청산 포지션이 남지 않는다.

6. 진입 조건을 바꾸지 않았다.
short_dev, rsi, wick, score 조건은 유지하고 청산/위험관리만 조정했다. 따라서 기존 short_main 구조의 연속성이 강하다.

7. time_reduce 조정 효과가 명확하다.
기존 time_reduce_bars 10을 8로 당긴 것이 상위권 개선 후보에서 반복적으로 좋은 결과를 만들었다. v1.5 상위권 대부분이 time_reduce 조합이었다.

3. 약점

1. 승률은 더 낮아졌다.
기존 short_main v2의 win_rate는 약 15.257%였고, v3는 약 14.608%다. 승률 개선이 아니라 손익비와 위험관리 개선으로 성과가 좋아진 구조다.

2. rr_mult를 낮췄다.
rr_mult가 6.0에서 5.75로 낮아졌다. 이로 인해 목표 수익은 조금 가까워졌지만, 초대형 이익 거래의 상단은 일부 줄어들 수 있다.

3. max_conc는 개선되지 않았다.
max_conc는 286으로 v2와 동일하다. 실제 운용에서 동시 포지션 부담은 여전히 존재한다.

4. time_reduce_bars 8이 과최적화일 가능성이 있다.
v1.5 결과에서는 8봉 조기 위험 축소가 강했지만, 7~9봉 주변의 안정성을 추가로 확인할 필요가 있다.

5. dd_brake는 기존과 동일하다.
MDD 개선은 dd_brake 변화가 아니라 rr/time_reduce 변화에서 나왔다. drawdown regime 자체를 더 정교하게 제어한 것은 아니다.

4. v2 대비 개선 요약

v2 기준선: short_beh_dd_brake
v3 기준선: SM15_B10_rr575_tr8_f005

trades: 28308 -> 28313
max_return_pct: 322.7577 -> 331.3434
max_drawdown_pct: 4.4066 -> 3.9773
official_cd_value: 404.1284 -> 414.1878
pf: 1.4414 -> 1.4757
max_conc: 286 -> 286

개선의 핵심:
rr_mult 6.0 -> 5.75
time_reduce_bars 10 -> 8

5. SM24 대비 개선 요약

SM24 후보는 rr_mult 5.75만 적용한 후보였다.
SM15_B10은 여기에 time_reduce_bars 8을 적용했다.

SM24 대비:
trades: +2
max_return_pct: +4.4126
max_drawdown_pct: -0.3846
official_cd_value: +5.8792

해석:
SM24의 개선은 rr 5.75에서 시작되었고, v3의 최종 개선은 time_reduce 조정에서 완성되었다.

6. 보존해야 할 성질

1. MDD 4% 전후 또는 5% 미만
2. trades 28000 전후 유지
3. active_leftover 0
4. next_bar_open 진입
5. fee_per_side 0.0004
6. position_fraction 0.01 복리 구조
7. dd_brake의 portfolio evaluation 단계 작동
8. short_main의 숏 과열 진입 구조
9. rr 5.75 근처
10. time_reduce_bars 8 근처

7. 다음 개선 방향

1. B10 주변값을 더 좁게 확인한다.
rr_mult: 5.72, 5.75, 5.78, 5.80
time_reduce_bars: 6, 7, 8, 9, 10
time_reduce_to_risk_frac: 0.04, 0.05, 0.06

2. fail_fast와 time_reduce 상호작용을 확인한다.
fail_fast_bars: 8, 10, 12
fail_fast_min_progress_r: 0.08, 0.10, 0.12

3. dd_brake는 약하게만 흔든다.
dd_brake_trigger_pct: 0.025, 0.030, 0.035
dd_brake_freeze_steps: 3, 5, 7

4. max_conc 개선은 별도 축으로 본다.
현재 v3는 max_conc를 개선하지 못했다. 다음 단계에서 동시 진입 과밀을 줄이는 약한 필터를 별도로 실험할 수 있다.

5. 진입 조건 대수술은 아직 하지 않는다.
v1.4와 v1.5 모두 청산/위험관리 쪽에서 성과가 나왔다. 따라서 다음 단계에서도 진입 조건 자체를 크게 바꾸지 않는다.

8. 승격 판단

SM15_B10_rr575_tr8_f005는 short_main v3 기준선으로 승격할 만하다.
이유는 다음과 같다.

1. 기존 기준선보다 CD가 +10.0594 개선됐다.
2. 기존 기준선보다 MDD가 낮다.
3. 기존 기준선보다 수익률이 높다.
4. 거래 수가 유지됐다.
5. active_leftover가 0이다.
6. 진입 조건은 유지했고, 위험관리만 개선했다.

단, 다음 개발에서는 이 기준선을 부모로 삼되 7~9봉 time_reduce 주변값의 안정성을 추가로 확인해야 한다.
