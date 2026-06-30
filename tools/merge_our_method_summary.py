"""Merge proposed-method best valid results into the main summary table.

Inputs:
    summary.csv
    scientific_calculation/<program>/our_method/round_*/evaluation_round_*.json
    scientific_calculation/<program>/our_method/round_*/filtered_evaluation_round_*.json

Outputs:
    our_method_best_summary.csv
    summary_with_our_method.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from paths import ROOT, SCI_ROOT

DEFAULT_BASELINE_SUMMARY = ROOT / "summary.csv"
DEFAULT_OUR_BEST = ROOT / "our_method_best_summary.csv"
DEFAULT_OUTPUT = ROOT / "summary_with_our_method.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge proposed-method results into summary.csv")
    parser.add_argument("--summary", type=Path, default=DEFAULT_BASELINE_SUMMARY)
    parser.add_argument("--our-best-output", type=Path, default=DEFAULT_OUR_BEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser


def read_evaluations(program: str) -> list[dict[str, Any]]:
    root = SCI_ROOT / program / "our_method"
    if not root.is_dir():
        return []
    evaluations: list[dict[str, Any]] = []
    for path in sorted(root.glob("round_*/evaluation_round_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_path"] = str(path)
        data["_source"] = "raw"
        evaluations.append(data)
    for path in sorted(root.glob("round_*/filtered_evaluation_round_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_path"] = str(path)
        data["_source"] = "filtered"
        evaluations.append(data)
    return evaluations


def best_for_program(program: str) -> dict[str, Any]:
    evaluations = read_evaluations(program)
    valid = [item for item in evaluations if item.get("returncode") == 0 and item.get("branch_coverage") != ""]
    invalid = [item for item in evaluations if item.get("returncode") != 0 and item.get("branch_coverage") != ""]

    best_valid = max(valid, key=lambda item: float(item.get("branch_coverage", 0.0)), default=None)
    best_invalid = max(invalid, key=lambda item: float(item.get("branch_coverage", 0.0)), default=None)

    if best_valid:
        return {
            "program": program,
            "our_branch": best_valid.get("branch_coverage", ""),
            "our_line": best_valid.get("line_coverage", ""),
            "our_line_branch": best_valid.get("line_branch_coverage", ""),
            "our_best_round": best_valid.get("round", ""),
            "our_result_source": best_valid.get("_source", ""),
            "our_num_failed_tests": best_valid.get("num_failed_tests", ""),
            "our_num_tests": best_valid.get("num_filtered_tests", best_valid.get("num_test_files", "")),
            "our_status": "valid",
            "our_invalid_best_branch": best_invalid.get("branch_coverage", "") if best_invalid else "",
            "our_attempts": len(evaluations),
        }
    return {
        "program": program,
        "our_branch": "",
        "our_line": "",
        "our_line_branch": "",
        "our_best_round": "",
        "our_result_source": "",
        "our_num_failed_tests": "",
        "our_num_tests": "",
        "our_status": "no_valid_tests" if evaluations else "not_attempted",
        "our_invalid_best_branch": best_invalid.get("branch_coverage", "") if best_invalid else "",
        "our_attempts": len(evaluations),
    }


def to_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def best_method(row: dict[str, Any]) -> tuple[str, str]:
    candidates = [
        ("pynguin", to_float(row.get("pynguin_branch"))),
        ("coverup", to_float(row.get("coverup_branch"))),
        ("codamosa", to_float(row.get("codamosa_branch"))),
        ("our_method", to_float(row.get("our_branch"))),
    ]
    present = [(name, value) for name, value in candidates if value is not None]
    if not present:
        return "", ""
    name, value = max(present, key=lambda item: item[1])
    return name, f"{value:.2f}"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = build_parser().parse_args()
    baseline_rows = list(csv.DictReader(args.summary.open(encoding="utf-8-sig")))
    best_rows = [best_for_program(row["program"]) for row in baseline_rows]
    best_by_program = {row["program"]: row for row in best_rows}

    best_fields = [
        "program",
        "our_branch",
        "our_line",
        "our_line_branch",
        "our_best_round",
        "our_result_source",
        "our_num_failed_tests",
        "our_num_tests",
        "our_status",
        "our_invalid_best_branch",
        "our_attempts",
    ]
    write_csv(args.our_best_output, best_rows, best_fields)

    merged_rows: list[dict[str, Any]] = []
    for row in baseline_rows:
        merged = dict(row)
        best = best_by_program.get(row["program"], {})
        for key in best_fields:
            if key != "program":
                merged[key] = best.get(key, "")

        pynguin_branch = to_float(merged.get("pynguin_branch"))
        our_branch = to_float(merged.get("our_branch"))
        merged["our_improvement"] = f"{our_branch - pynguin_branch:.2f}" if our_branch is not None and pynguin_branch is not None else ""
        method, branch = best_method(merged)
        merged["best_method"] = method
        merged["best_method_branch"] = branch
        merged_rows.append(merged)

    base_fields = list(baseline_rows[0].keys()) if baseline_rows else []
    extra_fields = [
        "our_line_branch",
        "our_best_round",
        "our_result_source",
        "our_num_failed_tests",
        "our_num_tests",
        "our_status",
        "our_invalid_best_branch",
        "our_attempts",
        "best_method_branch",
    ]
    fieldnames = list(dict.fromkeys(base_fields + extra_fields))
    write_csv(args.output, merged_rows, fieldnames)

    valid_count = sum(1 for row in best_rows if row["our_status"] == "valid")
    print(f"Wrote {args.our_best_output}")
    print(f"Wrote {args.output}")
    print(f"Valid proposed-method results: {valid_count}/{len(best_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
