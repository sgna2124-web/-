SHORT_MAX v10 actual train DEV candidates v1

이 결과는 2025-12-31 23:59:59까지의 train 데이터만 사용한다.
2026-01-01 이후 데이터는 지표 계산 전부터 제외하며, 검증용 holdout으로 남긴다.

공식 엔진:
actual_bar_engine_no_same_timestamp_reentry_force_final_close_train_to_20251231

핵심:
- 같은 timestamp 청산 결과를 같은 timestamp 신규 진입에 사용하지 않는다.
- t close 신호는 t+1 open pending entry가 된다.
- same-bar TP/SL은 유지한다.
- train 종료 시 active 포지션은 마지막 close로 forced_end 정산한다.

기준선 gate:
{
  "trades": 64339,
  "max_return_pct": 3689.4315334640614,
  "max_drawdown_pct": 4.629389056231814,
  "official_cd_value": 3614.004004760479,
  "active_leftover": 0,
  "pending_leftover": 0,
  "load_errors": 0
}

부하 제어:
- 기본은 기준선 재실행 없이 조합 후보 1개만 실행한다.
- 기준선 공식값은 baseline_reference_short_max_v10.csv에 reference로 저장한다.
- --run-baseline-gate를 붙이면 기준선을 실제 재현하지만 1시간을 넘길 수 있다.
- --max-runtime-min 기본 65분으로, 예산 도달 시 현재 후보 종료 후 저장하고 멈춘다.
- save-top-trades 기본값 0에서는 후보별 trades 원본을 메모리에 보관하지 않는다.
