"""
用 Pynguin 针对只读程序目录中的 example 模块生成测试；
默认产出写入各程序目录下的 result_4o/。

用法:
  python tools/run_pynguin.py --suite pynguin --program euler_diffusion
  python tools/run_pynguin.py --suite pynguin --all
  python tools/run_pynguin.py --suite pynguin --pde
  python tools/run_pynguin.py --list
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from paths import (
    default_results_root,
    example_path,
    load_pde_program_names,
    load_program_names,
    program_root,
    program_results_dir,
)

# 直接运行配置（可选）：不传 --program/--all/--pde 时使用
DEFAULT_SUITE = "pynguin"
DEFAULT_PROGRAM = "Linear_equation4"
DEFAULT_MODE = "program"  # "program" | "pde" | "all"
DEFAULT_TIME = 120
DEFAULT_ASSERTIONS = "NONE"  # "NONE" | "MUTATION_ANALYSIS"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Pynguin：输入程序目录，输出到各程序 result_4o 目录")
    p.add_argument("--suite", choices=("pynguin", "chatgpt"), default="pynguin")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--program", help="单个程序文件夹名（canonical，见 programs.json）")
    g.add_argument("--all", action="store_true", help="programs.json 中全部程序")
    g.add_argument("--pde", action="store_true", help="仅 programs.json 中 pde_subset")
    p.add_argument(
        "--results-root",
        type=Path,
        default=None,
        help="兼容参数，默认忽略；结果固定写到各程序目录下 result_4o/",
    )
    p.add_argument("--time", type=int, default=120, help="maximum-search-time（秒）")
    p.add_argument(
        "--exec-timeout",
        type=int,
        default=5,
        help="单条用例最大执行时间（秒），对应 Pynguin --maximum-test-execution-timeout",
    )
    p.add_argument(
        "--assertions",
        default="NONE",
        choices=("NONE", "MUTATION_ANALYSIS"),
        help="断言生成策略",
    )
    p.add_argument("--output-name", default="test_example.py", help="结果目录中的测试文件名")
    p.add_argument(
        "--staging-name",
        default="_pynguin_staging",
        help="结果目录内 Pynguin 工作子目录名",
    )
    p.add_argument("--keep-staging", action="store_true", help="保留 staging 目录")
    p.add_argument("--list", action="store_true", help="列出全部程序名")
    p.add_argument("-q", "--quiet", action="store_true", help="日志仍写入文件，终端少输出")
    return p


def _relocate_pynguin_report(prog_dir: Path, dest_parent: Path) -> None:
    src = prog_dir / "pynguin-report"
    if not src.exists():
        return
    dst = dest_parent / "pynguin-report"
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)
    try:
        shutil.move(str(src), str(dst))
    except PermissionError:
        # On Windows, Pynguin/coverage can briefly keep report files open.  The
        # report is useful metadata, but losing it should not discard the
        # generated baseline test file.
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        except OSError:
            pass
        shutil.rmtree(src, ignore_errors=True)


def run_pynguin_subprocess(
    *,
    prog_dir: Path,
    staging_dir: Path,
    search_time: int,
    exec_timeout_s: int,
    assertions: str,
    quiet: bool,
    log_path: Path,
) -> int:
    staging_dir = staging_dir.resolve()
    if staging_dir.exists():
        shutil.rmtree(staging_dir, ignore_errors=True)
    staging_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["PYNGUIN_DANGER_AWARE"] = "1"
    # 避免被测程序在 import-time 调用 plt.show() 等 GUI 行为导致崩溃/挂起
    # （solve_equation2 的 example.py 就有 plt.show()）。
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("MATPLOTLIBRC", "")

    cmd = [
        sys.executable,
        "-m",
        "pynguin",
        # rich 在某些 Windows 终端/管道环境下会触发 Bad file descriptor，
        # 这里统一关掉 rich 美化输出，避免生成过程被日志系统打断。
        "--no-rich",
        "--project-path",
        str(prog_dir.resolve()),
        "--module-name",
        "example",
        # solve_equation2 在类型推断阶段会因 inspect.signature(None) 崩溃；
        # 这里直接关闭类型推断，优先保证“能生成测试并测覆盖率”。
        "--type_inference_strategy",
        "NONE",
        # 关键：让 Pynguin 不要把大型第三方库/标准库模块当成覆盖目标，
        # 否则可能生成“只测 numpy/sympy 内部函数”的用例，导致 example.py 无覆盖率数据。
        # 注意：这是“分析/目标”层面的忽略，不影响 example 在运行时导入这些库。
        "--ignore-modules",
        "numpy",
        "sympy",
        "scipy",
        "matplotlib",
        "mpmath",
        "PIL",
        "inspect",
        "platform",
        "--output-path",
        str(staging_dir),
        "--maximum-search-time",
        str(search_time),
        "--maximum-test-execution-timeout",
        str(exec_timeout_s),
        "--assertion-generation",
        assertions,
        # 尽量贴近最朴素的 CLI 行为，避免一些高级模式在 Windows 下不稳定。
        "--subprocess",
        "false",
        "--subprocess-if-recommended",
        "false",
        "--use-master-worker",
        "false",
        # 避免后处理/最小化把用例删空（出现 Written 0 test cases）
        "--nopost-process",
        "--test_case_minimization_strategy",
        "NONE",
    ]
    if not quiet:
        cmd.append("-v")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    # Windows 上若使用 stdout=PIPE，Pynguin 大量输出会填满管道缓冲区，子进程在 write 处阻塞，
    # 表现为在某一个程序上“卡住”；直接把日志写入文件可避免死锁。
    env.setdefault("PYTHONUNBUFFERED", "1")
    with log_path.open("w", encoding="utf-8", errors="replace", newline="\n") as logf:
        completed = subprocess.run(
            cmd,
            cwd=prog_dir,
            env=env,
            stdout=logf,
            stderr=logf,
        )
    if not quiet:
        try:
            text = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        if text:
            tail = 24000
            print(text[-tail:] if len(text) > tail else text)
    return completed.returncode


def run_one(
    *,
    suite: str,
    canonical: str,
    results_root: Path,
    time_s: int,
    assertions: str,
    output_name: str,
    staging_name: str,
    keep_staging: bool,
    quiet: bool,
    exec_timeout_s: int,
) -> int:
    prog_dir = program_root(canonical)
    ex = example_path(suite, canonical)
    if not ex.is_file():
        print(f"[SKIP] 未找到被测文件: {ex}", file=sys.stderr)
        return 2

    out_dir = program_results_dir(results_root, suite, canonical)
    out_dir.mkdir(parents=True, exist_ok=True)
    staging = out_dir / staging_name
    log_path = out_dir / "pynguin.log"

    print(f"\n{'='*60}")
    print(f"[输入] {prog_dir}")
    print(f"[输出] {out_dir}")

    rc = run_pynguin_subprocess(
        prog_dir=prog_dir,
        staging_dir=staging,
        search_time=time_s,
        exec_timeout_s=exec_timeout_s,
        assertions=assertions,
        quiet=quiet,
        log_path=log_path,
    )
    _relocate_pynguin_report(prog_dir, out_dir)
    if rc != 0:
        print(f"[pynguin] 退出码 {rc}，详见 {log_path}", file=sys.stderr)

    generated = staging / "test_example.py"
    target = out_dir / output_name
    if generated.is_file():
        shutil.copy2(generated, target)
        print(f"[ok] 测试文件: {target}")
        if not keep_staging:
            shutil.rmtree(staging, ignore_errors=True)
        return 0 if rc == 0 else 1

    print(f"[fail] 未生成 {generated}", file=sys.stderr)
    return 1


def main() -> int:
    args = build_parser().parse_args()
    if args.list:
        for name in load_program_names():
            print(name)
        return 0

    try:
        import pynguin  # noqa: F401
    except Exception as e:
        print(
            "[error] 当前 Python 未安装 pynguin，请先 `pip install pynguin`（在已激活的 conda 环境中）。",
            file=sys.stderr,
        )
        print(f"[error] sys.executable={sys.executable}", file=sys.stderr)
        print(f"[error] {e}", file=sys.stderr)
        return 2

    modes = int(args.all) + int(args.pde) + int(args.program is not None)
    if modes > 1:
        print("错误：--program、--all、--pde 只能选一个", file=sys.stderr)
        return 2

    if modes == 0:
        args.suite = DEFAULT_SUITE
        args.time = DEFAULT_TIME
        args.assertions = DEFAULT_ASSERTIONS

        mode = (DEFAULT_MODE or "program").strip().lower()
        if mode == "all":
            programs = load_program_names()
        elif mode == "pde":
            programs = load_pde_program_names()
            if not programs:
                print("programs.json 中 pde_subset 为空", file=sys.stderr)
                return 2
        elif mode == "program":
            if not DEFAULT_PROGRAM:
                print("DEFAULT_PROGRAM 为空，请在脚本中设置", file=sys.stderr)
                return 2
            programs = [DEFAULT_PROGRAM]
        else:
            print(f"DEFAULT_MODE 不合法: {DEFAULT_MODE!r}（应为 program/pde/all）", file=sys.stderr)
            return 2
    elif args.all:
        programs = load_program_names()
    elif args.pde:
        programs = load_pde_program_names()
        if not programs:
            print("programs.json 中 pde_subset 为空", file=sys.stderr)
            return 2
    else:
        programs = [args.program]  # type: ignore[list-item]

    results_root = (args.results_root or default_results_root()).resolve()
    worst = 0
    for canonical in programs:
        code = run_one(
            suite=args.suite,
            canonical=canonical,
            results_root=results_root,
            time_s=args.time,
            assertions=args.assertions,
            output_name=args.output_name,
            staging_name=args.staging_name,
            keep_staging=args.keep_staging,
            quiet=args.quiet,
            exec_timeout_s=args.exec_timeout,
        )
        worst = max(worst, code)

    if len(programs) > 1:
        print(f"\n完成: {len(programs)} 个程序，最差退出码 {worst}")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
