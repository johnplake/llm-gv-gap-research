# V2G datasets: acquisition + EDA + suitability (draft)

Goal for V2G training/eval: per *prompt* (question/constraint/etc.) we want **multiple candidate completions** with validator-style correctness signals, ideally on the order of ~10 “correct” + ~10 “incorrect” per prompt (not necessarily balanced; can be fewer if many prompts).

This doc covers the three dataset categories mentioned in the draft paper:
- Hypernymy (lexical semantics)
- COLLIE (constrained generation)
- QA (PlausibleQA, AmbigQA)

Artifacts downloaded/inspected live under `Projects/v2g/datasets/`.

---

## 1) Hypernymy (RankAlign-style)

### Relevant papers/code
- RankAlign repo (branch `longform`) cloned to: `Projects/rankalign-longform/` (read-only)
- RankAlign paper: Rodriguez et al., COLM 2025 (background; method & evaluation framing)

### What data looks like (what I could inspect right now)
In the `rankalign-longform` checkout I do **not** currently see the per-hyponym CSVs that the task code expects (e.g. `data/fixed-hypernyms/hypernym_dogs_...-fixed.csv`). Those are the ones that would correspond directly to tasks like `hypernym-dogs`, `hypernym-elephants`.

However, I *can* inspect an aggregate JSON dataset present in the repo:
- `Projects/rankalign-longform/data/hypernym-train-gemma-2-2b.json`

Each row is a **(noun1, noun2) pair** with prompts and logged scores:
- `noun1`: hyponym (e.g. `elephants`)
- `noun2`: candidate hypernym completion (e.g. `mammal`)
- `taxonomic`: `yes`/`no` label
- `generator-prompt`: e.g. `Complete the sentence: elephants are a kind of`
- `discriminator-prompt`: few-shot yes/no format ending with `Do you think elephants are a mammal? Answer:`
- plus `generator-log-prob`, `discriminator-log-prob`, and gold completions.

### Quick exploratory stats (from that JSON)
I grouped by `noun1` (treating each unique `noun1` as a “prompt group” with multiple candidate hypernyms):
- Total rows inspected: **3000**
- Unique `noun1`: **1135**
- Candidates per `noun1`:
  - min **1**, median **2**, 90th percentile **5**, max **31**
- Positive (`taxonomic==yes`) count per `noun1`:
  - min **0**, median **1**, max **4**

So: this *particular* artifact doesn’t have ~10 positive candidates per prompt; it’s mostly **1-ish positive** per `noun1`.

### Suitability for V2G and what it would take
**Good news:** hypernymy is still one of the most V2G-friendly domains, because it’s easy to generate many candidate completions per noun1.

**To reach ~10 correct + ~10 incorrect per noun1**, we likely need to *expand candidate sets* beyond what’s in the small aggregate JSON:
- Sample many hypernym candidates per `noun1` (e.g. top-k next-token(s), beam search, or nucleus sampling over 1–3 tokens).
- Label candidates as correct/incorrect via:
  - a strong LLM judge (GPT-4/5) *or*
  - WordNet / taxonomy-based lookup (fast, but coverage/word-sense issues)
- Keep multiple correct hypernyms by allowing different abstraction levels:
  - `dogs → animal`, `mammal`, `canine`, `pet` (depending on what “correct” is defined as)

**Likely adaptation effort:** moderate. The main work is constructing and labeling richer candidate sets (and then ensuring the same-prompt slice definition is “same noun1”).

---

## 2) COLLIE (constrained generation)

(Results pending: sub-agent running COLLIE acquisition + EDA.)

---

## 3) QA: PlausibleQA + AmbigQA

(Results pending: sub-agent running PlausibleQA/AmbigQA acquisition + EDA.)
