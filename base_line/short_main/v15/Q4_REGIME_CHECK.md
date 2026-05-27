short_main v15 2025년 4분기 특이점 의존성 점검

목적
SM42_mdd10_aggr_v01_single_retest의 성과가 2025년 4분기 숏 유리 특이점에만 의존한 것인지 확인한다.

검증 파일
short_main_mdd10_aggr_v01_q4_regime_check_v4_3.py

결과 출처
local_results/short_main/SHORT_MAIN_MDD10_AGGR_V01_Q4_REGIME_CHECK_V4_3

자동 판정
GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14

핵심 결론
2025년 4분기 특이점만으로 만들어진 전략은 아니다.
2025년 Q4를 제거해도 official_cd_value가 기존 short_main v14 기준선을 넘는다.
다만 전체 CD 23902.932157469306은 Q4가 후반 복리 증폭 구간으로 작용하면서 크게 커진 면이 있다.
따라서 v15는 Q4 로또 전략이 아니라, 기본 엣지가 있고 후반 유리 구간에서 복리로 크게 증폭된 전략으로 해석한다.

주요 수치
FULL_TRAIN_TO_2025_END
trades: 140827
max_return_pct: 25200.7456885644
max_drawdown_pct: 5.524791831439535
official_cd_value: 23902.932157469306
profit_factor: 1.7005605337643628

EXCL_2025_Q4_ALL_BEFORE_2025_10_01
trades: 118497
max_return_pct: 7193.9920
max_drawdown_pct: 5.5248
official_cd_value: 6891.0141
profit_factor: 1.5959

PRE_2025_ALL_TO_2024_END
trades: 80450
max_return_pct: 1299.7022
max_drawdown_pct: 4.1247
official_cd_value: 1341.9680
profit_factor: 1.5429

2025_PRE_Q4_ONLY
trades: 38048
max_return_pct: 420.6532
max_drawdown_pct: 5.5248
official_cd_value: 491.8882
profit_factor: 1.6089

2025_Q1_ONLY
official_cd_value: 163.0315

2025_Q2_ONLY
official_cd_value: 143.5905

2025_Q3_ONLY
official_cd_value: 188.6334

2025_Q4_ONLY
trades: 22329
max_return_pct: 247.2814
max_drawdown_pct: 5.2209
official_cd_value: 329.1503
profit_factor: 1.7538

해석
1. Q4 제거 구간의 official_cd_value는 6891.0141이다.
2. 기존 short_main v14 official_cd_value는 6736.755883567657이다.
3. 따라서 Q4를 제거해도 v14를 근소하게 넘는다.
4. Q4 단독 official_cd_value는 329.1503으로, Q4만으로 v14를 이기는 구조가 아니다.
5. 전체 성과가 큰 이유는 Q4 이전에 자산이 크게 불어난 상태에서 Q4 수익률이 뒤에 곱해졌기 때문이다.

운영 판단
short_main v15 기준선 갱신은 가능하다.
다만 2026 holdout 검증은 다른 대화창에서 별도 수행한다.
2026 검증 전까지 v15는 2025 train 기준 공식 기준선이며, 2026 성과는 아직 확정하지 않는다.
