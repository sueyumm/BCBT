# SciCov Artifact

This repository contains the implementation scripts, benchmark programs, and experimental result data for the paper:

> SciCov: Improving Branch Coverage of Scientific Computing Programs with Large Language Models

SciCov is an LLM-assisted test generation approach for improving branch coverage on scientific computing programs. It starts from a Pynguin baseline, identifies uncovered branch targets, builds branch-aware prompts, executes generated tests, filters ineffective or failing tests, and re-measures branch coverage.

## Artifact Contents

The artifact is organized around four types of material.

| Type | Location | Description |
|---|---|---|
| Experiment scripts | `tools/` | Scripts for Pynguin, CoverUp, CodaMOSA, SciCov-style prompting, filtering, coverage measurement, and result summarization. |
| Benchmark programs | `scientific_calculation/<program>/example.py` and `package.txt` | Scientific-computing target programs and package metadata. |
| Summary results | Root-level `*.csv` and selected `*.json` files | Program-level branch coverage, baseline comparisons, ablation summaries, model sensitivity, target-branch category coverage, and failure summaries. |
| CodaMOSA raw result folders | `scientific_calculation/<program>/codamosa/result_4o/` | Per-program CodaMOSA outputs such as `statistics.csv`, generated tests, timelines, and run metadata. Logs containing private API keys are excluded. |
| Reproducibility guide | `artifact/REPRODUCIBILITY.md` | Commands and environment notes for reproducing the experiments without exposing private API keys. |

## Main Result Files

The most useful result files for checking the paper tables and figures are:

- `final_summary.csv`: program-level comparison among Pynguin, CoverUp, CodaMOSA, and SciCov.
- `effective104_comparison_table.csv`: compact method/model comparison on the effective 104-program subset.
- `ablation_effective104_summary.csv`: ablation-study summary.
- `target_branch_category_coverage_table.csv`: target-branch category coverage by method.
- `target_branch_level_coverage_raw.csv`: raw target-branch-level coverage data.
- `model_comparison_direct_vs_ours_program_level.csv`: program-level model-sensitivity comparison.
- `tool_failure_summary.csv`: summarized failure cases for baseline tools.
- `codamosa_coverage_summary.csv` and `coverup_summary_all_unified.csv`: baseline result summaries.

See `artifact/DATA_MANIFEST.csv` for a compact data index.

## Important Safety Note

Do not commit or publish private API configuration files. In this repository, `tools/local_api_config.json` is local-only and must remain ignored. Use environment variables or a private local config file when rerunning LLM-based experiments.

Some raw CodaMOSA `codamosa.log` files contain command lines with private authorization keys. They are intentionally excluded from the public artifact. The public CodaMOSA folders keep the result data needed for inspection, including statistics, generated tests, and run summaries.

## Recommended Citation

If this artifact is used, cite the accompanying paper once it is accepted/published. Until then, refer to the paper title above and the commit hash of the artifact repository.
