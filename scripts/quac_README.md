# QuAC scripts

QuAC = **Question Answering in Context** (`allenai/quac`). Each row is a *dialogue* containing lists of questions, answers, etc.

## Note on `datasets` version

`allenai/quac` uses a dataset loading script on Hugging Face. Some newer `datasets` versions reject script-based datasets.

These scripts are intended to run with a pinned, known-working `datasets` version via `uv`:

```bash
--with 'datasets==2.19.1'
```

## Download

```bash
cd Projects/v2g

~/.openclaw/workspace/bin/uv run --no-project \
  --with 'datasets==2.19.1' --with pyarrow --with pandas \
  -- python3 scripts/quac_download.py --out-dir datasets/raw
```

Outputs (ignored by git):
- `datasets/raw/quac/<split>/hf_datasets/`
- `datasets/raw/quac/<split>/data.jsonl`

## Exploration report

```bash
cd Projects/v2g

~/.openclaw/workspace/bin/uv run --no-project \
  --with 'datasets==2.19.1' --with pyarrow --with pandas \
  -- python3 scripts/quac_eda.py --out datasets/reports/quac_exploration.md --examples 2 --turns 3
```
