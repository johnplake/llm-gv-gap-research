# V2G Project: Modified RankAlign for Boosting Generators

**Goal:** Improve generator performance by training it to match validator rankings (V2G direction).

**Core hypothesis:** Validators may have access to knowledge that generators fail to express. By training generators to match validator rankings, we can "unlock" this hidden knowledge.

---

## Background: Why RankAlign Methodology is Suspect

**Original RankAlign approach:**
- Computes Pearson correlation ρ between generator log-odds and validator log-odds
- But computed **across ALL (question, answer) pairs globally**

**The problem:**
- This conflates within-question ranking consistency with cross-question calibration
- Comparing P(A|Q1) vs P(B|Q2) is meaningless — different prompts aren't comparable
- You can only meaningfully compare rankings **within the same question**

**Our fix:** Enforce same-prompt constraint throughout training and evaluation.

---

## Training

### Data Structure
- **Union of multiple datasets**
- Each dataset has: Question Q → Multiple candidate answers {A₁, A₂, ..., Aₙ}
- Need multiple answers per Q to form meaningful pairs

### Sampling Constraint (CRITICAL)
- Only pick pairs where **both prompts are identical** within each pair
- ✓ Correct: Compare (Q, A) vs (Q, B) — same Q, different answers
- ✗ Wrong: Compare (Q₁, A) vs (Q₂, B) — different Qs (not comparable)

### Training Objective
Train generator to match validator's ranking:
- If validator says P(Yes|Q,A) > P(Yes|Q,B)
- Then generator should have P(A|Q) > P(B|Q)

---

## Testing / Evaluation

### Metrics
1. **RankAlign paper metrics** — ρ correlation between generator and validator rankings
2. **Validator accuracy** — using threshold of 0 in log odds (log odds > 0 → Yes, else No)
3. **Generator ROC** — ROC curve for generator's ability to discriminate correct vs incorrect

### Methodological Fix for Evaluation
- **Test separately on each slice** where slice = all pairs sharing the same Q
- **Never compare across different Qs**
- Can aggregate by averaging metrics over all slices afterward
- This ensures we're measuring actual ranking consistency, not spurious cross-prompt correlations

---

## Modified Objective: Preventing Degeneration

### The Problem
Naive ranking loss causes **degeneration**: model learns to say "Yes" to everything (or assign high probability to everything). This trivially satisfies ranking constraints but is useless.

### The Solution: NLL Regularization
Add negative log-likelihood terms to the objective:

```
L_total = preference_loss_weight * L_ranking + nll_generator_weight * NLL_gen + nll_validator_weight * NLL_val
```

Where:
- `L_ranking` = pairwise ranking loss (V2G direction)
- `NLL_gen` = standard NLL on generator outputs
- `NLL_val` = NLL on validator log odds

**Effect:** The NLL terms force the model to maintain meaningful probability distributions, preventing collapse to trivial solutions.

**Result:** This approach successfully avoids the degeneration issue!

---

## Code Reference: `ranking_loss_ref.py`

**Location:** https://github.com/juand-r/rankalign/blob/longform/scripts/ranking_loss_ref.py

### Key Arguments

| Argument | Description |
|----------|-------------|
| `--train_g_or_d g` | **Mode "g" = V2G direction** (train generator to match validator) |
| `--train_g_or_d d` | G2V direction (train validator to match generator) |
| `--nll_validator_weight` | Weight for validator NLL term |
| `--nll_generator_weight` | Weight for generator NLL term |
| `--preference_loss_weight` | Weight for ranking loss (default 1.0) |
| `--force_same_x` | **Enforce same-prompt constraint** |
| `--typicality_correction` | Subtract completion frequency (see below) |
| `--length_normalize` | Normalize by completion length |
| `--validator_log_odds` | Use log(P(Yes)/P(No)) vs log(P(Yes)) |

### Typicality Correction

**Purpose:** Avoid favoring common/frequent completions just because they're typical.

**Method:** Compute GPT-2 unconditional log probability P(completion) and subtract it:
```
adjusted_score = model_score - gpt2_typicality_score
```

This isolates the model's *contextual* preference from general word frequency effects.

**Code function:** `compute_gpt2_typicality()` — computes P(completion) under GPT-2 for each candidate.

### Validator Scoring

```python
# Log-odds formulation (default)
val_score = log(P(Yes)) - log(P(No))

# Yes/No tokens include variants: "Yes", " Yes", "YES", "yes", " yes", etc.
```

### Generator Scoring

Two modes:
1. **Full completion:** Sum log probs over all tokens in completion
2. **First token only:** Just P(first_token | prompt)

Length normalization optional.

---

## Tasks / Datasets

### 1. Hypernymy (Custom Dataset)

**Prompt format:** "X is a kind of ___"

**Construction:**
- Selected various nouns: banana, car, elephant, etc.
- For each noun, sampled many completions from the model
- Labels: Correct/Incorrect — annotated using GPT-4

**Example:**
- Q: "Banana is a kind of ___"
- Candidates: fruit ✓, food ✓, vegetable ✗, animal ✗, plant ✓
- Each noun gives multiple (Q, A, label) triples

### 2. Collie (ICLR 2024)

**Paper:** "COLLIE: Systematic Construction of Constrained Text Generation Tasks"
- **Venue:** ICLR 2024
- **Authors:** Princeton NLP
- **GitHub:** https://github.com/princeton-nlp/Collie
- **arXiv:** https://arxiv.org/abs/2307.08689

**What it is:** Framework for constrained text generation tasks.

**Example constraints:**
- "Generate a sentence with exactly 5 words"
- "Generate a sentence containing the words 'have', 'rising', 'the'"
- Various structural constraints on outputs

**Our usage:**
- NOT using all of Collie
- Sampling some constraints and generating more answers
- Creates instruction-following tasks with verifiable correct/incorrect

### 3. QA Datasets

**PlausibleQA:**
- Source: https://github.com/DataScienceUIBK/PlausibleQA
- Structure: 10K questions × 10 candidates each = 100K examples
- Each candidate has plausibility score

**Label conversion (IMPORTANT):**
- **Positive (correct):** The one correct answer + additional correct ones sampled via GPT-5
- **Negative (incorrect):** All plausible-but-wrong answers
- NOT binarizing the plausibility scores — using semantic correctness

**AmbigQA:**
- Questions with ambiguous interpretations
- Multiple valid answers enumerated per question
- Good for cases where there isn't a single "right" answer

---

## Connections to Prior Work

### Inside-Out (Gekhman et al., COLM 2025)
- **Diagnosis:** Framework showing LLMs encode more knowledge than they express
- **Connection:** V2G is a **mitigation** — if validator "knows" more, train generator to match

### Original RankAlign (Rodriguez et al., COLM 2025)
- **Their finding:** G2V works better than V2G
- **Their hypothesis:** Generator is more calibrated than validator
- **Our angle:** With proper methodology (same-prompt pairs) and degeneration fix (NLL), can we make V2G work?

---

## Base Models

**Current:** Gemma-2-2B

**Planned expansion:**
- Larger sizes (7B, etc.)
- Other model families (Qwen, possibly others TBD)

**Training approach:** LoRA for memory-efficient fine-tuning (optional full fine-tuning)

---

## Current Status

**Status:** Shows promise but needs more investigation and tinkering.

**What's working:**
- Same-prompt constraint in training/eval
- NLL regularization prevents degeneration
- Multiple tasks set up (Hypernymy, Collie subset, PlausibleQA)
- Typicality correction available

**Next steps:**
- Investigate current results more deeply
- Tune hyperparameters (NLL weights, learning rate, etc.)
- Expand to larger models
- Test on more diverse tasks

---

## Summary of Key Differences from Original RankAlign

| Aspect | Original RankAlign | Our Approach |
|--------|-------------------|--------------|
| Direction | G2V (generator → validator) | **V2G (validator → generator)** |
| Pair comparison | Across all (Q,A) pairs | **Same-prompt only** |
| Degeneration | Not addressed | **NLL regularization** |
| Typicality | Not addressed | **GPT-2 frequency correction** |
| Evaluation | Global correlation | **Per-Q slice, then aggregate** |

---

*Notes by John P. Lake 🐟 — 2026-02-10 01:34 UTC*
*Last updated: 2026-02-10 02:19 UTC*
