#!/usr/bin/env python3
"""Normalize SummEval + FRANK into a common V2G-style candidates JSONL.

Outputs one JSON object per candidate with a stable schema so downstream code can
consume multiple datasets uniformly.

This script is deliberately stdlib-only.

Schema (per line):
  dataset: "summeval" | "frank"
  subset: dataset-specific filter label (e.g., "cnndm")
  split: "test" | "val" | "train" (when available)
  prompt_id: grouping key (string)
  candidate_id: candidate key within prompt (string)
  candidate: candidate text
  label: "pos" | "neg"
  label_rule: short description of how label was derived
  meta: dict (dataset-specific extras; small + JSON-serializable)

Usage:
  python3 normalize_summeval_frank_to_v2g_jsonl.py \
    --summeval datasets/candidates/nnd_data/summeval/model_annotations.aligned.jsonl \
    --frank-dir datasets/candidates/nnd_data/frank \
    --out-dir datasets/candidates/nnd_data/normalized \
    --summeval-consistency-threshold 4.0
"""

from __future__ import annotations

import argparse
import json
import math
import os
from typing import Dict, Iterable, List, Tuple


def mean(xs: List[float]) -> float:
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return sum(xs) / len(xs) if xs else float("nan")


def load_summeval_aligned(path: str) -> Iterable[Tuple[int, Dict]]:
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            yield i, json.loads(line)


def summeval_candidate_records(path: str, *, consistency_threshold: float) -> Iterable[Dict]:
    """Yield normalized candidate records from model_annotations.aligned.jsonl.

    Notes:
      - SummEval doesn't provide an explicit split in this file; the upstream
        loader in nnd_evaluation alternates val/test by line index parity.
      - We label POS iff mean(consistency) across all 8 raters (3 expert + 5 turker)
        is >= consistency_threshold.
    """

    label_rule = f"pos iff mean_consistency_all_raters >= {consistency_threshold:.3g}"

    for idx, d in load_summeval_aligned(path):
        split = "val" if (idx % 2 == 0) else "test"

        expert = d.get("expert_annotations") or []
        turker = d.get("turker_annotations") or []
        annos = expert + turker

        consistencies: List[float] = []
        for a in annos:
            if isinstance(a, dict) and "consistency" in a:
                consistencies.append(float(a["consistency"]))

        m_cons = mean(consistencies)
        label = "pos" if (not math.isnan(m_cons) and m_cons >= consistency_threshold) else "neg"

        yield {
            "dataset": "summeval",
            "subset": "cnndm",
            "split": split,
            "prompt_id": str(d.get("id")),
            "candidate_id": str(d.get("model_id")),
            "candidate": d.get("decoded"),
            "label": label,
            "label_rule": label_rule,
            "meta": {
                "mean_consistency_all": None if math.isnan(m_cons) else round(m_cons, 6),
                "n_raters": len(annos),
                "n_expert": len(expert),
                "n_turker": len(turker),
            },
        }


def load_frank(dataset_dir: str, split: str) -> List[Dict]:
    raw_file = os.path.join(dataset_dir, "human_annotations_sentence.json")
    split_file = os.path.join(dataset_dir, "validation_split.txt" if split == "val" else "test_split.txt")

    with open(split_file, "r", encoding="utf-8") as f:
        valid_hashes = {line.strip() for line in f if line.strip()}

    with open(raw_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    out = []
    for d in raw:
        h = d.get("hash")
        if h not in valid_hashes:
            continue

        # NND heuristic: CNNDM hashes are long.
        origin = "cnndm" if (isinstance(h, str) and len(h) >= 40) else "xsum"
        out.append({**d, "origin": origin})

    return out


def frank_candidate_records(dataset_dir: str, *, split: str, subset: str = "cnndm") -> Iterable[Dict]:
    """Yield normalized candidate records for FRANK.

    Label rule (V2G view): POS iff error_type == "NoE" else NEG.

    For grouping, we use `hash` as prompt_id, consistent with nnd_evaluation.
    """

    label_rule = "pos iff error_type == 'NoE'"

    data = load_frank(dataset_dir, split=split)
    for d in data:
        if d.get("origin") != subset:
            continue

        error_type = d.get("error_type")
        label = "pos" if error_type == "NoE" else "neg"

        yield {
            "dataset": "frank",
            "subset": subset,
            "split": split,
            "prompt_id": str(d.get("hash")),
            "candidate_id": str(d.get("model_name")),
            "candidate": d.get("summary"),
            "label": label,
            "label_rule": label_rule,
            "meta": {
                "error_type": error_type,
            },
        }


def write_jsonl(path: str, records: Iterable[Dict]) -> int:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summeval", required=True, help="Path to SummEval model_annotations.aligned.jsonl")
    ap.add_argument("--frank-dir", required=True, help="Path to FRANK dataset dir (contains human_annotations_sentence.json + split files)")
    ap.add_argument("--out-dir", required=True, help="Output directory")
    ap.add_argument("--summeval-consistency-threshold", type=float, default=4.0)

    args = ap.parse_args()

    summeval_out = os.path.join(args.out_dir, "summeval_cnndm_v2g_candidates.jsonl")
    frank_out = os.path.join(args.out_dir, "frank_test_cnndm_v2g_candidates.jsonl")

    n1 = write_jsonl(
        summeval_out,
        summeval_candidate_records(args.summeval, consistency_threshold=args.summeval_consistency_threshold),
    )
    n2 = write_jsonl(
        frank_out,
        frank_candidate_records(args.frank_dir, split="test", subset="cnndm"),
    )

    print(f"Wrote {n1} candidates -> {summeval_out}")
    print(f"Wrote {n2} candidates -> {frank_out}")


if __name__ == "__main__":
    main()
