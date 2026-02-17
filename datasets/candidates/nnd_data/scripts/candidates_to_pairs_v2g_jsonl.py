#!/usr/bin/env python3
"""Convert normalized V2G candidates JSONL -> capped, deterministic pairwise JSONL.

Why:
  Many V2G/NND pipelines consume pairwise comparisons (POS vs NEG) rather than
  standalone candidates.

Input schema:
  Produced by normalize_summeval_frank_to_v2g_jsonl.py (see normalized/README.md)

Output schema (one JSON object per line):
  dataset, subset, split, prompt_id
  pair_id: stable id for the pair within the prompt
  pos: {candidate_id, candidate, meta}
  neg: {candidate_id, candidate, meta}
  label: always "pos_better"
  pairing: {policy, max_pairs_per_prompt, seed}

Pairing policy:
  For each prompt, form the full POS×NEG cross-product, then sample up to N pairs
  *without replacement* using a deterministic RNG seeded by:
    md5(f"{seed}|{dataset}|{prompt_id}")

Stdlib-only.

Usage:
  python3 candidates_to_pairs_v2g_jsonl.py \
    --in datasets/candidates/nnd_data/normalized/summeval_cnndm_v2g_candidates.jsonl \
    --out datasets/candidates/nnd_data/normalized/summeval_cnndm_v2g_pairs.jsonl \
    --max-pairs-per-prompt 32 \
    --seed 0
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
from typing import Dict, Iterable, List, Tuple


def read_jsonl(path: str) -> Iterable[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def stable_prompt_seed(base_seed: int, dataset: str, prompt_id: str) -> int:
    s = f"{base_seed}|{dataset}|{prompt_id}".encode("utf-8")
    h = hashlib.md5(s).digest()
    # 64-bit int from first 8 bytes
    return int.from_bytes(h[:8], "big", signed=False)


def group_candidates(rows: Iterable[Dict]) -> Dict[Tuple[str, str, str, str], List[Dict]]:
    groups: Dict[Tuple[str, str, str, str], List[Dict]] = {}
    for r in rows:
        key = (
            str(r.get("dataset")),
            str(r.get("subset")),
            str(r.get("split")),
            str(r.get("prompt_id")),
        )
        groups.setdefault(key, []).append(r)
    return groups


def candidate_stub(r: Dict) -> Dict:
    return {
        "candidate_id": r.get("candidate_id"),
        "candidate": r.get("candidate"),
        "meta": r.get("meta", {}),
    }


def pairs_for_prompt(cands: List[Dict]) -> List[Tuple[Dict, Dict]]:
    pos = [c for c in cands if c.get("label") == "pos"]
    neg = [c for c in cands if c.get("label") == "neg"]
    # Stable ordering before cross-product
    pos = sorted(pos, key=lambda x: (str(x.get("candidate_id")), str(x.get("candidate"))[:32]))
    neg = sorted(neg, key=lambda x: (str(x.get("candidate_id")), str(x.get("candidate"))[:32]))
    out: List[Tuple[Dict, Dict]] = []
    for p in pos:
        for n in neg:
            out.append((p, n))
    return out


def write_jsonl(path: str, rows: Iterable[Dict]) -> int:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="Input candidates JSONL")
    ap.add_argument("--out", required=True, help="Output pairs JSONL")
    ap.add_argument("--max-pairs-per-prompt", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)

    args = ap.parse_args()

    groups = group_candidates(read_jsonl(args.inp))

    def gen_rows() -> Iterable[Dict]:
        for (dataset, subset, split, prompt_id), cands in sorted(groups.items()):
            all_pairs = pairs_for_prompt(cands)
            if not all_pairs:
                continue

            rng = random.Random(stable_prompt_seed(args.seed, dataset, prompt_id))
            idxs = list(range(len(all_pairs)))
            rng.shuffle(idxs)
            idxs = idxs[: max(0, min(args.max_pairs_per_prompt, len(idxs)))]

            # Stable pair_id within this prompt: use chosen order (after shuffle)
            for j, pair_idx in enumerate(idxs):
                p, n = all_pairs[pair_idx]
                yield {
                    "dataset": dataset,
                    "subset": subset,
                    "split": split,
                    "prompt_id": prompt_id,
                    "pair_id": f"{prompt_id}::pair{j:03d}",
                    "pos": candidate_stub(p),
                    "neg": candidate_stub(n),
                    "label": "pos_better",
                    "pairing": {
                        "policy": "sample_pos_x_neg_without_replacement",
                        "max_pairs_per_prompt": args.max_pairs_per_prompt,
                        "seed": args.seed,
                    },
                }

    n = write_jsonl(args.out, gen_rows())
    print(f"Wrote {n} pairs -> {args.out}")


if __name__ == "__main__":
    main()
