# SummEval raw data (as used for NND-style stats)

Downloaded from the Yale-LILY/SummEval public bucket:

- https://storage.googleapis.com/sfr-summarization-repo-research/model_annotations.aligned.jsonl

This file contains 1600 model summaries (100 CNNDM documents × 16 systems) with:
- `id` (looks like `dm-test-<hash>`): used as prompt grouping key (cnndm_id)
- `decoded`: system output summary
- `references`: list of reference summaries
- `expert_annotations` (3 raters) and `turker_annotations` (5 raters): each has 1–5 scores for {coherence, consistency, fluency, relevance}

Attempted but inaccessible at time of download (HTTP 403):
- `model_annotations.aligned.scored.jsonl`
- `model_annotations.aligned.paired.jsonl`

