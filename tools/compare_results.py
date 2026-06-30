"""
合并各 suite 的覆盖率汇总 CSV，输出对比表。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from paths import default_results_root, load_pde_program_names, load_program_names, summary_csv_path


def _load_suite_csv(suite: str, results_root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    p = summary_csv_path(results_root, suite)
    if not p.exists():
        return out
    with p.open(encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f)
        for row in r:
            out[row["program"]] = row.get("example_branch_cover_pct", "")
    return out


def _fmt(v: str) -> str:
    try:
        return f"{float(v):.2f}%"
    except Exception:
        return v or "-"


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare branch coverage across suites")
    ap.add_argument("--suites", nargs="+", default=["pynguin", "coverup", "codamosa", "chatgpt"])
    ap.add_argument("--pde-only", action="store_true")
    ap.add_argument("--results-root", type=Path, default=None, help="兼容参数，可忽略")
    args = ap.parse_args()

    results_root = (args.results_root or default_results_root()).resolve()
    names = load_pde_program_names() if args.pde_only else load_program_names()
    data = {s: _load_suite_csv(s, results_root) for s in args.suites}
    avail = [s for s in args.suites if data[s]]
    if not avail:
        print("未找到任何 coverage_summary_<suite>.csv")
        return 1

    rows: list[dict[str, str]] = []
    for n in names:
        row = {"program": n}
        for s in avail:
            row[s] = data[s].get(n, "")
        rows.append(row)

    out = (Path("comparison_table.csv")).resolve()
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["program", *avail])
        w.writeheader()
        w.writerows(rows)

    header = "Program".ljust(30) + "".join(s.rjust(14) for s in avail)
    print(header)
    print("-" * len(header))
    for r in rows:
        line = r["program"].ljust(30) + "".join(_fmt(r[s]).rjust(14) for s in avail)
        print(line)
    print(f"\n[ok] comparison csv: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
