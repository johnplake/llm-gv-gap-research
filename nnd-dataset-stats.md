# NND (Laban et al., EMNLP 2022) — dataset acquisition + global stats (V2G view)

This note summarizes what we currently have locally from the **Near-Negative Distinction (NND)** ecosystem and computes **global / distributional stats** in a way that is directly relevant to V2G training/evaluation.

**Paper:** Philippe Laban et al. (2022), *Near-Negative Distinction: Giving a Second Life to Human Evaluation Datasets* (EMNLP 2022)
- arXiv: https://arxiv.org/abs/2205.06871
- Code repo: https://github.com/salesforce/nnd_evaluation

**V2G goal:** for each prompt/group, obtain *many* candidate completions with a natural positive/negative distinction.

---

## Where the data/code is in this repo/workspace

- Code repo cloned (read-only, upstream):
  - `Projects/v2g/datasets/candidates/nnd_evaluation/`

- Data downloaded for analysis (raw files):
  - `Projects/v2g/datasets/candidates/nnd_data/`

---

## Conventions (V2G view)

For each sub-dataset:
- **Prompt** = the shared input that defines a slice/group (e.g., MT source segment)
- **Candidates** = multiple system outputs for the same prompt
- **POS vs NEG** = a natural label from human evaluation annotations

---

## Summary table (per sub-dataset)

| Sub-dataset | Natural prompt grouping | # prompts | # candidates / prompt (min / p50 / p90 / max) | POS share overall | POS per prompt (p50) | NEG per prompt (p50) | POS definition |
|---|---|---:|---:|---:|---:|---:|---|
| **MT: WMT21 MQM EN→DE** (`mqm_newstest2021_ende.tsv`) | (doc_id, seg_id, source) | **1180** | **1 / 2 / 17 / 17** | **0.588** | **2** | **1** | system has only `No-error` (category & severity) |
| **QA: Challenge300** (`challenge300-outputs.tsv`) | (id, question) | **300** | **1 / 5 / 5 / 5** | **0.689** | **4** | **1** | credit==1 is POS, credit==0 is NEG |
| **QGen: QuizDesign** (`quiz_design_groups.jsonl`) | (group_id, answer_span) | **452** | **1 / 6 / 7 / 7** | **0.460** | **2** | **3** | reason==`No error` is POS |
| **Summarization: “News Summarization in era of GPT‑3” (CNN)** (`cnn_human.json`) | doc_id | **100** | **3 / 3 / 3 / 3** | **0.377** | **1** | *(see note)* | POS = top voted summary (best/worst votes) |
| **Summarization: same (BBC)** (`bbc_human.json`) | doc_id | **100** | **3 / 3 / 3 / 3** | **0.377** | **1** | *(see note)* | same as above |
| **Summarization: same (Keyword)** (`keyword_human.json`) | — | **(not parsed yet)** | — | — | — | — | file schema differs (see below) |

**Notes:**
- The GPT‑3 summarization annotation sets (CNN/BBC) have exactly **3 candidates per prompt** (gpt3/t0/brio). POS was defined as “max score” where score is computed from annotators choosing best (+1) and worst (−1). This is not strictly a symmetric POS/NEG split because ties can occur.

---

## Distributional intuition (POS/NEG ratios)

### MT MQM (WMT21 EN→DE)
- Overall POS share across all (prompt, system) candidates: **0.588**.
- Per-prompt medians: **2 POS**, **1 NEG**.
- Strong variation: prompts can be all-POS, mixed, or all-NEG.

### QA Challenge300
- Overall POS share: **0.689**.
- Typical prompt has 5 candidates; median split is **4 POS / 1 NEG**.

### QGen QuizDesign
- Overall POS share: **0.460**.
- Typical prompt has 6 candidates; median split is **2 POS / 3 NEG**.

---

## MQM error categories (MT) — what “NEG” looks like

For MT MQM, we labeled system-candidates as:
- **POS** iff *all* annotations for that system on that segment have:
  - `category == No-error` **and** `severity == No-error`
- **NEG** otherwise

Top MQM categories observed across system-candidates (not mutually exclusive):
- `No-error`
- `Style/Awkward`
- `Accuracy/Mistranslation`
- `Fluency/Punctuation`
- `Fluency/Grammar`
- `Terminology/Inappropriate for context`

Top severities:
- `No-error`
- `Minor`
- `Major`

**Data hygiene note:** there are a small number of malformed severity entries in the raw TSV (likely a parsing / data issue). The conservative POS rule above avoids relying on those strings for positives.

---

## Concrete examples (prompt → many completions)

### Example A — 17 candidates, all POS
Prompt/source:
> When he refused, the officials tipped his cart over, destroying all the eggs, the boy alleged.

This segment has **17 systems**; **POS=17, NEG=0**.
Sample completions:
- POS hyp.Facebook-AI: “Als er sich weigerte, kippten die Beamten seinen Wagen um und zerstörten alle Eier, so der Junge.”
- POS hyp.HuaweiTSC: “Als er sich weigerte, kippten die Beamten seinen Wagen um und zerstörten alle Eier, behauptete der Junge.”
- POS hyp.Nemo: “Als er sich weigerte, kippten die Beamten seinen Wagen um und zerstörten alle Eier, behauptete der Junge.”

### Example B — 17 candidates, mixed
Prompt/source:
> Flat, Free Education For Indore Egg Seller Paras Raykar Whose Cart Was Overturned Allegedly Over Rs. 100 Bribe

This segment has **17 systems**; **POS=5, NEG=12**.
Sample completions:
- POS hyp.Online-W: “Freie Bildung für den Eierverkäufer Paras Raykar aus Indore, dessen Karren angeblich wegen 100 Rupien Bestechungsgeld umgeworfen wurde”
- POS ref.A: “Eine Wohnung und kostenlose Ausbildung für den Eierverkäufer Paras Raykar aus Indore, dessen Karren angeblich wegen 100 Rs Schmiergeld umgekippt wurde”
- NEG hyp.Facebook-AI: “*Flache*, kostenlose Bildung …” (Style/Awkward, Terminology/Inappropriate for context)
- NEG hyp.HuaweiTSC: contains untranslated/incorrect phrase (Accuracy/Mistranslation)

### Example C — 17 candidates, all NEG
Prompt/source:
> A roast of former press secretary Sarah Huckabee Sanders by comedian Michelle Wolf … was so vicious that even MSNBC host Mika Brzezinski called it “deplorable.”

This segment has **17 systems**; **POS=0, NEG=17**.
Sample completions:
- NEG hyp.Facebook-AI: uses “Braten” for “roast” (Terminology/Inappropriate for context; Major)
- NEG hyp.Online-W: similar issue plus fluency/punctuation flags

---

## What NND includes vs what is still pending

The NND paper/repo covers multiple domains. From what we can access in this environment, we currently have stats for:
- MT (MQM WMT21 EN→DE) ✅
- QA (Challenge300) ✅
- QGen (QuizDesign) ✅
- Summarization (GPT‑3-era human annotations for CNN/BBC) ✅

Still pending:
- **SummEval NND** (their code downloads a Google Drive file; may need manual fetch)
- **FRANK NND** (should be fetchable from GitHub raw URLs; likely easiest next)
- `keyword_human.json` parsing (schema differs from cnn/bbc)

---

## Repro / scripts

Stats in this note were computed via ad-hoc Python scripts executed in the OpenClaw environment, using only standard library parsing (no numpy/pandas/datasets installed).
