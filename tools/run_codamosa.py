"""Run CodaMosa for scientific_calculation programs via Docker.

Default output layout:
    scientific_calculation/<program>/codamosa/result_4o/

The script auto-creates per-program ``package.txt`` files from
``tools/package.txt`` so runs can be started with a single command.
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

DEFAULT_IMAGE = "codamosa-runner-chat"
DEFAULT_MODEL = "gpt-4o"
DEFAULT_BASE_URL = "https://sg.uiuiapi.com"
DEFAULT_RELATIVE_URL = "/v1/chat/completions"
DEFAULT_PACKAGE_TEMPLATE = _TOOLS / "package.txt"
LOCAL_API_CONFIG = _TOOLS / "local_api_config.json"
DEFAULT_MODE = "all"


def _load_local_api_config() -> dict[str, str]:
    if not LOCAL_API_CONFIG.is_file():
        return {}
    try:
        data = json.loads(LOCAL_API_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return {}
    result: dict[str, str] = {}
    if isinstance(data.get("openai_api_key"), str):
        result["api_key"] = data["openai_api_key"]
    if isinstance(data.get("openai_base_url"), str):
        result["base_url"] = data["openai_base_url"]
    if isinstance(data.get("openai_model"), str):
        result["model_name"] = data["openai_model"]
    return result


def build_parser() -> argparse.ArgumentParser:
    local_api = _load_local_api_config()
    p = argparse.ArgumentParser(description="Run CodaMosa via Docker")
    g = p.add_mutually_exclusive_group(required=False)
    g.add_argument("--program")
    g.add_argument("--all", action="store_true")
    g.add_argument("--pde", action="store_true")
    g.add_argument("--new-only", action="store_true", help="Only run newly added programs")
    p.add_argument("--budget", type=int, default=120, help="Maximum search time per program in seconds.")
    p.add_argument("--results-root", type=Path, default=None, help="Compatibility argument; ignored by the new layout.")
    p.add_argument("--image", default=DEFAULT_IMAGE)
    p.add_argument(
        "--api-key",
        default=(
            os.environ.get("CODAMOSA_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or local_api.get("api_key")
        ),
    )
    p.add_argument("--model-name", default=local_api.get("model_name", DEFAULT_MODEL))
    p.add_argument("--model-base-url", default=local_api.get("base_url", DEFAULT_BASE_URL))
    p.add_argument("--model-relative-url", default=DEFAULT_RELATIVE_URL)
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--network-host", action="store_true", default=True)
    p.add_argument("--no-network-host", dest="network_host", action="store_false")
    p.add_argument("--no-pull", action="store_true")
    p.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip programs that already have a successful codamosa_run.json in the output directory.",
    )
    return p


def _check_docker() -> None:
    r = subprocess.run(["docker", "info"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("Docker is not running. Please start Docker first.")


def _ensure_package_file(src_dir: Path) -> None:
    package_file = src_dir / "package.txt"
    if package_file.is_file():
        return
    if not DEFAULT_PACKAGE_TEMPLATE.is_file():
        raise SystemExit(f"Missing default package template: {DEFAULT_PACKAGE_TEMPLATE}")
    package_file.write_text(DEFAULT_PACKAGE_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")


def _pull_image(image: str) -> None:
    subprocess.run(["docker", "image", "inspect", image], check=True)


def _build_cmd(
    *,
    image: str,
    src_dir: Path,
    out_dir: Path,
    budget: int,
    api_key: str,
    model_name: str,
    model_base_url: str,
    model_relative_url: str,
    temperature: float,
    network_host: bool,
) -> list[str]:
    cmd = ["docker", "run", "--rm"]
    if network_host:
        cmd.extend(["--network", "host"])
    cmd.extend(
        [
            "-v",
            f"{src_dir.resolve()}:/input:ro",
            "-v",
            f"{out_dir.resolve()}:/output",
            "-v",
            f"{src_dir.resolve()}:/package:ro",
            image,
            "--assertion-generation",
            "NONE",
            "--project_path",
            "/input",
            "--module-name",
            "example",
            "--output-path",
            "/output",
            "--maximum_search_time",
            str(budget),
            "--output_variables",
            ",".join(
                [
                    "TargetModule",
                    "Coverage",
                    "BranchCoverage",
                    "LineCoverage",
                    "ParsedStatements",
                    "UninterpStatements",
                    "ParsableStatements",
                    "LLMCalls",
                    "LLMQueryTime",
                    "LLMStageSavedTests",
                    "LLMStageSavedMutants",
                    "LLMNeededExpansion",
                    "LLMNeededUninterpreted",
                    "LLMNeededUninterpretedCallsOnly",
                    "RandomSeed",
                    "AccessibleObjectsUnderTest",
                    "CodeObjects",
                    "CoverageTimeline",
                ]
            ),
            "--report-dir",
            "/output",
            "--coverage_metrics",
            "BRANCH,LINE",
            "--model_name",
            model_name,
            "--include-partially-parsable",
            "True",
            "--allow-expandable-cluster",
            "True",
            "--algorithm",
            "CODAMOSA",
            "--temperature",
            str(temperature),
            "--uninterpreted_statements",
            "ONLY",
            "--authorization-key",
            api_key,
            "--model_base_url",
            model_base_url,
            "--model_relative_url",
            model_relative_url,
            "-v",
        ]
    )
    return cmd


def _normalize_outputs(out_dir: Path) -> list[Path]:
    generated = sorted(out_dir.glob("test_*.py"))
    test_example = out_dir / "test_example.py"
    failing = out_dir / "test_example_failing.py"

    regular = [p for p in generated if p.name != failing.name]
    if regular and regular[0] != test_example:
        regular[0].replace(test_example)

    for extra in out_dir.glob("test_*.py"):
        if extra not in {test_example, failing}:
            extra.unlink(missing_ok=True)

    kept: list[Path] = []
    if test_example.exists():
        kept.append(test_example)
    if failing.exists():
        kept.append(failing)
    return kept


def _rename_legacy_outputs(out_dir: Path) -> None:
    legacy = out_dir / "codex_generations.py"
    llm_legacy = out_dir / "llm_generations.py"
    modern = out_dir / "gpt4o_generations.py"
    if legacy.exists():
        if modern.exists():
            modern.unlink()
        legacy.replace(modern)
    elif llm_legacy.exists():
        if modern.exists():
            modern.unlink()
        llm_legacy.replace(modern)


def _run_one(
    *,
    name: str,
    budget: int,
    results_root: Path,
    image: str,
    api_key: str,
    model_name: str,
    model_base_url: str,
    model_relative_url: str,
    temperature: float,
    network_host: bool,
) -> int:
    src_dir = program_root(name)
    out_dir = program_results_dir(results_root, "codamosa", name)
    out_dir.mkdir(parents=True, exist_ok=True)
    _ensure_package_file(src_dir)

    log_path = out_dir / "codamosa.log"
    meta_path = out_dir / "codamosa_run.json"

    for stale in out_dir.glob("test_*.py"):
        stale.unlink(missing_ok=True)

    cmd = _build_cmd(
        image=image,
        src_dir=src_dir,
        out_dir=out_dir,
        budget=budget,
        api_key=api_key,
        model_name=model_name,
        model_base_url=model_base_url,
        model_relative_url=model_relative_url,
        temperature=temperature,
        network_host=network_host,
    )

    print(f"\n[program] {name}")
    t0 = time.time()
    with log_path.open("w", encoding="utf-8", errors="replace") as f:
        safe_cmd = [part if part != api_key else "***REDACTED***" for part in cmd]
        f.write("[runner] tools/run_codamosa.py\n")
        f.write(f"[time] {datetime.datetime.now().isoformat()}\n")
        f.write(f"[program] {name}\n")
        f.write(f"[cwd] {src_dir}\n")
        f.write(f"[image] {image}\n")
        f.write(f"[budget] {budget}\n")
        f.write(f"[out_dir] {out_dir}\n")
        f.write(f"[cmd] {' '.join(safe_cmd)}\n\n")
        proc = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.STDOUT,
            timeout=budget + 600,
        )
    elapsed = time.time() - t0

    generated = _normalize_outputs(out_dir)
    _rename_legacy_outputs(out_dir)
    meta = {
        "program": name,
        "runner": "tools/run_codamosa.py",
        "image": image,
        "budget_sec": budget,
        "return_code": proc.returncode,
        "script_result": 0 if generated else 1,
        "elapsed_sec": round(elapsed, 3),
        "out_dir": str(out_dir),
        "generated_tests": [p.name for p in generated],
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[rc={proc.returncode}] tests={len(generated)} elapsed={elapsed:.0f}s out={out_dir}")
    return 0 if generated else 1


def _should_skip_existing(name: str, results_root: Path) -> bool:
    out_dir = program_results_dir(results_root, "codamosa", name)
    meta_path = out_dir / "codamosa_run.json"
    if not meta_path.is_file():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if meta.get("script_result") == 0:
        return True
    generated_tests = meta.get("generated_tests")
    return isinstance(generated_tests, list) and len(generated_tests) > 0


def main() -> int:
    args = build_parser().parse_args()
    _check_docker()
    if not args.api_key:
        raise SystemExit("Missing API key. Pass --api-key or set CODAMOSA_API_KEY / OPENAI_API_KEY.")
    if not args.no_pull:
        _pull_image(args.image)

    if args.program:
        names = [args.program]
    elif args.new_only:
        names = load_new_program_names()
    elif args.pde:
        names = load_pde_program_names()
    elif args.all or DEFAULT_MODE == "all":
        names = load_program_names()
    elif DEFAULT_MODE == "pde":
        names = load_pde_program_names()
    else:
        raise SystemExit("Please pass --program, --pde, or --all.")

    results_root = (args.results_root or default_results_root()).resolve()
    worst = 0
    for name in names:
        if args.skip_existing and _should_skip_existing(name, results_root):
            out_dir = program_results_dir(results_root, "codamosa", name)
            print(f"[skip-existing] {name} -> {out_dir}")
            continue
        try:
            worst = max(
                worst,
                _run_one(
                    name=name,
                    budget=args.budget,
                    results_root=results_root,
                    image=args.image,
                    api_key=args.api_key,
                    model_name=args.model_name,
                    model_base_url=args.model_base_url,
                    model_relative_url=args.model_relative_url,
                    temperature=args.temperature,
                    network_host=args.network_host,
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
