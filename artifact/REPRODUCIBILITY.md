# Reproducibility Guide

This document records the high-level steps needed to reproduce the experiments. The commands are intentionally written without private API keys.

## 1. Environment

Recommended setup:

- Python 3.10 or compatible version for Pynguin/CodaMOSA experiments.
- `coverage`, `pytest`, and the packages listed in `tools/requirements.txt`.
- Scientific-computing dependencies such as `numpy`, `scipy`, `sympy`, and `matplotlib`.
- Docker for CodaMOSA, if reproducing the CodaMOSA baseline.
- CoverUp installed in a separate compatible Python environment, if reproducing the CoverUp baseline.

Install basic Python dependencies:

```bash
pip install -r tools/requirements.txt
```

## 2. Benchmark Layout

Each benchmark program is stored under:

```text
scientific_calculation/<program>/
```

The target module is normally:

```text
scientific_calculation/<program>/example.py
```

Package metadata is stored in:

```text
scientific_calculation/<program>/package.txt
```

The canonical program list is:

```text
tools/programs.json
```

## 3. Pynguin Baseline

Run Pynguin on one program:

```bash
python tools/run_pynguin.py --program <program_name>
```

Run Pynguin on all configured programs, if supported by the current script:

```bash
python tools/run_pynguin.py --all
```

Measure coverage:

```bash
python tools/coverage_measure.py --suite pynguin --program <program_name>
```

or:

```bash
python tools/coverage_measure.py --suite pynguin --all
```

## 4. Branch Analysis and Prompt Construction

Extract uncovered branches and analyze hard-to-cover targets:

```bash
python tools/extract_uncovered_branches.py --all
python tools/analyze_hard_branches.py --all
python tools/build_branch_prompts.py --all
```

Check `--help` for each script before rerunning, because some local scripts also support subset options such as `--new-only`.

## 5. SciCov / Our Method

Run the multi-round LLM-assisted pipeline:

```bash
python tools/run_our_method_pipeline.py --all --max-rounds 3 --max-failures 2 --temperature 0.0 --model gpt-4o
```

Run one program:

```bash
python tools/run_our_method_pipeline.py --program <program_name> --max-rounds 3 --temperature 0.0 --model gpt-4o
```

Important implementation behavior:

- Generated tests are executed before being accepted.
- Failing tests and tests that do not improve branch coverage are filtered.
- Coverage is re-measured after accepted tests are added.
- API keys must be supplied privately through environment variables or a local ignored config file.

## 6. CoverUp Baseline

Typical command:

```bash
python tools/run_coverup.py --all --timeout-min 10
```

For one program:

```bash
python tools/run_coverup.py --program <program_name> --timeout-min 10
```

The summarized results are stored in:

```text
coverup_summary_all_unified.csv
```

## 7. CodaMOSA Baseline

Typical command:

```bash
python tools/run_codamosa.py --all --budget 120 --skip-existing
```

For one program:

```bash
python tools/run_codamosa.py --program <program_name> --budget 120
```

CodaMOSA requires Docker and private LLM API settings. Do not commit API keys. The summarized results are stored in:

```text
codamosa_coverage_summary.csv
```

## 8. Summarization

After runs finish, regenerate summary tables:

```bash
python tools/summarize_all_results.py
python tools/summarize_our_method_results.py
python tools/summarize_codamosa_results.py
python tools/final_experiment_report.py
```

The final paper-facing summary is:

```text
final_summary.csv
```

## 9. Known Reproducibility Constraints

- Exact LLM outputs may vary across model versions and providers.
- The paper reports branch coverage as the primary metric.
- Missing or failed tool runs should be reported separately, not silently counted as successful runs.
- API cost and latency depend on provider pricing and availability.
- CodaMOSA and CoverUp may require environment-specific setup.
