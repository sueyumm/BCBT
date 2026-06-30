"""Run the proposed branch-targeted method as an automatic multi-round pipeline.

The pipeline replaces manual round-by-round execution:

1. Run one LLM generation round.
2. Evaluate generated tests together with the Pynguin baseline.
3. Filter generated tests down to passing test functions and re-evaluate.
4. Stop per program when branch coverage reaches 100%, coverage fails to improve
   for the configured patience, generated tests fail consecutively, or
   ``--max-rounds`` is reached.
5. Build the next-round prompt automatically only for programs that should
   continue.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from paths import ROOT, SCI_ROOT, load_new_program_names

DEFAULT_MAX_ROUNDS = 3
DEFAULT_MAX_FAILURES = 2
DEFAULT_NO_IMPROVEMENT_PATIENCE = 1
DEFAULT_MIN_IMPROVEMENT = 0.01
DEFAULT_TIMEOUT = 60
DEFAULT_MAX_TOKENS = 1600
DEFAULT_METHOD_DIR = "our_method"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run proposed method with automatic stopping")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--program", help="Only run one program")
    group.add_argument("--all", action="store_true", help="Run all programs with round-1 prompts")
    group.add_argument("--new-only", action="store_true", help="Run only newly added programs with prompts")
    group.add_argument(
        "--effective-from-summary",
        action="store_true",
        help="Run programs marked scope=effective and entered_our_method=True in final_summary.csv",
    )
    parser.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS)
    parser.add_argument("--max-failures", type=int, default=DEFAULT_MAX_FAILURES)
    parser.add_argument(
        "--no-improvement-patience",
        type=int,
        default=DEFAULT_NO_IMPROVEMENT_PATIENCE,
        help=(
            "Stop after this many consecutive non-improving rounds. "
            "The default 1 preserves the original pipeline behavior."
        ),
    )
    parser.add_argument("--min-improvement", type=float, default=DEFAULT_MIN_IMPROVEMENT)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="LLM request timeout in seconds")
    parser.add_argument("--eval-timeout", type=int, default=180, help="pytest/coverage timeout in seconds")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument(
        "--method-dir",
        default=DEFAULT_METHOD_DIR,
        help="Per-program output directory for this method variant.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip programs with an existing pipeline_state.json marked complete",
    )
    parser.add_argument("--limit", type=int, default=0, help="Run at most this many selected programs")
    parser.add_argument("--dry-run", action="store_true", help="Print selected programs without calling the API")
    parser.add_argument(
        "--disable-error-feedback",
        action="store_true",
        help=(
            "Ablation mode: next-round prompts keep coverage context but omit "
            "previous generated tests, evaluation JSON, and pytest logs."
        ),
    )
    parser.add_argument(
        "--disable-filtering",
        action="store_true",
        help="Ablation mode: skip per-test failing-test filtering and evaluate raw generated tests only.",
    )
    return parser


def prompt_path(program: str, round_no: int, method_dir: str) -> Path:
    preferred = SCI_ROOT / program / method_dir / "prompts" / f"prompt_round_{round_no}.txt"
    if preferred.is_file():
        return preferred
    if method_dir != DEFAULT_METHOD_DIR:
        fallback = SCI_ROOT / program / DEFAULT_METHOD_DIR / "prompts" / f"prompt_round_{round_no}.txt"
        if fallback.is_file():
            return fallback
    return preferred


def method_root(program: str, method_dir: str) -> Path:
    return SCI_ROOT / program / method_dir


def round_dir(program: str, round_no: int, method_dir: str) -> Path:
    return method_root(program, method_dir) / f"round_{round_no}"


def state_path(program: str, method_dir: str) -> Path:
    return method_root(program, method_dir) / "pipeline_state.json"


def discover_programs(method_dir: str, round_no: int = 1) -> list[str]:
    return [
        program_dir.name
        for program_dir in sorted(p for p in SCI_ROOT.iterdir() if p.is_dir())
        if prompt_path(program_dir.name, round_no, method_dir).is_file()
    ]


def selected_programs(args: argparse.Namespace) -> list[str]:
    if args.program:
        programs = [args.program]
    elif args.effective_from_summary:
        programs = [
            program
            for program in load_effective_programs_from_summary(ROOT / "final_summary.csv")
            if prompt_path(program, 1, args.method_dir).is_file()
        ]
    elif args.new_only:
        allowed = set(load_new_program_names())
        programs = [program for program in discover_programs(args.method_dir, 1) if program in allowed]
        effective = branch_target_programs(ROOT / "uncovered_branches_new_only.json")
        if effective:
            programs = [program for program in programs if program in effective]
    else:
        programs = discover_programs(args.method_dir, 1)
        effective = branch_target_programs(ROOT / "uncovered_branches.json")
        effective.update(branch_target_programs(ROOT / "uncovered_branches_new_only.json"))
        if effective:
            programs = [program for program in programs if program in effective]

    if args.skip_existing:
        programs = [
            program
            for program in programs
            if not existing_completed_state(program, args.method_dir)
        ]
    if args.limit and args.limit > 0:
        programs = programs[: args.limit]
    return programs


def load_effective_programs_from_summary(path: Path) -> list[str]:
    """Load the fixed effective set used by final_summary.csv."""
    if not path.is_file():
        raise SystemExit(f"Missing summary file: {path}")
    programs: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("scope") != "effective":
                continue
            if str(row.get("entered_our_method", "")).strip().lower() != "true":
                continue
            program = str(row.get("program", "")).strip()
            if program:
                programs.append(program)
    return programs


def branch_target_programs(path: Path) -> set[str]:
    """Programs that currently have coverage.py missing branch targets."""
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    return {
        str(item.get("program", ""))
        for item in data.get("programs", [])
        if item.get("branches")
    }


def existing_completed_state(program: str, method_dir: str) -> bool:
    path = state_path(program, method_dir)
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if not data.get("complete"):
        return False
    rounds = data.get("rounds", [])
    if not rounds:
        return False
    # Older buggy states did not record generation_ok and could mark a program
    # complete after reusing stale generated tests.  Only skip states produced
    # by the fixed pipeline.
    return all(round_state.get("generation_ok") is True for round_state in rounds)


def run_command(command: list[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return completed.returncode, (completed.stdout or "") + (completed.stderr or "")


def run_generation(program: str, round_no: int, args: argparse.Namespace) -> tuple[int, str]:
    return run_command(
        [
            sys.executable,
            "tools/run_our_method_round.py",
            "--program",
            program,
            "--round",
            str(round_no),
            "--model",
            args.model,
            "--temperature",
            str(args.temperature),
            "--max-tokens",
            str(args.max_tokens),
            "--timeout",
            str(args.timeout),
            "--retries",
            str(args.retries),
            "--method-dir",
            args.method_dir,
        ],
        ROOT,
    )


def run_evaluation(program: str, round_no: int, args: argparse.Namespace) -> tuple[int, str]:
    return run_command(
        [
            sys.executable,
            "tools/evaluate_our_method_round.py",
            "--program",
            program,
            "--round",
            str(round_no),
            "--timeout",
            str(args.eval_timeout),
            "--include-pynguin-baseline",
            "--method-dir",
            args.method_dir,
        ],
        ROOT,
    )


def run_filter(program: str, round_no: int, args: argparse.Namespace) -> tuple[int, str]:
    return run_command(
        [
            sys.executable,
            "tools/filter_our_method_tests.py",
            "--program",
            program,
            "--round",
            str(round_no),
            "--timeout",
            str(args.eval_timeout),
            "--include-pynguin-baseline",
            "--method-dir",
            args.method_dir,
        ],
        ROOT,
    )


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def numeric(value: Any) -> float | None:
    try:
        if value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def round_evaluation(program: str, round_no: int, method_dir: str) -> dict[str, Any]:
    out_dir = round_dir(program, round_no, method_dir)
    filtered = read_json(out_dir / f"filtered_evaluation_round_{round_no}.json")
    raw = read_json(out_dir / f"evaluation_round_{round_no}.json")

    filtered_branch = numeric(filtered.get("branch_coverage"))
    raw_branch = numeric(raw.get("branch_coverage"))
    if filtered_branch is not None:
        filtered["result_source"] = "filtered"
        return filtered
    if raw_branch is not None:
        raw["result_source"] = "raw"
        return raw
    return {"program": program, "round": round_no, "result_source": "missing"}


def generated_test_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"generated_tests_round_{round_no}.py"


def pytest_log_path(program: str, round_no: int, method_dir: str) -> Path:
    out_dir = round_dir(program, round_no, method_dir)
    filtered_log = out_dir / f"filtered_pytest_round_{round_no}.log"
    raw_log = out_dir / f"pytest_round_{round_no}.log"
    return filtered_log if filtered_log.is_file() else raw_log


def read_limited(path: Path, limit: int = 9000) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n# ... truncated ...\n"


def build_next_prompt(
    program: str,
    round_no: int,
    method_dir: str,
    reason: str,
    previous_branch: float,
    current_branch: float,
    include_error_feedback: bool = True,
) -> None:
    next_round = round_no + 1
    current_prompt = read_limited(prompt_path(program, round_no, method_dir), 22000)
    generated = read_limited(generated_test_path(program, round_no, method_dir), 9000)
    pytest_log = read_limited(pytest_log_path(program, round_no, method_dir), 9000)
    evaluation = read_json(round_dir(program, round_no, method_dir) / f"evaluation_round_{round_no}.json")
    filtered = read_json(round_dir(program, round_no, method_dir) / f"filtered_evaluation_round_{round_no}.json")

    feedback_block = ""
    if include_error_feedback:
        feedback_block = f"""
Previous generated tests:
```python
{generated}
```

Raw evaluation JSON:
```json
{json.dumps(evaluation, ensure_ascii=False, indent=2)}
```

Filtered evaluation JSON:
```json
{json.dumps(filtered, ensure_ascii=False, indent=2)}
```

Pytest log:
```text
{pytest_log}
```
"""
    else:
        feedback_block = (
            "\nError-specific feedback is intentionally disabled for this ablation. "
            "Do not use previous generated tests, pytest logs, or evaluation JSON; "
            "use only the branch-targeting prompt and coverage numbers above.\n"
        )

    prompt = f"""You are improving pytest tests for a scientific-computing Python program.

Primary objective:
Improve branch coverage beyond the previous round while keeping all generated tests passing.

Stopping context:
- Previous best branch coverage before this round: {previous_branch:.2f}
- Current branch coverage after this round: {current_branch:.2f}
- Reason for another round: {reason}

Strict output rules:
- Output only raw Python code.
- Do not include explanations or markdown fences.
- Import the target module as: import example as module_0
- Include every required import explicitly.
- Do not modify example.py.
- Keep tests deterministic.
- Every test must call at least one target function and include at least one assert.
- Do not repeat tests that failed or did not improve coverage.

Original/current branch-targeting prompt:
{current_prompt}

{feedback_block}

Output only a corrected complete Python pytest test file for round {next_round}.
"""
    out = method_root(program, method_dir) / "prompts" / f"prompt_round_{next_round}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt, encoding="utf-8")


def baseline_branch(program: str) -> float:
    summary = ROOT / "coverage_summary_pynguin_new_only_branch.csv"
    if summary.is_file():
        with summary.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("program") == program:
                    value = numeric(row.get("branch_coverage"))
                    if value is not None:
                        return value
    return 0.0


def run_program(program: str, args: argparse.Namespace) -> dict[str, Any]:
    best_branch = baseline_branch(program)
    consecutive_failures = 0
    consecutive_no_improvement = 0
    rounds: list[dict[str, Any]] = []
    complete = False
    stop_reason = ""

    if best_branch >= 100.0:
        complete = True
        stop_reason = "baseline_full_coverage"

    for round_no in range(1, args.max_rounds + 1):
        if complete:
            break
        if not prompt_path(program, round_no, args.method_dir).is_file():
            stop_reason = f"missing_prompt_round_{round_no}"
            break

        previous_branch = best_branch
        gen_code, gen_output = run_generation(program, round_no, args)
        run_metadata = read_json(round_dir(program, round_no, args.method_dir) / "our_method_run.json")
        generation_ok = (
            gen_code == 0
            and run_metadata.get("status_code") == 200
            and int(run_metadata.get("generated_chars") or 0) > 0
            and bool(run_metadata.get("generated_tests"))
        )
        if generation_ok:
            eval_code, eval_output = run_evaluation(program, round_no, args)
            if args.disable_filtering:
                filter_code, filter_output = 0, "skipped filtering by --disable-filtering"
            else:
                filter_code, filter_output = run_filter(program, round_no, args)
            evaluation = round_evaluation(program, round_no, args.method_dir)
            branch = numeric(evaluation.get("branch_coverage"))
            returncode = evaluation.get("returncode")
            failed_tests = (
                int(evaluation.get("num_failed_tests") or 0)
                if str(evaluation.get("num_failed_tests", "")).isdigit()
                else 0
            )
            improved = branch is not None and branch > previous_branch + args.min_improvement
            passed = branch is not None and returncode == 0 and failed_tests == 0
        else:
            eval_code, eval_output = 1, "skipped evaluation because LLM generation failed"
            filter_code, filter_output = 1, "skipped filtering because LLM generation failed"
            evaluation = {"result_source": "missing"}
            branch = None
            improved = False
            passed = False

        if improved:
            best_branch = branch
            consecutive_no_improvement = 0
        else:
            consecutive_no_improvement += 1

        if not passed:
            consecutive_failures += 1
        else:
            consecutive_failures = 0

        round_state = {
            "round": round_no,
            "previous_branch": previous_branch,
            "branch": branch,
            "best_branch": best_branch,
            "improved": improved,
            "passed": passed,
            "consecutive_failures": consecutive_failures,
            "consecutive_no_improvement": consecutive_no_improvement,
            "result_source": evaluation.get("result_source"),
            "generation_returncode": gen_code,
            "generation_ok": generation_ok,
            "llm_status_code": run_metadata.get("status_code"),
            "generated_chars": run_metadata.get("generated_chars"),
            "evaluation_returncode": eval_code,
            "filter_returncode": filter_code,
            "generation_output_tail": gen_output[-1200:],
            "evaluation_output_tail": eval_output[-1200:],
            "filter_output_tail": filter_output[-1200:],
        }
        rounds.append(round_state)

        if best_branch >= 100.0:
            complete = True
            stop_reason = "all_target_branches_covered"
        elif consecutive_failures >= args.max_failures:
            complete = True
            stop_reason = "consecutive_llm_test_failures"
        elif consecutive_no_improvement >= args.no_improvement_patience:
            complete = True
            stop_reason = "branch_coverage_no_longer_improves"
        elif round_no >= args.max_rounds:
            complete = True
            stop_reason = "max_rounds_reached"
        else:
            feedback_reason = (
                "coverage did not improve; try a different deterministic test strategy"
                if not improved
                else "coverage improved but target branches remain uncovered"
            )
            build_next_prompt(
                program,
                round_no,
                args.method_dir,
                feedback_reason,
                previous_branch,
                best_branch,
                include_error_feedback=not args.disable_error_feedback,
            )

        print(
            f"[{program}] round {round_no}: previous={previous_branch:.2f}, "
            f"current={branch}, best={best_branch:.2f}, stop={stop_reason if complete else 'continue'}"
        )

    state = {
        "program": program,
        "method_dir": args.method_dir,
        "model": args.model,
        "complete": complete,
        "stop_reason": stop_reason,
        "baseline_branch": baseline_branch(program),
        "best_branch": best_branch,
        "max_rounds": args.max_rounds,
        "max_failures": args.max_failures,
        "no_improvement_patience": args.no_improvement_patience,
        "min_improvement": args.min_improvement,
        "disable_error_feedback": args.disable_error_feedback,
        "disable_filtering": args.disable_filtering,
        "rounds": rounds,
    }
    out = state_path(program, args.method_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return state


def main() -> int:
    args = build_parser().parse_args()
    if args.max_rounds < 1:
        raise SystemExit("--max-rounds must be at least 1")

    programs = selected_programs(args)
    if not programs:
        raise SystemExit("No programs selected. Build prompt_round_1.txt first.")

    print(f"Selected {len(programs)} programs.")
    if args.dry_run:
        for program in programs:
            print(program)
        return 0

    states = []
    for index, program in enumerate(programs, start=1):
        print(f"\n=== {index}/{len(programs)} {program} ===")
        states.append(run_program(program, args))

    summary = {
        "program_count": len(states),
        "completed": sum(1 for state in states if state.get("complete")),
        "average_best_branch": round(
            sum(float(state.get("best_branch", 0.0)) for state in states) / len(states),
            2,
        ),
        "states": states,
    }
    suffix = "" if args.method_dir == DEFAULT_METHOD_DIR else f"_{args.method_dir}"
    out = ROOT / f"our_method_pipeline_summary{suffix}.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved pipeline summary to {out}")
    print(f"Average best branch coverage: {summary['average_best_branch']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
