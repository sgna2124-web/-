from __future__ import annotations

import argparse, csv, json, os, shutil, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

BATCH = "short_max2_v2_combo08_retest20_preq4_primary_1h_v2"
OUT_SUBDIR = "short_max"
INITIAL_ASSET = 100.0
POS_FRAC = 0.01
FEE_PER_SIDE = 0.0004
COST_PCT = FEE_PER_SIDE * 2.0 * 100.0
WARMUP = 80
MIN_BARS = 120
PREQ4_END = "2025-09-30 23:59:59"
FULL_END = "2025-12-31 23:59:59"
Q4_START = "2025-10-01 00:00:00"
REC_DTYPE = np.dtype([("entry_ts", "<i8"), ("exit_ts", "<i8"), ("pnl", "<f4"), ("win", "i1"), ("symbol_i", "<i4")])

PREVIOUS_TOP1_REFERENCE = {
    "name": "smx2v2_combo08_stop253_rr5025_t320",
    "preq4_trades": 53528,
    "preq4_final_return_pct": 3691.4815,
    "preq4_mdd_pct": 2.1523,
    "preq4_official_cd_value": 3709.8784,
    "full_trades": 65117,
    "full_final_return_pct": 16374.5947,
    "full_mdd_pct": 2.2213,
    "full_official_cd_value": 16108.6431,
}

@dataclass(frozen=True)
class Strat:
    name: str
    tag: str
    atr_stop_mult: float = 2.53
    rr_mult: float = 5.025
    timeout_bars: int = 320
    fail_fast_bars: int = 12
    fail_fast_min_progress_r: float = 0.10
    time_reduce_bars: int = 3
    time_reduce_to_risk_frac: float = 0.0
    short_dev: float = 0.032
    short_rsi_min: float = 76.0
    short_wick_mult: float = 1.30
    score_min_short: float = 2.35
    score_dev_weight: float = 1.30
    score_rsi_weight: float = 0.80
    score_wick_weight: float = 0.70
    score_dev_cap: float = 2.0
    score_rsi_cap: float = 2.0
    score_wick_cap: float = 2.5
    wick_atr_floor_mult: float = 0.20
    dd_brake_trigger_pct: float = 0.035
    dd_brake_freeze_steps: int = 4
    close_pos_max: float = 1.00
    range20_max: float = 0.50
    atrp_min: float = 0.0018
    atrp_max: float = 0.110
    require_ema_reject: bool = False
    require_upper_sweep: bool = False


def log(msg: str) -> None:
    print(msg, flush=True)


def official_cd(final_return_pct: float, mdd_pct: float) -> float:
    if mdd_pct >= 100.0:
        return 0.0
    return INITIAL_ASSET * (1.0 - abs(mdd_pct) / 100.0) * (1.0 + final_return_pct / 100.0)


def parse_ts(s: pd.Series) -> pd.Series:
    if np.issubdtype(s.dtype, np.number):
        v = pd.to_numeric(s, errors="coerce")
        med = float(v.dropna().median()) if v.notna().any() else 0.0
        unit = "ms" if med > 1e12 else ("s" if med > 1e9 else None)
        if unit:
            return pd.to_datetime(v, unit=unit, utc=False, errors="coerce")
    return pd.to_datetime(s, utc=False, errors="coerce")


def standardize(df: pd.DataFrame) -> pd.DataFrame:
    ren = {}
    for c in df.columns:
        k = str(c).strip().lower()
        if k in {"time", "timestamp", "date", "datetime", "open_time", "ts"}: ren[c] = "timestamp"
        elif k in {"open", "o"}: ren[c] = "open"
        elif k in {"high", "h"}: ren[c] = "high"
        elif k in {"low", "l"}: ren[c] = "low"
        elif k in {"close", "c"}: ren[c] = "close"
        elif k in {"volume", "vol", "v", "quote_volume"}: ren[c] = "volume"
    df = df.rename(columns=ren)
    need = ["timestamp", "open", "high", "low", "close", "volume"]
    miss = [c for c in need if c not in df.columns]
    if miss: raise ValueError(f"missing columns: {miss}")
    df["dt"] = parse_ts(df["timestamp"])
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["dt", "open", "high", "low", "close", "volume"]).sort_values("dt")
    return df[["dt", "open", "high", "low", "close", "volume"]].drop_duplicates("dt").reset_index(drop=True)


def resample_1h(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) < 3: return df
    d = df.set_index("dt")
    med = d.index.to_series().diff().dropna().median()
    if pd.isna(med) or med >= pd.Timedelta(minutes=55):
        out = d
    else:
        out = d.resample("1h").agg({"open":"first", "high":"max", "low":"min", "close":"last", "volume":"sum"}).dropna()
    return out.reset_index()


def rsi_np(close: pd.Series, n: int = 14) -> np.ndarray:
    delta = close.diff().fillna(0.0)
    gain = delta.clip(lower=0).ewm(alpha=1.0/n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1.0/n, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100.0 - 100.0 / (1.0 + rs)).fillna(50.0).to_numpy(np.float32)


def make_feature_npz(csv_path: Path, out_path: Path, full_end_ns: int) -> Tuple[str, bool, str]:
    try:
        df = resample_1h(standardize(pd.read_csv(csv_path, low_memory=False)))
        df = df[df["dt"].view("int64") <= full_end_ns].reset_index(drop=True)
        if len(df) < MIN_BARS: raise ValueError(f"not enough 1h bars: {len(df)}")
        o,h,l,c,v = [df[x].astype("float64") for x in ["open","high","low","close","volume"]]
        pc = c.shift(1)
        tr = pd.concat([(h-l).abs(), (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1/14, adjust=False).mean().bfill().fillna(0)
        ema20 = c.ewm(span=20, adjust=False).mean()
        ema50 = c.ewm(span=50, adjust=False).mean()
        hh20 = h.rolling(20, min_periods=1).max(); ll20 = l.rolling(20, min_periods=1).min()
        hh50 = h.rolling(50, min_periods=1).max()
        rng = (h-l).replace(0, np.nan); body = (c-o).abs().replace(0, np.nan)
        uw = (h - np.maximum(o, c)).clip(lower=0)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(out_path,
            ts=df["dt"].view("int64").to_numpy(np.int64),
            o=o.to_numpy(np.float32), h=h.to_numpy(np.float32), l=l.to_numpy(np.float32), c=c.to_numpy(np.float32),
            atr=atr.to_numpy(np.float32), atrp=(atr/c.replace(0,np.nan)).fillna(0).to_numpy(np.float32),
            ema20=ema20.to_numpy(np.float32), ema50=ema50.to_numpy(np.float32), hh20=hh20.to_numpy(np.float32),
            hh50=hh50.to_numpy(np.float32), range20p=((hh20-ll20)/c.replace(0,np.nan)).fillna(0).to_numpy(np.float32),
            close_pos=((c-l)/rng).fillna(0.5).to_numpy(np.float32), uw_body=(uw/body).fillna(0).to_numpy(np.float32),
            uw_rng=(uw/rng).fillna(0).to_numpy(np.float32), rsi=rsi_np(c))
        return csv_path.stem, True, ""
    except Exception as e:
        return csv_path.stem, False, f"{type(e).__name__}: {e}"


def repo_root() -> Path:
    here = Path.cwd().resolve(); src = Path(__file__).resolve().parent
    for p in [here] + list(here.parents) + [src] + list(src.parents):
        if (p/"symbol_cost").exists() or (p/"코인"/"Data"/"time").exists() or (p/"Data"/"time").exists(): return p
    return here


def data_root(root: Path, explicit: Optional[str]) -> Path:
    if explicit: return Path(explicit).expanduser().resolve()
    for p in [root/"코인"/"Data"/"time", root/"Data"/"time", root/"time", root/"5m_data"]:
        if p.exists(): return p.resolve()
    return (root/"코인"/"Data"/"time").resolve()


def find_csvs(root: Path, max_symbols: Optional[int]) -> List[Path]:
    files = sorted(root.rglob("*.csv"))
    if not files: raise FileNotFoundError(f"csv not found: {root}")
    return files[:max_symbols] if max_symbols else files


def build_candidates() -> List[Strat]:
    b = Strat(name="RETEST_smx2v2_combo08_stop253_rr5025_t320", tag="top1_retest")
    rows: List[Strat] = [b]
    def r(n: int, tag: str, **kw: Any) -> None:
        d = asdict(b); d.update(kw); d["name"] = f"SMX2V2_C08_R20_{n:02d}_{tag}"; d["tag"] = tag; rows.append(Strat(**d))
    r(1,"stop250_rr505", atr_stop_mult=2.50, rr_mult=5.05)
    r(2,"stop256_rr505", atr_stop_mult=2.56, rr_mult=5.05)
    r(3,"stop253_rr515", rr_mult=5.15)
    r(4,"stop258_rr510_t340", atr_stop_mult=2.58, rr_mult=5.10, timeout_bars=340)
    r(5,"stop248_rr500_t300", atr_stop_mult=2.48, rr_mult=5.00, timeout_bars=300)
    r(6,"score237", score_min_short=2.37)
    r(7,"score240", score_min_short=2.40)
    r(8,"dev033", short_dev=0.033)
    r(9,"dev033_wick135", short_dev=0.033, short_wick_mult=1.35)
    r(10,"rsi77_score238", short_rsi_min=77.0, score_min_short=2.38)
    r(11,"ema_reject", require_ema_reject=True)
    r(12,"upper_sweep", require_upper_sweep=True)
    r(13,"closepos090", close_pos_max=0.90)
    r(14,"range45_score237", range20_max=0.45, score_min_short=2.37)
    r(15,"atrp095", atrp_max=0.095)
    r(16,"dd032_freeze5", dd_brake_trigger_pct=0.032, dd_brake_freeze_steps=5)
    r(17,"dd030_freeze6", dd_brake_trigger_pct=0.030, dd_brake_freeze_steps=6)
    r(18,"fail10", fail_fast_bars=10)
    r(19,"fail14_treduce4", fail_fast_bars=14, time_reduce_bars=4)
    r(20,"hybrid_q4low", short_dev=0.033, score_min_short=2.39, close_pos_max=0.92, dd_brake_trigger_pct=0.032, dd_brake_freeze_steps=5, rr_mult=5.08)
    return rows


def load_npz(path: Path, end_ns: int) -> Dict[str, np.ndarray]:
    z = np.load(path)
    ts = z["ts"]
    m = ts <= end_ns
    return {k: z[k][m] for k in z.files}


def score_signal(f: Dict[str, np.ndarray], i: int, s: Strat) -> Tuple[bool, float]:
    c = float(f["c"][i]); atr = float(f["atr"][i])
    if c <= 0 or atr <= 0: return False, 0.0
    if not (s.atrp_min <= float(f["atrp"][i]) <= s.atrp_max): return False, 0.0
    if float(f["range20p"][i]) > s.range20_max or float(f["close_pos"][i]) > s.close_pos_max: return False, 0.0
    dev = c / max(1e-12, float(f["ema20"][i])) - 1.0
    if dev < s.short_dev or float(f["rsi"][i]) < s.short_rsi_min: return False, 0.0
    if float(f["uw_body"][i]) < s.short_wick_mult and float(f["uw_rng"][i]) < min(0.62, 0.25 + s.short_wick_mult * s.wick_atr_floor_mult): return False, 0.0
    if s.require_upper_sweep and not (float(f["h"][i]) >= float(f["hh20"][i-1]) * 0.998 or float(f["h"][i]) >= float(f["hh50"][i-1]) * 0.996): return False, 0.0
    if s.require_ema_reject and not (float(f["h"][i]) >= float(f["ema20"][i]) and c <= float(f["ema20"][i]) * 1.006): return False, 0.0
    dev_component = min(s.score_dev_cap, max(0.0, (dev - s.short_dev) / max(1e-12, s.short_dev)))
    rsi_component = min(s.score_rsi_cap, max(0.0, (float(f["rsi"][i]) - s.short_rsi_min) / max(1e-12, 100.0 - s.short_rsi_min)))
    wick_component = min(s.score_wick_cap, max(0.0, float(f["uw_body"][i]) / max(1e-12, s.short_wick_mult)))
    score = s.score_dev_weight * dev_component + s.score_rsi_weight * rsi_component + s.score_wick_weight * wick_component
    return (score >= s.score_min_short), float(score)


def simulate_one(cache_path: str, symbol_i: int, sdict: Dict[str, Any], end_ns: int) -> Tuple[int, np.ndarray, str]:
    s = Strat(**sdict)
    try:
        f = load_npz(Path(cache_path), end_ns)
        n = len(f["c"])
        if n < MIN_BARS: return symbol_i, np.empty(0, dtype=REC_DTYPE), ""
        rec: List[Tuple[int,int,float,int,int]] = []
        pos = False; ep = stp = tgt = risk = 0.0; ei = entry_ts = 0; freeze_until = -1; peak = eq = 1.0
        for i in range(WARMUP, n-1):
            if pos:
                xp: Optional[float] = None
                if i - ei >= s.time_reduce_bars: stp = min(stp, ep + risk * s.time_reduce_to_risk_frac)
                if float(f["h"][i]) >= stp: xp = stp
                elif float(f["l"][i]) <= tgt: xp = tgt
                elif i - ei >= s.timeout_bars: xp = float(f["c"][i])
                elif i - ei >= s.fail_fast_bars:
                    progress_r = (ep - float(f["l"][i])) / max(1e-12, risk)
                    if progress_r < s.fail_fast_min_progress_r: xp = float(f["c"][i])
                if xp is not None:
                    pnl = (ep / max(1e-12, xp) - 1.0) * 100.0 - COST_PCT
                    rec.append((entry_ts, int(f["ts"][i]), float(pnl), int(pnl > 0), symbol_i))
                    eq *= max(0.0, 1.0 + POS_FRAC * pnl / 100.0); peak = max(peak, eq)
                    dd = abs(eq / peak - 1.0) * 100.0 if peak > 0 else 0.0
                    if dd >= s.dd_brake_trigger_pct * 100.0: freeze_until = max(freeze_until, i + s.dd_brake_freeze_steps)
                    pos = False
                    continue
            if (not pos) and i > freeze_until:
                ok, _ = score_signal(f, i, s)
                if not ok: continue
                ent_i = i + 1
                ep = float(f["o"][ent_i]); a = float(f["atr"][i])
                if ep <= 0 or a <= 0: continue
                risk = a * s.atr_stop_mult
                if risk * s.rr_mult / ep < 0.003: continue
                stp = ep + risk; tgt = max(1e-12, ep - risk * s.rr_mult); ei = ent_i; entry_ts = int(f["ts"][ent_i]); pos = True
        if pos:
            xp = float(f["c"][n-1]); pnl = (ep / max(1e-12, xp) - 1.0) * 100.0 - COST_PCT
            rec.append((entry_ts, int(f["ts"][n-1]), float(pnl), int(pnl > 0), symbol_i))
        return symbol_i, np.array(rec, dtype=REC_DTYPE), ""
    except Exception as e:
        return symbol_i, np.empty(0, dtype=REC_DTYPE), f"{Path(cache_path).name}: {type(e).__name__}: {e}"


def summarize(trades: np.ndarray) -> Dict[str, Any]:
    if len(trades) == 0:
        return {"trades":0,"win_rate":0.0,"pf":0.0,"final_asset":INITIAL_ASSET,"final_return_pct":0.0,"mdd_pct":0.0,"official_cd_value":INITIAL_ASSET,"max_conc":0,"same_bar_trades":0,"positive_months":0,"total_months":0,"positive_month_ratio":0.0,"avg_month_pnl":0.0}
    trades = np.sort(trades, order=["exit_ts", "entry_ts"])
    eq = peak = INITIAL_ASSET; mdd = 0.0; wins = 0; gp = gl = 0.0; month_eq: Dict[str, float] = {}
    for r in trades:
        p = float(r["pnl"]); before = eq; eq *= max(0.0, 1.0 + POS_FRAC * p / 100.0)
        peak = max(peak, eq); mdd = max(mdd, abs(eq / peak - 1.0) * 100.0 if peak > 0 else 100.0)
        if p > 0: wins += 1; gp += p
        else: gl += -p
        mon = pd.to_datetime(int(r["exit_ts"])).strftime("%Y-%m"); month_eq[mon] = month_eq.get(mon, 0.0) + (eq - before)
    ev: List[Tuple[int,int]] = []
    for r in trades: ev.append((int(r["entry_ts"]), 1)); ev.append((int(r["exit_ts"]), -1))
    active = mx = 0
    for _, d in sorted(ev, key=lambda x: (x[0], -x[1])): active += d; mx = max(mx, active)
    _, cnt = np.unique(trades["exit_ts"], return_counts=True)
    pos_m = sum(1 for v in month_eq.values() if v > 0); tot_m = len(month_eq)
    ret = (eq/INITIAL_ASSET-1)*100.0
    return {"trades":int(len(trades)), "win_rate":float(wins/len(trades)*100.0), "pf":float(gp/max(1e-12,gl)), "final_asset":float(eq), "final_return_pct":float(ret), "mdd_pct":float(mdd), "official_cd_value":float(official_cd(ret,mdd)), "max_conc":int(mx), "same_bar_trades":int(np.sum(cnt[cnt>1])), "positive_months":int(pos_m), "total_months":int(tot_m), "positive_month_ratio":float(pos_m/max(1,tot_m)*100.0), "avg_month_pnl":float(np.mean(list(month_eq.values())) if month_eq else 0.0)}


def run_candidate(cache_files: List[Path], strat: Strat, end_ns: int, workers: int) -> Tuple[Dict[str, Any], List[str]]:
    arrs: List[np.ndarray] = []; errs: List[str] = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(simulate_one, str(p), i, asdict(strat), end_ns) for i,p in enumerate(cache_files)]
        for fut in as_completed(futs):
            _, arr, err = fut.result()
            if err: errs.append(err)
            if len(arr): arrs.append(arr)
    trades = np.concatenate(arrs) if arrs else np.empty(0, dtype=REC_DTYPE)
    return summarize(trades), errs


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = sorted({k for r in rows for k in r.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)


def build_cache(csvs: List[Path], cache_dir: Path, workers: int, clean: bool) -> Tuple[List[Path], List[Dict[str, str]]]:
    if clean and cache_dir.exists(): shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    full_ns = pd.Timestamp(FULL_END).value; jobs = []; out_paths = []
    for i,p in enumerate(csvs):
        cp = cache_dir / f"{i:04d}_{p.stem}.npz"; out_paths.append(cp)
        if not cp.exists(): jobs.append((p, cp))
    errors: List[Dict[str,str]] = []
    if jobs:
        log(f"[CACHE] build 1h feature cache: {len(jobs)} files")
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(make_feature_npz, p, cp, full_ns) for p,cp in jobs]
            for k,fut in enumerate(as_completed(futs),1):
                sym, ok, err = fut.result()
                if not ok: errors.append({"symbol":sym,"error":err})
                if k % 50 == 0: log(f"[CACHE] {k}/{len(jobs)} done")
    return [p for p in out_paths if p.exists()], errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=None)
    ap.add_argument("--output-root", default="local_results")
    ap.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2)-1)))
    ap.add_argument("--max-symbols", type=int, default=None)
    ap.add_argument("--max-runtime-min", type=float, default=60.0)
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--rebuild-cache", action="store_true")
    ns = ap.parse_args()
    t0 = time.time(); root = repo_root(); dr = data_root(root, ns.data_root)
    out_dir = root / ns.output_root / OUT_SUBDIR / f"{BATCH}_results"
    if ns.clean and out_dir.exists(): shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = build_candidates(); write_csv(out_dir/"candidate_configs.csv", [asdict(c) for c in candidates])
    csvs = find_csvs(dr, ns.max_symbols); cache_files, load_errors = build_cache(csvs, out_dir/"_feature_cache_1h", ns.workers, ns.rebuild_cache)
    end_preq4 = pd.Timestamp(PREQ4_END).value; end_full = pd.Timestamp(FULL_END).value
    rows: List[Dict[str, Any]] = []; progress_path = out_dir/"progress.csv"
    for idx, s in enumerate(candidates, 1):
        if (time.time()-t0)/60.0 > ns.max_runtime_min and idx > 1:
            log(f"[TIME_LIMIT] stop before candidate {idx}; elapsed_min={(time.time()-t0)/60.0:.2f}"); break
        st = time.time(); log(f"[RUN] {idx}/{len(candidates)} {s.name}")
        pre, err1 = run_candidate(cache_files, s, end_preq4, ns.workers); full, err2 = run_candidate(cache_files, s, end_full, ns.workers)
        q4_return = full["final_return_pct"] - pre["final_return_pct"]; q4_share = q4_return / max(1e-12, abs(full["final_return_pct"])) * 100.0
        row = {"rank_input":idx, "strategy":s.name, "tag":s.tag, "elapsed_min":round((time.time()-st)/60.0,3), "errors":len(err1)+len(err2),
               **{f"preq4_{k}":v for k,v in pre.items()}, **{f"full_{k}":v for k,v in full.items()},
               "q4_delta_return_pct":q4_return, "q4_share_of_full_return_pct":q4_share,
               "preq4_primary_score": pre["official_cd_value"] * (1.0 + pre["positive_month_ratio"]/100.0) / max(1.0, 1.0 + pre["mdd_pct"]),
               "q4_penalized_score": pre["official_cd_value"] / max(1.0, 1.0 + max(0.0, q4_share-55.0)/10.0)}
        rows.append(row); write_csv(progress_path, rows)
        (out_dir/"latest_errors.json").write_text(json.dumps({"load_errors":load_errors, "candidate_errors":err1+err2}, ensure_ascii=False, indent=2), encoding="utf-8")
    scored = sorted(rows, key=lambda r: (float(r["preq4_primary_score"]), float(r["q4_penalized_score"])), reverse=True)
    write_csv(out_dir/"summary_full_unsorted.csv", rows); write_csv(out_dir/"scored_summary.csv", scored); write_csv(out_dir/"summary_compact.csv", scored[:30])
    meta = {"batch":BATCH,"script":Path(__file__).name,"elapsed_min":(time.time()-t0)/60.0,"candidate_count_requested":len(candidates),"candidate_count_completed":len(rows),"workers":ns.workers,"data_root":str(dr),"csv_files":len(csvs),"feature_cache_files":len(cache_files),"preq4_end":PREQ4_END,"full_end":FULL_END,"q4_start":Q4_START,"previous_top1_reference":PREVIOUS_TOP1_REFERENCE,"engine":"self_contained_1h_next_open_short_actual_bar_no_same_timestamp_reentry_no_heavy_trades"}
    (out_dir/"run_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"[BATCH] {BATCH}", f"[ELAPSED_MIN] {meta['elapsed_min']:.3f}", f"[COMPLETED] {len(rows)}/{len(candidates)}", "", "[TOP_PREQ4_PRIMARY]"]
    for r in scored[:10]:
        lines.append(f"{r['strategy']} | pre_cd={float(r['preq4_official_cd_value']):.4f} | pre_ret={float(r['preq4_final_return_pct']):.4f} | pre_mdd={float(r['preq4_mdd_pct']):.4f} | full_cd={float(r['full_official_cd_value']):.4f} | q4_share={float(r['q4_share_of_full_return_pct']):.2f}% | elapsed={r['elapsed_min']}")
    (out_dir/"README_RESULT.txt").write_text("\n".join(lines)+"\n", encoding="utf-8")
    log(f"[SAVE] {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
