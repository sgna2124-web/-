8V30 다음 개선 계획: 단일 조건 분해와 기준선 원형 복원 우선

작성 배경
8V29 결과는 이미 CORE_SUMMARY/47_8V29_RESULT_AND_TP03_AXIS_SPLIT_LESSON.md에 반영되었다. 8V29는 baseline gate는 통과했지만 개선안 4개가 전부 무효였다. long은 trade explosion, short는 zero trade였다.

8V29 핵심 수치 재확인
long_main 개선안
- trades: 6697
- baseline_trades: 592
- parent_trade_ratio: 11.312500
- verdict: invalid_trade_explosion
- max_drawdown_pct: 45.546841

long_max 개선안
- trades: 167541
- baseline_trades: 2276
- parent_trade_ratio: 73.612039
- verdict: invalid_trade_explosion
- max_drawdown_pct: 99.991579

short_main 개선안
- trades: 0
- baseline_trades: 28017
- parent_trade_ratio: 0.0
- verdict: invalid_zero_trade

short_max 개선안
- trades: 0
- baseline_trades: 36505
- parent_trade_ratio: 0.0
- verdict: invalid_zero_trade

8V29에서 얻은 다음 개선 전제
1. 기준선 개선의 1차 목표는 수익률이 아니라 parent_trade_ratio 정상화다.
2. parent_trade_ratio가 정상 범위에 들어오지 않으면 수익률/MDD를 평가하지 않는다.
3. long은 폭증을 줄이는 방향이 맞지만, 복합 품질 스택으로도 아직 기준선 규모에 접근하지 못했다.
4. short는 TP03 제거 자체는 맞지만, 추가 조건을 여러 개 동시에 넣으면 0트레이드가 된다.
5. 8V30은 한 번에 좋은 전략을 만들려 하지 말고 조건별 민감도를 분해해야 한다.

8V30 설계 원칙
1. 캔들 제한 없음.
2. 기준선과 같은 전체 데이터 환경 유지.
3. 기준선 embedded reference와 baseline gate 유지.
4. 기준선 원형을 절대 고정하는 것이 아니라, 조건군 안의 작은 대체/추가/완화만 허용.
5. 단, 한 후보에 여러 조건을 많이 쌓지 않는다.
6. long은 TP03 유지 가능. short는 TP03 기본 제거.
7. 결과 해석의 1순위는 parent_trade_ratio다.
8. 1시간 내외 목표는 후보 수로 조절한다.

8V30 후보 구성 제안
총 4개 후보를 권장한다. 각 축 1개씩 유지하되, 이번에는 복합 스택이 아니라 핵심 단일 조건 또는 2개 이하의 약한 조건만 둔다.

long_main 후보 방향
- 목적: 8V29에서 11.31배까지 줄었으나 여전히 폭증. 더 직접적인 기준선 anchor가 필요하다.
- 후보: shocklow/reclaim/green 원형 유지 + strict + close_pos 강한 제한만 적용.
- 제외: vol/body/range/wick/upper_wick/lowanchor를 한 번에 많이 넣지 않는다.
- 이유: 어떤 조건이 실제로 거래 폭증을 줄이는지 분리해야 한다.

long_max 후보 방향
- 목적: 8V29에서 73.61배로 줄었지만 여전히 폭증. V51 rare22 원형을 보존하면서 하나의 anchor만 강하게 본다.
- 후보: rare22/reclaim 원형 유지 + strict + range20_max 제한만 적용.
- 제외: lowanchor, vol, body, wick, upper_wick, sym_dd를 동시에 넣지 않는다.
- 이유: long_max 폭증은 조건 부족보다 기준선 핵심 anchor 누락 가능성이 크므로 단일 anchor 효과부터 확인한다.

short_main 후보 방향
- 목적: 8V29에서 0트레이드. TP03 제거 상태에서 어떤 추가 조건이 병목인지 확인한다.
- 후보: TP03 제거 + dev/rsi 원형 유지 + close_pos_short_max만 약하게 추가.
- 제외: require_upper_sweep, require_ema_reject, shock 강화, post_loss, sym_dd를 동시에 넣지 않는다.
- 이유: short 0트레이드 원인은 복합 조건 과잉이다. close_pos_short 하나만 넣어 거래 규모 변화를 본다.

short_max 후보 방향
- 목적: 8V29에서 0트레이드. blowoff 원형을 유지하며 wick/shock 조건을 급격히 바꾸지 않는다.
- 후보: TP03 제거 + 기존 blowoff 원형 유지 + wick_short_min만 약하게 완화 또는 close_pos_short만 약하게 추가.
- 제외: upper_sweep/ema_reject/shock 강화/post_loss/sym_dd 동시 적용 금지.
- 이유: short_max는 기준선 raw upside가 크므로 먼저 거래량 회복이 우선이다.

8V30 성공 기준
1. long_main parent_trade_ratio가 1.0~5.0 이하로 내려가면 조건 방향은 개선된 것으로 본다. 최종 후보 기준은 0.5~1.2지만 현재 11.3배에서 단계적으로 줄이는 중이다.
2. long_max parent_trade_ratio가 10.0 이하로 내려가면 일단 유효한 anchor 후보로 본다. 최종 후보 기준은 0.5~1.2다.
3. short_main parent_trade_ratio가 0.20 이상으로 회복되면 0트레이드 병목 해소로 본다. 최종 후보 기준은 0.6~1.1이다.
4. short_max parent_trade_ratio가 0.20 이상으로 회복되면 0트레이드 병목 해소로 본다. 최종 후보 기준은 0.6~1.1이다.
5. 위 기준을 만족한 축만 다음 배치에서 수익률/MDD 개선으로 넘어간다.

8V30에서 금지할 것
1. 한 후보에 5개 이상 조건을 동시에 추가하지 않는다.
2. short에 TP03을 다시 기본 적용하지 않는다.
3. 캔들 제한으로 시간을 맞추지 않는다.
4. long 폭증을 잡기 위해 무작정 모든 품질 조건을 쌓지 않는다.
5. short zero trade를 막기 위해 조건을 전부 제거하지도 않는다. 기존 과열 원형은 유지한다.

다음 백테스트 파일 작성 지침
- BATCH 예시: 8V30_DECOMPOSE_SINGLE_ANCHOR_NO_CANDLE_LIMIT_1H
- variants_for_axis만 교체한다.
- 기준선 관련 코드, base_spec, BASELINES, entry/exit 엔진, parent gate는 수정하지 않는다.
- 결과 저장 경로는 C:\Users\user\Documents\GitHub\-\local_results\{BATCH} 유지.
- subprocess cwd는 launch_cwd 유지.
- --max-bars 계열 인자는 제거한다.

최종 판단
8V30은 성과 개선 배치라기보다 거래량 정상화 배치다. parent_trade_ratio를 정상화하지 못하면 전략 개선은 계속 기준선 이탈로 판정된다. 따라서 8V30은 long의 폭증 anchor, short의 zero-trade 병목을 찾는 데 집중한다.
