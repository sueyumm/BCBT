# SciCov Artifact Repository

This repository contains code, benchmark programs, and experimental result data for:

> SciCov: Improving Branch Coverage of Scientific Computing Programs with Large Language Models

SciCov uses LLM-assisted, branch-aware, feedback-guided test generation to improve branch coverage for scientific computing programs. It starts from Pynguin-generated baseline tests, identifies residual uncovered branches, builds target-aware prompts, executes generated tests, filters failing or non-improving tests, and re-measures coverage.

## Quick Links

- Artifact overview: [`artifact/README.md`](artifact/README.md)
- Reproducibility guide: [`artifact/REPRODUCIBILITY.md`](artifact/REPRODUCIBILITY.md)
- Data manifest: [`artifact/DATA_MANIFEST.csv`](artifact/DATA_MANIFEST.csv)
- Publishing checklist: [`artifact/PUBLISH_CHECKLIST.md`](artifact/PUBLISH_CHECKLIST.md)

## Main Directories

- `tools/`: experiment scripts for baseline generation, coverage measurement, branch analysis, LLM-assisted test generation, filtering, and summarization.
- `scientific_calculation/`: benchmark programs and per-program metadata.
- `paper_figures/`: figure source data and generated paper figures.
- `artifact/`: public-facing documentation for reproducing and checking the artifact.

## Main Result Files

- `final_summary.csv`
- `effective104_comparison_table.csv`
- `ablation_effective104_summary.csv`
- `target_branch_category_coverage_table.csv`
- `target_branch_level_coverage_raw.csv`
- `model_comparison_direct_vs_ours_program_level.csv`
- `tool_failure_summary.csv`
- `codamosa_coverage_summary.csv`
- `coverup_summary_all_unified.csv`

## Private Configuration

Do not commit private API keys. The local file `tools/local_api_config.json` is intentionally ignored. Use environment variables or a private local config file when rerunning LLM-based experiments.
