# long_main v6 진입 조건 및 청산 조건

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`

이 문서는 다음 개선 작업에서 기준으로 삼아야 할 핵심 조건을 기록한다.

---

## 1. 전략 구조

이 전략은 두 단계 구조다.

1. parent 신호: `8V4_V09_V054_extreme_vol18`
2. child 신호: parent 신호에 `TP03 기대값 게이트`를 추가
3. 청산 프로파일: `risk_rr_plus20`

최종 entry_key:

`child::orig_V09_extreme_vol18::tp03`

---

## 2. parent 전략 식별자

| 항목 | 값 |
|---|---|
| parent_strategy | `8V4_V09_V054_extreme_vol18` |
| family | `V09` |
| anchor | `extreme` |
| guard | `vol18` |
| original parent entry_key | `orig_V09_extreme_vol18` |

V09는 8V4 계열의 family seed 중 하나다. 이 전략은 V09 family 신호에 `extreme` anchor와 `vol18` guard를 결합한 parent 신호에서 출발한다.

---

## 3. parent entry 개념식

개념적으로 parent 신호는 다음 구조다.

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

여기서:

- `family_signal_V09`: 원본 8V4 계열에서 V09 family로 정의된 롱 반전/리클레임 계열 신호
- `anchor_extreme`: 과매도 또는 극단 변동 후 반전 가능성이 높은 구간을 잡는 anchor
- `guard_vol18`: 거래량 비율 조건 `vol_ratio >= 1.18`을 의미하는 guard

중요:

다음 개선에서 이 조건을 임의로 새로 해석하지 않는다. 정확한 구현은 `03_STRATEGY_CODE_REFERENCE.py`의 `compute_entry_masks()`와 `build_single_target_strategy()`를 기준으로 한다.

---

## 4. child entry 조건

최종 child 신호는 parent 신호에 TP 기대값 0.3% 이상 조건을 추가한다.

개념식:

`child_entry = parent_entry AND tp03_gate`

TP03 게이트:

`tp03_gate = expected_take_profit_pct >= 0.3%`

구현상으로는 진입 시점의 close, ATR, stop/target 구조를 이용해 목표가까지의 기대폭이 0.3% 이상인 경우만 허용한다.

운영 원칙:

- 앞으로 이 전략을 기준으로 개선할 때 TP 기대값 0.3% 이상 조건은 기본 유지한다.
- TP03 조건을 제거하는 실험은 가능하지만, 기준선 개선 후보가 아니라 별도 완화 실험으로 기록한다.

---

## 5. 리스크/청산 조건

v6/v2 기준선의 고정 청산 파라미터는 다음과 같다.

| 항목 | 값 |
|---|---:|
| atr_stop | 1.01 |
| rr_target | 2.90 |
| max_hold_bars | 21 |
| cooldown_bars | 31 |
| use_tp03_gate | true |

청산 구조:

1. 진입 후 ATR 기반 손절선 계산
2. rr_target 기반 목표가 계산
3. max_hold_bars 초과 시 시간 청산
4. 청산 후 cooldown_bars 동안 같은 심볼의 재진입 제한
5. 왕복 수수료 8bps 반영
6. position_fraction 0.01 적용

---

## 6. 성과 계산식

공식 cd_value 계산식:

`official_cd_value = 100 * (1 - abs(max_drawdown_pct) / 100) * (1 + max_return_pct / 100)`

long_main 선별 조건:

`max_drawdown_pct < 5` 조건을 만족하는 전략 중 `official_cd_value`가 가장 높은 전략을 기준선으로 삼는다.

v6는 MDD 1.2219870757%로 long_main 조건을 통과한다.

---

## 7. 다음 개선에서 허용되는 변형

허용되는 직접 개선 방식:

1. `child_entry AND 추가 방어 필터`
2. `child_entry AND 과열 회피 필터`
3. `child_entry AND max_conc 감소 필터`
4. `child_entry` 유지 + 청산 파라미터 조정
5. `child_entry` 유지 + cooldown 조정
6. `child_entry` 유지 + 시간 청산 조정

주의해야 할 변형:

- parent_entry를 완전히 다른 family로 교체하면 v6 개선이 아니라 신규 전략이다.
- TP03 게이트를 제거하면 기준선 구조가 바뀌므로 별도 실험으로 분리한다.
- MDD 5% 미만 조건을 깨면 long_main 기준선 후보로 인정하지 않는다.

---

## 8. 기준선 정체성

이 전략의 정체성은 다음 4개로 고정한다.

1. V09 family
2. extreme anchor
3. vol18 guard
4. TP03 + risk_rr_plus20 child profile

다음 대화창에서 이 기준선을 이어받을 때는 이 4개를 기준으로 개선해야 한다.
