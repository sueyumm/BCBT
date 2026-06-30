"""Summarize CodaMosa coverage results under scientific_calculation.

Default result layout:
    scientific_calculation/<program>/codamosa/result_4o/

Outputs:
    - console summary
    - tools/codamosa_coverage_summary.csv by default
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from paths import ROOT, SCI_ROOT

DEFAULT_RESULT_DIR = Path("codamosa") / "result_4o"
DEFAULT_OUT = ROOT / "codamosa_coverage_summary.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize CodaMosa coverage results")
    parser.add_argument("--root", type=Path, default=SCI_ROOT)
    parser.add_argument("--result-dir", type=Path, default=DEFAULT_RESULT_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def _read_last_statistics_row(statistics_csv: Path) -> dict[str, str]:
    if not statistics_csv.is_file():
        return {}
    with statistics_csv.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        last_row: dict[str, str] | None = None
        for row in reader:
            last_row = row
    return last_row or {}


def collect_rows(root: Path, result_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for program_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        out_dir = program_dir / result_dir
        stat_file = out_dir / "statistics.csv"
        if not stat_file.is_file():
            continue
        row = _read_last_statistics_row(stat_file)
        rows.append(
            {
                "program": program_dir.name,
                "target_module": row.get("TargetModule", ""),
                "coverage": row.get("Coverage", ""),
                "branch_coverage": row.get("BranchCoverage", ""),
                "line_coverage": row.get("LineCoverage", ""),
                "parsed_statements": row.get("ParsedStatements", ""),
                "parsable_statements": row.get("ParsableStatements", ""),
                "uninterp_statements": row.get("UninterpStatements", ""),
                "llm_calls": row.get("LLMCalls", ""),
                "llm_query_time": row.get("LLMQueryTime", ""),
                "llm_stage_saved_tests": row.get("LLMStageSavedTests", ""),
                "accessible_objects_under_test": row.get("AccessibleObjectsUnderTest", ""),
                "code_objects": row.get("CodeObjects", ""),
            }
        )
    return rows


def _avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def print_summary(rows: list[dict[str, str]]) -> None:
    print(f"Scanned {len(rows)} CodaMosa result directories.\n")
    print(f"{'Program':<30} {'Cov':>8} {'Branch':>8} {'Line':>8} {'LLM':>6} {'Saved':>6}")
    print("-" * 74)
    for row in rows:
        print(
            f"{row['program']:<30} "
            f"{row['coverage']:>8} "
            f"{row['branch_coverage']:>8} "
            f"{row['line_coverage']:>8} "
            f"{row['llm_calls']:>6} "
            f"{row['llm_stage_saved_tests']:>6}"
        )

    cov_values: list[float] = []
    branch_values: list[float] = []
    line_values: list[float] = []
    for row in rows:
        for key, bucket in (
            ("coverage", cov_values),
            ("branch_coverage", branch_values),
            ("line_coverage", line_values),
        ):
            try:
                bucket.append(float(row[key]))
            except (TypeError, ValueError):
                pass

    print("\nAverages")
    print("-" * 74)
    print(f"Coverage       : {_avg(cov_values):.4f} (n={len(cov_values)})")
    print(f"BranchCoverage : {_avg(branch_values):.4f} (n={len(branch_values)})")
    print(f"LineCoverage   : {_avg(line_values):.4f} (n={len(line_values)})")


def write_csv(rows: list[dict[str, str]], out_path: Path) -> None:
    fieldnames = [
        "program",
        "target_module",
        "coverage",
        "branch_coverage",
        "line_coverage",
        "parsed_statements",
        "parsable_statements",
        "uninterp_statements",
        "llm_calls",
        "llm_query_time",
        "llm_stage_saved_tests",
        "accessible_objects_under_test",
        "code_objects",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved coverage summary to {out_path}")


def main() -> int:
    args = build_parser().parse_args()
    rows = collect_rows(args.root.resolve(), args.result_dir)
    if not rows:
        print("No statistics.csv files found. Check --root and --result-dir.")
        return 1
    print_summary(rows)
    try:
        write_csv(rows, args.out.resolve())
    except PermissionError as exc:
        print(f"\nCould not write CSV: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
