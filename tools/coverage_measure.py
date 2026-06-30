"""
在只读程序目录中加载 example，运行程序 result_4o 目录中的测试；
coverage 数据与报告只写入该程序 result_4o 目录。

用法:
  python tools/coverage_measure.py --suite pynguin --program euler_diffusion
  python tools/coverage_measure.py --suite pynguin --all
  python tools/coverage_measure.py --suite pynguin --program x --html
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from paths import (
    default_results_root,
    load_new_program_names,
    load_pde_program_names,
    load_program_names,
    example_path,
    program_results_dir,
    summary_csv_path,
)

# ===============================
# 直接运行配置（可选）
# ===============================
# 如果你想“在文件里指定要测哪个程序”，可以不传 --program 直接运行本脚本。
DEFAULT_SUITE = "pynguin"
DEFAULT_PROGRAM = "CG_general"
DEFAULT_TEST_FILE = "test_example.py"
DEFAULT_HTML = False
DEFAULT_MODE = "all"  # "program" | "pde" | "all"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="pytest + branch coverage，产出在各程序 result_4o 目录")
    p.add_argument("--suite", choices=("pynguin", "coverup", "coverup-failed", "codamosa", "chatgpt"), default="pynguin")
    p.add_argument("--program", help="程序名（canonical）")
    p.add_argument("--all", action="store_true", help="遍历 programs.json 全部")
    p.add_argument("--pde", action="store_true", help="仅 programs.json 中 pde_subset")
    p.add_argument("--new-only", action="store_true", help="Only measure newly added programs")
    p.add_argument("--test-file", default="test_example.py")
    p.add_argument(
        "--results-root",
        type=Path,
        default=None,
        help="兼容参数，默认忽略；测试与 .coverage 在各程序目录下 result_4o/",
    )
    p.add_argument(
        "--summary-name",
        default=None,
        help="批量汇总 CSV 文件名，默认 coverage_summary_<suite>.csv，写在 suite 根目录下",
    )
    p.add_argument("--html", action="store_true", help="HTML 报告写到结果目录 htmlcov/")
    p.add_argument(
        "--pytest-log",
        action="store_true",
        help="将 pytest 标准输出/错误写入结果目录 pytest_last.txt",
    )
    return p


def coveragerc_path() -> Path:
    return _TOOLS / "coveragerc"


def _clean_coverage_artifacts(out_dir: Path) -> None:
    for stale in ("htmlcov", ".coverage"):
        p = out_dir / stale
        if p.is_file():
            try:
                p.unlink(missing_ok=True)
            except PermissionError:
                # Windows can briefly keep coverage data files locked.  The
                # caller uses a unique COVERAGE_FILE, so a stale locked file is
                # safe to leave behind.
                pass
        elif p.is_dir():
            shutil.rmtree(p, ignore_errors=True)


def measure_one(
    suite: str,
    canonical: str,
    test_file: str,
    *,
    results_root: Path,
    html: bool,
    pytest_log: bool,
) -> tuple[int, str, str]:
    # example.py 只保留在程序根目录
    source_dir = example_path(suite, canonical).parent
    out_dir = program_results_dir(results_root, suite, canonical)
    test_path = out_dir / test_file
    if suite in {"coverup", "coverup-failed"}:
        tests_dir = out_dir / "tests"
        if tests_dir.is_dir():
            candidates = sorted(tests_dir.glob("test_*.py"))
            if not candidates:
                candidates = sorted(tests_dir.glob("*test*.py"))
            if candidates:
                test_path = tests_dir
    rc_path = coveragerc_path()
    data_file = out_dir / f".coverage_{os.getpid()}_{time.time_ns()}"

    if not (source_dir / "example.py").is_file():
        return 2, f"{canonical}\tMISSING example.py", ""
    if not (test_path.is_file() or test_path.is_dir()):
        return 2, f"{canonical}\tNO_TEST {out_dir / test_file}", ""

    out_dir.mkdir(parents=True, exist_ok=True)
    _clean_coverage_artifacts(out_dir)

    env = os.environ.copy()
    env["COVERAGE_FILE"] = str(data_file)
    # 确保 pytest 能 import example（某些生成的测试可能不带 conftest 注入）
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(source_dir) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")

    abs_test = str(test_path.resolve())
    run_cmd = [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--data-file",
        str(data_file),
        "--rcfile",
        str(rc_path),
        "--branch",
        "-m",
        "pytest",
        abs_test,
        "-q",
        "--tb=no",
    ]
    r1 = subprocess.run(run_cmd, cwd=source_dir, env=env, capture_output=True, text=True)
    if pytest_log or r1.returncode != 0:
        plog = out_dir / "pytest_last.txt"
        try:
            plog.write_text(
                f"returncode={r1.returncode}\n--- stdout ---\n{r1.stdout}\n--- stderr ---\n{r1.stderr}",
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            pass

    # 即使 pytest 失败，也尝试生成 coverage 报告：
    # - 对“断言失败/运行时异常”这类情况，coverage 数据往往是有效的
    # - 对“导入失败/依赖缺失”这类情况，通常会出现 no-data-collected

    rep_cmd = [
        sys.executable,
        "-m",
        "coverage",
        "report",
        "-m",
        "--data-file",
        str(data_file),
        "--rcfile",
        str(rc_path),
        "--include=example.py",
    ]
    r2 = subprocess.run(rep_cmd, cwd=source_dir, env=env, capture_output=True, text=True)
    text = r2.stdout.strip()

    report_txt = out_dir / "coverage_report_example.txt"
    try:
        report_txt.write_text(text + "\n", encoding="utf-8", errors="replace")
    except OSError:
        pass

    if html:
        html_dir = out_dir / "htmlcov"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "coverage",
                "html",
                "--data-file",
                str(data_file),
                "--rcfile",
                str(rc_path),
                "--include=example.py",
                "-d",
                str(html_dir),
            ],
            cwd=source_dir,
            env=env,
            check=False,
        )

    pct = _parse_example_percent(text)

    status = "OK"
    if r1.returncode != 0:
        status = "PYTEST_FAIL"
    if "No data was collected" in (r2.stderr or ""):
        status = "NO_DATA"

    # 汇总字段保持为“百分比（若有）”，状态写入 notes，避免后处理脚本无法解析百分比。
    code = 0 if (status == "OK" and r2.returncode == 0 and pct != "?") else 1
    summary = f"{canonical}\t{pct}"
    notes = status
    if r1.returncode != 0:
        tail = (r1.stdout + r1.stderr)[-1200:]
        if tail:
            notes += "\n" + tail
    return code, summary, notes


def _parse_example_percent(report_text: str) -> str:
    # coverage report 的 example.py 行末尾可能是 Missing 列（例如 "6->5, 9-11"），
    # 不能用 parts[-1] 取值；应从 token 中找到真正带 % 的覆盖率 token。
    for line in report_text.splitlines():
        parts = line.split()
        if not parts or parts[0] != "example.py":
            continue
        for tok in parts:
            if tok.endswith("%"):
                return tok.rstrip("%")
    return "?"


def main() -> int:
    args = build_parser().parse_args()
    try:
        import coverage  # noqa: F401
    except Exception as e:
        print(
            "[error] 当前 Python 未安装 coverage。请在已激活的 conda 环境中执行：",
            file=sys.stderr,
        )
        print("  pip install coverage", file=sys.stderr)
        print(f"[error] sys.executable={sys.executable}", file=sys.stderr)
        print(f"[error] {e}", file=sys.stderr)
        return 2

    results_root = (args.results_root or default_results_root()).resolve()

    modes = int(args.all) + int(args.pde) + int(args.new_only) + int(args.program is not None)
    if modes > 1:
        print("错误：--program、--all、--pde、--new-only 只能选一个", file=sys.stderr)
        return 2

    programs: list[str]
    if args.all:
        programs = load_program_names()
    elif args.new_only:
        programs = load_new_program_names()
    elif args.pde:
        programs = load_pde_program_names()
        if not programs:
            print("programs.json 中 pde_subset 为空", file=sys.stderr)
            return 2
    elif args.program:
        programs = [args.program]
    else:
        args.suite = DEFAULT_SUITE
        args.test_file = DEFAULT_TEST_FILE
        args.html = bool(args.html or DEFAULT_HTML)

        mode = (DEFAULT_MODE or "program").strip().lower()
        if mode == "all":
            programs = load_program_names()
            args.all = True
        elif mode == "pde":
            programs = load_pde_program_names()
            if not programs:
                print("programs.json 中 pde_subset 为空", file=sys.stderr)
                return 2
            args.pde = True
        elif mode == "program":
            if not DEFAULT_PROGRAM:
                print("DEFAULT_PROGRAM 为空，请在脚本中设置", file=sys.stderr)
                return 2
            programs = [DEFAULT_PROGRAM]
        else:
            print(f"DEFAULT_MODE 不合法: {DEFAULT_MODE!r}（应为 program/pde/all）", file=sys.stderr)
            return 2

    batch = args.all or args.pde or args.new_only

    rows: list[tuple[str, str, str]] = []
    worst = 0
    for name in programs:
        html = bool(args.html and not batch)
        plog = bool(args.pytest_log)
        code, summary, full = measure_one(
            args.suite,
            name,
            args.test_file,
            results_root=results_root,
            html=html,
            pytest_log=plog,
        )
        worst = max(worst, code)
        if batch:
            rows.append(
                (
                    name,
                    summary.split("\t", 1)[-1] if "\t" in summary else "?",
                    summary + ("\n" + full if full else ""),
                )
            )
            print(summary)
        else:
            print(summary)
            if full:
                print(full)
            out_dir = program_results_dir(results_root, args.suite, name)
            print(f"[结果目录] {out_dir}")
            if code != 0 and not full:
                print("(无 coverage 报告，见 pytest_last.txt)", file=sys.stderr)

    if batch:
        results_root.mkdir(parents=True, exist_ok=True)
        if args.summary_name:
            out = Path(args.summary_name)
            if not out.is_absolute():
                out = results_root / out
        else:
            out = summary_csv_path(results_root, args.suite)
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["program", "example_branch_cover_pct", "notes"])
            for canonical, pct, notes in rows:
                w.writerow([canonical, pct, notes.replace("\n", " | ")])
        print(f"[ok] 汇总: {out}")

    return worst


if __name__ == "__main__":
    raise SystemExit(main())
