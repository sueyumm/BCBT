"""Build next-round prompts from failed proposed-method evaluations.

Input:
    scientific_calculation/<program>/<method_dir>/prompts/prompt_round_<N>.txt
    scientific_calculation/<program>/<method_dir>/round_<N>/generated_tests_round_<N>.py
    scientific_calculation/<program>/<method_dir>/round_<N>/pytest_round_<N>.log
    scientific_calculation/<program>/<method_dir>/round_<N>/evaluation_round_<N>.json

Output:
    scientific_calculation/<program>/<method_dir>/prompts/prompt_round_<N+1>.txt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import SCI_ROOT, load_new_program_names

DEFAULT_LOG_LIMIT = 9000
DEFAULT_TEST_LIMIT = 9000
DEFAULT_METHOD_DIR = "our_method"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build feedback prompts for failed generated tests")
    parser.add_argument("--from-round", type=int, default=1)
    parser.add_argument("--program", help="Only build feedback prompt for one program")
    parser.add_argument("--new-only", action="store_true", help="Only build prompts for newly added programs")
    parser.add_argument(
        "--method-dir",
        default=DEFAULT_METHOD_DIR,
        help="Per-program output directory for this method variant.",
    )
    parser.add_argument("--log-limit", type=int, default=DEFAULT_LOG_LIMIT)
    parser.add_argument("--test-limit", type=int, default=DEFAULT_TEST_LIMIT)
    return parser


def read_limited(path: Path, limit: int) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n# ... truncated ...\n"


def round_dir(program: str, round_no: int, method_dir: str) -> Path:
    return SCI_ROOT / program / method_dir / f"round_{round_no}"


def prompt_path(program: str, round_no: int, method_dir: str) -> Path:
    preferred = SCI_ROOT / program / method_dir / "prompts" / f"prompt_round_{round_no}.txt"
    if preferred.is_file():
        return preferred
    if method_dir != DEFAULT_METHOD_DIR:
        fallback = SCI_ROOT / program / DEFAULT_METHOD_DIR / "prompts" / f"prompt_round_{round_no}.txt"
        if fallback.is_file():
            return fallback
    return preferred


def evaluation_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"evaluation_round_{round_no}.json"


def generated_test_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"generated_tests_round_{round_no}.py"


def pytest_log_path(program: str, round_no: int, method_dir: str) -> Path:
    return round_dir(program, round_no, method_dir) / f"pytest_round_{round_no}.log"


def discover_failed_programs(round_no: int, selected_program: str | None, *, method_dir: str, new_only: bool) -> list[str]:
    allowed = set(load_new_program_names()) if new_only else None
    programs: list[str] = []
    for program_dir in sorted(p for p in SCI_ROOT.iterdir() if p.is_dir()):
        program = program_dir.name
        if selected_program and program != selected_program:
            continue
        if allowed is not None and program not in allowed:
            continue
        path = evaluation_path(program, round_no, method_dir)
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("returncode") != 0:
            programs.append(program)
    return programs


def build_feedback_prompt(program: str, round_no: int, method_dir: str, log_limit: int, test_limit: int) -> str:
    original_prompt = read_limited(prompt_path(program, round_no, method_dir), 20000)
    generated_tests = read_limited(generated_test_path(program, round_no, method_dir), test_limit)
    pytest_log = read_limited(pytest_log_path(program, round_no, method_dir), log_limit)
    next_round = round_no + 1

    return f"""You are revising failed pytest tests for a scientific-computing Python program.

Primary objective:
Produce a corrected pytest test file that improves branch coverage and passes pytest.

Strict output rules:
- Output only raw Python code.
- Do not include explanations or markdown fences.
- Include every required import explicitly, including pytest if pytest.approx is used.
- Import the target module as: import example as module_0
- Do not modify example.py.
- Keep tests deterministic.
- Do not assert overly strict floating-point values unless they are mathematically stable.
- Prefer assertions about shape, type, finite values, monotonic properties, or pytest.approx with tolerance.
- Every test must call at least one target function and include at least one assert.
- Do not repeat the exact same failing assertions from the previous round.

Program: {program}
Revision round: {next_round}

Original branch-targeting prompt:
{original_prompt}

Previous generated tests that failed:
```python
{generated_tests}
```

Pytest failure log:
```text
{pytest_log}
```

Output only the corrected complete Python pytest test file for round {next_round}.
"""


def main() -> int:
    args = build_parser().parse_args()
    failed_programs = discover_failed_programs(
        args.from_round,
        args.program,
        method_dir=args.method_dir,
        new_only=args.new_only,
    )
    written = 0
    for program in failed_programs:
        prompt = build_feedback_prompt(program, args.from_round, args.method_dir, args.log_limit, args.test_limit)
        out_path = SCI_ROOT / program / args.method_dir / "prompts" / f"prompt_round_{args.from_round + 1}.txt"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt, encoding="utf-8")
        written += 1

    print(f"Wrote {written} feedback prompt files for round {args.from_round + 1}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
