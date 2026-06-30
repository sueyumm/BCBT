"""Filter generated tests by keeping only individually passing test functions.

This is a cleanup step for the proposed method. Some LLM-generated test files
cover the target branches but contain one or more failing assertions. This
script extracts each test function, runs it independently, keeps the passing
ones, and then evaluates the filtered suite with branch coverage.

Inputs:
    scientific_calculation/<program>/<method_dir>/round_<N>/generated_tests_round_<N>.py

Outputs:
    scientific_calculation/<program>/<method_dir>/round_<N>/filtered_tests_round_<N>.py
    scientific_calculation/<program>/<method_dir>/round_<N>/filtered_evaluation_round_<N>.json
    scientific_calculation/<program>/<method_dir>/round_<N>/filtered_pytest_round_<N>.log
"""

from __future__ import annotations

import argparse
import ast
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

DEFAULT_TIMEOUT = 120
DEFAULT_METHOD_DIR = "our_method"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Filter generated tests to passing test functions")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--program", help="Only filter one program")
    group.add_argument("--all", action="store_true", help="Filter all programs with generated tests")
    group.add_argument("--new-only", action="store_true", help="Filter only newly added programs")
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
        help="Evaluate filtered tests together with the Pynguin baseline",
    )
    return parser


def program_root(program: str) -> Path:
    return SCI_ROOT / program


def round_dir(program: str, round_no: int, method_dir: str) -> Path:
    return program_root(program) / method_dir / f"round_{round_no}"


def generated_test_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"generated_tests_round_{round_no}.py"


def filtered_test_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"filtered_tests_round_{round_no}.py"


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


def split_test_file(path: Path) -> tuple[str, list[tuple[str, str]]]:
    code = repair_missing_imports(path.read_text(encoding="utf-8", errors="replace"))
    tree = ast.parse(code)
    lines = code.splitlines()
    imports_and_helpers: list[str] = []
    tests: list[tuple[str, str]] = []

    test_ranges: list[tuple[int, int]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            end_lineno = getattr(node, "end_lineno", node.lineno)
            test_ranges.append((node.lineno, end_lineno))
            tests.append((node.name, "\n".join(lines[node.lineno - 1 : end_lineno])))

    test_line_numbers = {
        line_no
        for start, end in test_ranges
        for line_no in range(start, end + 1)
    }
    for index, line in enumerate(lines, start=1):
        if index not in test_line_numbers:
            imports_and_helpers.append(line)
    prefix = "\n".join(imports_and_helpers).strip()
    if prefix:
        prefix += "\n\n"
    return prefix, tests


def write_single_test(
    program: str,
    round_no: int,
    method_dir: str,
    prefix: str,
    test_name: str,
    test_code: str,
) -> Path:
    out_dir = round_dir(program, round_no, method_dir) / "filter_tmp"
    out_dir.mkdir(parents=True, exist_ok=True)
    test_file = out_dir / "test_single.py"
    safe_unlink(test_file)
    test_file.write_text(prefix + test_code + "\n", encoding="utf-8")
    conftest = out_dir / "conftest.py"
    conftest.write_text(
        "import sys\n"
        f"sys.path.insert(0, {str(program_root(program))!r})\n",
        encoding="utf-8",
    )
    return test_file


def run_pytest_file(program: str, path: Path, timeout: int) -> tuple[int, str]:
    root = program_root(program)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        str(path),
    ]
    run = subprocess.run(
        command,
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return run.returncode, (run.stdout or "") + "\n" + (run.stderr or "")


def evaluate_filtered(
    program: str,
    round_no: int,
    method_dir: str,
    test_file: Path,
    timeout: int,
    *,
    include_pynguin_baseline: bool,
) -> dict[str, Any]:
    root = program_root(program)
    out_dir = round_dir(program, round_no, method_dir)
    eval_dir = out_dir / "filtered_eval_tests"
    eval_dir.mkdir(parents=True, exist_ok=True)
    for stale in eval_dir.glob("test_*.py"):
        safe_unlink(stale)
    safe_unlink(eval_dir / "conftest.py")

    copied_tests: list[Path] = []
    baseline = pynguin_test_path(program) if include_pynguin_baseline else None
    if baseline is not None:
        baseline_target = eval_dir / "test_00_pynguin_baseline.py"
        shutil.copy2(baseline, baseline_target)
        copied_tests.append(baseline_target)

    target_test = eval_dir / f"test_10_filtered_round_{round_no}.py"
    shutil.copy2(test_file, target_test)
    copied_tests.append(target_test)
    (eval_dir / "conftest.py").write_text(
        "import sys\n"
        f"sys.path.insert(0, {str(root)!r})\n",
        encoding="utf-8",
    )

    coverage_file = out_dir / f".coverage_filtered_round_{round_no}_{os.getpid()}_{int(time.time() * 1000)}"
    coverage_json = out_dir / f"filtered_coverage_round_{round_no}.json"
    pytest_log = out_dir / f"filtered_pytest_round_{round_no}.log"
    evaluation_json = out_dir / f"filtered_evaluation_round_{round_no}.json"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["COVERAGE_FILE"] = str(coverage_file)
    command = [
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
        str(eval_dir),
    ]
    run = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=timeout)
    pytest_log.write_text((run.stdout or "") + "\n" + (run.stderr or ""), encoding="utf-8", errors="replace")

    json_run = subprocess.run(
        [sys.executable, "-m", "coverage", "json", "-o", str(coverage_json)],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    summary = parse_coverage_json(coverage_json)
    metadata: dict[str, Any] = {
        "program": program,
        "round": round_no,
        "method_dir": method_dir,
        "returncode": run.returncode,
        "coverage_json_returncode": json_run.returncode,
        "filtered_tests": str(test_file),
        "test_files": [str(path) for path in copied_tests],
        "include_pynguin_baseline": include_pynguin_baseline,
        "num_filtered_tests": count_test_functions(test_file),
        "num_failed_tests": count_failed_tests(pytest_log.read_text(encoding="utf-8", errors="replace")),
        "pytest_log": str(pytest_log),
        "coverage_json": str(coverage_json),
        **summary,
    }
    evaluation_json.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return metadata


def parse_coverage_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return empty_coverage()
    data = json.loads(path.read_text(encoding="utf-8"))
    for filename, file_data in data.get("files", {}).items():
        if Path(filename).name == "example.py":
            summary = file_data.get("summary", {})
            covered_lines = int(summary.get("covered_lines", 0))
            num_statements = int(summary.get("num_statements", 0))
            covered_branches = int(summary.get("covered_branches", 0))
            num_branches = int(summary.get("num_branches", 0))
            return {
                "line_coverage": round(100.0 * covered_lines / num_statements, 2) if num_statements else 100.0,
                "branch_coverage": round(100.0 * covered_branches / num_branches, 2) if num_branches else 100.0,
                "line_branch_coverage": round(float(summary.get("percent_covered", 0.0)), 2),
                "covered_branches": covered_branches,
                "num_branches": num_branches,
            }
    return empty_coverage()


def empty_coverage() -> dict[str, Any]:
    return {
        "line_coverage": "",
        "branch_coverage": "",
        "line_branch_coverage": "",
        "covered_branches": "",
        "num_branches": "",
    }


def count_failed_tests(log_text: str) -> int:
    match = re.search(r"(\d+)\s+failed", log_text)
    return int(match.group(1)) if match else 0


def count_test_functions(path: Path) -> int:
    if not path.is_file():
        return 0
    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    return sum(1 for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))


def filter_one(
    program: str,
    round_no: int,
    method_dir: str,
    timeout: int,
    *,
    include_pynguin_baseline: bool,
) -> dict[str, Any]:
    source = generated_test_path(program, round_no, method_dir)
    out_dir = round_dir(program, round_no, method_dir)
    filter_log = out_dir / f"filter_round_{round_no}.json"
    if not source.is_file():
        return {"program": program, "round": round_no, "status": "missing_generated_tests"}

    prefix, tests = split_test_file(source)
    passing: list[tuple[str, str]] = []
    results: list[dict[str, Any]] = []

    for test_name, test_code in tests:
        test_file = write_single_test(program, round_no, method_dir, prefix, test_name, test_code)
        try:
            returncode, output = run_pytest_file(program, test_file, timeout)
        except subprocess.TimeoutExpired:
            returncode, output = 124, "timeout"
        results.append({"test": test_name, "returncode": returncode, "output_head": output[:1200]})
        if returncode == 0:
            passing.append((test_name, test_code))

    filtered = filtered_test_path(program, round_no, method_dir)
    if passing:
        filtered.write_text(prefix + "\n\n".join(test_code for _, test_code in passing) + "\n", encoding="utf-8")
        evaluation = evaluate_filtered(
            program,
            round_no,
            method_dir,
            filtered,
            timeout,
            include_pynguin_baseline=include_pynguin_baseline,
        )
    else:
        safe_unlink(filtered)
        evaluation = {"program": program, "round": round_no, "returncode": 1, "num_filtered_tests": 0}

    metadata = {
        "program": program,
        "round": round_no,
        "method_dir": method_dir,
        "source": str(source),
        "filtered_tests": str(filtered) if passing else "",
        "total_tests": len(tests),
        "passing_tests": len(passing),
        "test_results": results,
        "evaluation": evaluation,
    }
    filter_log.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return metadata


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

    with_passing = 0
    for program in programs:
        try:
            result = filter_one(
                program,
                args.round,
                args.method_dir,
                args.timeout,
                include_pynguin_baseline=args.include_pynguin_baseline,
            )
        except Exception as exc:
            print(f"[error] {program}: {exc}")
            continue
        total = result.get("total_tests", 0)
        passing = result.get("passing_tests", 0)
        evaluation = result.get("evaluation", {})
        if passing:
            with_passing += 1
            print(
                f"[filtered] {program}: kept {passing}/{total}, "
                f"branch={evaluation.get('branch_coverage', '')}%"
            )
        else:
            print(f"[none] {program}: kept 0/{total}")

    print(f"Programs with at least one passing filtered test: {with_passing}/{len(programs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
