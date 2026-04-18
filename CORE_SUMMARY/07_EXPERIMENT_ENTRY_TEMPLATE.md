실험 기록 템플릿

아래 형식을 새 전략 결과 기록에 그대로 사용한다.
모든 항목은 가능한 한 채운다.
max_return_pct는 반드시 포함한다.

strategy_name:
side:
family:
version_reference:
status:

code_path:
config_path:
combinations_path:
result_path:
summary_file:

capital_per_trade_pct: 1
fee_pct: 0.04
full_universe_backtest: true
fast_screening_used: false
early_rejection_used: false
trade_log_required: false

trades:
win_rate_pct:
pf:
final_return_pct:
max_return_pct:
max_drawdown_pct:
cd_value:
max_conc:
verdict:

notes:

verdict 사용 규칙
official_long_reference
official_short_reference
candidate
strong_candidate_not_promoted
carry_forward_same_as_official_long_1
carry_forward_same_as_official_short_1
archive_reference_only
reject
invalid_env
pending_review

기록 규칙
공식 판단 기준은 cd_value와 max_drawdown_pct(MDD)다.
final_return_pct는 참고 지표다.
max_return_pct는 참고 지표이면서 cd_value 산출에 반드시 필요한 항목이다.
invalid_env는 정상 실패가 아니라 제거 대상 실험이다.
