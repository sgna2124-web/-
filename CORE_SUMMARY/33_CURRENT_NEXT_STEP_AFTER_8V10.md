CURRENT NEXT STEP AFTER 8V10

이 파일은 다음 대화창이 8V10 이후 현재 상태를 즉시 복원하기 위한 최신 포인터다.

공식 cd_value 계산식
cd_value = 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)
final_return_pct는 공식 cd_value 계산에 쓰지 않는다.
공식 승격은 MDD 5% 미만이어야 한다.

현재 공식 long 기준선
6V2_L01_doubleflush_core
max_return_pct: 23.9191
max_drawdown_pct: 1.7512
cd_value: 121.7490
trades: 592
status: official_long_reference 유지

8V10 결과 요약
batch: 8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP
failed_symbols: 0
공식 기준선 교체 없음.

8V10 MDD 5% 미만 cd_value 1위, 다음 후보 A
8V10_B_ANYCD_I013_I376_b_rescue_mix_b176
parent: 8V9_RAWV51_I013_entry_timing_window_r013
max_return_pct: 20.9416
max_drawdown_pct: 4.4791
cd_value: 115.524476
trades: 1714
win_rate_pct: 38.7981
해석: MDD 5% 미만, 거래 밀도 양호, max_return_pct 복원 성공. 다만 6V2 기준선 121.7490에는 미달.

8V10 MDD 무관 cd_value 1위, 다음 후보 B
8V10_B_ANYCD_I013_I302_b_trend_runner_b102
parent: 8V9_RAWV51_I013_entry_timing_window_r013
max_return_pct: 26.3362
max_drawdown_pct: 5.6679
cd_value: 119.175585
trades: 1263
win_rate_pct: 46.9517
해석: 수익 확장력은 기준선에 근접하지만 MDD가 5%를 초과해 공식 승격 불가. 다음 라운드에서 MDD를 4.9 이하로 압축할 최우선 후보.

8V10의 의미
8V8 best cd_value 105.766560, 8V9 best cd_value 105.640342에서 8V10 best under MDD5 cd_value 115.524476으로 큰 폭 개선되었다.
거래 수 제한을 두지 않는 방향이 맞다는 점을 재확인했다.
다만 공식 기준선 6V2의 cd_value 121.7490을 넘지 못했으므로 승격은 없다.

다음 작업 지시
1. 다음 개선은 후보 A와 후보 B를 각각 개선한다.
2. 거래 수 제한은 두지 않는다.
3. 단순 파라미터 조정은 아직 하지 않는다.
4. 후보 A는 MDD 5% 미만을 유지하면서 max_return_pct를 23~26%대로 끌어올리는 방향.
5. 후보 B는 max_return_pct 26%대 강점을 최대한 보존하면서 MDD 5.6679를 4.9 이하로 낮추는 방향.
6. b_rescue_mix와 b_trend_runner의 조건을 교차 이식한다.
7. strict, lowanchor, spring은 hard filter가 아니라 risk brake/rescue 보조 조건으로 사용한다.
8. post_loss_brake, soft_safe_mix는 edge를 죽이지 않도록 약한 사후 제어 모듈로만 사용한다.
9. deep_sweep은 단독 부모보다 MDD 안정화 보조로만 쓴다.
10. 다음 목표는 cd_value 121.7490 초과와 MDD 5% 미만을 동시에 달성하는 것이다.

필수 참조 파일
CORE_SUMMARY/32_8V10_LONG_DUAL_LEADERS_400_NO_TRADE_CAP_ADDENDUM.md
local_results/8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP/master_summary.txt
local_results/8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP/8V10_B_ANYCD_I013_I376_b_rescue_mix_b176/summary.json
local_results/8V10_LONG_DUAL_LEADERS_400_NEW_NO_TRADE_CAP/8V10_B_ANYCD_I013_I302_b_trend_runner_b102/summary.json
