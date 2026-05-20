# -*- coding: utf-8 -*-
"""
LONG MAX v12 frozen runner.

long_max v12는 long_main v17과 동일한 LM26 조건을 공식 기준선으로 사용한다.
이 파일은 저장소 내부의 long_main v17 frozen runner를 복원 소스로 사용하되,
출력 폴더와 RUN_LABEL만 long_max용으로 치환해 실행한다.

외부 절대경로는 참조하지 않는다.
이 파일은 반드시 저장소 내부 base_line/long_max/v12 위치에서 실행하거나,
저장소 루트 하위 어디서든 실행 가능하다.
"""
from pathlib import Path
import re


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / "base_line" / "long_main" / "v17" / "08_STANDALONE_FROZEN_RUNNER.py").exists():
            return p
    raise FileNotFoundError("Cannot find base_line/long_main/v17/08_STANDALONE_FROZEN_RUNNER.py from current path")


def main():
    root = find_repo_root(Path(__file__).parent)
    src_path = root / "base_line" / "long_main" / "v17" / "08_STANDALONE_FROZEN_RUNNER.py"
    src = src_path.read_text(encoding="utf-8")

    # The source is compressed. It restores the full standalone retest code at runtime.
    # Replace visible policy strings in the wrapper first. The decompressed code also has
    # long_main output policy; below replacement is applied after decompression by wrapping exec.
    prefix = """
import base64, zlib
"""
    m = re.search(r'_SRC_B64 = """([A-Za-z0-9+/=]+)"""', src)
    if not m:
        raise RuntimeError("Cannot locate compressed source payload")
    payload = m.group(1)
    code = __import__("zlib").decompress(__import__("base64").b64decode(payload)).decode("utf-8")
    code = code.replace('RUN_LABEL = "LONG_MAIN_LM26_TOP_CD32_RETEST"', 'RUN_LABEL = "LONG_MAX_LM26_TOP_CD32_RETEST"')
    code = code.replace('"local_results",\n        "long_main",', '"local_results",\n        "long_max",')
    code = code.replace('Path.cwd()/local_results/long_main only', 'Path.cwd()/local_results/long_max only')
    code = code.replace('./local_results/long_main', './local_results/long_max')
    exec(compile(code, __file__, "exec"), globals(), globals())


if __name__ == "__main__":
    main()
