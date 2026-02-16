#!/usr/bin/env python3
"""Fetch FRANK components used by nnd_evaluation and compute V2G-view stats.

- Downloads from https://raw.githubusercontent.com/artidoro/frank/main/data/
  * human_annotations_sentence.json
  * validation_split.txt
  * test_split.txt

- Re-implements the essential parsing in nnd_evaluation/utils_summarization.py::load_frank
  but using only the Python standard library.

Stats (V2G view):
- prompt grouping: hash (filtered to origin=="cnndm"; i.e., long hashes)
- candidate: summary (claim)
- POS: error_type == "NoE" (No Error)
- NEG: error_type != "NoE" (majority error type per doc)

Output:
- Writes a small JSON stats blob alongside a human-readable printout.

Usage:
  python frank_fetch_and_stats.py \
    --frank-dir ../frank \
    --cut test
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import urllib.request
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

RAW_BASE = "https://raw.githubusercontent.com/artidoro/frank/main/data"
FILES = [
    "human_annotations_sentence.json",
    "validation_split.txt",
    "test_split.txt",
]


def _download_text(url: str) -> str:
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8")


def ensure_frank_files(frank_dir: str) -> None:
    os.makedirs(frank_dir, exist_ok=True)
    for fn in FILES:
        out_path = os.path.join(frank_dir, fn)
        if os.path.exists(out_path):
            continue
        url = f"{RAW_BASE}/{fn}"
        txt = _download_text(url)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(txt)


def load_split_hashes(frank_dir: str, cut: str) -> set[str]:
    assert cut in {"val", "test"}
    split_fn = "validation_split.txt" if cut == "val" else "test_split.txt"
    path = os.path.join(frank_dir, split_fn)
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def frank_origin(h: str) -> str:
    # Matches nnd_evaluation heuristic: CNNDM hashes are long (>=40)
    return "cnndm" if len(h) >= 40 else "xsum"


@dataclass
class FrankRow:
    hash: str
    origin: str
    model_name: str
    document: str
    claim: str
    error_type: str  # "NoE" for positive else majority error label


def parse_frank_rows(frank_dir: str, cut: str) -> List[FrankRow]:
    valid_hashes = load_split_hashes(frank_dir, cut)

    raw_path = os.path.join(frank_dir, "human_annotations_sentence.json")
    with open(raw_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rows: List[FrankRow] = []
    for d in raw:
        h = d.get("hash")
        if h not in valid_hashes:
            continue

        origin = frank_origin(h)
        article = d.get("article", "")
        summary = d.get("summary", "")
        model_name = d.get("model_name", "")

        # Determine label + majority error type as in utils_summarization.load_frank
        summ_labels: List[int] = []
        annotator_labels: Dict[str, List[str]] = {}

        for annot in d.get("summary_sentences_annotations", []):
            # annot: dict of {annotator_name: [labels...]}
            annot_vals = [an for ans in annot.values() for an in ans]
            noerror_count = len([an for an in annot_vals if an == "NoE"])
            label = 1 if noerror_count >= 2 else 0
            summ_labels.append(label)
            for anno_name, anno_list in annot.items():
                annotator_labels.setdefault(anno_name, []).extend(anno_list)

        # label = 1 iff every sentence label is 1
        label_doc = 0 if any(sl == 0 for sl in summ_labels) else 1

        if label_doc == 1:
            error_type = "NoE"
        else:
            errors = [
                lab
                for labs in annotator_labels.values()
                for lab in labs
                if lab != "NoE"
            ]
            error_type = Counter(errors).most_common(1)[0][0] if errors else "Unknown"

        rows.append(
            FrankRow(
                hash=h,
                origin=origin,
                model_name=model_name,
                document=article,
                claim=summary,
                error_type=error_type,
            )
        )

    return rows


def percentile(sorted_vals: List[int], p: float) -> int:
    """Nearest-rank percentile for small integer lists."""
    if not sorted_vals:
        raise ValueError("empty")
    if p <= 0:
        return sorted_vals[0]
    if p >= 100:
        return sorted_vals[-1]
    k = int((p / 100.0) * (len(sorted_vals) - 1))
    return sorted_vals[k]


def compute_stats(rows: List[FrankRow]) -> dict:
    # Filter to CNNDM (matches NND construction)
    rows = [r for r in rows if r.origin == "cnndm"]

    by_hash: Dict[str, List[FrankRow]] = {}
    for r in rows:
        by_hash.setdefault(r.hash, []).append(r)

    prompts = sorted(by_hash.keys())
    cand_counts = sorted([len(by_hash[h]) for h in prompts])

    # POS/NEG overall across candidates
    pos_overall = sum(1 for r in rows if r.error_type == "NoE")
    neg_overall = sum(1 for r in rows if r.error_type != "NoE")
    pos_share = pos_overall / (pos_overall + neg_overall) if (pos_overall + neg_overall) else 0.0

    # Per prompt: POS and NEG counts
    pos_per_prompt = []
    neg_per_prompt = []
    for h in prompts:
        group = by_hash[h]
        pos = sum(1 for r in group if r.error_type == "NoE")
        neg = len(group) - pos
        pos_per_prompt.append(pos)
        neg_per_prompt.append(neg)

    pos_per_prompt_sorted = sorted(pos_per_prompt)
    neg_per_prompt_sorted = sorted(neg_per_prompt)

    def pctl(vals: List[int], p: float) -> int:
        return percentile(sorted(vals), p)

    out = {
        "origin_filter": "cnndm",
        "n_prompts": len(prompts),
        "n_candidates": len(rows),
        "candidates_per_prompt": {
            "min": cand_counts[0] if cand_counts else 0,
            "p50": pctl(cand_counts, 50) if cand_counts else 0,
            "p90": pctl(cand_counts, 90) if cand_counts else 0,
            "max": cand_counts[-1] if cand_counts else 0,
        },
        "pos_overall": pos_overall,
        "neg_overall": neg_overall,
        "pos_share_overall": pos_share,
        "pos_per_prompt": {
            "p50": pctl(pos_per_prompt_sorted, 50) if pos_per_prompt_sorted else 0,
        },
        "neg_per_prompt": {
            "p50": pctl(neg_per_prompt_sorted, 50) if neg_per_prompt_sorted else 0,
        },
    }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frank-dir", required=True)
    ap.add_argument("--cut", choices=["val", "test"], default="test")
    ap.add_argument("--write-json", action="store_true")
    args = ap.parse_args()

    ensure_frank_files(args.frank_dir)
    rows = parse_frank_rows(args.frank_dir, cut=args.cut)
    stats = compute_stats(rows)

    print("FRANK (V2G view; origin=cnndm)")
    print(json.dumps(stats, indent=2, sort_keys=True))

    if args.write_json:
        out_path = os.path.join(args.frank_dir, f"frank_stats_{args.cut}_cnndm.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, sort_keys=True)
        print(f"Wrote: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
