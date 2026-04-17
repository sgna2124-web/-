# EXPERIMENT ENTRY TEMPLATE

아래 템플릿을 복붙해서 새 실험 문서를 만들면 된다.

---

# [실험명]

## 1. 기본 정보
- version_prefix:
- side:
- date:
- compare_target:
- strategy_id:
- code_path:
- result_path:

## 2. 실험 의도
- 왜 이 실험을 했는가:
- 이전 기준선의 어떤 한계를 건드리려는가:
- 기대한 핵심 개선점:

## 3. 변경 사항
- entry 변경:
- filter 변경:
- exit 변경:
- risk 변경:
- 기타:

## 4. 결과
- final_return_pct:
- mdd_pct:
- cd_value:
- pf:
- win_rate:
- max_conc:

## 5. 기준선 대비 비교
- delta_final_return_pct:
- delta_mdd_pct:
- delta_cd_value:
- delta_pf:
- delta_max_conc:

## 6. 해석
- 잘된 점:
- 안된 점:
- 구조적으로 배운 점:
- 재시도 가치:

## 7. 판정
- verdict: promoted / candidate / hold / failed / invalid
- one_line_reason:
- next_action:

---

## 빠른 복붙용 한 줄 요약 형식
experiment=[이름] | compare=[기준선] | final_return_pct=[값] | mdd_pct=[값] | cd_value=[값] | pf=[값] | max_conc=[값] | verdict=[판정]
