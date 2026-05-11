# long_main v6 기준선 재현 시작 문서

이 폴더의 목적은 다음 대화창의 새로운 작업자가 이전 대화 흐름을 몰라도 long_main v6 기준선을 같은 값으로 재현하고, 그 기준선에서 개선을 시작하게 만드는 것이다.

## 1. 현재 공식 기준선

- axis: long_main
- version: v6
- strategy: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`
- side: long
- parent_strategy: `8V4_V09_V054_extreme_vol18`
- parent_entry_key: `orig_V09_extreme_vol18`
- final_entry_key: `child::orig_V09_extreme_vol18::tp03`
- family: `V09`
- anchor: `extreme`
- guard: `vol18`
- child filter: `TP expected >= 0.3%`
- exit profile: `risk_rr_plus20`

## 2. 공식 결과값

아래 값이 재현 기준이다. 이 값과 다르면 기준선 재현 실패로 본다.

| 항목 | 값 |
|---|---:|
| trades | 57243 |
| wins | 20312 |
| losses | 36931 |
| win_rate_pct | 35.4838146149 |
| final_return_pct | 214.7144460828 |
| max_return_pct | 215.2271020267 |
| max_drawdown_pct | 1.2219870757 |
| official_cd_value | 311.3750675807 |
| max_conc | 429 |
| symbol_files | 597 |
| errors | 0 |
| ruined | false |

## 3. 공식 계산식

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_main 기준선 선별식:

`max_drawdown_pct < 5` 조건을 만족하는 전략 중 `official_cd_value`가 가장 큰 전략.

이 전략의 MDD는 `1.2219870757%`이므로 long_main 기준을 통과한다.

## 4. 재현에 필요한 고정 파라미터

| 항목 | 값 |
|---|---:|
| atr_stop | 1.01 |
| rr_target | 2.90 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| position_fraction | 0.01 |
| round_trip_cost_bps | 8.0 |
| warmup_bars | 120 |
| min_bars | 250 |
| timeframe | 5m |
| max_bars | 0, 전체 캔들 사용 |

## 5. 절대 하면 안 되는 재현 방식

다음 방식으로는 재현하면 안 된다.

1. `V09`, `extreme`, `vol18`이라는 이름만 보고 새로 Boolean 조건을 추측해서 구현하는 것.
2. `03_STRATEGY_CODE_REFERENCE.py`만 보고 기준선 백테스트를 만드는 것.
3. `parent_entry = V09 AND extreme AND vol18`이라는 개념식만 보고 임의로 feature 계산을 만드는 것.
4. `final_return_pct`로 cd_value를 계산하는 것. cd_value는 반드시 `max_return_pct`를 사용한다.
5. 기준선이 다르게 나오는데도 그 결과를 기준으로 개선을 시작하는 것.

## 6. 왜 이전 재현이 실패했는가

이 폴더의 기존 기록에는 전략명, entry_key, 리스크 파라미터, 기대값은 있었지만 실제 Boolean 구현 전체가 들어 있지 않았다.

특히 다음 구현이 빠져 있었다.

- `compute_entry_masks()` 전체 구현
- `raw_shock_down_at()`
- `raw_l01_signal_at()`
- `raw_shock_reversal_balance_at()`
- `raw_extreme_reclaim_at()`
- `family_risk_profile()`
- `compute_child_filter_masks()`의 TP03 계산
- ATR, RSI, EMA, volume ratio 등 feature 계산
- 진입/청산 루프의 hit_stop/hit_target 우선순위
- cooldown 적용 타이밍
- 수수료 반영 방식
- equity curve 및 cd_value 계산 방식

따라서 새로운 작업자가 이 폴더만 보고 조건을 다시 해석하면 거의 반드시 trades, wins, losses가 달라진다.

## 7. 정확한 진입 구조

개념식은 다음과 같다.

`family_signal_V09 = shock_down OR l01 OR shock_balance`

`anchor_extreme = raw_extreme_reclaim OR rsi14 <= 34.0`

`guard_vol18 = vol_ratio >= 1.18`

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

`tp03_gate = ((atr_stop * atr14 * rr_target / close) * 100.0) >= 0.30`

`final_entry = parent_entry AND tp03_gate`

단, 위 식은 이해용 요약이다. 실제 재현에서는 반드시 원본 runner의 feature 계산, raw signal 함수, warmup 처리, 마지막 봉 제외 처리까지 동일해야 한다.

## 8. TP03 계산에서 특히 틀리기 쉬운 부분

TP03은 단순히 ATR percentage만 보는 것이 아니다. 실제 child filter에서는 다음 형태를 사용한다.

`target_pct = (atr_stop * atr14 * rr_target / close) * 100.0`

`tp03 = target_pct >= 0.30`

이 기준선에서는 `atr_stop = 1.01`, `rr_target = 2.90`을 사용한다.

## 9. 청산 구조

각 진입 후 다음 순서로 청산을 계산한다.

1. entry_price 기준 stop distance 계산
2. stop_price = entry_price - stop_dist
3. target_price = entry_price + stop_dist * rr_target
4. 이후 봉에서 stop 또는 target 도달 여부 확인
5. 같은 봉에서 stop과 target이 동시에 맞으면 보수적으로 stop 우선 처리
6. target 도달 시 target 청산
7. stop 도달 시 stop 청산
8. max_hold_bars 초과 시 시간 청산
9. 청산 후 cooldown_bars 동안 같은 심볼 재진입 금지
10. 왕복 수수료 8bps 반영
11. 포지션 비중 0.01로 equity curve 계산

## 10. 재현 성공 판정

다음 조건을 모두 만족해야 재현 성공이다.

1. trades == 57243
2. wins == 20312
3. losses == 36931
4. errors == 0
5. ruined == false
6. official_cd_value가 311.3750675807 근처일 것
7. max_drawdown_pct가 1.2219870757 근처일 것
8. max_return_pct가 215.2271020267 근처일 것

trades/wins/losses가 하나라도 다르면 재현 실패다. 이 경우 개선을 시작하지 말고 entry mask, feature, cooldown, 청산 우선순위부터 다시 확인한다.

## 11. 다음 개선의 기준

long_main 다음 개선은 이 기준선에서 시작한다.

- 목표: `MDD < 5` 유지 + `official_cd_value > 311.3750675807`
- 기준 entry: `child::orig_V09_extreme_vol18::tp03`
- 기준 청산: `atr_stop 1.01`, `rr_target 2.90`, `max_hold 21`, `cooldown 31`

허용되는 개선:

1. `baseline_entry AND 추가 방어 필터`
2. `baseline_entry AND 과열 회피 필터`
3. `baseline_entry AND max_conc 감소 필터`
4. `baseline_entry` 유지 + 청산 파라미터 조정
5. `baseline_entry` 유지 + cooldown/max_hold 조정

금지되는 개선:

1. V09 family를 완전히 다른 family로 교체하는 것
2. extreme anchor를 완전히 다른 anchor로 교체하는 것
3. vol18 guard를 없애고 다른 guard만 쓰는 것
4. 기준선 재현 없이 개선 후보를 평가하는 것

## 12. 새 대화창 인수인계 문장

`long_main 현재 기준선은 v6 8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20이다. 기준선 재현값은 trades 57243, wins 20312, losses 36931, MDD 1.2219870757, cd_value 311.3750675807이다. V09/extreme/vol18/TP03를 이름만 보고 재해석하지 말고, frozen runner와 동일한 feature 계산·entry mask·청산 루프로 먼저 기준선을 재현한 뒤 개선한다.`
