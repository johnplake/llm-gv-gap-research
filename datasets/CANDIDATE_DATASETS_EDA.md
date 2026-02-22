# Candidate datasets from `main.tex` ("% Some candidates") — acquisition + EDA + V2G suitability

This note covers the three candidate dataset families listed in `Projects/v2g/main.tex` comments:

1. **Laban et al. (2022)** — *Near-Negative Distinction (NND)*
2. **Jennifer Hu & Michael Frank (2024)** — *Auxiliary task demands mask the capabilities of smaller language models*
3. **Personality / persona datasets** — as used/mentioned in Bigelow et al. (2025) *Belief Dynamics Reveal…*; concretely points to **Anthropic evals persona** datasets.

Target use case (V2G): per **prompt** we want multiple candidate completions with correctness/quality labels (ideally ~10+ candidates; not necessarily balanced between correct/incorrect).

All data/repos were pulled into: `Projects/v2g/datasets/candidates/`.

---

## 1) Laban et al. — Near-Negative Distinction (NND)

### Paper
- *Near-Negative Distinction: Giving a Second Life to Human Evaluation Datasets* (EMNLP 2022)
  - arXiv: https://arxiv.org/abs/2205.06871

### Code / data access
- Repo cloned: `Projects/v2g/datasets/candidates/nnd_evaluation/`
  - https://github.com/salesforce/nnd_evaluation
- Important: the repo mostly provides **code + notebooks**; many datasets are fetched from upstream sources (Google Drive, other GitHub repos).

### Dataset structure (core idea)
NND is built from *human-evaluated* candidate outputs, grouped by an input/document.
- group_key = prompt id / segment id / doc id
- candidate_key = a system output (summary, translation, answer, question)
- quality_key = a human label or score

Then NND constructs **pairwise comparisons within each group** (combinations of candidates) to yield many preference pairs per prompt.

### EDA: WMT 2021 MQM EN→DE (high-candidate setting)
I downloaded the MQM annotations TSV used by their code:
- `Projects/v2g/datasets/candidates/nnd_data/mqm_newstest2021_ende.tsv`
  - 11,572 rows
  - 1,180 unique segments

If we group by segment (doc_id, seg_id, source) and count **unique systems**, we get:
- systems per segment: min 1, median 2, p90 17, max 17

If we aggregate to **system-level correctness** per segment using a simple rule:
- correct := (category == No-error AND severity == No-error) for that system on that segment

Then per segment:
- correct count: median 2, p90 13, max 17
- incorrect count: median 1, p90 10, max 17

So we can often get **~17 total candidates** per prompt, and often **≥10 candidates** in at least one of correct/incorrect.

### EDA: Challenge300 QA (lower-candidate setting)
Downloaded:
- `challenge300-outputs.tsv` from the Macaw repo

This has credits for only ~5 systems (so ~5 labeled candidates per question). That’s probably **too few** to hit the “~10 correct + ~10 incorrect” ambition without augmentation.

### Suitability for V2G
**Strong candidate overall.**
- Pros:
  - Naturally provides *same-prompt candidate sets* (exactly what we want).
  - Often provides >10 candidates per prompt (MQM does; SummEval-style likely does too).
  - Can define correctness several ways (binary No-error vs error; or use severity/category as graded signal).
- Cons / work needed:
  - Some NND tasks fetch data via nontrivial dependencies (google drive download helpers, HF datasets, etc.).
  - Many “groups” have fewer candidates (median 2), so we may want to filter to segments with enough systems.

**Adaptation suggestion:** Start with MQM, filter segments with systems>=10, define label = No-error vs other, and treat each segment as a prompt with up to 17 candidate completions.

---

## 2) Jennifer Hu — "Auxiliary task demands…" datasets

### Paper
- *Auxiliary task demands mask the capabilities of smaller language models* (COLM 2024)
  - arXiv: https://arxiv.org/abs/2404.02418

### Code / data access
- Repo cloned: `Projects/v2g/datasets/candidates/lm-task-demands/`
  - https://github.com/jennhu/lm-task-demands

### What’s inside (at a glance)
- `external_stimuli/` contains task stimuli for:
  - BLiMP (grammatical minimal pairs) — jsonl pairs
  - CRT (reflective reasoning) — csv
  - DGL, etc.
  - digit_mat is stored as `all_problems.npz` (NumPy npz)

### Suitability for V2G
**Probably not a great match for the “10+ candidates per prompt” goal** as-is.
- Many of these tasks are **minimal-pair** or **few-choice** (2–5 candidates per prompt).
- Still potentially useful for **same-prompt** comparisons, but mostly pairwise.

**What it would take to adapt:**
- For minimal-pair tasks (BLiMP), you’d only ever have 2 candidates per prompt.
- For digit-matrix/analogies, there may be richer candidate sets, but the data is in NPZ; we’d need to either:
  - parse NPZ without NumPy (possible but annoying), or
  - install minimal python deps (not currently available in this runtime).

Net: I would treat this as a **secondary** option unless we decide 2-candidate prompts are acceptable.

---

## 3) Persona/personality datasets (Bigelow et al. mention)

### Paper pointer
- Bigelow et al. *Belief Dynamics Reveal the Dual Nature of In-Context Learning and Activation Steering* (arXiv:2511.00617)
  - https://arxiv.org/abs/2511.00617

The arXiv HTML explicitly points to persona datasets from Anthropic evals.

### Data access
- Repo cloned: `Projects/v2g/datasets/candidates/anthropics-evals/`
- Persona data is in: `Projects/v2g/datasets/candidates/anthropics-evals/persona/*.jsonl`

EDA:
- number of persona files: **135**
- examples per file: min 518, median 1000, max 1000

Each example has keys:
- `question` ("Is the following statement something you would say?\n\"...\"")
- `statement`
- `answer_matching_behavior` ∈ {" Yes", " No"}
- `answer_not_matching_behavior`
- `label_confidence`

### Suitability for V2G
This is a **binary forced-choice** dataset (Yes/No).
- As-is, each prompt has only **2 candidate completions**.
- So it does **not** meet the “~10 candidate completions per prompt” target.

**What it could still be good for:**
- Measuring or training a *validator* that distinguishes persona-consistent vs inconsistent responses.
- Many-shot ICL / steering style experiments (as in Bigelow et al.).

**What it would take to adapt for our V2G ranking-over-candidates setting:**
- We’d need to change the task formulation so that the generator produces richer outputs (not just Yes/No), e.g.:
  - prompt: “Write a statement you would say…” with persona conditioning
  - validator: scores persona-consistency
  - candidates: multiple generated statements
- That becomes a *new synthetic candidate-generation pipeline*, not a ready-made 10+/prompt dataset.

---

## Bottom line (recommendation)

If the requirement is truly “~10+ candidates per prompt”, the best immediate fit among these is:
- **NND / MQM translation segments** (up to 17 system candidates per segment; filter segments with enough systems; binary No-error vs error or use severity/category).

Hu’s datasets and the persona datasets are still useful scientifically, but they are not naturally “many-candidates-per-prompt” datasets.
