# 8V7_AB_BEST_200 장단점 addendum

이 문서는 8V7_AB_BEST_200_FROM_8V6_CANDIDATE 결과를 반영한 최신 장단점 기록이다.

## 1. 배치 개요

batch_name: 8V7_AB_BEST_200_FROM_8V6_CANDIDATE
result_path: local_results/8V7_AB_BEST_200_FROM_8V6_CANDIDATE/
master_summary: local_results/8V7_AB_BEST_200_FROM_8V6_CANDIDATE/master_summary.txt
registry_file: local_results/8V7_AB_BEST_200_FROM_8V6_CANDIDATE/8V7_AB_BEST_200_FROM_8V6_CANDIDATE_registry.csv
strategies: 200
failed_symbols: 0
cd_value_formula: max_return_pct / max_drawdown_pct
official_promotion_rule: max_drawdown_pct < 5.0 and cd_value must beat current official long baseline

## 2. 현재 공식 long 기준선과 비교

current_official_long_baseline: 6V2_L01_doubleflush_core
baseline_max_return_pct: 23.9191
baseline_max_drawdown_pct: 1.7512
baseline_cd_value: 13.6587

8V7 최고 cd_value는 6.261968로, 공식 long 기준선 13.6587을 넘지 못했다.
따라서 공식 long 기준선 교체는 없다.

## 3. 후보 A / 후보 B

baseline_candidate_under_mdd5:
strategy_name: 8V7_AB_BEST_I070_post_loss_brake_plb20
parent: 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18
group: post_loss_brake
verdict: official_mdd_pass
trades: 93
win_rate_pct: 60.2151
final_return_pct: 1.1655
max_return_pct: 1.3290
max_drawdown_pct: 0.2122
cd_value: 6.261968
legacy_cd: 100.9508

raw_cd_candidate_any_mdd:
same_as_baseline_candidate_under_mdd5

candidate_cd_win_mdd_fail:
none

## 4. TOP 구조 요약

1위: 8V7_AB_BEST_I070_post_loss_brake_plb20 | trades 93 | max 1.3290 | mdd 0.2122 | cd 6.261968
2위: 8V7_AB_BEST_I068_post_loss_brake_plb18 | trades 104 | max 1.2213 | mdd 0.2154 | cd 5.669132
3위: 8V7_AB_BEST_I193_soft_safe_mix_ssm13 | trades 96 | max 0.9030 | mdd 0.1729 | cd 5.222699
4위: 8V7_AB_BEST_I198_soft_safe_mix_ssm18 | trades 68 | max 0.7782 | mdd 0.1550 | cd 5.018994
5위: 8V7_AB_BEST_I067_post_loss_brake_plb17 | trades 106 | max 1.0445 | mdd 0.2260 | cd 4.621651

8V7 상위권은 post_loss_brake와 soft_safe_mix가 대부분을 차지했다.
이 구조는 MDD를 매우 낮추는 데는 성공했지만, 거래 수와 max_return_pct를 동시에 크게 줄였다.

## 5. 장점

1. MDD 압축 능력은 매우 강하다.
상위권의 MDD가 0.15~0.42% 수준까지 내려갔다. 8V6도 MDD 압축에는 성공했지만, 8V7은 그보다 더 극단적인 방어형 결과를 만들었다.

2. post_loss_brake 계열은 손실 군집 차단 기능이 실제로 작동했다.
1위, 2위, 5위, 7위, 8위, 9위, 10위 등이 post_loss_brake다. 손실 이후 재진입을 늦추거나 차단하는 방식이 drawdown을 줄이는 데 유효하다는 근거가 생겼다.

3. soft_safe_mix는 보조 안정화 축으로 쓸 수 있다.
3위와 4위가 soft_safe_mix이며, 매우 낮은 MDD를 만들었다. 다만 단독 코어가 아니라 위험 구간에서 부분적으로만 켜야 한다.

4. failed_symbols가 0이다.
이번 실행은 환경 실패가 아니라 정상 백테스트 결과로 해석한다.

## 6. 단점

1. raw edge가 거의 사라졌다.
8V7 최고 max_return_pct는 1.3290%에 불과하다. 이는 8V6 최고 5.2510%보다도 낮고, 8V5 core 계열의 41~42%대와는 완전히 다른 수준이다.

2. 거래 수가 너무 적다.
1위의 trades는 93이다. 8V5 core_base/core_rare22_c1의 2277 trades와 비교하면 신호 대부분을 제거한 구조다. 이 정도 거래 수에서는 cd_value가 높아 보여도 공식 기준선 후보로 보기 어렵다.

3. 8V6 후보를 부모로 삼은 것이 edge 복원에는 부적합했다.
8V6 자체가 이미 edge를 과도하게 잘라낸 상태였기 때문에, 그 위에 post_loss_brake나 soft_safe_mix를 얹자 MDD는 더 낮아졌지만 수익 기회도 함께 사라졌다.

4. 공식 기준선 13.6587을 넘지 못했다.
MDD는 훌륭하지만 cd_value가 6.261968에 그쳤다. 공식 승격 조건과 개선 후보 조건 모두에서 강한 후보는 아니다.

## 7. 핵심 해석

8V7은 실패라기보다 중요한 방향 검증이다.
post_loss_brake와 soft_safe_mix는 MDD 압축 도구로는 유효하다.
그러나 8V6처럼 이미 희소화된 후보 위에 다시 방어 필터를 얹으면 V51 edge가 완전히 죽는다.

따라서 다음 라운드에서 8V7 상위 전략을 직접 부모로 삼으면 안 된다.
8V7의 top 전략은 너무 방어적이고, trades와 max_return_pct가 낮다.
다음 실험은 8V5의 core_base/core_rare22_c1 또는 strict/lowanchor safe branch로 되돌아가야 한다.
8V7에서 검증된 post_loss_brake와 soft_safe_mix는 전면 필터가 아니라 부분 브레이크, 쿨다운, 손실 군집 차단 모듈로만 이식한다.

## 8. 다음 실험 지시

우선순위는 다음과 같다.

1. 8V5_V51P_V001_core_base와 8V5_V51P_V002_core_rare22_c1을 다시 부모로 삼는다.
2. trades 목표는 1500~2300 구간으로 둔다. 500~700 trades 이하로 줄이는 구조는 피한다.
3. max_return_pct 목표는 최소 25% 이상, 이상적으로 35~42%대 보존이다.
4. MDD 목표는 6.28~6.31에서 4.9 이하로 낮추는 것이다.
5. post_loss_brake는 전체 진입 차단이 아니라 손실 직후 제한적 쿨다운으로만 사용한다.
6. soft_safe_mix는 strict/lowanchor safe branch의 보조 안정화 조건으로만 사용한다.
7. volshock_brake는 거래 수가 250~450까지 줄어들지만 max_return_pct가 3~4%대까지는 남았으므로, 아주 가벼운 위험 구간 회피로만 활용한다.
8. edge_restore는 이름과 달리 8V7에서는 edge를 복원하지 못했으므로 단독 축으로 쓰지 않는다.

## 9. 재사용 규칙

재사용 가능:
- post_loss_brake: 손실 군집 차단 모듈로 부분 사용
- soft_safe_mix: safe branch 보조 안정화 모듈로 부분 사용
- volshock_brake: 극단 변동성 직후 일시 회피 모듈로 제한 사용

재사용 주의:
- 8V7 top 전략 자체를 부모로 쓰지 않는다.
- post_loss_brake를 hard entry filter로 크게 걸지 않는다.
- trades가 100~300대로 떨어지는 조합은 공식 기준선 후보로 우선하지 않는다.
- max_return_pct 5% 미만 전략은 MDD가 낮아도 V51 핵심 개선 후보로 보지 않는다.

최신 결론:
V51 심화는 계속하되, 8V7 방식의 과도한 방어형 희소화는 폐기한다.
다음 라운드는 8V5 core 계열로 되돌아가 edge를 보존한 상태에서 8V7의 손실 군집 브레이크만 가볍게 이식해야 한다.
