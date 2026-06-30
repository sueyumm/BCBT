"""
批量运行 CoverUp 生成测试。

默认结果目录：
  scientific_calculation/<program>/coverup/result_4o/

其中：
- `coverup.log` 在 `coverup/result_4o/`
- 生成的 pytest 用例在 `coverup/result_4o/tests/`
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
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
    program_results_dir,
    program_root,
)

# 手动配置
# primary: https://sg.uiuiapi.com/v1
# backup:  https://api1.uiuiapi.com/v1
DEFAULT_OPENAI_MODEL = os.environ.get("COVERUP_MODEL", "gpt-4o")
DEFAULT_OPENAI_BASE_URL = (
    os.environ.get("OPENAI_BASE_URL")
    or os.environ.get("OPENAI_API_BASE")
    or "https://sg.uiuiapi.com/v1"
)

# 直接运行配置
# DEFAULT_MODE: "program" | "pde" | "all"
DEFAULT_MODE = "program"
DEFAULT_PROGRAM = "2DJacobiPoissonSolver"
DEFAULT_TIMEOUT_MIN = 30
DEFAULT_ROUNDS = 3
DEFAULT_REPEAT_TESTS = 5
DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_MODEL_TEMPERATURE = 0.0
DEFAULT_EMPTY_START = True
DEFAULT_INSTALL_MISSING_MODULES = True
_COVERUP_PYTHON_CANDIDATES = [
    os.environ.get("COVERUP_PYTHON"),
    r"D:\Anaconda\envs\Py10\python.exe",
    sys.executable,
]
_COVERUP_MODULE_CANDIDATES = ("coverup", "coverup-failed")

# 空 tests 时 Slipcover 可能误报 100%，导致 CoverUp 认为 0 个缺口、0 轮生成（0it）
_BOOTSTRAP_NAME = "test__coverup_bootstrap.py"
_CONFTEST_NAME = "conftest.py"
_LOCAL_API_CONFIG = _TOOLS / "local_api_config.json"


def _ensure_bootstrap_test(tests_dir: Path) -> None:
    """若无任何测试文件，写入仅 import example 的引导用例，避免 0it / 假 100%。"""
    if any(tests_dir.glob("test_*.py")):
        return
    p = tests_dir / _BOOTSTRAP_NAME
    p.write_text(
        'def test__coverup_bootstrap_import():\n    import example  # noqa: F401\n',
        encoding="GBK",
    )


def _ensure_conftest(tests_dir: Path, src_dir: Path) -> None:
    """
    CoverUp 有时会生成“直接调用 jacobi(...) 但忘了 import”的测试。
    pytest 不会把 conftest 的符号自动注入到测试模块作用域里，
    因此这里把 example 的公开符号注入 builtins，兜底让这类测试可运行。
    """
    p = tests_dir / _CONFTEST_NAME
    if p.is_file():
        return

    src = str(src_dir)
    p.write_text(
        "import builtins\n"
        "import sys\n\n"
        f"sys.path.insert(0, {src!r})\n"
        "import example as _example\n\n"
        "for _name in dir(_example):\n"
        "    if _name.startswith('_'):\n"
        "        continue\n"
        "    setattr(builtins, _name, getattr(_example, _name))\n",
        encoding="GBK",
        errors="replace",
    )


def _count_generated_tests(tests_dir: Path) -> list[Path]:
    return sorted(
        p
        for p in tests_dir.glob("test_*.py")
        if p.name != _BOOTSTRAP_NAME
    )


def _load_local_api_config() -> dict[str, str]:
    if not _LOCAL_API_CONFIG.is_file():
        return {}
    try:
        data = json.loads(_LOCAL_API_CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"本地 API 配置文件解析失败: {_LOCAL_API_CONFIG} ({exc})") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"本地 API 配置文件格式错误: {_LOCAL_API_CONFIG}（需为 JSON object）")
    return {str(k): str(v) for k, v in data.items() if v is not None}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run CoverUp on selected programs")
    g = p.add_mutually_exclusive_group(required=False)
    g.add_argument("--program")
    g.add_argument("--all", action="store_true")
    g.add_argument("--pde", action="store_true")
    g.add_argument("--new-only", action="store_true", help="Only run newly added programs")
    p.add_argument("--timeout-min", type=int, default=30, help="每个程序最大分钟数")
    p.add_argument("--results-root", type=Path, default=None, help="兼容参数，可忽略")
    p.add_argument("--model", default=DEFAULT_OPENAI_MODEL, help="LLM model name passed to CoverUp")
    # 默认 None：避免把密钥写进 argparse help / 默认值泄露；运行时再解析为 env 或报错提示
    p.add_argument(
        "--openai-api-key",
        default=None,
        help="OpenAI-compatible API key（优先级：本参数 > 环境变量 OPENAI_API_KEY）",
    )
    p.add_argument("--openai-base-url", default=DEFAULT_OPENAI_BASE_URL, help="OpenAI-compatible base URL")
    p.add_argument("--skip-checks", action="store_true")
    p.add_argument("--rounds", type=int, default=DEFAULT_ROUNDS, help="连续运行轮数（后续轮次基于前一轮测试集）")
    p.add_argument("--repeat-tests", type=int, default=DEFAULT_REPEAT_TESTS, help="每轮测试重复执行次数（用于 flaky 检测）")
    p.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS, help="每个代码片段最大尝试次数")
    p.add_argument(
        "--model-temperature",
        type=float,
        default=DEFAULT_MODEL_TEMPERATURE,
        help="传给 CoverUp 的模型温度",
    )
    p.add_argument(
        "--empty-start",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_EMPTY_START,
        help="首轮前清空 tests_dir 里的历史测试，模拟“无预置测试集”起跑",
    )
    p.add_argument(
        "--install-missing-modules",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_INSTALL_MISSING_MODULES,
        help="是否允许 CoverUp 自动安装缺失模块",
    )
    p.add_argument(
        "--bootstrap-empty-tests",
        action="store_true",
        help="仅当 tests 为空时写入 bootstrap import 测试（默认关闭，保持空起跑）",
    )
    return p


def _check_env(api_key: str) -> None:
    coverup_python, coverup_module = _resolve_coverup_runner()
    r = subprocess.run([str(coverup_python), "-m", coverup_module, "--help"], capture_output=True, text=True)
    if r.returncode not in (0, 1):
        raise SystemExit("CoverUp 未安装，请先执行: pip install coverup")
    if not api_key:
        raise SystemExit(
            "OPENAI_API_KEY 为空：请设置环境变量 OPENAI_API_KEY，或使用 --openai-api-key"
        )


def _resolve_coverup_runner() -> tuple[Path, str]:
    for candidate in _COVERUP_PYTHON_CANDIDATES:
        if not candidate:
            continue
        exe = Path(candidate)
        if not exe.exists():
            continue
        for module in _COVERUP_MODULE_CANDIDATES:
            r = subprocess.run([str(exe), "-m", module, "--help"], capture_output=True, text=True)
            combined = (r.stdout or "") + "\n" + (r.stderr or "")
            if ("usage: CoverUp" in combined) or (f"usage: {module}" in combined) or ("--tests-dir" in combined):
                return exe, module
    raise SystemExit("Unable to find a Python interpreter with CoverUp installed.")


def _resolve_coverup_python() -> Path:
    return _resolve_coverup_runner()[0]


def _run_one(
    name: str,
    timeout_min: int,
    results_root: Path,
    *,
    model: str,
    model_temperature: float,
    rounds: int,
    repeat_tests: int,
    max_attempts: int,
    empty_start: bool,
    install_missing_modules: bool,
    bootstrap_empty_tests: bool,
    openai_api_key: str,
    openai_base_url: str,
) -> int:
    # suite 目录只负责输出；example.py 只保留在程序根目录
    source_dir = program_root(name)
    out_dir = program_results_dir(results_root, "coverup", name)
    out_dir.mkdir(parents=True, exist_ok=True)
    tests_dir = out_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "coverup.log"
    source_file = source_dir / "example.py"

    if empty_start:
        for old_test in tests_dir.glob("test_*.py"):
            old_test.unlink(missing_ok=True)
    if bootstrap_empty_tests:
        _ensure_bootstrap_test(tests_dir)
    _ensure_conftest(tests_dir, source_dir)
    print(f"\n[program] {name}")
    t0 = time.time()
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = openai_api_key
    if openai_base_url:
        env["OPENAI_BASE_URL"] = openai_base_url
        env["OPENAI_API_BASE"] = openai_base_url
    else:
        env.pop("OPENAI_BASE_URL", None)
        env.pop("OPENAI_API_BASE", None)
    env.pop("OPENAI_CHAT_COMPLETIONS_URL", None)
    # repeat-tests 依赖 pytest-repeat，不能关闭 autoload
    env.pop("PYTEST_DISABLE_PLUGIN_AUTOLOAD", None)
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(source_dir) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")

    coverup_python, coverup_module = _resolve_coverup_runner()
    last_rc = 0
    with log_path.open("w", encoding="GBK", errors="replace") as f:
        f.write(f"[runner] tools/run_coverup.py\n")
        f.write(f"[python] {sys.executable}\n")
        f.write(f"[coverup_python] {coverup_python}\n")
        f.write(f"[coverup_module] {coverup_module}\n")
        f.write(f"[model] {model}\n")
        f.write(f"[model_temperature] {model_temperature}\n")
        f.write(f"[repeat_tests] {repeat_tests}\n")
        f.write(f"[max_attempts] {max_attempts}\n")
        f.write(f"[rounds] {rounds}\n")
        f.write(f"[empty_start] {empty_start}\n")
        f.write(f"[install_missing_modules] {install_missing_modules}\n")
        f.write(f"[openai_base_url] {openai_base_url or '(default)'}\n")
        f.write(f"[time] {datetime.datetime.now().isoformat()}\n")
        f.write(f"[cwd] {source_dir}\n")

        for round_idx in range(1, rounds + 1):
            cmd = [
                str(coverup_python),
                "-m",
                coverup_module,
                "--tests-dir",
                str(tests_dir),
                "--add-to-pythonpath",
                "--branch-coverage",
                "--show-details",
                "--debug",
                "--max-attempts",
                str(max_attempts),
                "--model-temperature",
                str(model_temperature),
                "--repeat-tests",
                str(repeat_tests),
                "--model",
                model,
            ]
            if install_missing_modules:
                cmd.append("--install-missing-modules")
            else:
                cmd.append("--no-install-missing-modules")
            cmd.append(str(source_file))

            f.write(f"\n---- round {round_idx}/{rounds} ----\n")
            f.write(f"[cmd] {' '.join(cmd)}\n\n")
            proc = subprocess.run(
                cmd,
                cwd=str(source_dir),
                env=env,
                stdout=f,
                stderr=subprocess.STDOUT,
                timeout=timeout_min * 60,
            )
            last_rc = proc.returncode
            f.write(f"\n[round_rc] {last_rc}\n")

    elapsed = time.time() - t0
    generated = _count_generated_tests(tests_dir)
    print(
        f"[rc={last_rc}] generated_tests={len(generated)} "
        f"(excl. bootstrap) elapsed={elapsed:.0f}s out={tests_dir}"
    )
    return 0 if generated else 1


def main() -> int:
    args = build_parser().parse_args()
    local_api = _load_local_api_config()
    # 允许“直接运行无参数”：按脚本内默认配置执行
    if not (args.program or args.all or args.pde or args.new_only):
        args.timeout_min = DEFAULT_TIMEOUT_MIN
        mode = (DEFAULT_MODE or "all").strip().lower()
        if mode == "all":
            args.all = True
        elif mode == "pde":
            args.pde = True
        elif mode == "program":
            if not DEFAULT_PROGRAM:
                raise SystemExit("DEFAULT_MODE=program 时，DEFAULT_PROGRAM 不能为空")
            args.program = DEFAULT_PROGRAM
        else:
            raise SystemExit(f"DEFAULT_MODE 不合法: {DEFAULT_MODE!r}（应为 program/pde/all）")
    openai_api_key = (
        args.openai_api_key
        or os.environ.get("OPENAI_API_KEY", "")
        or local_api.get("openai_api_key", "")
        or local_api.get("OPENAI_API_KEY", "")
    )
    args.openai_base_url = (
        args.openai_base_url
        or os.environ.get("OPENAI_BASE_URL")
        or os.environ.get("OPENAI_API_BASE")
        or local_api.get("openai_base_url")
        or local_api.get("OPENAI_BASE_URL")
        or local_api.get("OPENAI_API_BASE")
        or DEFAULT_OPENAI_BASE_URL
    )
    if not args.skip_checks:
        _check_env(openai_api_key)

    if args.program:
        names = [args.program]
    elif args.new_only:
        names = load_new_program_names()
    elif args.pde:
        names = load_pde_program_names()
    else:
        names = load_program_names()

    results_root = (args.results_root or default_results_root()).resolve()
    worst = 0
    for name in names:
        try:
            worst = max(
                worst,
                _run_one(
                    name,
                    args.timeout_min,
                    results_root,
                    model=args.model,
                    model_temperature=args.model_temperature,
                    rounds=args.rounds,
                    repeat_tests=args.repeat_tests,
                    max_attempts=args.max_attempts,
                    empty_start=args.empty_start,
                    install_missing_modules=args.install_missing_modules,
                    bootstrap_empty_tests=args.bootstrap_empty_tests,
                    openai_api_key=openai_api_key,
                    openai_base_url=args.openai_base_url,
                ),
            )
        except subprocess.TimeoutExpired:
            print(f"[timeout] {name}")
            worst = max(worst, 1)
        except Exception as e:
            print(f"[error] {name}: {e}")
            worst = max(worst, 1)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
