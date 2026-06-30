"""Run a direct LLM baseline on the fixed effective program set.

Direct LLM baseline:
    - Give the model only the source code of example.py and optional generic pytest rules.
    - Do not include uncovered branch targets.
    - Do not include branch-category hints.
    - Do not include Pynguin baseline tests in the prompt.
    - Generate once, then evaluate/filter generated tests with the same harness.

Outputs are written to:
    scientific_calculation/<program>/<method_dir>/round_1/
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from paths import ROOT, SCI_ROOT

DEFAULT_TIMEOUT = 60
DEFAULT_EVAL_TIMEOUT = 180
DEFAULT_MAX_TOKENS = 1600
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run direct LLM baseline")
    parser.add_argument("--program", help="Only run one program")
    parser.add_argument(
        "--effective-from-summary",
        action="store_true",
        help="Run programs marked scope=effective and entered_our_method=True in final_summary.csv",
    )
    parser.add_argument("--method-dir", default="direct_llm_gpt4o")
    parser.add_argument(
        "--prompt-style",
        choices=["strong", "naive", "ablated_ours"],
        default="strong",
        help=(
            "strong keeps explicit branch/edge-case rules; naive is minimal; "
            "ablated_ours keeps our method's test-generation constraints but removes "
            "target branches, categories, Pynguin baseline tests, and feedback"
        ),
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--eval-timeout", type=int, default=DEFAULT_EVAL_TIMEOUT)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument(
        "--llm-only",
        action="store_true",
        help=(
            "Evaluate only the LLM-generated tests. By default this script keeps "
            "the previous behavior and evaluates generated tests together with "
            "the Pynguin baseline."
        ),
    )
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def load_effective_programs_from_summary(path: Path) -> list[str]:
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


def read_limited(path: Path, limit: int = 18000) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n# ... truncated ...\n"


def prompt_path(program: str, method_dir: str) -> Path:
    return SCI_ROOT / program / method_dir / "prompts" / "prompt_round_1.txt"


def state_path(program: str, method_dir: str) -> Path:
    return SCI_ROOT / program / method_dir / "direct_llm_state.json"


def completed(program: str, method_dir: str) -> bool:
    path = state_path(program, method_dir)
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return data.get("complete") is True


def build_direct_prompt(program: str) -> str:
    source = read_limited(SCI_ROOT / program / "example.py")
    return f"""You are generating pytest tests for a scientific-computing Python module.

Task:
Write a complete pytest test file for the source code below.

Rules:
- Output only raw Python code.
- Do not include explanations or markdown fences.
- Import the target module as: import example as module_0
- Include every required import explicitly.
- Do not modify example.py.
- Keep tests deterministic.
- Avoid tests that depend on random outcomes.
- For floating point assertions, use pytest.approx or a reasonable tolerance.
- Every test must call at least one target function and include at least one assert.
- Prefer meaningful tests that exercise different branches and edge cases.

Source code of example.py:
```python
{source}
```

Output only a complete Python pytest test file.
"""


def build_naive_prompt(program: str) -> str:
    source = read_limited(SCI_ROOT / program / "example.py")
    return f"""Write pytest tests for the following Python code.

```python
{source}
```
"""


def build_ablated_ours_prompt(program: str) -> str:
    source = read_limited(SCI_ROOT / program / "example.py")
    return f"""You are generating pytest tests for a scientific-computing Python program.

Primary objective:
Generate tests that improve branch coverage for the program.

Rules:
- Do not modify example.py.
- Generate only Python pytest code.
- Do not include explanations or markdown fences.
- Import the target module as: import example as module_0
- Include every required import explicitly.
- Prefer deterministic inputs.
- Avoid tests that depend on random outcomes.
- For floating point assertions, use pytest.approx or a reasonable tolerance.
- Every generated test must call at least one target function and include at least one assert.
- Construct concrete valid inputs for scientific-computing code, such as arrays, matrices, numeric boundary values, or small deterministic problem instances when appropriate.

Program: {program}

Source code of example.py:
```python
{source}
```

Output only a complete Python pytest test file.
"""


def ensure_prompt(program: str, method_dir: str, prompt_style: str) -> Path:
    path = prompt_path(program, method_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    if prompt_style == "naive":
        prompt = build_naive_prompt(program)
    elif prompt_style == "ablated_ours":
        prompt = build_ablated_ours_prompt(program)
    else:
        prompt = build_direct_prompt(program)
    path.write_text(prompt, encoding="utf-8")
    return path


def run_command(command: list[str]) -> tuple[int, str]:
    completed_process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return completed_process.returncode, (completed_process.stdout or "") + (completed_process.stderr or "")


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


def result_evaluation(program: str, method_dir: str) -> dict[str, Any]:
    out_dir = SCI_ROOT / program / method_dir / "round_1"
    filtered = read_json(out_dir / "filtered_evaluation_round_1.json")
    raw = read_json(out_dir / "evaluation_round_1.json")
    if numeric(filtered.get("branch_coverage")) is not None:
        filtered["result_source"] = "filtered"
        return filtered
    if numeric(raw.get("branch_coverage")) is not None:
        raw["result_source"] = "raw"
        return raw
    return {"program": program, "round": 1, "result_source": "missing"}


def run_one(program: str, args: argparse.Namespace) -> dict[str, Any]:
    ensure_prompt(program, args.method_dir, args.prompt_style)

    gen_code, gen_output = run_command(
        [
            sys.executable,
            "tools/run_our_method_round.py",
            "--program",
            program,
            "--round",
            "1",
            "--method-dir",
            args.method_dir,
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
        ]
    )
    eval_command = [
        sys.executable,
        "tools/evaluate_our_method_round.py",
        "--program",
        program,
        "--round",
        "1",
        "--method-dir",
        args.method_dir,
        "--timeout",
        str(args.eval_timeout),
    ]
    filter_command = [
        sys.executable,
        "tools/filter_our_method_tests.py",
        "--program",
        program,
        "--round",
        "1",
        "--method-dir",
        args.method_dir,
        "--timeout",
        str(args.eval_timeout),
    ]
    if not args.llm_only:
        eval_command.append("--include-pynguin-baseline")
        filter_command.append("--include-pynguin-baseline")

    eval_code, eval_output = run_command(eval_command)
    filter_code, filter_output = run_command(filter_command)

    run_meta = read_json(SCI_ROOT / program / args.method_dir / "round_1" / "our_method_run.json")
    evaluation = result_evaluation(program, args.method_dir)
    state = {
        "program": program,
        "method_dir": args.method_dir,
        "model": args.model,
        "prompt_style": args.prompt_style,
        "llm_only": args.llm_only,
        "include_pynguin_baseline": not args.llm_only,
        "complete": True,
        "generation_returncode": gen_code,
        "evaluation_returncode": eval_code,
        "filter_returncode": filter_code,
        "llm_status_code": run_meta.get("status_code"),
        "generated_chars": run_meta.get("generated_chars"),
        "branch": numeric(evaluation.get("branch_coverage")),
        "line": numeric(evaluation.get("line_coverage")),
        "result_source": evaluation.get("result_source"),
        "generation_output_tail": gen_output[-1200:],
        "evaluation_output_tail": eval_output[-1200:],
        "filter_output_tail": filter_output[-1200:],
    }
    state_path(program, args.method_dir).write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return state


def selected_programs(args: argparse.Namespace) -> list[str]:
    if args.program:
        programs = [args.program]
    elif args.effective_from_summary:
        programs = load_effective_programs_from_summary(ROOT / "final_summary.csv")
    else:
        raise SystemExit("Use --program or --effective-from-summary")

    if args.skip_existing:
        programs = [program for program in programs if not completed(program, args.method_dir)]
    if args.limit > 0:
        programs = programs[: args.limit]
    return programs


def main() -> int:
    args = build_parser().parse_args()
    programs = selected_programs(args)
    print(f"Selected {len(programs)} programs.")
    if args.dry_run:
        for program in programs:
            print(program)
        return 0

    states: list[dict[str, Any]] = []
    for index, program in enumerate(programs, start=1):
        print(f"\n=== {index}/{len(programs)} {program} ===")
        state = run_one(program, args)
        states.append(state)
        print(
            f"[{program}] branch={state.get('branch')} "
            f"status={state.get('llm_status_code')} chars={state.get('generated_chars')}"
        )

    numeric_branches = [float(state["branch"]) for state in states if state.get("branch") is not None]
    summary = {
        "program_count": len(states),
        "numeric_programs": len(numeric_branches),
        "average_branch": round(sum(numeric_branches) / len(numeric_branches), 2) if numeric_branches else "",
        "states": states,
    }
    out = ROOT / f"direct_llm_summary_{args.method_dir}.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved direct LLM summary to {out}")
    print(f"Average branch coverage: {summary['average_branch']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
