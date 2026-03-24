from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "results" / "latest"


def main() -> None:
    summary_path = RESULT_DIR / "summary.json"
    trades_path = RESULT_DIR / "trades.csv"
    by_symbol_path = RESULT_DIR / "by_symbol.csv"

    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)

    trades = pd.read_csv(trades_path) if trades_path.exists() else pd.DataFrame()
    by_symbol = pd.read_csv(by_symbol_path) if by_symbol_path.exists() else pd.DataFrame()

    report = {
        "strategy": summary.get("strategy"),
        "symbols": summary.get("symbols", 0),
        "trades": summary.get("trades", 0),
        "final_asset": summary.get("final_asset"),
        "final_return_pct": summary.get("final_return", 0.0) * 100.0,
        "peak_asset": summary.get("peak_asset"),
        "peak_growth_pct": summary.get("peak_growth", 0.0) * 100.0,
        "mdd_pct": summary.get("mdd", 0.0) * 100.0,
        "win_rate_pct": summary.get("win_rate", 0.0) * 100.0,
        "pf": summary.get("pf"),
        "max_conc": summary.get("max_conc"),
        "top_symbols_by_trades": by_symbol.head(10).to_dict(orient="records") if not by_symbol.empty else [],
        "first_5_trades": trades.head(5).to_dict(orient="records") if not trades.empty else [],
    }

    with open(RESULT_DIR / "report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    lines = []
    lines.append("Backtest Report")
    lines.append("")
    lines.append(f"Strategy: {report['strategy']}")
    lines.append(f"Symbols: {report['symbols']}")
    lines.append(f"Trades: {report['trades']}")
    lines.append(f"Final asset: {report['final_asset']}")
    lines.append(f"Final return: {report['final_return_pct']:.4f}%")
    lines.append(f"Peak asset: {report['peak_asset']}")
    lines.append(f"Peak growth: {report['peak_growth_pct']:.4f}%")
    lines.append(f"MDD: {report['mdd_pct']:.4f}%")
    lines.append(f"Win rate: {report['win_rate_pct']:.4f}%")
    lines.append(f"PF: {report['pf']}")
    lines.append(f"Max concurrency: {report['max_conc']}")

    if report["top_symbols_by_trades"]:
        lines.append("")
        lines.append("Top symbols by trades:")
        for row in report["top_symbols_by_trades"]:
            lines.append(
                f"{row.get('symbol')} | bars={row.get('bars')} | trades={row.get('trades')} | wins={row.get('wins')} | losses={row.get('losses')} | win_rate={row.get('win_rate')} | pf={row.get('pf')} | sum_r={row.get('sum_r')}"
            )

    (RESULT_DIR / "report.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
