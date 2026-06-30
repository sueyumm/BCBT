"""Classify uncovered branches into hard-branch categories.

Input:
    uncovered_branches.json

Output:
    hard_branch_analysis.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from paths import ROOT

DEFAULT_IN = ROOT / "uncovered_branches.json"
DEFAULT_OUT = ROOT / "hard_branch_analysis.json"

CATEGORY_COMPLEX_DATA = "Complex Data Dependency"
CATEGORY_CROSS_FUNCTION = "Cross-Function / Cross-Module Dependency"
CATEGORY_LOOP_STATE = "Loop/Iteration State Dependency"
CATEGORY_GENERIC = "Generic / Other"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Classify uncovered branches")
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser


def _contains_any(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _count_function_calls(text: str) -> int:
    names = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", text)
    keywords = {"if", "for", "while", "return", "range", "len", "abs", "min", "max"}
    return len([name for name in names if name not in keywords])


CATEGORY_REASONS = {
    CATEGORY_COMPLEX_DATA: "The branch condition or nearby code depends on structured inputs such as arrays, matrices, lists, or dictionaries.",
    CATEGORY_CROSS_FUNCTION: "The branch appears to depend on values produced through function calls or object/module interactions.",
    CATEGORY_LOOP_STATE: "The branch depends on loop entry/exit behavior, convergence, or an iteration-related state.",
    CATEGORY_GENERIC: "The branch does not match the specialized hard-branch categories and can likely be targeted with a direct test.",
}

CATEGORY_PROMPT_HINTS = {
    CATEGORY_COMPLEX_DATA: "Provide concrete structured input examples with valid shapes and values.",
    CATEGORY_CROSS_FUNCTION: "Provide the relevant call-chain context and construct inputs through the same public functions.",
    CATEGORY_LOOP_STATE: "Provide initial values and loop-state constraints that force the target loop direction.",
    CATEGORY_GENERIC: "Generate a direct pytest test with concrete values for the branch condition.",
}


def choose_primary_category(categories: list[str]) -> str:
    priority = [
        CATEGORY_LOOP_STATE,
        CATEGORY_COMPLEX_DATA,
        CATEGORY_CROSS_FUNCTION,
        CATEGORY_GENERIC,
    ]
    for category in priority:
        if category in categories:
            return category
    return categories[0]


def classify_branch(branch: dict[str, Any]) -> tuple[str, list[str], str, list[str]]:
    condition = str(branch.get("condition", ""))
    snippet = str(branch.get("source_snippet", ""))
    direction = str(branch.get("direction", ""))
    combined = f"{condition}\n{snippet}"
    categories: list[str] = []

    loop_markers = [
        "loop_enter",
        "loop_exit",
        "while ",
        "for ",
        "iteration",
        "iter",
        "error",
        "residual",
        "converge",
        "tol",
        "epsilon",
        "eps",
        "1e-",
    ]
    if direction in {"loop_enter", "loop_exit"} or _contains_any(combined, loop_markers):
        categories.append(CATEGORY_LOOP_STATE)

    complex_markers = [
        "np.",
        "numpy",
        "array",
        "matrix",
        "shape",
        "reshape",
        "zeros",
        "ones",
        "dict",
        "list",
        "[",
        "]",
        ".append",
        ".keys",
        ".values",
    ]
    if _contains_any(combined, complex_markers):
        categories.append(CATEGORY_COMPLEX_DATA)

    cross_function_markers = [
        "return ",
        "module.",
        "self.",
    ]
    if _count_function_calls(snippet) >= 2 or _contains_any(combined, cross_function_markers):
        categories.append(CATEGORY_CROSS_FUNCTION)

    if not categories:
        categories.append(CATEGORY_GENERIC)

    category = choose_primary_category(categories)
    reason = " ".join(CATEGORY_REASONS[item] for item in categories)
    prompt_hints = [CATEGORY_PROMPT_HINTS[item] for item in categories]
    return category, categories, reason, prompt_hints


def analyze(input_path: Path) -> dict[str, Any]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    programs_out = []
    counts = {
        CATEGORY_COMPLEX_DATA: 0,
        CATEGORY_CROSS_FUNCTION: 0,
        CATEGORY_LOOP_STATE: 0,
        CATEGORY_GENERIC: 0,
    }

    for program in data.get("programs", []):
        branch_items = []
        for branch in program.get("branches", []):
            category, categories, reason, prompt_hints = classify_branch(branch)
            for item in categories:
                counts[item] += 1
            branch_items.append(
                {
                    "program": program.get("program", ""),
                    "line": branch.get("line", ""),
                    "target": branch.get("target", ""),
                    "direction": branch.get("direction", ""),
                    "condition": branch.get("condition", ""),
                    "function": branch.get("function", ""),
                    "class": branch.get("class", ""),
                    "context": branch.get("source_snippet", ""),
                    "category": category,
                    "categories": categories,
                    "reason": reason,
                    "prompt_hints": prompt_hints,
                    "prompt_hint": " ".join(prompt_hints),
                }
            )
        programs_out.append(
            {
                "program": program.get("program", ""),
                "status": program.get("status", ""),
                "branch_count": len(branch_items),
                "branches": branch_items,
            }
        )

    return {
        "source": str(input_path),
        "taxonomy": [
            CATEGORY_COMPLEX_DATA,
            CATEGORY_CROSS_FUNCTION,
            CATEGORY_LOOP_STATE,
            CATEGORY_GENERIC,
        ],
        "program_count": len(programs_out),
        "total_branches": sum(program.get("branch_count", 0) for program in programs_out),
        "category_counts": counts,
        "programs": programs_out,
    }


def main() -> int:
    args = build_parser().parse_args()
    result = analyze(args.input.resolve())
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Analyzed {result['total_branches']} uncovered branches.")
    for category, count in result["category_counts"].items():
        print(f"{category}: {count}")
    print(f"Saved hard branch analysis to {args.out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
