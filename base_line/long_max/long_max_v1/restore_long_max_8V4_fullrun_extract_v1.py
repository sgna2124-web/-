#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
restore_long_max_8V4_fullrun_extract_v1.py

long_max 기준선 복원용 실행 파일.

핵심 원칙:
- 8V4_V51_V002_core_rare22_c1만 먼저 필터링하지 않는다.
- base_line/8V4_long400_reviewed.py 원본의 400개 전략 전체를 실행한다.
- 실행 완료 후 target 전략만 결과에서 추출한다.

실행:
python .\restore_long_max_8V4_fullrun_extract_v1.py

병렬 실행이 불안정하면:
python .\restore_long_max_8V4_fullrun_extract_v1.py --sequential

결과만 다시 추출:
python .\restore_long_max_8V4_fullrun_extract_v1.py --extract-only
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional


TARGET_STRATEGY = "8V4_V51_V002_core_rare22_c1"
SOURCE_FILENAME = "8V4_long400_reviewed.py"

BATCH_LABEL = "RESTORE_EXACT_8V4_LONG400_FULL_FEE008_V1"
WRAPPER_RESULT_DIRNAME = "RESTORE_LONG_MAX_8V4_FULLRUN_EXTRACT_V1"
PATCHED_FILENAME = "restore_8V4_long400_fullrun_fee008_v1__patched.py"

REFERENCE = {
    "strategy_name": TARGET_STRATEGY,
    "trades": 2276,
    "win_rate_pct": 45.2548,
    "final_return_pct": 43.6673,
    "max_return_pct": 44.2664,
    "max_drawdown_pct": 6.7587,
    "official_cd_value": 133.9572,
}

SCRIPT_DIR = Path(__file__).resolve().parent
CWD = Path.cwd().resolve()


def unique_paths(paths: Iterable[Path]) -> List[Path]:
    out: List[Path] = []
    seen = set()
    for p in paths:
        try:
            rp = p.resolve()
        except Exception:
            rp = p
        key = str(rp).lower()
        if key not in seen:
            seen.add(key)
            out.append(rp)
    return out


def candidate_roots() -> List[Path]:
    roots: List[Path] = []
    for base in [SCRIPT_DIR, CWD]:
        roots.append(base)
        roots.extend(base.parents)

    for base in [SCRIPT_DIR, CWD]:
        roots.extend([
            base / "base_line",
            base / "baseline",
            base / "코인",
            base / "22_gpt_",
            base / "코인" / "22_gpt_",
            base.parent / "base_line",
            base.parent / "baseline",
            base.parent / "코인",
            base.parent / "22_gpt_",
            base.parent / "코인" / "22_gpt_",
        ])
    return unique_paths([p for p in roots if p.exists()])


def find_source_file(explicit: Optional[str]) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.is_file():
            raise FileNotFoundError(f"--source-path not found: {p}")
        return p

    checked: List[Path] = []
    for root in candidate_roots():
        for p in [
            root / SOURCE_FILENAME,
            root / "base_line" / SOURCE_FILENAME,
            root / "baseline" / SOURCE_FILENAME,
            root / "코인" / "22_gpt_" / "base_line" / SOURCE_FILENAME,
            root / "22_gpt_" / "base_line" / SOURCE_FILENAME,
        ]:
            checked.append(p)
            if p.is_file():
                return p

    scan_roots: List[Path] = []
    for base in [SCRIPT_DIR, CWD]:
        scan_roots.append(base)
        scan_roots.extend(list(base.parents)[:4])

    for root in unique_paths([p for p in scan_roots if p.exists()]):
        try:
            for p in root.rglob(SOURCE_FILENAME):
                ps = str(p).lower()
                if p.is_file() and ("base_line" in ps or "baseline" in ps):
                    return p
        except Exception:
            continue

    lines = [f"[SOURCE_NOT_FOUND] {SOURCE_FILENAME}", "checked:"]
    for p in checked[:120]:
        lines.append(f"  {p}")
    if len(checked) > 120:
        lines.append(f"  ... {len(checked) - 120} more")
    raise FileNotFoundError("\n".join(lines))


def find_data_root(source_path: Path, explicit_data_dir: Optional[str]) -> Path:
    if explicit_data_dir:
        p = Path(explicit_data_dir).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"--data-dir does not exist: {p}")
        if not any(p.rglob("*.csv")):
            raise FileNotFoundError(f"--data-dir has no csv files: {p}")
        return p

    bases: List[Path] = [SCRIPT_DIR, CWD, source_path.parent, source_path.parent.parent]
    roots: List[Path] = []
    for base in bases:
        roots.append(base)
        roots.extend(base.parents)

    candidates: List[Path] = []
    for root in unique_paths([p for p in roots if p.exists()]):
        candidates.extend([
            root / "코인" / "Data" / "time",
            root / "Data" / "time",
            root / "time",
        ])

    for p in unique_paths(candidates):
        if p.exists() and any(p.rglob("*.csv")):
            return p

    lines = ["[DATA_ROOT_NOT_FOUND] CSV 데이터 폴더를 찾지 못했다.", "checked:"]
    for p in unique_paths(candidates)[:120]:
        lines.append(f"  {p}")
    raise FileNotFoundError("\n".join(lines))


def find_repo_root(source_path: Path, data_root: Path, explicit_repo_root: Optional[str]) -> Path:
    if explicit_repo_root:
        p = Path(explicit_repo_root).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"--repo-root does not exist: {p}")
        return p

    if data_root.name.lower() == "time" and data_root.parent.name.lower() == "data":
        return data_root.parent.parent

    if source_path.parent.name.lower() in {"base_line", "baseline"}:
        return source_path.parent.parent

    return CWD


def find_symbol_cost(repo_root: Path, source_path: Path, explicit_symbol_cost: Optional[str]) -> Path:
    if explicit_symbol_cost:
        return Path(explicit_symbol_cost).expanduser().resolve()

    candidates: List[Path] = []
    bases = [repo_root, SCRIPT_DIR, CWD, source_path.parent, source_path.parent.parent]
    for base in bases:
        candidates.append(base / "symbol_cost")
        for parent in base.parents:
            candidates.append(parent / "symbol_cost")

    for p in unique_paths(candidates):
        if p.exists():
            return p

    return repo_root / "symbol_cost"


def replace_assignment(src: str, name: str, value_literal: str, required: bool = True) -> str:
    pattern = rf"^{re.escape(name)}\s*=\s*.*$"
    out, n = re.subn(pattern, f"{name} = {value_literal}", src, count=1, flags=re.MULTILINE)
    if required and n != 1:
        raise RuntimeError(f"assignment replace failed: {name}")
    return out


def inject_sequential_executor(src: str, sequential: bool) -> str:
    if not sequential:
        return src

    import_line = "from concurrent.futures import ProcessPoolExecutor, as_completed"
    if import_line not in src:
        print("[WARN] ProcessPool import line not found. sequential patch skipped.")
        return src

    injection = r'''
# ---- injected sequential executor for restore safety ----
class _ImmediateFuture:
    def __init__(self, fn, *args, **kwargs):
        self._result = None
        self._exc = None
        try:
            self._result = fn(*args, **kwargs)
        except BaseException as exc:
            self._exc = exc

    def result(self):
        if self._exc is not None:
            raise self._exc
        return self._result


class ProcessPoolExecutor:
    def __init__(self, max_workers=None):
        self.max_workers = max_workers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def submit(self, fn, *args, **kwargs):
        return _ImmediateFuture(fn, *args, **kwargs)


def as_completed(futures):
    return list(futures)
# --------------------------------------------------------
'''
    return src.replace(import_line, import_line + "\n" + injection, 1)


def inject_fixed_paths(src: str, repo_root: Path, data_root: Path, symbol_cost: Path) -> str:
    marker = "RESULT_ROOT.mkdir(parents=True, exist_ok=True)"
    override = f'''
# ---- injected fixed paths for long_max restore ----
REPO_ROOT = Path({str(repo_root)!r})
DATA_ROOT = Path({str(data_root)!r})
SYMBOL_COST_PATH = Path({str(symbol_cost)!r})
RESULT_ROOT = REPO_ROOT / "local_results" / {BATCH_LABEL!r}
RESULT_ROOT.mkdir(parents=True, exist_ok=True)
print(f"[PATHS] REPO_ROOT={{REPO_ROOT}}", flush=True)
print(f"[PATHS] DATA_ROOT={{DATA_ROOT}}", flush=True)
print(f"[PATHS] SYMBOL_COST_PATH={{SYMBOL_COST_PATH}} exists={{SYMBOL_COST_PATH.exists()}}", flush=True)
print(f"[PATHS] RESULT_ROOT={{RESULT_ROOT}}", flush=True)
# --------------------------------------------------
'''
    if marker in src:
        return src.replace(marker, marker + "\n" + override, 1)

    idx = src.find("STRATEGIES")
    if idx >= 0:
        return src[:idx] + override + "\n" + src[idx:]

    raise RuntimeError("path override marker not found")


def inject_target_probe(src: str) -> str:
    marker = "@dataclass\nclass TradeRecord:"
    if marker not in src:
        raise RuntimeError("target probe marker not found: @dataclass\\nclass TradeRecord:")

    probe = f'''
# ---- injected target probe, do not filter STRATEGIES ----
_TARGET_STRATEGY_NAME = {TARGET_STRATEGY!r}
_target_matches = [s for s in STRATEGIES if getattr(s, "name", None) == _TARGET_STRATEGY_NAME]
print(f"[TARGET_PROBE] target={{_TARGET_STRATEGY_NAME}} count={{len(_target_matches)}} total_strategies={{len(STRATEGIES)}}", flush=True)
if not _target_matches:
    print("[TARGET_PROBE] first 20 strategy names:", [getattr(s, "name", None) for s in STRATEGIES[:20]], flush=True)
    raise RuntimeError(f"target strategy was not generated: {{_TARGET_STRATEGY_NAME}}")
else:
    s = _target_matches[0]
    print(f"[TARGET_PROBE] found={{s.name}} desc={{s.description}} atr_stop={{s.atr_stop}} rr={{s.rr_target}} hold={{s.max_hold_bars}} cooldown={{s.cooldown_bars}}", flush=True)
# --------------------------------------------------------
'''
    return src.replace(marker, probe + "\n" + marker, 1)


def patch_source(src: str, repo_root: Path, data_root: Path, symbol_cost: Path, sequential: bool) -> str:
    src = inject_sequential_executor(src, sequential=sequential)
    src = replace_assignment(src, "BATCH_LABEL", repr(BATCH_LABEL))
    src = replace_assignment(src, "ROUND_TRIP_COST_BPS", "8.0")
    src = replace_assignment(src, "POSITION_FRACTION", "0.01", required=False)
    src = replace_assignment(src, "DEFAULT_WORKERS", "1" if sequential else "max(1, (os.cpu_count() or 2) - 1)", required=False)
    src = inject_fixed_paths(src, repo_root=repo_root, data_root=data_root, symbol_cost=symbol_cost)
    src = inject_target_probe(src)

    header = (
        "# AUTO-GENERATED PATCHED RUNNER FOR LONG_MAX FULL 8V4 RESTORE\n"
        f"# target={TARGET_STRATEGY}\n"
        f"# batch_label={BATCH_LABEL}\n"
        f"# repo_root={repo_root}\n"
        f"# data_root={data_root}\n"
        f"# symbol_cost={symbol_cost}\n"
        f"# sequential={sequential}\n\n"
    )
    return header + src


def stream_subprocess(cmd: List[str], cwd: Path, log_path: Path) -> int:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    with log_path.open("w", encoding="utf-8", errors="replace") as logf:
        logf.write(f"[CMD] {' '.join(cmd)}\n")
        logf.write(f"[CWD] {cwd}\n\n")
        logf.flush()

        proc = subprocess.Popen(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=env)
        assert proc.stdout is not None

        for line in proc.stdout:
            print(line, end="")
            logf.write(line)
            logf.flush()

        return proc.wait()


def load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def find_target_result_dir(full_result_root: Path) -> Optional[Path]:
    direct = full_result_root / TARGET_STRATEGY
    if direct.exists():
        return direct

    if not full_result_root.exists():
        return None

    for p in full_result_root.rglob(TARGET_STRATEGY):
        if p.is_dir():
            return p

    for js in list(full_result_root.rglob("summary.json")) + list(full_result_root.rglob("registry.json")):
        data = load_json(js)
        if not isinstance(data, dict):
            continue
        name = data.get("strategy_name") or data.get("strategy") or data.get("name")
        if name == TARGET_STRATEGY:
            return js.parent

    return None


def read_csv_target_rows(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        return []
    rows: List[Dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = set(str(v) for v in row.values())
            if TARGET_STRATEGY in values or row.get("strategy") == TARGET_STRATEGY or row.get("strategy_name") == TARGET_STRATEGY:
                rows.append(row)
    return rows


def make_compare(summary: Optional[dict], registry: Optional[dict]) -> Dict[str, object]:
    data = {}
    if isinstance(registry, dict):
        data.update(registry)
    if isinstance(summary, dict):
        data.update(summary)

    def get_num(*keys, default=None):
        for k in keys:
            if k in data:
                try:
                    return float(data[k])
                except Exception:
                    return data[k]
        return default

    actual = {
        "strategy_name": data.get("strategy_name") or data.get("strategy") or TARGET_STRATEGY,
        "trades": int(get_num("trades", default=0) or 0),
        "wins": int(get_num("wins", default=0) or 0),
        "losses": int(get_num("losses", default=0) or 0),
        "win_rate_pct": get_num("win_rate_pct", "win_rate", default=0),
        "final_return_pct": get_num("final_return_pct", "final_return", default=0),
        "max_return_pct": get_num("max_return_pct", "max_return", default=0),
        "max_drawdown_pct": get_num("max_drawdown_pct", "max_drawdown", default=0),
        "official_cd_value": get_num("official_cd_value", "cd_value", "official_cd", default=0),
    }

    def diff(key):
        a = actual.get(key)
        b = REFERENCE.get(key)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a - b
        return None

    compare = {
        "target": TARGET_STRATEGY,
        "reference": REFERENCE,
        "actual": actual,
        "diff": {
            "trades": diff("trades"),
            "win_rate_pct": diff("win_rate_pct"),
            "final_return_pct": diff("final_return_pct"),
            "max_return_pct": diff("max_return_pct"),
            "max_drawdown_pct": diff("max_drawdown_pct"),
            "official_cd_value": diff("official_cd_value"),
        },
        "verdict": "unknown",
    }

    trades_ok = actual["trades"] == REFERENCE["trades"]
    maxret_ok = isinstance(actual["max_return_pct"], (int, float)) and abs(actual["max_return_pct"] - REFERENCE["max_return_pct"]) <= 1.0
    mdd_ok = isinstance(actual["max_drawdown_pct"], (int, float)) and abs(actual["max_drawdown_pct"] - REFERENCE["max_drawdown_pct"]) <= 1.0

    if trades_ok and maxret_ok and mdd_ok:
        compare["verdict"] = "restore_success"
    elif actual["trades"] > 0:
        compare["verdict"] = "partial_restore_nonzero_trades"
    else:
        compare["verdict"] = "restore_fail_zero_trades"

    return compare


def extract_target(repo_root: Path, wrapper_root: Path) -> Dict[str, object]:
    full_result_root = repo_root / "local_results" / BATCH_LABEL
    target_dir = find_target_result_dir(full_result_root)

    extracted_dir = wrapper_root / "extracted_target"
    extracted_dir.mkdir(parents=True, exist_ok=True)

    summary = None
    registry = None
    copied_files: List[str] = []

    if target_dir is not None:
        for fname in ["summary.json", "registry.json", "trades.csv", "equity_curve.csv", "summary.csv"]:
            src = target_dir / fname
            if src.exists():
                dst = extracted_dir / fname
                shutil.copy2(src, dst)
                copied_files.append(str(dst))

        summary = load_json(target_dir / "summary.json")
        registry = load_json(target_dir / "registry.json")

    target_rows: List[Dict[str, str]] = []
    for fname in ["master_summary.csv", "summary.csv", "registry.csv"]:
        rows = read_csv_target_rows(full_result_root / fname)
        if rows:
            target_rows.extend(rows)

    if target_rows:
        target_csv = extracted_dir / "target_rows_from_batch_csv.csv"
        with target_csv.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(target_rows[0].keys()))
            writer.writeheader()
            writer.writerows(target_rows)
        copied_files.append(str(target_csv))

    compare = make_compare(summary=summary, registry=registry)
    compare["full_result_root"] = str(full_result_root)
    compare["target_dir"] = str(target_dir) if target_dir is not None else None
    compare["extracted_dir"] = str(extracted_dir)
    compare["copied_files"] = copied_files
    compare["target_rows_from_csv_count"] = len(target_rows)

    compare_path = extracted_dir / "target_compare.json"
    compare_path.write_text(json.dumps(compare, ensure_ascii=False, indent=2), encoding="utf-8")

    report_lines = [
        "LONG_MAX RESTORE TARGET COMPARE",
        f"target: {TARGET_STRATEGY}",
        f"full_result_root: {full_result_root}",
        f"target_dir: {target_dir}",
        f"verdict: {compare['verdict']}",
        "",
        "[reference]",
    ]
    for k, v in REFERENCE.items():
        report_lines.append(f"{k}: {v}")

    report_lines.extend(["", "[actual]"])
    for k, v in compare["actual"].items():
        report_lines.append(f"{k}: {v}")

    report_lines.extend(["", "[diff]"])
    for k, v in compare["diff"].items():
        report_lines.append(f"{k}: {v}")

    report_path = extracted_dir / "target_compare_report.txt"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"[EXTRACT] full_result_root={full_result_root}")
    print(f"[EXTRACT] target_dir={target_dir}")
    print(f"[EXTRACT] extracted_dir={extracted_dir}")
    print(f"[EXTRACT] verdict={compare['verdict']}")
    print(f"[EXTRACT] actual={compare['actual']}")

    return compare


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-path", default=None)
    ap.add_argument("--data-dir", default=None)
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--symbol-cost", default=None)
    ap.add_argument("--sequential", action="store_true", help="원본 병렬 실행 대신 순차 실행")
    ap.add_argument("--extract-only", action="store_true", help="이미 생성된 결과에서 target만 추출")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    source_path = find_source_file(args.source_path)
    data_root = find_data_root(source_path, args.data_dir)
    repo_root = find_repo_root(source_path, data_root, args.repo_root)
    symbol_cost = find_symbol_cost(repo_root, source_path, args.symbol_cost)

    wrapper_root = repo_root / "local_results" / WRAPPER_RESULT_DIRNAME
    wrapper_root.mkdir(parents=True, exist_ok=True)

    log_dir = wrapper_root / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "8V4_fullrun.log"

    patched_dir = wrapper_root / "_patched_sources"
    patched_dir.mkdir(parents=True, exist_ok=True)
    patched_path = patched_dir / PATCHED_FILENAME

    print(f"[SCRIPT_DIR] {SCRIPT_DIR}")
    print(f"[CWD] {CWD}")
    print(f"[SOURCE] {source_path}")
    print(f"[REPO_ROOT] {repo_root}")
    print(f"[DATA_ROOT] {data_root}")
    print(f"[SYMBOL_COST] {symbol_cost} exists={symbol_cost.exists()}")
    print(f"[WRAPPER_ROOT] {wrapper_root}")
    print(f"[BATCH_LABEL] {BATCH_LABEL}")
    print(f"[TARGET] {TARGET_STRATEGY}")
    print(f"[MODE] {'sequential' if args.sequential else 'parallel'}")
    print("[FEE] ROUND_TRIP_COST_BPS=8.0")
    print("[POSITION] POSITION_FRACTION=0.01")

    manifest: Dict[str, object] = {
        "script": Path(__file__).name,
        "source_path": str(source_path),
        "repo_root": str(repo_root),
        "data_root": str(data_root),
        "symbol_cost": str(symbol_cost),
        "wrapper_root": str(wrapper_root),
        "batch_label": BATCH_LABEL,
        "target_strategy": TARGET_STRATEGY,
        "mode": "sequential" if args.sequential else "parallel",
        "fee_bps": 8.0,
        "position_fraction": 0.01,
        "reference": REFERENCE,
        "run": None,
        "extract": None,
    }

    if not args.extract_only:
        src = source_path.read_text(encoding="utf-8", errors="replace")
        patched = patch_source(src, repo_root=repo_root, data_root=data_root, symbol_cost=symbol_cost, sequential=args.sequential)
        patched_path.write_text(patched, encoding="utf-8")
        print(f"[PATCHED] {patched_path}")
        print(f"[LOG] {log_path}")

        if not args.dry_run:
            start = time.time()
            rc = stream_subprocess([sys.executable, str(patched_path)], cwd=repo_root, log_path=log_path)
            elapsed = time.time() - start
            manifest["run"] = {"returncode": rc, "elapsed_sec": elapsed, "patched_path": str(patched_path), "log_path": str(log_path)}
            print(f"[DONE] returncode={rc} elapsed={elapsed:.1f}s")
            if rc != 0:
                manifest_path = wrapper_root / "restore_long_max_manifest.json"
                manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
                raise RuntimeError(f"8V4 full run failed. log={log_path}")
        else:
            manifest["run"] = {"dry_run": True, "patched_path": str(patched_path), "log_path": str(log_path)}

    if not args.dry_run:
        compare = extract_target(repo_root=repo_root, wrapper_root=wrapper_root)
        manifest["extract"] = compare

    manifest_path = wrapper_root / "restore_long_max_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[MANIFEST] {manifest_path}")

    print("[RESULT_PATHS]")
    print(f"full batch: {repo_root / 'local_results' / BATCH_LABEL}")
    print(f"target extracted: {wrapper_root / 'extracted_target'}")
    print(f"compare report: {wrapper_root / 'extracted_target' / 'target_compare_report.txt'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
