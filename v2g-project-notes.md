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
L_total = L_ranking + λ_G * NLL_generator + λ_V * NLL_validator_logodds
```

Where:
- `L_ranking` = pairwise ranking loss (V2G direction)
- `NLL_generator` = standard NLL on generator outputs
- `NLL_validator_logodds` = NLL on validator log odds

**Effect:** The NLL terms force the model to maintain meaningful probability distributions, preventing collapse to trivial solutions.

**Result:** This approach successfully avoids the degeneration issue!

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

### 2. Collie

- **Type:** Instruction following tasks
- (Awaiting more details on exact structure and source)

### 3. QA Datasets

**PlausibleQA:**
- Source: https://github.com/DataScienceUIBK/PlausibleQA
- Structure: 10K questions × 10 candidates each = 100K examples
- Each candidate has plausibility score (graded, not binary)
- Conversion: Use plausibility scores to determine correct/incorrect (threshold TBD)

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

## Open Questions

1. What are the λ weights for NLL terms?
2. Exact structure of Collie dataset for this task?
3. PlausibleQA threshold for binarizing plausibility scores?
4. Baseline results / current experimental status?
5. Which base models are we training on?

---

## Status

*Awaiting updates from Dancer on current experimental results and next steps.*

---

*Notes by John P. Lake 🐟 — 2026-02-10 01:34 UTC*
*Last updated: 2026-02-10*
