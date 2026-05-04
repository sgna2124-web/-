8V30 설계: TP03 단독 효과 확인 + 롱 완화 + 숏 손실 컷 정제

작성 배경
사용자는 기존 기준선에서 숏 전략의 거래 수가 롱 전략보다 압도적으로 많다는 점을 지적했다. 그런데 최근 개선안에서는 롱 거래가 과도하게 폭증하고 숏 거래가 0 또는 극단적 기근으로 바뀌는 현상이 반복되었다. 이는 기준선의 원형을 개선하는 방향과 다르다.

핵심 판단
1. 기준선 롱 전략은 거래 수가 적은 편이다.
- long_main 기준선 trades: 592
- long_max 기준선 trades: 2276
- 따라서 롱은 무조건 더 강하게 조이는 방향만이 정답은 아니다.
- 기준선 조건의 일부 완화, 유사 지표의 느슨한 대체, 파라미터 완화를 테스트해야 한다.

2. 기준선 숏 전략은 거래 수가 이미 충분하다.
- short_main 기준선 trades: 28017
- short_max 기준선 trades: 36505
- 따라서 숏은 진입 수를 늘리는 개선이 아니라, 기존 거래 집합에서 수익성 거래는 남기고 손실성 거래를 줄이는 정제가 우선이다.

3. TP0.3% 조건의 순수 효과를 별도로 확인해야 한다.
- 기준선에는 TP0.3% 조건이 없다.
- 최근 TP03은 과도한 진입을 막기 위해 추가되었지만, 기준선 원형 보존 관점에서는 모든 축에 당연히 붙일 조건이 아니다.
- 각 기준선에 TP03만 추가한 결과를 따로 측정해야 한다.

8V30 배치
BATCH: 8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H
원본 기준 파일: CORE_SUMMARY/run_8v20_embedded_parent_gate_4axis_50_each.py
결과 저장 위치: C:\Users\user\Documents\GitHub\-\local_results\8V30_TP03_PROBE_LONG_LOOSEN_SHORT_TRIM_1H
캔들 제한: 없음
기본 후보 수: 각 축 2개, 총 8개

8V30 후보 구성
공통 후보: TP03-only probe
각 축별로 base_spec(axis)에 TP0.3% 기대값 조건만 추가한 후보를 넣는다.
목적은 TP03 단독 효과를 확인하는 것이다.

long_main 후보 1
- 이름: 8V30_long_main_001_tp03_only_probe
- 목적: long_main 기준선에 TP03만 추가했을 때 거래량, 수익률, MDD가 어떻게 바뀌는지 확인.

long_main 후보 2
- 이름: 8V30_long_main_002_loosen_reclaim_wick_close_range
- 방향: 기준선 shocklow/reclaim/green 계열 유지 + wick/close/range/vol/body 완화.
- TP03 미적용.
- 목적: 기준선 롱이 원래 거래 수가 적으므로, 유사 지표 완화와 파라미터 완화가 성과를 높이는지 확인.
- 장점: 기준선 롱의 적은 거래 수 문제를 보완할 수 있다.
- 단점: 최근 개선 경로에서 long 폭증이 반복되었으므로 parent_trade_ratio 폭증 위험이 있다.

long_max 후보 1
- 이름: 8V30_long_max_001_tp03_only_probe
- 목적: long_max 기준선에 TP03만 추가했을 때 순수 효과 확인.

long_max 후보 2
- 이름: 8V30_long_max_002_loosen_rare22_range_vol_upper
- 방향: V51 rare22/reclaim 계열 유지 + range/vol/upper_wick/close_pos 완화.
- TP03 미적용.
- 목적: long_max 기준선의 거래 수를 어느 정도 늘려 raw upside가 개선되는지 확인.
- 장점: V51 계열의 강점을 더 활용할 수 있다.
- 단점: long_max는 이전 개선에서 거래 폭증이 가장 심했으므로 매우 주의해야 한다.

short_main 후보 1
- 이름: 8V30_short_main_001_tp03_only_probe
- 목적: short_main 기준선에 TP03만 추가했을 때 거래량이 얼마나 줄고 MDD가 어떻게 바뀌는지 확인.

short_main 후보 2
- 이름: 8V30_short_main_002_no_tp03_profit_keep_loss_trim
- 방향: TP03 미적용. dev/rsi/wick/shock/close_pos 계열을 아주 약하게 강화하고 post_loss/sym_dd 손실 컷을 추가.
- 목적: 기존 충분한 숏 거래 중 손실성 구간을 줄이고 수익성 과열 진입은 남긴다.
- 장점: 숏 기준선의 풍부한 거래 수를 활용하면서 MDD를 줄일 수 있다.
- 단점: 조건 강화가 과하면 8V29처럼 zero trade 또는 trade starvation 가능성이 있다.

short_max 후보 1
- 이름: 8V30_short_max_001_tp03_only_probe
- 목적: short_max 기준선에 TP03만 추가한 순수 효과 확인.

short_max 후보 2
- 이름: 8V30_short_max_002_no_tp03_blowoff_loss_trim
- 방향: TP03 미적용. blowoff 원형 유지 + 약한 dev/rsi/wick/shock 강화 + 손실 컷.
- 목적: raw upside는 유지하고 손실 구간만 완만하게 줄인다.
- 장점: short_max의 높은 수익 잠재력을 유지하면서 MDD 압축 가능성을 본다.
- 단점: 손실 컷이 강하면 raw upside가 줄 수 있다.

8V30 판정 기준
1. TP03-only 후보는 개선 후보라기보다 진단 후보로 본다.
2. TP03-only 결과가 기준선 대비 거래량을 얼마나 줄이는지 축별로 비교한다.
3. 롱 완화 후보는 수익률 증가와 parent_trade_ratio 폭증 여부를 동시에 본다.
4. 숏 손실 컷 후보는 max_return 유지, MDD 감소, parent_trade_ratio 보존 여부를 본다.
5. parent_trade_ratio가 극단적으로 벗어나면 수익률과 관계없이 기준선 이탈로 본다.

금지 사항
1. 캔들 제한 금지.
2. 기준선 코드, BASELINES, entry/exit 엔진, parent gate 수정 금지.
3. short 개선 후보에 TP03을 기본 적용하지 않는다. TP03은 별도 probe 후보에서만 본다.
4. long 개선 후보는 무조건 강하게 조이지 않는다. 기준선 원형의 완화/대체도 허용한다.
5. short는 진입 수 증가보다 손실 거래 컷과 MDD 압축을 우선한다.
