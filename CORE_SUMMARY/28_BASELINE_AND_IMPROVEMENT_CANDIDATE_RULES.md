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

10. main / max 기준선 별칭 및 버전 표기 규칙
앞으로 long/short 개선은 main과 max 두 축으로 관리한다.
main은 MDD 5% 미만 중 cd_value 1위인 공식 기준선이다.
max는 MDD와 관계없는 전체 cd_value 1위인 raw 개선 기준선이다.

현재 기준선 별칭은 다음과 같이 고정한다.
long_main_v1 = 6V2_L01_doubleflush_core
- 의미: 롱 공식 기준선
- 조건: MDD 5% 미만 중 cd_value 1위
- max_return_pct: 23.9191
- max_drawdown_pct: 1.7512
- cd_value: 121.7490

long_max_v1 = 8V4_V51_V002_core_rare22_c1
- 의미: 롱 raw 개선 후보 기준선
- 조건: MDD 무관 롱 cd_value 1위
- max_return_pct: 44.2664
- max_drawdown_pct: 6.7587
- cd_value: 약 134.5172

short_main_v1 = short_beh_dd_brake
- 의미: 숏 공식 기준선
- 조건: MDD 5% 미만 중 cd_value 1위
- max_return_pct: 311.8122
- max_drawdown_pct: 4.7589
- cd_value: 약 392.2145

short_max_v1 = short_only_reference_1x
- 의미: 숏 raw 개선 후보 기준선
- 조건: MDD 무관 1x 숏 cd_value 1위
- max_return_pct: 394.6145
- max_drawdown_pct: 7.7792
- cd_value: 약 456.1372
- note: 10x 실험 short_only_leverage_10x는 숫자상 cd_value가 더 높지만 fail/레버리지 실험 성격이므로 공식 short_max 기준선에서 제외한다.

개선안 이름 표기법은 다음과 같이 고정한다.
long_main_v(기준선버전)_(개선안버전)_(전략명)
long_max_v(기준선버전)_(개선안버전)_(전략명)
short_main_v(기준선버전)_(개선안버전)_(전략명)
short_max_v(기준선버전)_(개선안버전)_(전략명)

예시:
long_main_v1_1_rescue_mix
long_main_v1_2_trend_runner_brake
long_max_v1_1_raw_mdd_compress
short_main_v1_1_dd_brake_refine
short_max_v1_1_reference_mdd_compress

버전 상승 규칙:
1) 기준선 자체가 유지되는 상태에서 개선 실험을 이어가면 마지막 개선안 버전만 올린다.
   예: long_main_v1_1, long_main_v1_2, long_main_v1_3
2) main 기준선을 넘어서는 전략이 나오면 해당 축의 기준선 버전을 v2로 승격한다.
   예: long_main_v2 = 신규 공식 long 기준선
3) max 기준선을 넘어서는 전략이 나오면 해당 축의 기준선 버전을 v2로 승격한다.
   예: long_max_v2 = 신규 long raw cd_value 기준선
4) 이후 기준선이 다시 올라갈 때마다 v3, v4, v5 순서로 올린다.
5) main과 max는 서로 독립적으로 승격한다. long_main_v2가 나와도 long_max는 그대로 v1일 수 있고, 반대도 가능하다.
6) long과 short도 독립적으로 관리한다.
7) 공식 승격은 여전히 MDD 5% 미만 조건을 통과해야 한다. max 기준선은 MDD 초과도 허용하되, raw 개선 축으로만 쓴다.

이 규칙은 즉시 고정 규칙으로 적용한다.
앞으로 max_return_pct / max_drawdown_pct는 공식 cd_value로 쓰지 않는다.
