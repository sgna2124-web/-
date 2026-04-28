8V11 long/short main/max 400 addendum

version_reference: 8V11_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP
result_path: local_results/8V11_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/
summary_file: local_results/8V11_LONG_SHORT_MAIN_MAX_400_NEW_NO_TRADE_CAP/master_summary.txt
strategies: 400
failed_symbols: 0
cd_value_formula: 100 * (1 - abs(max_drawdown_pct)/100) * (1 + max_return_pct/100)
official_promotion_rule: max_drawdown_pct < 5.0

기준선 정의
long_main_v1: 6V2_L01_doubleflush_core | side long | cd 121.749029 | mdd 1.7512 | max 23.9191
long_max_v1: 8V4_V51_V002_core_rare22_c1 | side long | cd 134.515867 | mdd 6.7587 | max 44.2664
short_main_v1: short_beh_dd_brake | side short | cd 392.214469 | mdd 4.7589 | max 311.8122
short_max_v1: short_only_reference_1x | side short | cd 456.137449 | mdd 7.7792 | max 394.6145

결론
8V11은 공식 기준선 교체 없음.
long_main_v1, long_max_v1, short_main_v1, short_max_v1 모두 beat=False.
long 쪽은 long_max_v1 개선군에서 MDD 5% 미만 후보가 나왔지만, cd_value가 현 long_main_v1 기준선 121.749029를 넘지 못했다.
short 쪽은 거래 수가 지나치게 적고 cd_value가 100대 초반으로 기존 short 기준선과 비교할 수준이 아니었다.

long 결과
long_mdd5_cd_1: long_max_v1_51_lx_deep_absorb_lx051
parent: 8V4_V51_V002_core_rare22_c1
family: long_max_v1_improvements
group: lx_deep_absorb
trades: 1024
win_rate_pct: 47.5586
final_return_pct: 14.0480
max_return_pct: 18.2706
max_drawdown_pct: 3.5871
official_cd_value: 114.028108
verdict: official_mdd_pass_but_no_promotion

long_any_cd_1: same_as_long_mdd5_cd_1

long 해석
lx_deep_absorb는 V51 raw의 MDD를 3.5%대까지 낮추면서 max_return_pct 18.2706을 확보했다.
8V8~8V9의 105대 cd_value보다 개선됐고, 8V10의 MDD<5 1위 115.524476보다는 낮다.
8V11 long top은 안정성은 괜찮지만, 수익률 회복력이 부족하다.
long_main_v1을 넘기려면 같은 MDD 3.5~4.8% 구간에서 max_return_pct를 최소 25~27% 근처까지 끌어올려야 한다.
lx_deep_absorb 계열은 폐기 대상이 아니라 MDD 압축 모듈로 보관한다.
다만 lx_deep_absorb 단독 심화는 8V10의 b_rescue_mix/b_trend_runner보다 우선순위가 낮다.

long 상위권 구조 메모
1위 long_max_v1_51_lx_deep_absorb_lx051: trades 1024 | max 18.2706 | mdd 3.5871 | cd 114.028108
2위 long_max_v1_46_lx_deep_absorb_lx046: trades 1001 | max 17.5212 | mdd 3.3633 | cd 113.568662
3위 long_max_v1_41_lx_deep_absorb_lx041: trades 1001 | max 12.3987 | mdd 3.1439 | cd 108.864945
4위 long_max_v1_69_lx_trend_repair_lx069: trades 1316 | max 12.0073 | mdd 3.0864 | cd 108.550348
5위 long_max_v1_37_lx_sweep_runner_lx037: trades 965 | max 12.8054 | mdd 3.8653 | cd 108.445071

short 결과
short_mdd5_cd_1: short_max_v1_87_sx_vol_reversal_sx087
parent: short_only_reference_1x
family: short_max_v1_improvements
group: sx_vol_reversal
trades: 6
win_rate_pct: 16.6667
final_return_pct: 0.3790
max_return_pct: 0.3800
max_drawdown_pct: 0.0554
official_cd_value: 100.324360
verdict: official_mdd_pass_but_not_valid_baseline_candidate_due_to_extreme_low_trades

short_any_cd_1: same_as_short_mdd5_cd_1

short 해석
short 개선군은 사실상 실패다.
상위 후보들의 trades가 2~38 수준으로 너무 적고, short_main_v1 또는 short_max_v1과 비교 가능한 수익 구조를 만들지 못했다.
이번 short 개선 코드는 구조 탐색용으로는 의미가 있지만 다음 기준 후보로 삼지 않는다.
short는 기존 기준선 자체가 강하므로, 단순 전단 필터형 개선보다 원본 short edge를 보존하는 후행 위험 제어 또는 상태별 exit 조정이 필요하다.

기준선 변경 체크
long_main_v1 후보: long_max_v1_51_lx_deep_absorb_lx051 | delta_cd -7.720920 | beat False
long_max_v1 후보: long_max_v1_51_lx_deep_absorb_lx051 | delta_cd -20.487758 | beat False
short_main_v1 후보: short_max_v1_87_sx_vol_reversal_sx087 | delta_cd -291.890109 | beat False
short_max_v1 후보: short_max_v1_87_sx_vol_reversal_sx087 | delta_cd -355.813089 | beat False

다음 단계
다음 라운드는 8V10의 long 후보를 우선한다.
후보 A: 8V10_B_ANYCD_I013_I376_b_rescue_mix_b176 | MDD<5 cd 1위 | cd 115.524476 | max 20.9416 | mdd 4.4791 | trades 1714
후보 B: 8V10_B_ANYCD_I013_I302_b_trend_runner_b102 | MDD 무관 cd 1위 | cd 119.175585 | max 26.3362 | mdd 5.6679 | trades 1263
8V11의 lx_deep_absorb는 후보 A/B의 보조 모듈로만 사용한다.
목표 1: b_rescue_mix의 MDD 4.4~4.8%를 유지하면서 max_return_pct를 23.9% 이상으로 올린다.
목표 2: b_trend_runner의 max_return_pct 26%대는 유지하면서 MDD를 4.9% 이하로 낮춘다.
거래 수 제한은 두지 않는다. 거래 수가 많아 손실이면 조건의 질이 낮은 것으로 해석한다.
단순 파라미터 조정은 아직 하지 않는다. 조건 구조 개선을 우선한다.

재사용/금지 메모
재사용 가능: b_rescue_mix, b_trend_runner, lx_deep_absorb, lx_trend_repair의 일부 MDD 압축 로직.
주의: long_main_v1 직접 개선군은 지나치게 보수화되어 수익률이 거의 나오지 않았다.
주의: short 개선군은 거래 수가 극단적으로 부족했으므로 이번 설계를 그대로 반복하지 않는다.
금지: 8V6/8V7식 강한 전단 희소화, 100 trades 이하 수준의 과도한 안전화, max_return_pct를 10% 이하로 죽이는 hard conversion.
