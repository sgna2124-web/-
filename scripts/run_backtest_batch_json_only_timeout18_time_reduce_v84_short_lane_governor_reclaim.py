from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "experiments" / "v80_short_base.json"
COMB = ROOT.parent / "experiments" / "v84_short_combinations.json"
ENGINE = ROOT / "run_backtest_batch_json_only_timeout18_time_reduce_v80_short_lane_governor_refine.py"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_batch(base_path=BASE, comb_path=COMB):
    mod = _load_module(ENGINE, "v80mod")
    if not hasattr(mod, "run_batch"):
        raise AttributeError("v80mod.run_batch not found")
    return mod.run_batch(str(base_path), str(comb_path))


if __name__ == "__main__":
    run_batch()
