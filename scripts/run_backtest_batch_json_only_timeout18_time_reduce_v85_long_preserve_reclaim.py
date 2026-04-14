from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "experiments" / "v81_long_base.json"
COMB = ROOT.parent / "experiments" / "v85_long_combinations.json"
ENGINE = ROOT / "run_backtest_batch_json_only_timeout18_time_reduce_v81_long_preserve_prior_no_reentry.py"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_batch(base_path=BASE, comb_path=COMB):
    mod = _load_module(ENGINE, "v81mod")
    if not hasattr(mod, "run_batch"):
        raise AttributeError("v81mod.run_batch not found")
    return mod.run_batch(str(base_path), str(comb_path))


if __name__ == "__main__":
    run_batch()
