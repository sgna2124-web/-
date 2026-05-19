# long_main v16 장단점

## 장점

1. 단독 리테스트 통과
   - `pass_frozen_reproduction_gate=true`
   - `pass_rank1_retest_gate=true`
   - `errors=0`

2. 직전 기준 LM22R_068보다 cd_value가 개선됐다.
   - 539.1375335808302 -> 547.2610302171641
   - 개선폭: +8.1234966363339

3. 수익성과 리스크가 같이 좋아졌다.
   - max_return_pct: 447.0278919263715 -> 455.0171719748199
   - max_drawdown_pct: 1.4424051244910419 -> 1.3974597812998368

4. 거래 구조가 개선됐다.
   - wins: 21871 -> 21969
   - losses: 34720 -> 34582
   - win_rate_pct: 38.64748811648495 -> 38.84811939665081

5. long_main 기준 MDD 5% 미만을 충분히 만족한다.
   - max_drawdown_pct: 1.3974597812998368

6. entry source를 바꾸지 않고, 검증된 TP03 구조 위에서 body/stop/RR/hold를 조정한 전략이다.

## 단점

1. max_conc가 445로 1 증가했다.
   - 직전 기준 LM22R_068은 444였다.

2. stop과 RR이 더 공격적으로 바뀌었다.
   - atr_stop: 1.20 -> 1.21
   - rr_target: 5.00 -> 5.05
   - 실거래에서는 목표가 미체결, 슬리피지, 순간 고가 체결 실패 영향을 더 받을 수 있다.

3. body_atr 기준이 0.22로 올라갔다.
   - 거래 수는 56591 -> 56551로 40건 감소했다.
   - 다만 wins는 늘고 losses는 줄었으므로 현재 결과에서는 긍정적이다.

4. TP03 source와 final exit 파라미터가 다르다.
   - TP03 source: atr_stop 1.10, rr_target 3.80
   - final exit: atr_stop 1.21, rr_target 5.05
   - 이 둘을 혼동하면 재현이 깨진다.

## 다음 개선 방향

1. v16을 exact frozen 후보로 둔 뒤, 다음 좁은 주변값만 테스트한다.
   - stop: 1.21, 1.22, 1.23
   - rr_target: 5.05, 5.10, 5.15
   - body_atr: 0.20, 0.22, 0.24, 0.26
   - hold: 17 고정 우선

2. max_conc 445를 줄이는 후보를 따로 탐색한다.
   - 단, close_pos/quiet_ratio는 이전 테스트에서 성과가 크게 훼손됐으므로 후순위다.

3. hold 16/18은 이전 리테스트에서 성과가 낮았으므로 우선 제외한다.

4. 다음 갱신은 반드시 단독 리테스트까지 통과해야 한다.
