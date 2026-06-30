"""Build first-round LLM prompts for uncovered branch targets.

Input:
    hard_branch_analysis.json

Output:
    scientific_calculation/<program>/our_method/prompts/prompt_round_1.txt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paths import ROOT, SCI_ROOT

DEFAULT_INPUT = ROOT / "hard_branch_analysis.json"
DEFAULT_MAX_BRANCHES = 6
DEFAULT_SOURCE_LIMIT = 12000
DEFAULT_TEST_LIMIT = 6000


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build LLM prompts for hard branch targets")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--program", help="Only build prompts for one program")
    parser.add_argument("--max-branches", type=int, default=DEFAULT_MAX_BRANCHES)
    parser.add_argument("--method-dir", default="our_method", help="Output method directory under each program")
    parser.add_argument(
        "--disable-category-prompts",
        action="store_true",
        help=(
            "Ablation mode: keep target branch locations and code context, "
            "but remove category labels, category-specific strategies, reasons, and prompt hints."
        ),
    )
    return parser


def read_limited(path: Path, limit: int) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n# ... truncated ...\n"


def pynguin_test_path(program: str) -> Path:
    candidates = [
        SCI_ROOT / program / "pynguin" / "result_4o" / "test_example.py",
        SCI_ROOT / program / "pynguin" / "result" / "test_example.py",
        SCI_ROOT / program / "result_4o" / "test_example.py",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


def format_branch(branch: dict[str, Any], index: int, include_categories: bool = True) -> str:
    categories = branch_categories(branch)
    lines = [
        f"Target branch {index}\n"
        f"- line: {branch.get('line', '')}\n"
        f"- target: {branch.get('target', '')}\n"
        f"- direction: {branch.get('direction', '')}\n"
        f"- condition: {branch.get('condition', '')}\n"
        f"- function: {branch.get('function', '')}\n"
    ]
    if include_categories:
        lines.extend(
            [
                f"- primary category: {branch.get('category', '')}\n",
                f"- categories: {', '.join(categories)}\n",
                f"- reason: {branch.get('reason', '')}\n",
                f"- prompt hint: {branch.get('prompt_hint', '')}\n",
            ]
        )
    lines.append(f"- context:\n{branch.get('context', '')}\n")
    return "".join(lines)


def branch_categories(branch: dict[str, Any]) -> list[str]:
    categories = branch.get("categories")
    if isinstance(categories, list):
        return [str(category).strip() for category in categories if str(category).strip()]
    category = str(branch.get("category", "")).strip()
    return [category] if category else []


def category_instruction_block(branches: list[dict[str, Any]]) -> str:
    categories = {category for branch in branches for category in branch_categories(branch)}
    blocks: list[str] = []

    if "Loop/Iteration State Dependency" in categories:
        blocks.append(
            """Loop/Iteration State Dependency strategy:
- Identify the loop guard and choose inputs that force the requested direction.
- For loop_enter targets, construct values that make the loop condition true on the first check.
- For loop_exit targets, construct values that make the loop condition false immediately or converge quickly.
- Pay special attention to tolerance variables, error thresholds, residuals, iteration counters, and maximum-iteration guards.
- Prefer small deterministic inputs so the test finishes quickly."""
        )

    if "Complex Data Dependency" in categories:
        blocks.append(
            """Complex Data Dependency strategy:
- Construct concrete valid arrays, matrices, lists, dictionaries, or object states needed by the target branch.
- Match the expected shape, dtype, and dimensionality used by the source code.
- Include boundary structures when relevant, such as empty collections, singleton arrays, square matrices, singular matrices, or non-square matrices.
- Avoid unrealistic placeholder values such as None or arbitrary strings unless the target branch explicitly handles them.
- Assert stable properties such as shape, finite values, equality to a known small result, or raised exceptions."""
        )

    if "Cross-Function / Cross-Module Dependency" in categories:
        blocks.append(
            """Cross-Function / Cross-Module Dependency strategy:
- Do not only test the final branch in isolation if it depends on intermediate results.
- Use the public functions in the call chain to build realistic intermediate values.
- If a helper function transforms inputs before the branch, call that helper or reproduce its expected output carefully.
- Assert both the final behavior and a stable intermediate property when possible.
- Keep the test focused on the target branch rather than broad end-to-end behavior."""
        )

    if "Generic / Other" in categories:
        blocks.append(
            """Generic / Other strategy:
- Construct the smallest concrete input that makes the target condition take the missing direction.
- Cover both true and false directions when both are listed.
- Prefer direct assertions on return values, raised exceptions, or simple state changes."""
        )

    if not blocks:
        return "No category-specific strategies were detected for the selected branches."
    return "\n\n".join(blocks)


def build_prompt(
    program: str,
    branches: list[dict[str, Any]],
    max_branches: int,
    include_categories: bool = True,
) -> str:
    source_path = SCI_ROOT / program / "example.py"
    baseline_path = pynguin_test_path(program)
    source = read_limited(source_path, DEFAULT_SOURCE_LIMIT)
    baseline_tests = read_limited(baseline_path, DEFAULT_TEST_LIMIT)

    selected_branches = branches[:max_branches]
    branch_text = "\n".join(
        format_branch(branch, idx + 1, include_categories=include_categories)
        for idx, branch in enumerate(selected_branches)
    )
    category_instructions = (
        category_instruction_block(selected_branches)
        if include_categories
        else (
            "Category-specific branch strategies are intentionally disabled for this ablation. "
            "Use only the target branch location, condition, and code context."
        )
    )

    return f"""You are generating additional pytest tests for a scientific-computing Python program.

Primary objective:
Prioritize covering the listed target branches, while maximizing the overall branch coverage of example.py.

Rules:
- Do not modify example.py.
- Generate only Python pytest code.
- Do not include explanations or markdown fences.
- Import the target module as: import example as module_0
- Add new tests only; do not rewrite the Pynguin baseline tests.
- Prefer deterministic inputs.
- Avoid tests that depend on random outcomes.
- For floating point assertions, use pytest.approx or a reasonable tolerance.
- Every generated test must call at least one target function and include at least one assert.

Program: {program}

Category-specific generation strategy:
{category_instructions}

Target branches:
{branch_text}

Source code of example.py:
```python
{source}
```

Existing Pynguin baseline tests:
```python
{baseline_tests}
```

Output only a complete Python pytest test file.
"""


def load_programs(input_path: Path, selected_program: str | None) -> list[dict[str, Any]]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    programs = data.get("programs", [])
    if selected_program:
        programs = [program for program in programs if program.get("program") == selected_program]
    return programs


def main() -> int:
    args = build_parser().parse_args()
    programs = load_programs(args.input.resolve(), args.program)
    written = 0
    for item in programs:
        program = item.get("program", "")
        branches = item.get("branches", [])
        if not program or not branches:
            continue
        prompt = build_prompt(
            program,
            branches,
            args.max_branches,
            include_categories=not args.disable_category_prompts,
        )
        out_dir = SCI_ROOT / program / args.method_dir / "prompts"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "prompt_round_1.txt"
        out_file.write_text(prompt, encoding="utf-8")
        written += 1

    print(f"Wrote {written} prompt files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
