# 다음 러너 구현 TODO

## 최우선
1. 과확장 복귀 전략 v1를 실제 실행 코드로 복원
2. 전체 종목 기준으로 다시 돌려 benchmark_overextension_reversion_v1_result.json을 실제 산출물로 교체
3. raw trades csv, per-symbol summary csv, aggregate summary json 저장

## 그 다음
다음 후보를 배치 러너에 넣고 같은 결과 스키마로 저장
- squeeze_breakout
- insidebar_trend
- base_breakout
- retest_breakout
- pullback_trend

## 저장 규칙
- results/{strategy_name}_aggregate.json
- results/{strategy_name}_per_symbol.csv
- results/{strategy_name}_trades.csv

## 비교 규칙
- 모든 신규 전략은 overextension_reversion_v1와 비교
- 최소 비교 항목: final_asset, pf, mdd, max_conc, peak_asset
