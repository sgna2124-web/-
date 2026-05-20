# LONG MAX v12 장단점 및 다음 개선 방향

## 장점

1. 리테스트 재현 성공

LM26 단독 리테스트에서 공식 성과 지표가 재현되었다.

2. CD 603 달성

official_cd_value 603.3485179858741이다.

3. long_max 기준에서도 VALID

summary_long_max_cd_rank.csv에서 동일 후보가 VALID로 확인되었다.

4. 기존 entry_source 유지

child::orig_V09_extreme_vol18::tp03를 유지하므로 기존 long 계열 기준선과 연결된다.

## 단점

1. max_conc가 낮지 않다

관측값은 436이다. 현재 기준에서는 공식 결격값이 아니라 진단값이다.

2. MDD는 직전 일부 후보보다 약간 높다

max_drawdown_pct는 1.0930827574126778이다.

3. body_atr 필터가 강하다

body_atr_min 0.36으로 약한 신호를 줄이는 대신 일부 진입 기회를 놓칠 수 있다.

## 다음 long_max 개선 방향

1. CD 620 이상 탐색

body_atr 0.34~0.44, cooldown 32~34, stop 1.27~1.31, rr 5.00~5.15를 중심으로 섞는다.

2. max_return 확대 후보 탐색

rr 5.10~5.25와 hold 17~19를 일부 섞어본다.

3. MDD 방어 후보 탐색

stop 1.25~1.28, body_atr 0.36~0.42, cooldown 33~35 조합을 테스트한다.

4. 단독 리테스트 필수

상위 후보가 나오면 반드시 단독 리테스트를 통과한 뒤 기준선 갱신한다.
