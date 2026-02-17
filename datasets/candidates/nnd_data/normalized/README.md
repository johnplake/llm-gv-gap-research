# Normalized V2G candidates (SummEval + FRANK)

This folder contains **candidate-level JSONL** files with a common schema so we can treat multiple NND-style summarization datasets uniformly.

## Schema (one JSON object per line)

- `dataset`: `"summeval"` | `"frank"`
- `subset`: e.g. `"cnndm"`
- `split`: `"test"` | `"val"` | `"train"` (when available)
- `prompt_id`: prompt/group key (string)
- `candidate_id`: candidate key within prompt (string)
- `candidate`: candidate text (summary)
- `label`: `"pos"` | `"neg"`
- `label_rule`: short description of labeling heuristic
- `meta`: small dataset-specific extras

## Files

- `summeval_cnndm_v2g_candidates.jsonl`
  - Source: `../summeval/model_annotations.aligned.jsonl`
  - Split assignment: alternates `val/test` by line index parity (to match the upstream `nnd_evaluation` convention).
  - Label: POS iff mean(consistency) across **all 8 raters** (3 expert + 5 turker) is >= 4.0.

- `frank_test_cnndm_v2g_candidates.jsonl`
  - Source: `../frank/human_annotations_sentence.json` + `../frank/test_split.txt`
  - Subset: cnndm-only via NND heuristic `len(hash) >= 40`
  - Label: POS iff `error_type == "NoE"`.

## Regeneration

From repo root (`Projects/v2g`):

```bash
python3 datasets/candidates/nnd_data/scripts/normalize_summeval_frank_to_v2g_jsonl.py \
  --summeval datasets/candidates/nnd_data/summeval/model_annotations.aligned.jsonl \
  --frank-dir datasets/candidates/nnd_data/frank \
  --out-dir datasets/candidates/nnd_data/normalized \
  --summeval-consistency-threshold 4.0
```
