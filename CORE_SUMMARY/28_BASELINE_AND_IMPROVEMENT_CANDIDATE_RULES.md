기준선 및 개선 후보 선정 규칙

이 문서는 앞으로 모든 long/short 결과 해석에서 적용할 기준선과 개선 후보 선정 규칙이다.

1. 공식 지표 정의
현재 프로젝트의 공식 cd_value는 사용자가 정의한 자산 기준 계산식으로 고정한다.

공식 cd_value 계산식:
cd_value = (base_asset * (1 - (abs(max_drawdown_pct) / 100))) * (1 + (max_return_pct / 100))

기본 base_asset은 100으로 둔다.
따라서 실무 계산식은 다음과 같다.
cd_value = 100 * (1 - (abs(max_drawdown_pct) / 100)) * (1 + (max_return_pct / 100))

해석:
1) 기초 자산 100에 MDD를 먼저 적용한다.
2) MDD 적용 후 남은 자산에 max_return_pct를 적용한다.
3) final_return_pct는 참고 지표이며 공식 cd_value 계산에 사용하지 않는다.
4) max_return_pct / max_drawdown_pct 방식은 폐기된 비공식 ratio이며, 앞으로 공식 cd_value로 쓰지 않는다.
5) 이전 문서의 official_ratio, current_cd_value_ratio, legacy_equity_cd_value 표기는 혼동을 만들 수 있으므로 신규 기록에서는 official_cd_value 또는 cd_value만 사용한다.

예시:
base_asset = 100, max_drawdown_pct = 10, max_return_pct = 10이면
cd_value = 100 * (1 - 0.10) * (1 + 0.10) = 99

2. 공식 기준선 선정 규칙
공식 기준선은 MDD 5% 미만 전략 중 공식 cd_value 1위인 전략이다.
즉 공식 승격은 다음 순서로 판단한다.
1) max_drawdown_pct < 5.0 조건을 통과한 전략만 공식 기준선 후보가 된다.
2) 그 후보들 중 공식 cd_value가 가장 높은 전략을 공식 기준선으로 본다.
3) 같은 cd_value 수준이면 max_return_pct, trades, 재현성, 구조 안정성을 보조 판단한다.
4) 거래 수가 0이거나 극단적으로 적은 전략은 cd_value가 높아도 공식 기준선으로 삼지 않는다.

3. 개선 후보 선정 규칙
각 배치가 끝나면 개선 후보는 최대 2개를 반드시 뽑는다.

후보 A: MDD 5% 미만 중 공식 cd_value 1위
- 공식 기준선 후보이자 safe branch 대표 후보다.
- 공식 기준선 교체 판단의 직접 비교 대상이다.

후보 B: MDD와 관계없이 전체 공식 cd_value 1위
- MDD가 5%를 넘더라도 개선 후보로 올린다.
- 목적은 raw edge가 강하지만 MDD 때문에 탈락한 구조를 다음 라운드에서 압축하기 위함이다.
- 단, cd_value가 공식 기준선보다 낮더라도 배치 내부 최고 raw 후보로 기록할 수 있다.
- cd_value가 공식 기준선보다 높고 MDD만 초과한 경우에는 candidate_cd_win_mdd_fail로 강하게 표시한다.

4. 후보 A와 후보 B가 같은 경우
후보 A와 후보 B가 동일 전략이면 중복 후보로 기록한다.
이 경우 해당 배치의 개선 후보는 실질적으로 1개지만, 문서에는 다음처럼 명시한다.
- baseline_candidate_under_mdd5: 해당 전략
- raw_cd_candidate_any_mdd: same_as_baseline_candidate

5. 현재 공식 long 기준선의 공식 cd_value
현재 공식 long 기준선은 6V2_L01_doubleflush_core다.
- max_return_pct: 23.9191
- max_drawdown_pct: 1.7512
- official_cd_value: 121.7490
계산: 100 * (1 - 0.017512) * (1 + 0.239191) = 121.7490

6. 8V6 적용 예시
8V6 전체 공식 cd_value 1위는 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 이다.
8V6 MDD 5% 미만 중 공식 cd_value 1위도 8V6_P2_CORE_BASE_I088_hybrid_cover_hyb18 이다.
따라서 8V6에서는 후보 A와 후보 B가 동일하다.
- max_return_pct: 5.2510
- max_drawdown_pct: 2.1312
- official_cd_value: 103.0070
해당 전략의 official_cd_value는 현재 공식 long 기준선 121.7490보다 낮으므로 공식 승격이나 기준선 초과 개선 후보는 아니다.

7. 8V7 적용 예시
8V7 전체 공식 cd_value 1위는 8V7_AB_BEST_I070_post_loss_brake_plb20 이다.
8V7 MDD 5% 미만 중 공식 cd_value 1위도 8V7_AB_BEST_I070_post_loss_brake_plb20 이다.
따라서 8V7에서도 후보 A와 후보 B가 동일하다.
- max_return_pct: 1.3290
- max_drawdown_pct: 0.2122
- official_cd_value: 101.1140
해당 전략의 official_cd_value는 현재 공식 long 기준선 121.7490보다 낮으므로 공식 승격이나 기준선 초과 개선 후보는 아니다.

8. 앞으로 결과 확인 시 반드시 남길 항목
각 신규 배치 결과를 확인하면 다음 항목을 문서에 기록한다.
- batch_name
- baseline_candidate_under_mdd5
- raw_cd_candidate_any_mdd
- candidate_cd_win_mdd_fail 여부
- 현재 공식 기준선 대비 cd_value 초과 여부
- max_return_pct, max_drawdown_pct, official_cd_value, trades
- 후보의 장점과 단점
- 다음 라운드에서 후보를 어떻게 개선할지

9. 현재 프로젝트 해석상 중요한 구분
공식 기준선 = MDD 5% 미만 중 official_cd_value 1위
개선 후보 = MDD 5% 미만 중 official_cd_value 1위 + MDD 관계없는 전체 official_cd_value 1위
candidate_cd_win_mdd_fail = official_cd_value는 공식 기준선보다 높지만 MDD 5%를 초과한 전략

이 규칙은 즉시 고정 규칙으로 적용한다.
앞으로 max_return_pct / max_drawdown_pct는 공식 cd_value로 쓰지 않는다.
