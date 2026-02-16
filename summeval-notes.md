# SummEval notes (for V2G / NND-style use)

This note summarizes what the SummEval dataset contains, what the **expert annotations** mean, how we convert them into **POS/NEG** labels in this repo, and some practical guidance for **generator vs discriminator prompts**.

**Paper:** Fabbri et al., *SummEval: Re-evaluating Summarization Evaluation* (TACL 2021; arXiv:2007.12626)
- arXiv: https://arxiv.org/abs/2007.12626
- Project repo (data + toolkit): https://github.com/Yale-LILY/SummEval

**Data file used in this repo (public):**
- `datasets/candidates/nnd_data/summeval/model_annotations.aligned.jsonl`
  - 100 documents × 16 model summaries each = 1600 (doc,candidate) records
  - Each record includes:
    - `decoded`: the candidate summary
    - `expert_annotations`: **3** expert ratings (per-dimension 1–5)
    - `turker_annotations`: **5** crowd ratings (per-dimension 1–5)
    - `references`: reference summaries (used in the annotation UI setup; see below)

---

## 1) What are the “expert annotations”?

SummEval collected human judgments from **two groups**:
- **5 crowd-sourced workers** per summary (Mechanical Turk)
- **3 “expert” annotators** per summary

The paper describes the expert annotators as people who have **written papers on summarization**:
- 2 wrote papers for academic conferences
- 1 wrote a senior thesis

Experts were asked to evaluate the **same set of summaries under the same instructions** as the crowd workers.

### Expert quality-control protocol
The paper reports **two rounds** of expert annotation:
- Round 1: experts scored all summaries.
- Round 2: experts re-checked examples to correct “obvious mistakes” / confirm judgments.
  - When re-evaluating, experts were allowed to see other experts’ round-1 scores.
  - The authors note this could shift scores toward the round-1 average, but they encouraged experts to remain critical.

This two-round setup is one reason expert annotations are often treated as higher-quality than crowd ratings in subsequent analyses.

---

## 2) What instructions were annotators given?

Annotators rated summaries along **four dimensions** (Likert scale **1–5**, higher is better). The paper defines each dimension (and ties some definitions to DUC guidelines):

- **Coherence**: the collective quality of all sentences; the summary should be well-structured and well-organized, not a heap of related information.
- **Consistency**: factual alignment between summary and source; a consistent summary contains only statements entailed by the source. Annotators were asked to penalize **hallucinated facts**.
- **Fluency**: sentence-level readability/well-formedness; penalize formatting/capitalization/grammar issues, fragments, missing components, etc.
- **Relevance**: selection of important content; include only important information from the source.

Additional instruction noted in the paper:
- Annotators were instructed to penalize summaries containing **redundancies and excess information**.

### Annotation UI / presentation details (important)
The annotation interface:
- displayed the **source article** and associated summaries,
- grouped summaries in sets of **5**,
- and **each group contained the reference summary** “to establish a common point of reference between groups.”

Summary grouping and order were randomized per annotator.

### Crowdworker hiring constraints (brief)
Crowd annotators were hired through Mechanical Turk with constraints like a minimum number of approved HITs and a high approval rate, and geographic constraints (US/UK/AU) to promote English proficiency.

---

## 3) What “POS” and “NEG” mean for SummEval (in this repo)

SummEval natively provides **1–5** ratings per dimension, not binary labels.

For V2G / NND-style use, we convert ratings into **POS/NEG** labels by a “near-perfect by experts” rule:

### Rule: expert-majority-of-5 (per dimension)
For each dimension in `{consistency, coherence, fluency, relevance}` we define a separate binary-label dataset:
- Use **only** the **3 expert** ratings (`expert_annotations`).
- Let `num_5 = number of experts who gave a score of 5` on that dimension.
- **POS** iff `num_5 >= 2` (i.e., a strict majority of experts rated the candidate **5/5**).
- **NEG** otherwise.

Key interpretation:
- **POS** means “expert-near-perfect” for that specific dimension.
- **NEG does *not* mean bad**. It means “not in the expert-near-perfect bucket” and includes many “pretty good” 4/5-ish candidates.

This produces four datasets:
- `summ_summeval_consistency`
- `summ_summeval_coherence`
- `summ_summeval_fluency`
- `summ_summeval_relevance`

### Dimension behavior under this POS/NEG mapping
Under the expert-majority-of-5 rule (1600 records total):
- **Consistency:** POS share ~0.889; median per prompt **14 POS / 2 NEG**
- **Fluency:** POS share ~0.862; median per prompt **14 POS / 2 NEG**
- **Coherence:** POS share ~0.244; median per prompt **3 POS / 13 NEG**
- **Relevance:** POS share ~0.223; median per prompt **3 POS / 13 NEG**

This is why the dimensions “behave very differently” for V2G filtering: some are extremely POS-heavy (few NEGs), others are NEG-heavy (few POS).

---

## 4) Is there a good way to combine the dimensions into an “overall score”?

The dataset/paper is fundamentally **multi-dimensional**; there is no single canonical “overall” label in the public aligned JSONL we use. So an “overall” is something we define.

Reasonable options:

### A) Continuous overall score (simple)
Per candidate:
- compute the expert mean per dimension, then average across dimensions:
  - `overall = mean([mean_expert(coh), mean_expert(con), mean_expert(flu), mean_expert(rel)])`

Pros: simple, uses full signal.
Cons: can hide important structure (e.g., very fluent but inconsistent can still look decent).

### B) Strict “all-pass” overall POS (binary)
Per candidate:
- `POS_overall = POS_coh ∧ POS_con ∧ POS_flu ∧ POS_rel` under the expert-majority-of-5 rule.

Pros: very high precision “excellent overall.”
Cons: likely sparse because coherence/relevance are strict.

### C) Weighted overall score
If your main objective is faithfulness, weight **consistency** more heavily:
- example: `0.4*consistency + 0.2*relevance + 0.2*coherence + 0.2*fluency`

Pros: aligns with research goals.
Cons: subjective (but defensible if stated).

### D) Pairwise preferences (often best for training/evals)
Instead of absolute labels, define preferences within each prompt:
- A > B if overall score is higher, or if a key dimension (e.g., consistency) is higher.

Pros: avoids thresholds; maps well to preference/discriminator training.
Cons: requires tie-handling and a comparison rule.

---

## 5) Suggested generator / discriminator prompts for V2G

Because SummEval is multi-axis, it is usually cleanest to train/use **dimension-specific discriminators**, or a single model with **four heads**.

### Generator (G)
**Input:** source article

**Prompt skeleton:**
- “Write a summary of the following news article.”

(Optionally add length/style constraints.)

### Discriminator / validator (V)
**Input:** source article + candidate summary

**Dimension-specific prompt skeletons:**

**Consistency validator:**
- “Rate the factual consistency of the summary with respect to the article on a 1–5 scale. A consistent summary contains only statements entailed by the article. Penalize hallucinated facts.”

**Relevance validator:**
- “Rate relevance on a 1–5 scale: does the summary include the important information from the article and avoid unimportant/excess details?”

**Fluency validator:**
- “Rate fluency on a 1–5 scale: grammar, readability, formatting/capitalization; penalize fragments/ungrammatical text.”

**Coherence validator:**
- “Rate coherence on a 1–5 scale: organization and logical flow across sentences; not a heap of related facts.”

### Should we include the reference summary in the validator prompt?
Humans saw a **reference summary** in each group of 5 during annotation. Two possible approaches:
- **Mimic annotation setting:** include the reference summary as additional context.
- **Cleaner deployment setting:** omit the reference (often you won’t have it; also avoids anchoring).

Both are defensible; which is better depends on whether you’re trying to replicate *their* judgment protocol vs build a general-purpose factuality/relevance evaluator.

---

## Appendix: where we store examples

See `nnd-summeval-examples.md` for concrete prompt→multiple-candidate examples (and contrastive cases where a candidate is POS on one dimension but NEG on another).
