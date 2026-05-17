SHORT_MAX v8 actual train MIX candidates v1

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
  "trades": 45500,
  "max_return_pct": 1424.4317435070927,
  "max_drawdown_pct": 6.104584306764704,
  "official_cd_value": 1431.3715225256192,
  "active_leftover": 0,
  "pending_leftover": 0,
  "load_errors": 0
}
