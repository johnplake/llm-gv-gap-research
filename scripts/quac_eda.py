"""Lightweight exploration for QuAC (allenai/quac).

QuAC records are dialogues; each record contains lists for questions, answers, etc.
The dataset supports multiple reference answers for dev/test in `answers`.

Run (recommended):
  cd Projects/v2g
  ~/.openclaw/workspace/bin/uv run --no-project \
    --with 'datasets==2.19.1' --with pyarrow --with pandas \
    -- python3 scripts/quac_eda.py --out datasets/reports/quac_exploration.md --examples 2
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


def _sample(ds, k: int, seed: int) -> List[Dict[str, Any]]:
    random.seed(seed)
    n = len(ds)
    idxs = random.sample(range(n), k=min(k, n))
    return [ds[i] for i in idxs]


def _answers_for_turn(answers_obj: Dict[str, Any], turn_idx: int) -> List[str]:
    """Extract a list of answer strings for a particular turn.

    In QuAC, `answers` includes fields like `text` and `answer_start`.
    For multi-ref splits, `text[turn_idx]` can itself be a list of strings.
    """
    if not isinstance(answers_obj, dict):
        return []

    # HF QuAC uses `texts` (list over turns), and `answer_starts`.
    texts = answers_obj.get("texts")
    if texts is None:
        # older variants might use `text`
        texts = answers_obj.get("text")
    if texts is None:
        return []

    # texts is usually list over turns.
    if not isinstance(texts, list) or turn_idx >= len(texts):
        return []

    t = texts[turn_idx]
    if t is None:
        return []

    if isinstance(t, list):
        return [str(x) for x in t if x is not None]
    return [str(t)]


def _dialogue_snippet(ex: Dict[str, Any], max_turns: int = 3) -> str:
    title = ex.get("wikipedia_page_title", "")
    section = ex.get("section_title", "")
    background = ex.get("background", "")
    questions = ex.get("questions", [])
    answers = ex.get("answers", {})
    yesnos = ex.get("yesnos", [])
    followups = ex.get("followups", [])

    lines: List[str] = []
    lines.append(f"**Wikipedia page:** {_md_escape(str(title))}")
    lines.append(f"**Section:** {_md_escape(str(section))}")
    if background:
        lines.append(f"**Background:** {_md_escape(str(background))}")

    lines.append("")
    lines.append(f"**First {max_turns} turns:**")

    for t in range(min(max_turns, len(questions))):
        q = questions[t]
        ans_list = _answers_for_turn(answers, t)
        yn = yesnos[t] if t < len(yesnos) else None
        fu = followups[t] if t < len(followups) else None

        lines.append(f"- Turn {t}: Q: {_md_escape(str(q))}")
        if ans_list:
            # Show up to 5 references.
            preview = ans_list[:5]
            if len(ans_list) > 5:
                preview.append(f"... (+{len(ans_list)-5} more)")
            lines.append("  - A refs: " + "; ".join([_md_escape(a) for a in preview]))
        else:
            lines.append("  - A refs: (none)")
        if yn is not None or fu is not None:
            lines.append(f"  - yesno: {yn} ; followup: {fu}")

    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="datasets/reports/quac_exploration.md",
        help="Output markdown path",
    )
    ap.add_argument("--examples", type=int, default=2, help="Dialogues per split")
    ap.add_argument("--turns", type=int, default=3, help="Turns to show per dialogue")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    load_dataset = _import_hf_datasets()

    # QuAC is script-based; pin datasets version when running (see module docstring).
    quac = load_dataset("allenai/quac")

    lines: List[str] = []
    lines.append("# QuAC dataset exploration")
    lines.append("")
    lines.append("This report focuses on: what’s in the dataset, and concrete Q/answer examples.")
    lines.append("")

    lines.append("## QuAC (`allenai/quac`) — Question Answering in Context")
    lines.append("")
    lines.append("**High-level:** Dialogue-based extractive QA grounded in a Wikipedia section. Each dataset row is a dialogue with lists of questions and answers.")
    lines.append("")

    lines.append("### Splits")
    for split, ds in quac.items():
        lines.append(f"- {split}: {len(ds):,} dialogues")
    lines.append("")

    lines.append("### Fields")
    lines.append(f"- columns: `{quac['train'].column_names}`")
    lines.append("")

    lines.append("### Where are the ‘multiple answers’? ")
    lines.append("- The dataset stores answers per-turn inside the `answers` object.")
    lines.append("- In multi-reference splits, `answers.texts[turn]` can contain multiple reference spans (a list).")
    lines.append("")

    # Examples across splits
    lines.append("### Examples (sampled across splits)")

    for i, (split, ds) in enumerate(quac.items()):
        exs = _sample(ds, args.examples, seed=10 + 31 * i)
        for j, ex in enumerate(exs, start=1):
            lines.append("")
            lines.append(f"#### Example {j} ({split})")
            lines.append(_dialogue_snippet(ex, max_turns=args.turns))

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ Wrote report: {out_path}")


if __name__ == "__main__":
    main()
