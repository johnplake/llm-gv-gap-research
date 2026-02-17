# QASC + ASQA scripts

These scripts download and inspect two datasets that have **multiple candidate answers / multiple reference answers** structures:

- **QASC** (`allenai/qasc`): 8-way multiple-choice candidate answers per question.
- **ASQA** (`din0s/asqa`): ambiguous question with multiple disambiguations (`qa_pairs`) + long-form answers (`annotations`).

## Why `uv run --no-project`

This repo has a top-level `datasets/` directory, which can shadow the Hugging Face `datasets` Python package when running from the repo root.

So these scripts are designed to be run with `uv run --no-project --with datasets ...` which:
- installs dependencies ephemerally, and
- ensures we import the correct `datasets` package.

## Download

```bash
cd Projects/v2g

~/.openclaw/workspace/bin/uv run --no-project \
  --with datasets --with pyarrow --with pandas \
  -- python3 scripts/qasc_asqa_download.py --out-dir datasets/raw
```

Outputs:
- `datasets/raw/qasc/<split>/hf_datasets/` (+ JSONL)
- `datasets/raw/asqa/<split>/hf_datasets/` (+ JSONL)

## Exploration report

```bash
cd Projects/v2g

~/.openclaw/workspace/bin/uv run --no-project \
  --with datasets --with pyarrow --with pandas \
  -- python3 scripts/qasc_asqa_eda.py --out datasets/reports/qasc_asqa_exploration.md --examples 3
```
