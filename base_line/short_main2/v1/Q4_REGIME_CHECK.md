short_main2 v1 2025년 4분기 특이점 의존성 점검

목적
SM52_B04_stop230_score270_single_retest의 성과가 2025년 4분기 숏 유리 특이점에만 의존한 것인지 확인한다.

검증 파일
short_main_v15_B04_q4_regime_check_v5_1.py

결과 출처
local_results/short_main/SHORT_MAIN_V15_B04_Q4_REGIME_CHECK_V5_1

자동 판정
GENERAL_EDGE_CONFIRMED_EX_Q4_STILL_BEATS_V14

핵심 결론
2025년 4분기 특이점만으로 만들어진 전략은 아니다.
2025년 Q4를 제거해도 official_cd_value가 12736.7326으로 강하다.
Q4 단독 official_cd_value는 378.1772로 전체 성과를 단독으로 설명할 수준이 아니다.
따라서 short_main2 v1은 Q4 몰빵 전략이 아니라, 기본 엣지가 있고 후반 유리 구간에서 복리로 증폭된 전략으로 해석한다.

주요 수치
FULL_TRAIN_TO_2025_END
trades: 154015
max_return_pct: 53676.4626
max_drawdown_pct: 5.9231
official_cd_value: 50591.2024
profit_factor: 1.7648

EXCL_2025_Q4_ALL_BEFORE_2025_10_01
trades: 129976
max_return_pct: 13438.6469
max_drawdown_pct: 5.9231
official_cd_value: 12736.7326
profit_factor: 1.6422

PRE_2025_ALL_TO_2024_END
official_cd_value: 2048.8025
max_drawdown_pct: 3.9829

2025_PRE_Q4_ONLY
official_cd_value: 596.9068
max_drawdown_pct: 5.9231

2025_Q1_ONLY
official_cd_value: 177.9034

2025_Q2_ONLY
official_cd_value: 154.2001

2025_Q3_ONLY
official_cd_value: 195.0139

2025_Q4_ONLY
trades: 24058
max_return_pct: 299.3296
max_drawdown_pct: 5.2970
official_cd_value: 378.1772
profit_factor: 1.8182

해석
1. Q4 제거 구간의 official_cd_value는 12736.7326이다.
2. Q4 단독 official_cd_value는 378.1772이다.
3. 따라서 Q4 단독 성과가 전체 성과를 설명하지 않는다.
4. Q4는 2025년 분기 중 가장 좋은 구간이지만, 몰빵이라고 보기 어렵다.
5. 전체 성과가 큰 이유는 Q4 이전에 자산이 크게 불어난 상태에서 Q4 수익률이 뒤에 곱해졌기 때문이다.

운영 판단
short_main2 v1 기준선 갱신은 가능하다.
2026 holdout 검증은 다른 대화창에서 별도 수행한다.
2026 검증 전까지 short_main2 v1은 2025 train 기준 공식 기준선이며, 2026 성과는 아직 확정하지 않는다.
