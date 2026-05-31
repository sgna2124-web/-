short_main2 v2 2025년 4분기 의존성 및 실전성 점검

목적
SM60_C03_stop240_score270_timeout315의 성과가 2025년 4분기 숏 유리 특이점에만 의존한 것인지, 그리고 실제 계좌 평가손익과 비용 스트레스에서도 기준선 우위가 유지되는지 확인한다.

검증 파일
short_main2_v1_q4_realism_recheck_v1_2_1_MEMFIX.py

결과 출처
local_results/short_main/SHORT_MAIN2_V1_Q4_REALISM_RECHECK_V1_2_1_MEMFIX

검증 대상
C00_short_main2_v1_same
C03_stop240_score270_timeout315

검증 기간
FULL_TRAIN_TO_2025_END
EXCL_2025_Q4_ALL_BEFORE_2025_10_01
2025_Q4_ONLY

검증 비용
slippage_per_side 0.0
slippage_per_side 0.0005

실전성 조건
포지션 수 제한 없음.
이전 캔들 close 신호는 다음 캔들 open 진입.
같은 timestamp 청산 후 같은 timestamp 신규 진입 금지.
same-bar TP/SL 허용.
same-bar에서 stop과 target이 동시에 닿으면 stop 우선.
DD brake는 다음 timestamp부터 적용.
기간 종료 시 active position은 마지막 close로 forced_end 청산.
2026 데이터는 지표 계산 전 제외.
편도 슬리피지는 숏에 불리하게 적용.

자동 판정
q4_dependency_flag: GENERAL_EDGE_CONFIRMED

핵심 결론
2025년 Q4 특이점만으로 만들어진 전략은 아니다.
Q4를 제외해도 C03의 official_cd_value는 16979.64262769056으로 강하다.
Q4 단독 official_cd_value는 390.894405739309로 전체 성과를 단독으로 설명할 수준이 아니다.
따라서 short_main2 v2는 Q4 몰빵 전략이 아니라, Q4 이전에도 기본 엣지가 있고 후반 유리 구간에서 복리로 증폭된 전략으로 해석한다.

주요 수치, no slippage
FULL_TRAIN_TO_2025_END
trades: 152030
max_return_pct: 73746.55353592646
max_drawdown_pct: 5.888592725709996
official_cd_value: 69498.03075622236
profit_factor: 1.8286053579584032
mtm_close_max_drawdown_pct: 15.017466599306728
mtm_worstbar_max_drawdown_pct: 14.23277215250176
mtm_worstbar_cd_value: 63347.67993125091

EXCL_2025_Q4_ALL_BEFORE_2025_10_01
trades: 128404
max_return_pct: 17942.066439621896
max_drawdown_pct: 5.888592725709996
official_cd_value: 16979.64262769056
profit_factor: 1.7110313125769783
mtm_worstbar_cd_value: 15476.651550710532

2025_Q4_ONLY
trades: 23527
max_return_pct: 311.4467680751428
max_drawdown_pct: 4.995144920443351
official_cd_value: 390.894405739309
profit_factor: 1.8777264082396752
mtm_worstbar_cd_value: 386.0097145773214

Q4 비율
exq4_to_full_cd_ratio: 0.24431832733865372
q4_to_full_cd_ratio: 0.005624539306882607
exq4_to_full_mtm_worstbar_cd_ratio: 0.24431283935744477
q4_to_full_mtm_worstbar_cd_ratio: 0.006093509896435744

편도 0.05% 슬리피지 주요 수치
FULL_TRAIN_TO_2025_END
official_cd_value: 15177.194065003236
mtm_worstbar_cd_value: 14001.429941017343

EXCL_2025_Q4_ALL_BEFORE_2025_10_01
official_cd_value: 4617.4606705665265
mtm_worstbar_cd_value: 4259.174009564572

2025_Q4_ONLY
official_cd_value: 310.33515316809167
mtm_worstbar_cd_value: 308.43949858990305

기준선 C00 대비 주요 개선, no slippage, FULL
C00 official_cd_value: 50591.202383140204
C03 official_cd_value: 69498.03075622236
delta_official_cd_value: +18906.828373082157

C00 mtm_worstbar_cd_value: 46118.507807405054
C03 mtm_worstbar_cd_value: 63347.67993125091
delta_mtm_worstbar_cd_value: +17229.172123845856

C00 max_drawdown_pct: 5.923149464550481
C03 max_drawdown_pct: 5.888592725709996
delta_mdd: -0.034556738840485046

C00 mtm_worstbar_max_drawdown_pct: 14.283961553717994
C03 mtm_worstbar_max_drawdown_pct: 14.23277215250176
delta_mtm_worstbar_mdd: -0.05118940121623439

해석
1. C03은 전체 구간에서 C00보다 official_cd_value와 mtm_worstbar_cd_value가 높다.
2. C03은 Q4 제외 구간에서도 C00보다 official_cd_value와 mtm_worstbar_cd_value가 높다.
3. C03은 Q4 단독 구간에서도 C00보다 높다.
4. Q4 단독 CD가 전체 CD의 약 0.56%에 불과하므로 Q4 몰빵 전략이 아니다.
5. realized MDD는 5.8886%지만, mtm_close MDD는 약 15.0175%, mtm_worstbar MDD는 약 14.2328%다.
6. 앞으로 short_main2 계열 기준선 평가에는 realized MDD와 함께 MTM MDD를 반드시 기록한다.

운영 판단
short_main2 v2 기준선 갱신 가능.
2026 holdout 검증은 다른 대화창에서 별도 수행한다.
2026 검증 전까지 short_main2 v2는 2025 train 기준 공식 기준선이며, 2026 성과는 아직 확정하지 않는다.
