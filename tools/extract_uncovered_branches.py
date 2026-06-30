"""Extract uncovered branch targets from Pynguin baseline coverage data.

The script reads each program's Pynguin ``.coverage`` file, asks coverage.py for
JSON data, and writes a structured ``uncovered_branches.json`` file that can be
used by the LLM prompt-generation stage.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any

from paths import ROOT, SCI_ROOT, load_new_program_names, load_program_names

DEFAULT_OUT = ROOT / "uncovered_branches.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract uncovered branches from Pynguin coverage data")
    parser.add_argument("--program", help="Only process one program")
    parser.add_argument(
        "--new-only",
        action="store_true",
        help="Only process programs added after the original 36-program dataset",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def pynguin_result_candidates(program_dir: Path) -> list[Path]:
    return [
        program_dir / "pynguin" / "result_4o",
        program_dir / "pynguin" / "result",
        program_dir / "result_4o",
    ]


def find_pynguin_result_dir(program_dir: Path) -> Path | None:
    for candidate in pynguin_result_candidates(program_dir):
        if find_coverage_data_file(candidate) is not None:
            return candidate
    return None


def find_coverage_data_file(result_dir: Path) -> Path | None:
    fixed = result_dir / ".coverage"
    if fixed.is_file():
        return fixed
    candidates = [path for path in result_dir.glob(".coverage*") if path.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


class SourceIndex:
    def __init__(self, source: str) -> None:
        self.source = source
        self.lines = source.splitlines()
        self.tree = ast.parse(source)

    def enclosing_scope(self, line_no: int) -> dict[str, str]:
        best_function: ast.FunctionDef | ast.AsyncFunctionDef | None = None
        best_class: ast.ClassDef | None = None
        for node in ast.walk(self.tree):
            if not hasattr(node, "lineno"):
                continue
            end_lineno = getattr(node, "end_lineno", getattr(node, "lineno", None))
            if end_lineno is None or not (node.lineno <= line_no <= end_lineno):
                continue
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if best_function is None or node.lineno >= best_function.lineno:
                    best_function = node
            elif isinstance(node, ast.ClassDef):
                if best_class is None or node.lineno >= best_class.lineno:
                    best_class = node
        return {
            "function": best_function.name if best_function else "",
            "class": best_class.name if best_class else "",
        }

    def branch_condition(self, line_no: int) -> str:
        for node in ast.walk(self.tree):
            if getattr(node, "lineno", None) != line_no:
                continue
            if isinstance(node, ast.If):
                return ast.unparse(node.test)
            if isinstance(node, ast.While):
                return ast.unparse(node.test)
            if isinstance(node, ast.For):
                return f"{ast.unparse(node.target)} in {ast.unparse(node.iter)}"
            if isinstance(node, ast.AsyncFor):
                return f"{ast.unparse(node.target)} in {ast.unparse(node.iter)}"
            if isinstance(node, ast.Try):
                return "try/except/finally"
            if isinstance(node, ast.BoolOp):
                return ast.unparse(node)
        if 1 <= line_no <= len(self.lines):
            return self.lines[line_no - 1].strip()
        return ""

    def snippet(self, line_no: int, radius: int = 3) -> str:
        start = max(1, line_no - radius)
        end = min(len(self.lines), line_no + radius)
        return "\n".join(f"{idx}: {self.lines[idx - 1]}" for idx in range(start, end + 1))


def read_executed_arcs(data_file: Path) -> set[tuple[int, int]]:
    if not data_file.is_file():
        return set()
    con = sqlite3.connect(data_file)
    try:
        rows = con.execute("select fromno, tono from arc").fetchall()
    finally:
        con.close()
    return {(int(start), int(end)) for start, end in rows}


def read_coverage_json(source_dir: Path, data_file: Path) -> dict[str, Any]:
    """Read coverage.py JSON data for example.py from a stored data file."""
    import coverage

    out_file = Path("C:/tmp") / f"bcbt_coverage_json_{os.getpid()}_{time.time_ns()}.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    old_cwd = Path.cwd()
    try:
        os.chdir(source_dir)
        cov = coverage.Coverage(data_file=str(data_file), branch=True)
        cov.load()
        cov.json_report(outfile=str(out_file), include=["example.py"])
        return json.loads(out_file.read_text(encoding="utf-8"))
    finally:
        os.chdir(old_cwd)
        try:
            out_file.unlink(missing_ok=True)
        except PermissionError:
            # Windows can briefly keep the JSON report locked; leaving a temp
            # report is safer than failing branch extraction.
            pass


def missing_branch_arcs(source_dir: Path, data_file: Path) -> list[tuple[int, int]]:
    data = read_coverage_json(source_dir, data_file)
    files = data.get("files", {})
    if not files:
        return []
    file_data = next(iter(files.values()))
    return [
        (int(start), int(target))
        for start, target in file_data.get("missing_branches", [])
    ]


def _first_statement_line(statements: list[ast.stmt]) -> int | None:
    for statement in statements:
        line = getattr(statement, "lineno", None)
        if line is not None:
            return int(line)
    return None


def _statement_lines(tree: ast.AST) -> list[int]:
    lines = {
        int(node.lineno)
        for node in ast.walk(tree)
        if isinstance(node, ast.stmt) and getattr(node, "lineno", None) is not None
    }
    return sorted(lines)


def _next_statement_line(all_statement_lines: list[int], after_line: int) -> int | None:
    for line in all_statement_lines:
        if line > after_line:
            return line
    return None


def possible_branch_arcs(tree: ast.AST) -> list[tuple[int, int, str]]:
    all_statement_lines = _statement_lines(tree)
    arcs: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        start = getattr(node, "lineno", None)
        if start is None:
            continue
        end = int(getattr(node, "end_lineno", start))
        if isinstance(node, ast.If):
            body_line = _first_statement_line(node.body)
            else_line = _first_statement_line(node.orelse) or _next_statement_line(all_statement_lines, end)
            if body_line is not None:
                arcs.append((int(start), body_line, "if_true"))
            if else_line is not None:
                arcs.append((int(start), else_line, "if_false"))
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            body_line = _first_statement_line(node.body)
            exit_line = _next_statement_line(all_statement_lines, end)
            if body_line is not None:
                arcs.append((int(start), body_line, "loop_enter"))
            if exit_line is not None:
                arcs.append((int(start), exit_line, "loop_exit"))
    return arcs


def extract_program(program: str) -> dict[str, Any]:
    program_dir = SCI_ROOT / program
    source_path = program_dir / "example.py"
    result_dir = find_pynguin_result_dir(program_dir)
    base = {
        "program": program,
        "source": str(source_path),
        "pynguin_result_dir": str(result_dir) if result_dir else "",
        "branches": [],
        "status": "ok",
    }
    if not source_path.is_file():
        base["status"] = "missing_source"
        return base
    if result_dir is None:
        base["status"] = "missing_coverage"
        return base

    source_text = source_path.read_text(encoding="utf-8", errors="replace")
    source_index = SourceIndex(source_text)
    coverage_file = find_coverage_data_file(result_dir)
    if coverage_file is None:
        base["status"] = "missing_coverage"
        return base
    base["coverage_data_file"] = str(coverage_file)
    possible_arc_directions = {
        (start, target): direction
        for start, target, direction in possible_branch_arcs(source_index.tree)
    }
    missing_arcs = [
        (start, target, possible_arc_directions.get((start, target), "missing_branch"))
        for start, target in missing_branch_arcs(program_dir, coverage_file)
    ]

    branches = []
    for start_line, target_line, direction in missing_arcs:
        scope = source_index.enclosing_scope(start_line)
        branches.append(
            {
                "line": start_line,
                "target": target_line,
                "direction": direction,
                "condition": source_index.branch_condition(start_line),
                "function": scope["function"],
                "class": scope["class"],
                "source_snippet": source_index.snippet(start_line),
            }
        )
    base["branches"] = branches
    return base


def main() -> int:
    args = build_parser().parse_args()
    if args.program:
        programs = [args.program]
    elif args.new_only:
        programs = load_new_program_names()
    else:
        programs = load_program_names()
    results = [extract_program(program) for program in programs]

    output = {
        "metric": "branch coverage",
        "source_suite": "pynguin",
        "program_count": len(results),
        "total_uncovered_branches": sum(len(item["branches"]) for item in results),
        "programs": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Processed {len(results)} programs.")
    print(f"Total uncovered branches: {output['total_uncovered_branches']}")
    print(f"Saved uncovered branch data to {args.out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
