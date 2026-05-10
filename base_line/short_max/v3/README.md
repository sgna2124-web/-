# short_max v3 기준선

## 공식 기준선명

short_max_v3_combo_dev033_timeout240

## 출처

이 기준선은 short_max v2 기준선 short_only_reference_1x를 정확히 재현한 `run_short_max_v2_dev_strict_time_axis_v5.py` 결과에서 1위를 기록한 `combo_dev033_timeout240` 후보를 새 기준선으로 승격한 것이다.

기준선 개발 방식은 완전한 신규 전략이 아니라 기존 short_max v2 진입 구조를 유지한 상태에서 다음 두 가지만 변경한 개발형 개선이다.

1. short_dev: 0.032 → 0.033
2. timeout_bars: 200 → 240

나머지 핵심 구조는 short_max v2와 동일하게 유지한다.

## 공식 성과

테스트 환경:

- CSV 파일 수: 597
- initial_asset: 100
- position_fraction: 0.01
- fee_per_side: 0.0004
- side: short only
- entry: next bar open
- score 적용 위치: 포트폴리오 평가 단계
- same-bar 처리: entry_ts == exit_ts 거래는 같은 timestamp에서 즉시 청산
- engine mode: strict_time_axis_revalidated_hardened_absolute_score_embedded_restore 계열

성과:

- strategy: combo_dev033_timeout240
- trades: 34,782
- parent_trade_ratio: 0.9442906010750937
- win_rate_pct: 14.070496233684091
- final_return_pct: 451.45526435735064
- max_return_pct: 451.8246548170149
- max_drawdown_pct: 7.484506060174601
- official_cd_value: 510.52330508569787
- cd_delta_vs_baseline: +39.17083164043339
- mdd_delta_vs_baseline: +0.08895563439099696
- max_return_delta_vs_baseline: +42.8291631181994
- profit_factor: 1.4377856344586135
- max_conc: 292
- max_conc_unique_symbols: 292
- same_bar_trades: 3,585
- active_leftover: 0
- errors: 0

## v2 대비 변경 요약

short_max v2 기준선:

- short_dev: 0.032
- short_rsi_min: 76.0
- short_wick_mult: 1.3
- score_min_short: 2.0
- atr_stop_mult: 1.8975
- rr_mult: 6.0
- min_expected_tp: 0.003
- timeout_bars: 200

short_max v3 기준선:

- short_dev: 0.033
- short_rsi_min: 76.0
- short_wick_mult: 1.3
- score_min_short: 2.0
- atr_stop_mult: 1.8975
- rr_mult: 6.0
- min_expected_tp: 0.003
- timeout_bars: 240

## 기준선 채택 이유

`combo_dev033_timeout240`은 short_max v2 대비 official_cd_value가 471.3524734452645에서 510.52330508569787로 상승했다. max_return_pct는 408.9954916988155에서 451.8246548170149로 크게 증가했지만, max_drawdown_pct 증가는 7.395550425783604에서 7.484506060174601로 매우 작다.

따라서 short_max 축의 목표인 “MDD 10% 미만 유지 + 수익 극대화”에 가장 부합한다.

## 다음 개발 기준

앞으로 short_max 개발은 이 v3 기준선을 기본 부모 전략으로 사용한다.

우선 개발 방향:

1. timeout 230~280 주변 구조 탐색
2. short_dev 0.0328~0.0335 주변 구조 탐색
3. score_min_short 2.00~2.08 주변 구조 탐색
4. rsi_755_relax의 장점과 결합 가능성 검토
5. time_reduce 8~12, time_reduce_to_risk_frac 0.03~0.05 조정 검토

주의점:

- 완전히 새로운 전략으로 바꾸지 않는다.
- short_max v3의 과열 숏 진입 구조를 유지한다.
- score_min_short는 진입 마스크에 넣지 않고 포트폴리오 평가 단계에서 적용한다.
- same-bar 거래는 반드시 즉시 청산 처리한다.
- MDD 10% 미만 조건을 유지한다.
