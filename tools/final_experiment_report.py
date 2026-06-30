"""Create final experiment summary tables for the branch-coverage study.

Input:
    summary_with_our_method.csv

Outputs:
    final_experiment_report.txt
    final_experiment_report.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

from paths import ROOT

DEFAULT_INPUT = ROOT / "summary_with_our_method.csv"
DEFAULT_TXT = ROOT / "final_experiment_report.txt"
DEFAULT_CSV = ROOT / "final_experiment_report.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build final experiment summary")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--txt-out", type=Path, default=DEFAULT_TXT)
    parser.add_argument("--csv-out", type=Path, default=DEFAULT_CSV)
    return parser


def to_float(value: Any) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def pct(numerator: int, denominator: int) -> float:
    return 100.0 * numerator / denominator if denominator else 0.0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def metric_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    total = len(rows)
    attempted = [row for row in rows if row.get("our_status") != "not_attempted"]
    valid = [row for row in rows if row.get("our_status") == "valid"]
    raw_valid = [row for row in valid if row.get("our_result_source") == "raw"]
    filtered_valid = [row for row in valid if row.get("our_result_source") == "filtered"]
    improved = [row for row in valid if (to_float(row.get("our_improvement")) or 0.0) > 0.0]
    best_method_counts = Counter(row.get("best_method", "") for row in rows if row.get("best_method"))

    pynguin_values = [value for row in rows if (value := to_float(row.get("pynguin_branch"))) is not None]
    coverup_values = [value for row in rows if (value := to_float(row.get("coverup_branch"))) is not None]
    codamosa_values = [value for row in rows if (value := to_float(row.get("codamosa_branch"))) is not None]
    our_values = [value for row in valid if (value := to_float(row.get("our_branch"))) is not None]
    valid_improvements = [value for row in valid if (value := to_float(row.get("our_improvement"))) is not None]

    report_rows = [
        {"metric": "total_programs", "value": str(total)},
        {"metric": "our_method_attempted_programs", "value": str(len(attempted))},
        {"metric": "our_method_not_attempted_programs", "value": str(total - len(attempted))},
        {"metric": "our_method_valid_programs", "value": str(len(valid))},
        {"metric": "our_method_valid_rate_all_programs_pct", "value": f"{pct(len(valid), total):.2f}"},
        {"metric": "our_method_valid_rate_attempted_pct", "value": f"{pct(len(valid), len(attempted)):.2f}"},
        {"metric": "our_method_raw_valid_programs", "value": str(len(raw_valid))},
        {"metric": "our_method_filtered_valid_programs", "value": str(len(filtered_valid))},
        {"metric": "our_method_improved_over_pynguin_programs", "value": str(len(improved))},
        {"metric": "our_method_improved_over_pynguin_rate_valid_pct", "value": f"{pct(len(improved), len(valid)):.2f}"},
        {"metric": "avg_pynguin_branch_pct", "value": f"{mean(pynguin_values):.2f}"},
        {"metric": "avg_coverup_branch_pct", "value": f"{mean(coverup_values):.2f}"},
        {"metric": "avg_codamosa_branch_pct", "value": f"{mean(codamosa_values):.2f}"},
        {"metric": "avg_our_method_branch_valid_pct", "value": f"{mean(our_values):.2f}"},
        {"metric": "avg_our_method_improvement_over_pynguin_valid_pct_points", "value": f"{mean(valid_improvements):.2f}"},
    ]
    for method in ("pynguin", "coverup", "codamosa", "our_method"):
        report_rows.append(
            {
                "metric": f"best_method_count_{method}",
                "value": str(best_method_counts.get(method, 0)),
            }
        )
    return report_rows


def not_attempted_reasons(rows: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    not_attempted = [row for row in rows if row.get("our_status") == "not_attempted"]
    for row in not_attempted:
        branch = to_float(row.get("pynguin_branch"))
        line = to_float(row.get("pynguin_line"))
        if branch == 100.0 and line is not None and line < 100.0:
            reason = "no branch targets; line coverage below 100"
        elif branch == 100.0:
            reason = "pynguin branch coverage already 100"
        else:
            reason = "no extracted target branch"
        lines.append(f"- {row['program']}: {reason} (pynguin_branch={row.get('pynguin_branch', '')}, pynguin_line={row.get('pynguin_line', '')})")
    return lines


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(rows)


def write_txt(path: Path, metrics: list[dict[str, str]], rows: list[dict[str, str]]) -> None:
    lines = ["Final Experiment Report", "=" * 24, ""]
    lines.extend(f"{row['metric']}: {row['value']}" for row in metrics)
    lines.extend(["", "Not Attempted Programs", "-" * 24])
    lines.extend(not_attempted_reasons(rows))
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    rows = read_rows(args.input.resolve())
    metrics = metric_rows(rows)
    write_csv(args.csv_out.resolve(), metrics)
    write_txt(args.txt_out.resolve(), metrics, rows)
    print(f"Wrote {args.csv_out.resolve()}")
    print(f"Wrote {args.txt_out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
