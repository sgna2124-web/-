# long_max v2 진입 조건 및 청산 조건

전략명: `8V4_V09_V054_extreme_vol18__CH_tp03_risk_rr_plus20`

이 문서는 다음 long_max 개선 작업에서 기준으로 삼아야 할 핵심 조건을 기록한다.

---

## 1. 전략 구조

이 전략은 V11 parent-signal 개발 과정에서 발견되고, V12 단독 재백테스트로 재현된 long_max 새 기준선이다.

구조:

1. parent 신호: `8V4_V09_V054_extreme_vol18`
2. child 신호: parent 신호에 `TP03 기대값 게이트` 추가
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

`parent_entry = family_signal_V09 AND anchor_extreme AND guard_vol18`

여기서:

- `family_signal_V09`: 원본 8V4 계열의 V09 family 신호
- `anchor_extreme`: 극단 변동/과매도/리클레임 성격을 가진 anchor
- `guard_vol18`: 거래량 비율 조건 `vol_ratio >= 1.18`

중요:

`V09`, `extreme`, `vol18`의 정확한 Boolean은 `03_STRATEGY_CODE_REFERENCE.py`의 `compute_entry_masks()` 구현을 기준으로 한다. 전략명만 보고 조건을 재해석하지 않는다.

---

## 4. child entry 조건

최종 child 신호:

`child_entry = parent_entry AND tp03_gate`

TP03 게이트:

`tp03_gate = expected_take_profit_pct >= 0.3%`

운영 원칙:

- TP03 게이트는 기준선의 일부다.
- TP03 제거 실험은 가능하지만, v2 기준선의 직접 개선이 아니라 완화 실험으로 분리한다.
- long_max 목적은 cd_value 극대화이므로 TP03 유지/완화/강화 후보는 모두 cd_value 기준으로 평가하되, 기준선 기록에는 어떤 구조에서 파생됐는지 명확히 남긴다.

---

## 5. 리스크/청산 조건

v2 기준선의 고정 청산 파라미터:

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

long_max 선별 조건:

`MDD 제한 없이 전체 전략 중 official_cd_value 최대`

v2의 official_cd_value는 `311.3750675807`이며, v1의 `134.4697`을 크게 초과한다.

---

## 7. 다음 개선에서 허용되는 변형

long_max는 cd_value 극대화가 목적이므로 long_main보다 확장 실험 폭이 넓다.

허용되는 직접 개선 방식:

1. `child_entry AND 추가 필터`
2. `child_entry OR 근접 parent 신호`
3. `child_entry` 유지 + 청산 파라미터 조정
4. `child_entry` 유지 + cooldown 조정
5. TP03 게이트 강화 또는 완화
6. rr_target, atr_stop, max_hold_bars 조합 탐색
7. max_conc 감소 조건 추가
8. 수수료 민감도 감소 조건 추가

단, 다음은 별도 신규 전략으로 분리한다.

- V09 family를 다른 family로 완전히 교체
- extreme anchor를 완전히 다른 anchor로 교체
- vol18 guard 없이 전혀 다른 guard 조합만으로 만든 전략

---

## 8. 기준선 정체성

이 전략의 정체성은 다음 4개로 고정한다.

1. V09 family
2. extreme anchor
3. vol18 guard
4. TP03 + risk_rr_plus20 child profile

앞으로 long_max 개발의 기준선은 v1 V51이 아니라 이 v2 전략이다.
