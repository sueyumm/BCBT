"""Merge Pynguin, CoverUp, and CodaMosa baseline results into one table.

The merged table uses branch coverage as the primary metric. Coverage values are
written as percentages to keep Pynguin, CoverUp, and CodaMosa comparable.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from paths import ROOT, SCI_ROOT, load_program_names

PYNGUIN_SUMMARY = SCI_ROOT / "coverage_summary_pynguin.csv"
COVERUP_SUMMARY = ROOT / "coverup_summary.csv"
CODAMOSA_COVERAGE_SUMMARY = ROOT / "codamosa_coverage_summary.csv"
CODAMOSA_QUALITY_SUMMARY = ROOT / "codamosa_quality_summary.csv"
DEFAULT_OUT = ROOT / "summary.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge baseline branch coverage results")
    parser.add_argument("--pynguin", type=Path, default=PYNGUIN_SUMMARY)
    parser.add_argument("--coverup", type=Path, default=COVERUP_SUMMARY)
    parser.add_argument("--codamosa", type=Path, default=CODAMOSA_COVERAGE_SUMMARY)
    parser.add_argument("--codamosa-quality", type=Path, default=CODAMOSA_QUALITY_SUMMARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def _read_csv_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        return {row[key]: row for row in reader if row.get(key)}


def _to_float(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _fraction_to_pct(value: object) -> str:
    parsed = _to_float(value)
    if parsed is None:
        return ""
    return f"{parsed * 100:.2f}"


def _pct(value: object) -> str:
    parsed = _to_float(value)
    if parsed is None:
        return ""
    return f"{parsed:.2f}"


def _pynguin_coverage_from_report(program: str) -> tuple[str, str]:
    report_path = SCI_ROOT / program / "pynguin" / "result" / "coverage_report_example.txt"
    if not report_path.is_file():
        return "", ""
    text = report_path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if not line.strip().startswith("example.py"):
            continue
        parts = line.split()
        if len(parts) < 7:
            continue
        try:
            stmts = int(parts[1])
            miss = int(parts[2])
            branches = int(parts[3])
            partial = int(parts[4])
        except ValueError:
            continue
        line_coverage = 100.0 * (stmts - miss) / stmts if stmts else 100.0
        # coverage.py's text report does not expose covered branch count directly;
        # for files with no branch opportunities, branch coverage is vacuously 100%.
        if branches == 0:
            branch_coverage = 100.0
        else:
            match = re.search(r"(\d+(?:\.\d+)?)%", line)
            branch_coverage = float(match.group(1)) if match else 100.0
        return f"{branch_coverage:.2f}", f"{line_coverage:.2f}"
    return "", ""


def _best_baseline(values: dict[str, str]) -> tuple[str, str]:
    best_name = ""
    best_value: float | None = None
    for name, text in values.items():
        value = _to_float(text)
        if value is None:
            continue
        if best_value is None or value > best_value:
            best_name = name
            best_value = value
    return best_name, "" if best_value is None else f"{best_value:.2f}"


def collect_rows(
    *,
    pynguin_path: Path,
    coverup_path: Path,
    codamosa_path: Path,
    codamosa_quality_path: Path,
) -> list[dict[str, str]]:
    pynguin = _read_csv_by_key(pynguin_path, "program")
    coverup = _read_csv_by_key(coverup_path, "Program")
    codamosa = _read_csv_by_key(codamosa_path, "program")
    codamosa_quality = _read_csv_by_key(codamosa_quality_path, "program")

    all_programs = sorted(
        set(load_program_names())
        | set(pynguin)
        | set(coverup)
        | set(codamosa)
        | set(codamosa_quality)
    )

    rows: list[dict[str, str]] = []
    for program in all_programs:
        py_row = pynguin.get(program, {})
        cu_row = coverup.get(program, {})
        co_row = codamosa.get(program, {})
        cq_row = codamosa_quality.get(program, {})

        py_branch, py_line = _pynguin_coverage_from_report(program)
        if not py_branch:
            py_branch = _pct(py_row.get("example_branch_cover_pct"))
        coverup_branch = _pct(cu_row.get("Final"))
        codamosa_branch = _fraction_to_pct(co_row.get("branch_coverage"))
        codamosa_line = _fraction_to_pct(co_row.get("line_coverage"))

        best_baseline, best_baseline_branch = _best_baseline(
            {
                "pynguin": py_branch,
                "coverup": coverup_branch,
                "codamosa": codamosa_branch,
            }
        )

        rows.append(
            {
                "program": program,
                "pynguin_branch": py_branch,
                "pynguin_line": py_line,
                "coverup_branch": coverup_branch,
                "coverup_line": "",
                "codamosa_branch": codamosa_branch,
                "codamosa_line": codamosa_line,
                "codamosa_category": cq_row.get("category", ""),
                "codamosa_llm_calls": co_row.get("llm_calls", cq_row.get("llm_calls", "")),
                "codamosa_saved_tests": co_row.get(
                    "llm_stage_saved_tests", cq_row.get("llm_stage_saved_tests", "")
                ),
                "best_baseline": best_baseline,
                "best_baseline_branch": best_baseline_branch,
                "our_branch": "",
                "our_line": "",
                "our_improvement": "",
                "best_method": "",
                "generation_time": "",
                "num_tests": "",
                "num_failed_tests": "",
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]], out_path: Path) -> None:
    fieldnames = [
        "program",
        "pynguin_branch",
        "pynguin_line",
        "coverup_branch",
        "coverup_line",
        "codamosa_branch",
        "codamosa_line",
        "codamosa_category",
        "codamosa_llm_calls",
        "codamosa_saved_tests",
        "best_baseline",
        "best_baseline_branch",
        "our_branch",
        "our_line",
        "our_improvement",
        "best_method",
        "generation_time",
        "num_tests",
        "num_failed_tests",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, str]]) -> None:
    print(f"Merged {len(rows)} programs into baseline summary.\n")
    print(
        f"{'Program':<30} {'Pynguin':>8} {'CoverUp':>8} "
        f"{'CodaMosa':>8} {'Best':>10} {'BestBr':>8}"
    )
    print("-" * 84)
    for row in rows:
        print(
            f"{row['program']:<30} "
            f"{row['pynguin_branch']:>8} "
            f"{row['coverup_branch']:>8} "
            f"{row['codamosa_branch']:>8} "
            f"{row['best_baseline']:>10} "
            f"{row['best_baseline_branch']:>8}"
        )


def main() -> int:
    args = build_parser().parse_args()
    rows = collect_rows(
        pynguin_path=args.pynguin.resolve(),
        coverup_path=args.coverup.resolve(),
        codamosa_path=args.codamosa.resolve(),
        codamosa_quality_path=args.codamosa_quality.resolve(),
    )
    print_summary(rows)
    write_csv(rows, args.out.resolve())
    print(f"\nSaved merged summary to {args.out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
