"""Classify CodaMosa result quality under scientific_calculation.

Categories:
    - failed: run failed or no generated tests
    - empty_main: main test file exists but is essentially empty
    - nontrivial: main test file contains substantial content
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from paths import ROOT, SCI_ROOT

DEFAULT_RESULT_DIR = Path("codamosa") / "result_4o"
DEFAULT_OUT = ROOT / "codamosa_quality_summary.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Classify CodaMosa result quality")
    parser.add_argument("--root", type=Path, default=SCI_ROOT)
    parser.add_argument("--result-dir", type=Path, default=DEFAULT_RESULT_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def count_nontrivial_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and stripped != "pass":
            count += 1
    return count


def read_last_statistics_row(statistics_csv: Path) -> dict[str, str]:
    if not statistics_csv.is_file():
        return {}
    with statistics_csv.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        last_row: dict[str, str] | None = None
        for row in reader:
            last_row = row
    return last_row or {}


def classify_row(row: dict[str, object]) -> str:
    main_nontrivial_lines = int(row["main_nontrivial_lines"])
    failing_nontrivial_lines = int(row["failing_nontrivial_lines"])
    generated_tests = int(row["generated_tests"])
    return_code = int(row["return_code"])

    if return_code != 0 and main_nontrivial_lines == 0 and failing_nontrivial_lines == 0:
        return "failed"
    if generated_tests == 0 and main_nontrivial_lines == 0 and failing_nontrivial_lines == 0:
        return "failed"
    if main_nontrivial_lines <= 2:
        return "empty_main"
    return "nontrivial"


def collect_rows(root: Path, result_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for program_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        out_dir = program_dir / result_dir
        if not out_dir.is_dir():
            continue

        meta_path = out_dir / "codamosa_run.json"
        return_code = -1
        generated_tests = 0
        if meta_path.is_file():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8", errors="replace"))
                return_code = int(meta.get("return_code", -1))
                generated_tests = len(meta.get("generated_tests", []))
            except Exception:
                pass

        main_test = out_dir / "test_example.py"
        failing_test = out_dir / "test_example_failing.py"
        gpt4o_generations = out_dir / "gpt4o_generations.py"
        codex_generations = out_dir / "codex_generations.py"
        generation_file = gpt4o_generations if gpt4o_generations.is_file() else codex_generations
        llm_generation_count = 0
        if generation_file.is_file():
            text = generation_file.read_text(encoding="utf-8", errors="replace")
            llm_generation_count = text.count("# Generated at")

        stat = read_last_statistics_row(out_dir / "statistics.csv")
        row: dict[str, object] = {
            "program": program_dir.name,
            "return_code": return_code,
            "generated_tests": generated_tests,
            "main_nontrivial_lines": count_nontrivial_lines(main_test),
            "failing_nontrivial_lines": count_nontrivial_lines(failing_test),
            "llm_generation_count": llm_generation_count,
            "coverage": stat.get("Coverage", ""),
            "branch_coverage": stat.get("BranchCoverage", ""),
            "line_coverage": stat.get("LineCoverage", ""),
            "llm_calls": stat.get("LLMCalls", ""),
            "llm_stage_saved_tests": stat.get("LLMStageSavedTests", ""),
        }
        row["category"] = classify_row(row)
        rows.append(row)
    return rows


def print_summary(rows: list[dict[str, object]]) -> None:
    groups = ("nontrivial", "empty_main", "failed")
    print(f"Scanned {len(rows)} CodaMosa result directories.\n")
    for group in groups:
        subset = [row for row in rows if row["category"] == group]
        print(f"{group} ({len(subset)})")
        print(f"{'Program':<30} {'Cov':>8} {'Branch':>8} {'LLM':>6} {'Main':>6} {'Gen':>6}")
        print("-" * 74)
        for row in subset:
            print(
                f"{str(row['program']):<30} "
                f"{str(row['coverage']):>8} "
                f"{str(row['branch_coverage']):>8} "
                f"{str(row['llm_calls']):>6} "
                f"{str(row['main_nontrivial_lines']):>6} "
                f"{str(row['llm_generation_count']):>6}"
            )
        print()


def write_csv(rows: list[dict[str, object]], out_path: Path) -> None:
    fieldnames = [
        "program",
        "category",
        "return_code",
        "generated_tests",
        "main_nontrivial_lines",
        "failing_nontrivial_lines",
        "llm_generation_count",
        "coverage",
        "branch_coverage",
        "line_coverage",
        "llm_calls",
        "llm_stage_saved_tests",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved quality summary to {out_path}")


def main() -> int:
    args = build_parser().parse_args()
    rows = collect_rows(args.root.resolve(), args.result_dir)
    if not rows:
        print("No CodaMosa result directories found. Check --root and --result-dir.")
        return 1
    print_summary(rows)
    try:
        write_csv(rows, args.out.resolve())
    except PermissionError as exc:
        print(f"Could not write CSV: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
