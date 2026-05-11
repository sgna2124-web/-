# LONG_MAIN_DEV_V11 결과 메모

## 기준
- 기준선: 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20
- 기준선 진입 조건: V09 cluster_pressure AND anchor_extreme AND guard_vol18 AND TP03 gate
- 기준선 청산 조건: atr_stop=1.01, rr_target=2.90, max_hold_bars=21, cooldown_bars=31
- 수수료: round_trip_cost_bps=8.0
- 자산분할: position_fraction=0.01

## 이번 개발 방향
- 기준선 child_entry를 기본으로 두고 cluster 강도, reclaim 품질, 거래량 클라이맥스, 추세 손상, 낙하 칼날 제거를 구조적으로 분리 검증했다.
- CPU/메모리 부하를 낮추기 위해 기본 workers=1, 결과 폴더는 Path.cwd() 아래에만 생성하도록 고정했다.
- 캔들 제한과 종목 제한은 기본값으로 두지 않았다.

## 다음 확인 포인트
- summary_long_main_mdd_lt5.csv에서 official_cd_value 기준 1위가 기준선 cd=311.37506758074795를 넘는지 확인한다.
- baseline_audit.json에서 LM11_00_BASELINE_V6가 기준선 기록과 얼마나 일치하는지 먼저 본다.
- 기준선과 다르게 나오면 V12 원본 compute_entry_masks와 parent_entry 구현 차이를 우선 보정한다.

## long_main 1위 후보
- strategy: LM11_01_CLUSTER_3_CONFIRM
- official_cd_value: 118.5786260909954
- max_return_pct: 20.128758114451408
- max_drawdown_pct: 1.2903921157489395
- trades: 420
- verdict: baseline_fail

## long_max 계산식 1위 후보
- strategy: LM11_01_CLUSTER_3_CONFIRM
- official_cd_value: 118.5786260909954
- max_return_pct: 20.128758114451408
- max_drawdown_pct: 1.2903921157489395
- trades: 420
- verdict: baseline_fail
