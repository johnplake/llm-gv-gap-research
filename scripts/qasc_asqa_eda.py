"""Lightweight exploration for QASC and ASQA.

Writes a markdown report with:
- split sizes
- schema/fields
- notes on where "multiple answers" live
- a few concrete examples (Q + answers)

Run (recommended):
  cd Projects/v2g
  ~/.openclaw/workspace/bin/uv run --no-project \
    --with datasets --with pyarrow --with pandas \
    -- python3 scripts/qasc_asqa_eda.py --out datasets/reports/qasc_asqa_exploration.md
"""

from __future__ import annotations

import argparse
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _import_hf_datasets():
    # Avoid importing the local `datasets/` directory as a python module.
    cwd = os.getcwd()
    if "" in os.sys.path:
        os.sys.path.remove("")
    if cwd in os.sys.path:
        os.sys.path.remove(cwd)

    from datasets import load_dataset  # type: ignore

    return load_dataset


def _md_escape(s: str) -> str:
    return s.replace("\n", " ").strip()


def _qasc_example(ex: Dict[str, Any]) -> str:
    q = ex.get("question", "")
    choices = ex.get("choices", {})
    labels = choices.get("label", [])
    texts = choices.get("text", [])
    answer_key = ex.get("answerKey")

    lines = [f"**Q:** {_md_escape(q)}", "", "**Candidate answers (8-way MCQ):**"]
    for lab, txt in zip(labels, texts):
        mark = " ✅" if lab == answer_key else ""
        lines.append(f"- {lab}. {_md_escape(str(txt))}{mark}")

    # QASC also includes supporting facts.
    fact1 = ex.get("fact1")
    fact2 = ex.get("fact2")
    if fact1 or fact2:
        lines.append("")
        lines.append("**Supporting facts:**")
        if fact1:
            lines.append(f"- fact1: {_md_escape(str(fact1))}")
        if fact2:
            lines.append(f"- fact2: {_md_escape(str(fact2))}")

    return "\n".join(lines)


def _asqa_example(ex: Dict[str, Any]) -> str:
    q = ex.get("ambiguous_question", "")
    qa_pairs = ex.get("qa_pairs", [])
    annotations = ex.get("annotations", [])

    lines = [f"**Ambiguous Q:** {_md_escape(q)}", "", "**Disambiguations (qa_pairs):**"]
    for i, pair in enumerate(qa_pairs, start=1):
        dq = pair.get("question", "")
        short_ans = pair.get("short_answers", [])
        ans_preview = ", ".join([_md_escape(str(a)) for a in short_ans][:6])
        lines.append(f"- {i}. {_md_escape(dq)}")
        lines.append(f"  - short answers: {ans_preview}")

    if annotations:
        ann0 = annotations[0]
        long_ans = ann0.get("long_answer", "")
        lines.append("")
        lines.append("**One long-form reference answer (annotations[0].long_answer):**")
        lines.append(f"> {_md_escape(long_ans)}")

    return "\n".join(lines)


def _sample(ds, k: int, seed: int = 0) -> List[Dict[str, Any]]:
    random.seed(seed)
    n = len(ds)
    idxs = random.sample(range(n), k=min(k, n))
    return [ds[i] for i in idxs]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="datasets/reports/qasc_asqa_exploration.md",
        help="Output markdown path",
    )
    ap.add_argument("--examples", type=int, default=3, help="Examples per dataset")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    load_dataset = _import_hf_datasets()

    qasc = load_dataset("allenai/qasc")
    asqa = load_dataset("din0s/asqa")

    lines: List[str] = []
    lines.append("# QASC + ASQA dataset exploration")
    lines.append("")
    lines.append("This report focuses on: what’s in the dataset, and concrete Q/answers examples.")
    lines.append("")

    # QASC
    lines.append("## QASC (`allenai/qasc`)")
    lines.append("")
    lines.append("**High-level:** Multiple *candidate answers* per question (8-way MCQ), with a single labeled correct choice (`answerKey`).")
    lines.append("")
    lines.append("### Splits")
    for split, ds in qasc.items():
        lines.append(f"- {split}: {len(ds):,}")
    lines.append("")
    lines.append("### Fields")
    lines.append(f"- columns: `{qasc['train'].column_names}`")
    lines.append("")
    lines.append("### Where are the ‘multiple answers’? ")
    lines.append("- `choices.text` contains **8 candidate answer strings**")
    lines.append("- `answerKey` selects the correct one")
    lines.append("")
    lines.append("### Examples")
    qasc_examples = _sample(qasc["train"], args.examples, seed=1)
    for i, ex in enumerate(qasc_examples, start=1):
        lines.append("")
        lines.append(f"#### QASC example {i}")
        lines.append(_qasc_example(ex))

    # ASQA
    lines.append("")
    lines.append("## ASQA (`din0s/asqa`) — Answer Summaries for Questions which are Ambiguous")
    lines.append("")
    lines.append("**High-level:** One ambiguous question + multiple disambiguated QA pairs (`qa_pairs`), plus long-form reference answers (`annotations[].long_answer`).")
    lines.append("")
    lines.append("### Splits")
    for split, ds in asqa.items():
        lines.append(f"- {split}: {len(ds):,}")
    lines.append("")
    lines.append("### Fields")
    lines.append(f"- columns: `{asqa['train'].column_names}`")
    lines.append("")
    lines.append("### Where are the ‘multiple answers’? ")
    lines.append("- `qa_pairs` is a list: each element has a disambiguated `question` and a list of short answers in `short_answers`")
    lines.append("- `annotations` contains one or more long-form answers that (ideally) cover all disambiguations")
    lines.append("")
    lines.append("### Examples")
    asqa_examples = _sample(asqa["train"], args.examples, seed=2)
    for i, ex in enumerate(asqa_examples, start=1):
        lines.append("")
        lines.append(f"#### ASQA example {i}")
        lines.append(_asqa_example(ex))

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ Wrote report: {out_path}")


if __name__ == "__main__":
    main()
