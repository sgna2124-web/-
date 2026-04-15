workflow 오류 및 안전 패턴 인수인계

이 문서는 최근 workflow 관련 실수와, 다음 어시스턴트가 반드시 따라야 할 안전 패턴을 정리한 것이다.

실제로 발생했던 주요 문제

1. pathspec 오류
- v60/v61 계열에서 single_changes_quick_summary.csv를 git add 하도록 되어 있었지만, 실제 그 경로에 파일이 없어서 실패
- 교훈: 커밋 대상 파일은 실제 생성 경로와 반드시 일치해야 한다

2. Git LFS 포인터 파일 읽기 오류
- multimethod 공용 러너가 repo-assets에서 압축 해제한 DATA_DIR를 안 보고 저장소의 5m_data 안 LFS 포인터 csv를 읽어서 실패
- 교훈: 공용 러너는 DATA_DIR 환경변수를 우선 읽도록 만들어야 한다

3. results 디렉터리 없음 오류
- 공용 quick summary를 results/... 아래에 쓰려다가 부모 디렉터리가 없어서 실패
- 교훈: results/.gitkeep 같은 식으로 부모 디렉터리를 미리 보장하거나, 스크립트 내부에서 parent.mkdir를 해야 한다

4. shared quick summary 충돌
- 62와 63이 같은 results/single_changes_timeout18_multimethod_quick_summary.csv를 저장소에 커밋하려다가 rebase conflict 발생
- 교훈: 공용 quick summary 파일은 artifact 전용으로 두고, 저장소 커밋 대상에서는 제외하는 편이 안전하다

5. unstaged changes 때문에 rebase 실패
- 커밋 대상이 아닌 생성 파일이 작업 디렉터리에 남아 있어서 git rebase 전에 막힘
- 교훈: push 전에 git stash -u -m 'post-run-noncommit-artifacts' || true 를 사용하면 안전하다

현재 안전 패턴

A. 가능한 경우 safer workflow 사용
- save results safer 계열 workflow는 다음 단계를 포함한다.
  1) repo-assets 압축 해제
  2) DATA_DIR로 실제 csv 사용
  3) 결과 summary 생성
  4) 저장소 반영 전 git stash -u 처리
  5) fetch/rebase/push

B. 새 workflow를 만들 때 체크리스트
1) 실제 csv를 읽는가
- data_dir = Path(os.environ.get('DATA_DIR', ...)) 형태 우선 확인

2) 결과 저장 경로가 존재하는가
- parent.mkdir(parents=True, exist_ok=True) 또는 results 폴더 보장

3) 공용 quick summary를 저장소에 커밋하지 않는가
- artifact로만 남기고 git add 대상에서는 빼는 것이 안전

4) rebase 전에 비커밋 산출물을 치우는가
- git stash push -u -m 'post-run-noncommit-artifacts' || true

5) git add 대상을 결과 폴더 내부 전용 summary 파일로 제한하는가
- */summary.json
- master_summary.csv / json / txt
- lane_summary.csv
- 이 정도면 충분하다

현재 상대적으로 안전한 흐름
- repo-assets fixed
- env-fix가 이미 들어간 러너 사용
- save results safer 패턴 사용

현재 주의점
- 원본 workflow와 수정 workflow가 공존하는 경우가 있다.
- 다음 어시스턴트는 가장 마지막 safer 버전만 써야 한다.
- 새 라운드를 만들 때는 원본을 패치하는 것보다, 새 safer workflow를 만드는 편이 실제로 덜 꼬였다.

실전 조언
- 사용자가 다시 결과를 확인하자고 하면, 저장소에 master_summary가 실제 반영된 workflow만 사용해야 한다.
- artifact만 남는 workflow는 분석 흐름이 끊긴다.
- workflow 이름은 길어도 되지만, "Save Results Safer" 패턴을 명시적으로 포함하면 다음 턴의 어시스턴트가 구분하기 쉽다.
