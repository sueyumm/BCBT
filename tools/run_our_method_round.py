"""Run one LLM generation round for the proposed branch-targeted method.

Inputs:
    scientific_calculation/<program>/<method_dir>/prompts/prompt_round_<N>.txt
    or fallback scientific_calculation/<program>/our_method/prompts/prompt_round_<N>.txt
    tools/local_api_config.json

Outputs:
    scientific_calculation/<program>/<method_dir>/round_<N>/generated_tests_round_<N>.py
    scientific_calculation/<program>/<method_dir>/round_<N>/llm_response_round_<N>.json
    scientific_calculation/<program>/<method_dir>/round_<N>/our_method_run.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from paths import SCI_ROOT, load_new_program_names

TOOLS_ROOT = Path(__file__).resolve().parent
LOCAL_API_CONFIG = TOOLS_ROOT / "local_api_config.json"

DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 1600
DEFAULT_TIMEOUT = 60
DEFAULT_RETRIES = 2
DEFAULT_METHOD_DIR = "our_method"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate branch-targeted pytest tests with an LLM")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--program", help="Only run one program")
    group.add_argument("--all", action="store_true", help="Run all programs that have a prompt file")
    group.add_argument("--new-only", action="store_true", help="Run only newly added programs that have a prompt file")
    parser.add_argument("--round", type=int, default=1, help="Prompt/generation round number")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--method-dir",
        default=DEFAULT_METHOD_DIR,
        help="Per-program output directory for this method variant.",
    )
    return parser


def load_api_config() -> dict[str, str]:
    if not LOCAL_API_CONFIG.is_file():
        raise SystemExit(f"Missing API config: {LOCAL_API_CONFIG}")
    data = json.loads(LOCAL_API_CONFIG.read_text(encoding="utf-8"))
    api_key = str(data.get("openai_api_key", "")).strip()
    base_url = str(data.get("openai_base_url", "")).strip().rstrip("/")
    if not api_key:
        raise SystemExit(f"Missing openai_api_key in {LOCAL_API_CONFIG}")
    if not base_url:
        raise SystemExit(f"Missing openai_base_url in {LOCAL_API_CONFIG}")
    return {"api_key": api_key, "url": f"{base_url}/v1/chat/completions"}


def prompt_path(program: str, round_no: int, method_dir: str) -> Path:
    preferred = SCI_ROOT / program / method_dir / "prompts" / f"prompt_round_{round_no}.txt"
    if preferred.is_file():
        return preferred
    if method_dir != DEFAULT_METHOD_DIR:
        fallback = SCI_ROOT / program / DEFAULT_METHOD_DIR / "prompts" / f"prompt_round_{round_no}.txt"
        if fallback.is_file():
            return fallback
    return preferred


def output_dir(program: str, round_no: int, method_dir: str) -> Path:
    return SCI_ROOT / program / method_dir / f"round_{round_no}"


def discover_programs(round_no: int, method_dir: str) -> list[str]:
    programs: list[str] = []
    for program_dir in sorted(p for p in SCI_ROOT.iterdir() if p.is_dir()):
        if prompt_path(program_dir.name, round_no, method_dir).is_file():
            programs.append(program_dir.name)
    return programs


def extract_code(content: str) -> str:
    """Extract usable Python from a chat response and tolerate common GPT-4o shapes."""
    match = re.search(r"```(?:python|py)?\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1)

    lines = content.strip().splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "def test_")):
            content = "\n".join(lines[index:])
            break

    content = normalize_generated_code(content.strip())
    content = repair_missing_imports(content)
    if not content.endswith("\n"):
        content += "\n"
    return content


def repair_missing_imports(code: str) -> str:
    imports: list[str] = []
    if re.search(r"\bpytest\.", code) and not re.search(r"^\s*(import pytest|from pytest import)", code, re.MULTILINE):
        imports.append("import pytest")
    if re.search(r"\bnp\.", code) and not re.search(r"^\s*import numpy as np", code, re.MULTILINE):
        imports.append("import numpy as np")
    if re.search(r"\bsp\.", code) and not re.search(r"^\s*import sympy as sp", code, re.MULTILINE):
        imports.append("import sympy as sp")
    if not imports:
        return code
    return "\n".join(imports) + "\n" + code


def normalize_generated_code(code: str) -> str:
    """Expand one-line test functions such as ``def test_x():assert ...``."""
    normalized_lines: list[str] = []
    for line in code.splitlines():
        match = re.match(r"^(\s*def\s+test_\w+\s*\([^)]*\)\s*:\s*)(\S.*)$", line)
        if not match:
            normalized_lines.append(line)
            continue
        header = match.group(1).rstrip()
        body = match.group(2).strip()
        normalized_lines.append(header)
        normalized_lines.append(f"    {body}")
    return "\n".join(normalized_lines)


def call_llm(
    *,
    url: str,
    api_key: str,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    timeout: int,
) -> tuple[int, dict[str, Any] | None, str]:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Python pytest test generator. Output only raw Python code. "
                    "No markdown, no explanations, no prose."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
            return response.status, json.loads(text), text
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        return exc.code, parsed, text
    except Exception as exc:
        return 0, None, repr(exc)


def run_one(program: str, args: argparse.Namespace, api: dict[str, str]) -> dict[str, Any]:
    prompt_file = prompt_path(program, args.round, args.method_dir)
    if not prompt_file.is_file():
        return {"program": program, "status": "skipped", "reason": "missing prompt"}

    out_dir = output_dir(program, args.round, args.method_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    response_file = out_dir / f"llm_response_round_{args.round}.json"
    tests_file = out_dir / f"generated_tests_round_{args.round}.py"
    run_file = out_dir / "our_method_run.json"
    if tests_file.exists():
        tests_file.unlink()

    prompt = prompt_file.read_text(encoding="utf-8", errors="replace")
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    t0 = time.time()
    final_status = 0
    parsed: dict[str, Any] | None = None
    raw_text = ""

    for attempt in range(args.retries + 1):
        final_status, parsed, raw_text = call_llm(
            url=api["url"],
            api_key=api["api_key"],
            prompt=prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        if final_status == 200 and parsed:
            break
        if attempt < args.retries:
            time.sleep(2 + attempt)

    elapsed = time.time() - t0
    response_payload: dict[str, Any] = parsed if parsed is not None else {"raw": raw_text}
    response_file.write_text(json.dumps(response_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    content = ""
    if final_status == 200 and parsed:
        try:
            content = str(parsed["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError):
            content = ""

    code = extract_code(content) if content else ""
    if code:
        tests_file.write_text(code, encoding="utf-8")

    metadata = {
        "program": program,
        "round": args.round,
        "model": args.model,
        "method_dir": args.method_dir,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "timeout": args.timeout,
        "status_code": final_status,
        "started_utc": started,
        "elapsed_seconds": round(elapsed, 3),
        "prompt": str(prompt_file),
        "response": str(response_file),
        "generated_tests": str(tests_file) if code else "",
        "generated_chars": len(code),
    }
    run_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return metadata


def main() -> int:
    args = build_parser().parse_args()
    api = load_api_config()
    if args.program:
        programs = [args.program]
    elif args.new_only:
        new_programs = set(load_new_program_names())
        programs = [program for program in discover_programs(args.round, args.method_dir) if program in new_programs]
    else:
        programs = discover_programs(args.round, args.method_dir)

    if not programs:
        raise SystemExit(f"No prompt files found for round {args.round}.")

    ok = 0
    failed = 0
    for program in programs:
        result = run_one(program, args, api)
        status = result.get("status_code")
        chars = result.get("generated_chars", 0)
        if status == 200 and chars:
            ok += 1
            print(f"[ok] {program}: {chars} chars")
        else:
            failed += 1
            print(f"[failed] {program}: status={status}, chars={chars}")

    print(f"Generated tests for {ok} programs; failed/skipped {failed}.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
