# NND plots + filtering grid (POS>=N1, NEG>=N2)

This note describes how to reproduce the distribution plots and the **(N1,N2) filtering grid** for NND sub-datasets.

## Python environment
The base system Python has no pip, so plotting deps are installed in a uv-managed venv:

- venv: `~/.openclaw/workspace/.uv/venvs/v2g-plot/`
- packages: numpy, pandas, matplotlib, seaborn

## Script
- `Projects/v2g/scripts/nnd_plots.py`

## Run
```bash
~/.openclaw/workspace/.uv/venvs/v2g-plot/bin/python \
  ~/.openclaw/workspace/Projects/v2g/scripts/nnd_plots.py \
  --nnd-data ~/.openclaw/workspace/Projects/v2g/datasets/candidates/nnd_data \
  --out ~/.openclaw/workspace/Projects/v2g/figures/nnd \
  --write-csv ~/.openclaw/workspace/Projects/v2g/figures/nnd/filter_grid.csv
```

## Outputs
Written to `Projects/v2g/figures/nnd/`:
- `*_hist_n_total.png` — histogram of candidates per prompt
- `*_hist_pos_neg.png` — histograms of POS and NEG per prompt
- `*_heatmap_pos_vs_neg.png` — heatmap of prompt counts at (n_pos, n_neg)
- `filter_grid.csv` — for each dataset and each (N1,N2), how many prompts remain

## Datasets included (currently)
- `mt_mqm`
- `qa_challenge300`
- `qgen_quizdesign`
- `summ_gpt3_cnn`
- `summ_gpt3_bbc`
- `summ_frank_cnndm_test`
- `summ_summeval_aligned`
