현재 공식 기준선

이 문서는 새 대화창의 어시스턴트가 현재 공식 long 1위와 short 1위를 즉시 파악하기 위한 기준선 문서다.
비교는 long-only와 short-only를 분리하여 수행한다.

현재 프로젝트의 공식 판단 기준
공식 판단 기준은 MDD와 cd_value다.
현재 프로젝트에서 cd_value의 공식 정의는 다음과 같다.
cd_value = max_return_pct / max_drawdown_pct
final_return_pct는 참고 지표다.

중요한 주의사항
현재 기준선 교체 판단은 동일한 프로젝트 규칙을 따른 결과끼리 비교한다.
즉 신규 전략은 MDD 5% 미만을 먼저 통과해야 하며, 그 다음 cd_value(max_return_pct 기반)를 본다.
거래 수가 0이거나 극단적으로 적은 전략은 cd_value 숫자가 높아 보여도 공식 기준선으로 승격하지 않는다.

보조 후보 규칙
MDD가 5%를 넘더라도 cd_value가 현 공식 long 기준선 121.5300 이상이면 candidate_cd_win_mdd_fail로 기록한다.
이 표시는 공식 승격이 아니라, 다음 개선 시도의 우선 검토 후보라는 뜻이다.

1. 현재 공식 long-only 기준선
strategy_name: 6V2_L01_doubleflush_core
family: long_only_doubleflush_cap_reclaim
version_reference: 6V2_LONG10_REVIEWED
result_path: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/
summary_file: local_results/6V2_LONG10_REVIEWED/6V2_L01_doubleflush_core/summary.json
final_return_pct: 23.6961
max_return_pct: 23.9191
max_drawdown_pct: 1.7512
current_cd_value: 121.5300
win_rate_pct: 58.1081
trades: 592
status: official_long_reference
note: 현재 공식 long 기준선은 변동 없음.

2. 현재 공식 short-only 기준선
strategy_name: short_beh_dd_brake
family: short_only_behavioral_guards
version_reference: legacy_v52
legacy_final_return_pct: 311.5456
legacy_mdd_pct: 4.7589
legacy_cd_value: 391.9606
status: official_short_reference

3. 직전 long 기준선 보관
strategy_name: long_hybrid_wick_bridge_halfhalf
family: long_only_hybrid_wick_bridge
version_reference: legacy_v67
legacy_final_return_pct: 9.9603
legacy_mdd_pct: 1.0456
legacy_cd_value: 108.8106
status: archived_previous_long_reference

4. mixed historical reference
strategy_name: official_top200_reference
legacy_final_return_pct: 1120.69995
legacy_mdd_pct: 36.03441
legacy_cd_value: 780.8279
status: archive_reference_only

5. 최근 상태 메모
6V2_LONG10_REVIEWED에서 long 공식 기준선이 처음 교체되었다.
- 1위: 6V2_L01_doubleflush_core | final_return_pct 23.6961 | max_return_pct 23.9191 | max_drawdown_pct 1.7512 | cd_value 121.5300 | trades 592
- 2위: 6V2_L04_doubleflush_extremeclose | final_return_pct 19.2086 | max_return_pct 19.4782 | max_drawdown_pct 1.0102 | cd_value 118.0043 | trades 442

6V3~6V5에서는 기준선 교체가 없었다.
핵심 학습은 다음과 같았다.
- post-signal 강화는 과선택화 또는 늦은 추격으로 악화되기 쉬움
- hard state gate는 0~1 trade 문제를 만들기 쉬움
- soft score + spacing은 안정화에는 유효하지만 초과 엣지를 만들지는 못함

7V1에서는 신규 reversal family의 raw upside가 처음 확인되었다.
하지만 broad same-bar reversal은 MDD와 거래 수가 함께 커졌다.

7V2에서는 신규 family가 제한형 구조에서도 실제로 110대 cd까지 올라왔다.
- MDD<5 최고: 7V2_L09_V09_beartrap_extreme_synergy | final_return_pct 15.8330 | max_return_pct 16.0180 | max_drawdown_pct 2.5330 | cd_value 112.8990 | trades 730
- 다음: 7V2_L07_V08_wick_closedrive | final_return_pct 15.3392 | max_return_pct 15.7100 | max_drawdown_pct 3.3512 | cd_value 111.4740 | trades 1439
이로써 L09 beartrap family가 1순위, L07 wick family가 2순위로 굳어졌다.

7V3에서도 기준선 교체는 없었다.
- MDD<5 최고: 7V3_L09_V02_beartrap_extreme_synergy | final_return_pct 15.8330 | max_return_pct 16.0180 | max_drawdown_pct 2.5330 | cd_value 112.8990 | trades 730
- 다음: 7V3_L07_V02_wick_drive_reclaim | final_return_pct 15.6410 | max_return_pct 16.0068 | max_drawdown_pct 3.2136 | cd_value 111.9247 | trades 1443
- 7V3에서는 속도 개선 구조가 실제 성과로 확인되어, 공통 feature/raw를 심볼당 한 번만 계산하는 실행 구조를 유지하기로 했다.

7V4에서도 공식 기준선 교체는 없었다.
- candidate_cd_win_mdd_fail 1위: 7V4_L09_V09_beartrap_cluster_pressure | final_return_pct 41.1544 | max_return_pct 42.1291 | max_drawdown_pct 11.2133 | cd_value 125.3264 | trades 6863
- candidate_cd_win_mdd_fail 2위: 7V4_L09_V03_beartrap_lowanchor_drive | final_return_pct 39.3617 | max_return_pct 40.1602 | max_drawdown_pct 11.9139 | cd_value 122.7583 | trades 7664
- MDD<5 최고: 7V4_L09_V02_beartrap_extreme_synergy | final_return_pct 15.8330 | max_return_pct 16.0180 | max_drawdown_pct 2.5330 | cd_value 112.8990 | trades 730
- 다음: 7V4_L07_V02_wick_drive_reclaim | final_return_pct 15.6410 | max_return_pct 16.0068 | max_drawdown_pct 3.2136 | cd_value 111.9247 | trades 1443
해석은 명확하다. L09 family 안에는 이미 기준선보다 높은 cd를 가진 개선 후보가 존재한다. 다만 MDD를 충분히 낮추지 못해 아직 공식 승격은 아니다.
따라서 다음 우선순위는 L09 family를 가장 먼저 다듬고, L07 family를 보조 축으로 유지하는 것이다.

6. 현재 우선순위
1) L09 beartrap family
2) L07 wick family
3) L10 balance family
4) L04 engulf family

7. 승격 규칙
신규 long 전략은 1번 기준선과 비교한다.
신규 short 전략은 2번 기준선과 비교한다.
새 전략 결과에는 최소한 final_return_pct, max_return_pct, max_drawdown_pct, cd_value, result_path가 포함되어야 한다.
현재 공식 1위를 교체하려면 challenger와 incumbent가 동일 계산 규칙으로 비교 가능해야 한다.
