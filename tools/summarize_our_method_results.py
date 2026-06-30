"""Summarize proposed-method evaluation results.

Input:
    scientific_calculation/<program>/our_method/round_<N>/evaluation_round_<N>.json

Output:
    our_method_summary.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from paths import ROOT, SCI_ROOT

DEFAULT_OUTPUT = ROOT / "our_method_summary.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize proposed-method branch coverage")
    parser.add_argument("--round", type=int, default=1)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser


def evaluation_path(program: str, round_no: int) -> Path:
    return SCI_ROOT / program / "our_method" / f"round_{round_no}" / f"evaluation_round_{round_no}.json"


def collect(round_no: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for program_dir in sorted(p for p in SCI_ROOT.iterdir() if p.is_dir()):
        path = evaluation_path(program_dir.name, round_no)
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "program": program_dir.name,
                "round": data.get("round", round_no),
                "branch_coverage": data.get("branch_coverage", ""),
                "line_coverage": data.get("line_coverage", ""),
                "line_branch_coverage": data.get("line_branch_coverage", ""),
                "covered_branches": data.get("covered_branches", ""),
                "num_branches": data.get("num_branches", ""),
                "num_failed_tests": data.get("num_failed_tests", ""),
                "num_test_files": data.get("num_test_files", ""),
                "include_pynguin_baseline": data.get("include_pynguin_baseline", ""),
                "returncode": data.get("returncode", ""),
            }
        )
    return rows


def main() -> int:
    args = build_parser().parse_args()
    rows = collect(args.round)
    fieldnames = [
        "program",
        "round",
        "branch_coverage",
        "line_coverage",
        "line_branch_coverage",
        "covered_branches",
        "num_branches",
        "num_failed_tests",
        "num_test_files",
        "include_pynguin_baseline",
        "returncode",
    ]
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
