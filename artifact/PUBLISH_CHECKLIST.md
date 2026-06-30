# GitHub Publishing Checklist

Use this checklist before making the repository public or pushing an artifact branch.

## Must Include

- [ ] `tools/` scripts needed to run baselines, SciCov-style generation, filtering, coverage measurement, and summarization.
- [ ] `scientific_calculation/<program>/example.py` benchmark programs.
- [ ] `scientific_calculation/<program>/package.txt` package metadata.
- [ ] Root-level result summaries listed in `artifact/DATA_MANIFEST.csv`.
- [ ] Sanitized CodaMOSA result folders, excluding `codamosa.log` and `.coverage*` files.
- [ ] `artifact/README.md` and `artifact/REPRODUCIBILITY.md`.
- [ ] A license file, if the artifact is intended for public reuse.

## Must Not Include

- [ ] `tools/local_api_config.json`.
- [ ] Any `.env` file or file containing API keys.
- [ ] Real authorization headers or bearer tokens.
- [ ] Raw `codamosa.log` files, because they may contain private authorization keys.
- [ ] Private manuscript drafts, reviewer notes, or unpublished unrelated Word documents.
- [ ] Large temporary extracted PDFs/images unrelated to the artifact.
- [ ] Local IDE metadata such as `.idea/`.
- [ ] Literature-download folders such as `_icse2027_testing_papers/`.

## Before Push

Run:

```bash
git status --short
git check-ignore -v tools/local_api_config.json
git ls-files | grep -i "local_api\\|\\.env\\|secret\\|token\\|password"
```

Also run a secret scan. If any real key was ever committed, rotate the key before publishing.

## Suggested GitHub Layout

For a clean artifact repository, the public-facing layout should be:

```text
README.md
LICENSE
artifact/
tools/
scientific_calculation/
paper_figures/*_source.csv
*.csv / selected *.json result summaries
```

Large raw per-run logs can be placed in a GitHub Release or Zenodo archive and linked from the README.
