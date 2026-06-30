"""Rerun CodaMOSA for programs that were previously run with a 600s budget.

The canonical CodaMOSA comparison budget for this project is 120 seconds.
This helper reads ``codamosa_budget600_programs.txt`` from the repository root
and reruns those programs through ``tools/run_codamosa.py`` without
``--skip-existing`` so the old 600s results are replaced by 120s results.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIST = ROOT / "codamosa_budget600_programs.txt"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rerun 600s CodaMOSA results with a 120s budget")
    parser.add_argument("--program-list", type=Path, default=DEFAULT_LIST)
    parser.add_argument("--budget", type=int, default=120)
    parser.add_argument("--start-at", help="Skip programs before this name")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--no-pull", action="store_true", default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def load_programs(path: Path) -> list[str]:
    if not path.is_file():
        raise SystemExit(f"Missing program list: {path}")
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    args = build_parser().parse_args()
    programs = load_programs(args.program_list)
    if args.start_at:
        if args.start_at not in programs:
            raise SystemExit(f"--start-at program not in list: {args.start_at}")
        programs = programs[programs.index(args.start_at) :]
    if args.limit > 0:
        programs = programs[: args.limit]

    print(f"Selected {len(programs)} programs for CodaMOSA rerun with budget={args.budget}s")
    failures: list[str] = []
    for index, program in enumerate(programs, start=1):
        command = [
            sys.executable,
            "tools/run_codamosa.py",
            "--program",
            program,
            "--budget",
            str(args.budget),
        ]
        if args.no_pull:
            command.append("--no-pull")
        print(f"\n=== {index}/{len(programs)} {program} ===")
        print(" ".join(command))
        if args.dry_run:
            continue
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode != 0:
            failures.append(program)
            print(f"[failed] {program}: rc={completed.returncode}")

    if failures:
        print("\nFailed programs:")
        for program in failures:
            print(program)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
