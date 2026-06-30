"""Summarize the official CodaMOSA result dataset without extracting it.

The ICSE'23 CodaMOSA dataset is distributed as an outer zip containing one zip
per benchmark.  Each inner zip contains repeated runs for several techniques,
with Pynguin statistics in ``statistics.csv``.  This helper builds a compact CSV
that is useful for comparing our local experiment setup with the official data.
"""

from __future__ import annotations

import argparse
import csv
import io
import statistics
import zipfile
from collections import defaultdict
from pathlib import Path


NUMERIC_FIELDS = (
    "Coverage",
    "BranchCoverage",
    "LineCoverage",
    "ParsedStatements",
    "UninterpStatements",
    "ParsableStatements",
    "LLMCalls",
    "LLMQueryTime",
    "LLMStageSavedTests",
)


def _float_or_none(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _read_statistics(entry: zipfile.ZipInfo, archive: zipfile.ZipFile) -> dict[str, str]:
    with archive.open(entry) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
        rows = list(csv.DictReader(text))
    if not rows:
        return {}
    return rows[0]


def summarize_dataset(zip_path: Path) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, float | str]]] = defaultdict(list)

    with zipfile.ZipFile(zip_path) as outer:
        inner_entries = [
            entry
            for entry in outer.infolist()
            if entry.filename.startswith("codamosa-dataset-main/final-exp/")
            and entry.filename.endswith(".zip")
        ]

        for inner_entry in inner_entries:
            benchmark = Path(inner_entry.filename).name.removesuffix(".zip")
            with outer.open(inner_entry) as fh:
                payload = io.BytesIO(fh.read())

            with zipfile.ZipFile(payload) as inner:
                for stat_entry in inner.infolist():
                    if not stat_entry.filename.endswith("/statistics.csv"):
                        continue
                    parts = stat_entry.filename.split("/")
                    if len(parts) < 3:
                        continue
                    technique = parts[0]
                    row = _read_statistics(stat_entry, inner)
                    if not row:
                        continue
                    record: dict[str, float | str] = {
                        "target_module": row.get("TargetModule", benchmark),
                    }
                    for field in NUMERIC_FIELDS:
                        value = _float_or_none(row.get(field))
                        if value is not None:
                            record[field] = value
                    grouped[(benchmark, technique)].append(record)

    summary: list[dict[str, object]] = []
    for (benchmark, technique), runs in sorted(grouped.items()):
        out: dict[str, object] = {
            "benchmark": benchmark,
            "technique": technique,
            "runs": len(runs),
            "target_module": runs[0].get("target_module", benchmark),
        }
        for field in NUMERIC_FIELDS:
            values = [run[field] for run in runs if field in run]
            if values:
                out[f"avg_{field}"] = statistics.fmean(values)
                out[f"max_{field}"] = max(values)
        summary.append(out)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, type=Path, help="Path to codamosa-dataset-main.zip")
    parser.add_argument(
        "--out",
        default=Path("codamosa_official_summary.csv"),
        type=Path,
        help="Output CSV path",
    )
    args = parser.parse_args()

    rows = summarize_dataset(args.zip)
    fields = [
        "benchmark",
        "technique",
        "runs",
        "target_module",
    ]
    for field in NUMERIC_FIELDS:
        fields.extend([f"avg_{field}", f"max_{field}"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    benchmarks = len({row["benchmark"] for row in rows})
    techniques = len({row["technique"] for row in rows})
    print(f"benchmarks={benchmarks}")
    print(f"techniques={techniques}")
    print(f"rows={len(rows)}")
    print(f"wrote={args.out}")


if __name__ == "__main__":
    main()
