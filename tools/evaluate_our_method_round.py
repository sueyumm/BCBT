"""Evaluate generated tests from the proposed method with branch coverage.

For each selected program this script runs generated tests from:
    - <method_dir>/round_<N>/generated_tests_round_<N>.py

Optionally, pass --include-pynguin-baseline to combine Pynguin baseline tests
with the generated tests.

Then it runs pytest under coverage with branch tracking and writes:
    scientific_calculation/<program>/<method_dir>/round_<N>/coverage_round_<N>.json
    scientific_calculation/<program>/<method_dir>/round_<N>/pytest_round_<N>.log
    scientific_calculation/<program>/<method_dir>/round_<N>/evaluation_round_<N>.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from paths import SCI_ROOT, load_new_program_names

DEFAULT_TIMEOUT = 180
DEFAULT_METHOD_DIR = "our_method"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate proposed-method generated tests")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--program", help="Only evaluate one program")
    group.add_argument("--all", action="store_true", help="Evaluate all programs with generated tests")
    group.add_argument("--new-only", action="store_true", help="Evaluate only newly added programs")
    parser.add_argument("--round", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--method-dir",
        default=DEFAULT_METHOD_DIR,
        help="Per-program output directory for this method variant.",
    )
    parser.add_argument(
        "--include-pynguin-baseline",
        action="store_true",
        help="Also run Pynguin baseline tests together with generated tests",
    )
    return parser


def program_root(program: str) -> Path:
    return SCI_ROOT / program


def round_dir(program: str, round_no: int, method_dir: str) -> Path:
    return program_root(program) / method_dir / f"round_{round_no}"


def generated_test_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"generated_tests_round_{round_no}.py"


def pynguin_test_path(program: str) -> Path | None:
    candidates = [
        program_root(program) / "pynguin" / "result_4o" / "test_example.py",
        program_root(program) / "pynguin" / "result" / "test_example.py",
        program_root(program) / "result_4o" / "test_example.py",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def discover_programs(round_no: int, method_dir: str) -> list[str]:
    programs: list[str] = []
    for candidate in sorted(p for p in SCI_ROOT.iterdir() if p.is_dir()):
        if generated_test_path(candidate.name, round_no, method_dir).is_file():
            programs.append(candidate.name)
    return programs


def prepare_eval_tests(
    program: str,
    round_no: int,
    method_dir: str,
    include_pynguin_baseline: bool,
) -> tuple[Path, list[Path]]:
    root = program_root(program)
    out_dir = round_dir(program, round_no, method_dir)
    eval_tests = out_dir / "eval_tests"
    eval_tests.mkdir(parents=True, exist_ok=True)
    for stale in eval_tests.glob("test_*.py"):
        safe_unlink(stale)
    safe_unlink(eval_tests / "conftest.py")

    copied: list[Path] = []
    baseline = pynguin_test_path(program) if include_pynguin_baseline else None
    if baseline is not None:
        target = eval_tests / "test_00_pynguin_baseline.py"
        shutil.copy2(baseline, target)
        copied.append(target)

    generated = generated_test_path(program, round_no, method_dir)
    if generated.is_file():
        target = eval_tests / f"test_10_our_round_{round_no}.py"
        target.write_text(repair_missing_imports(generated.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
        copied.append(target)

    conftest = eval_tests / "conftest.py"
    conftest.write_text(
        "import sys\n"
        f"sys.path.insert(0, {str(root)!r})\n",
        encoding="utf-8",
    )
    return eval_tests, copied


def safe_unlink(path: Path) -> None:
    if not path.exists():
        return
    try:
        path.chmod(stat.S_IWRITE | stat.S_IREAD)
    except OSError:
        pass
    try:
        path.unlink()
    except PermissionError:
        path.write_text("", encoding="utf-8")


def repair_missing_imports(code: str) -> str:
    imports: list[str] = []
    if re.search(r"\bpytest\.", code) and not re.search(r"^\s*(import pytest|from pytest import)", code, re.MULTILINE):
        imports.append("import pytest")
    if re.search(r"\bnp\.", code) and not re.search(r"^\s*import numpy as np", code, re.MULTILINE):
        imports.append("import numpy as np")
    if re.search(r"\bsp\.", code) and not re.search(r"^\s*import sympy as sp", code, re.MULTILINE):
        imports.append("import sympy as sp")
    if not imports:
        return code
    return "\n".join(imports) + "\n" + code


def run_coverage(
    program: str,
    round_no: int,
    method_dir: str,
    timeout: int,
    *,
    include_pynguin_baseline: bool,
) -> dict[str, Any]:
    root = program_root(program)
    out_dir = round_dir(program, round_no, method_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    coverage_file = out_dir / f".coverage_round_{round_no}_{os.getpid()}_{int(time.time() * 1000)}"
    coverage_json = out_dir / f"coverage_round_{round_no}.json"
    pytest_log = out_dir / f"pytest_round_{round_no}.log"
    evaluation_json = out_dir / f"evaluation_round_{round_no}.json"

    eval_tests, copied = prepare_eval_tests(program, round_no, method_dir, include_pynguin_baseline)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["COVERAGE_FILE"] = str(coverage_file)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    run_cmd = [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--branch",
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        str(eval_tests),
    ]
    run = subprocess.run(
        run_cmd,
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    pytest_log.write_text((run.stdout or "") + "\n" + (run.stderr or ""), encoding="utf-8", errors="replace")

    json_cmd = [
        sys.executable,
        "-m",
        "coverage",
        "json",
        "-o",
        str(coverage_json),
    ]
    json_run = subprocess.run(
        json_cmd,
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    summary = parse_coverage_json(coverage_json)
    failed = count_failed_tests(pytest_log.read_text(encoding="utf-8", errors="replace"))
    metadata: dict[str, Any] = {
        "program": program,
        "round": round_no,
        "method_dir": method_dir,
        "returncode": run.returncode,
        "coverage_json_returncode": json_run.returncode,
        "test_files": [str(path) for path in copied],
        "num_test_files": len(copied),
        "include_pynguin_baseline": include_pynguin_baseline,
        "num_failed_tests": failed,
        "pytest_log": str(pytest_log),
        "coverage_json": str(coverage_json),
        **summary,
    }
    evaluation_json.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return metadata


def parse_coverage_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "line_coverage": "",
            "branch_coverage": "",
            "line_branch_coverage": "",
            "covered_branches": "",
            "num_branches": "",
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get("files", {})
    example_summary: dict[str, Any] | None = None
    for filename, file_data in files.items():
        if Path(filename).name == "example.py":
            example_summary = file_data.get("summary", {})
            break
    if example_summary is None:
        return {
            "line_coverage": "",
            "branch_coverage": "",
            "line_branch_coverage": "",
            "covered_branches": "",
            "num_branches": "",
        }

    covered_lines = int(example_summary.get("covered_lines", 0))
    num_statements = int(example_summary.get("num_statements", 0))
    covered_branches = int(example_summary.get("covered_branches", 0))
    num_branches = int(example_summary.get("num_branches", 0))
    line_coverage = 100.0 * covered_lines / num_statements if num_statements else 100.0
    branch_coverage = 100.0 * covered_branches / num_branches if num_branches else 100.0
    return {
        "line_coverage": round(line_coverage, 2),
        "branch_coverage": round(branch_coverage, 2),
        "line_branch_coverage": round(float(example_summary.get("percent_covered", 0.0)), 2),
        "covered_branches": covered_branches,
        "num_branches": num_branches,
    }


def count_failed_tests(log_text: str) -> int:
    match = re.search(r"(\d+)\s+failed", log_text)
    if match:
        return int(match.group(1))
    return 0


def main() -> int:
    args = build_parser().parse_args()
    if args.program:
        programs = [args.program]
    elif args.new_only:
        new_programs = set(load_new_program_names())
        programs = [program for program in discover_programs(args.round, args.method_dir) if program in new_programs]
    else:
        programs = discover_programs(args.round, args.method_dir)
    if not programs:
        raise SystemExit(f"No generated tests found for round {args.round}.")

    failures = 0
    for program in programs:
        try:
            result = run_coverage(
                program,
                args.round,
                args.method_dir,
                args.timeout,
                include_pynguin_baseline=args.include_pynguin_baseline,
            )
        except subprocess.TimeoutExpired:
            failures += 1
            print(f"[timeout] {program}")
            continue
        if result.get("returncode") == 0:
            print(
                f"[ok] {program}: branch={result.get('branch_coverage')}%, "
                f"line={result.get('line_coverage')}%"
            )
        else:
            failures += 1
            print(
                f"[failed] {program}: rc={result.get('returncode')}, "
                f"failed_tests={result.get('num_failed_tests')}"
            )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
