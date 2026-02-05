# RankAlign: A Ranking View of the Generator-Validator Gap in Large Language Models

**Paper:** Rodriguez, Ding, Erk, Durrett (UT Austin)  
**Venue:** COLM 2025  
**arXiv:** https://arxiv.org/abs/2504.11381  
**Code:** https://github.com/juand-r/rankalign

---

## Core Problem: The Generator-Validator (G-V) Gap

LLMs are inconsistent between:
- **Generator mode**: "Complete: Olives are a kind of ___" → "fruit" (high probability)
- **Validator mode**: "Are olives fruit?" → "No" (contradicts generation!)

This is the **Generator-Validator Gap** — models disagree with their own generative responses when prompted discriminatively.

### Why This Matters
1. Models can generate wrong answers they'd reject if asked to validate
2. Models can validate correct answers they'd never generate
3. Critical for LLM-as-judge applications (evaluating arbitrary responses, not just high-confidence ones)
4. Reflects inconsistency in underlying "beliefs" or knowledge representation

---

## New Formulation: Correlation-Based Measurement

**Prior work** (Li et al. 2024b): Binary agreement — does validator accept the top generation?

**This paper**: Measure correlation of log-odds over the *entire* set of candidate answers.

### The Metric
- **Generator log-odds**: `l_G(z, y_A) = log(p(A|G(z)) / (1-p(A|G(z))))`
- **Validator log-odds**: `l_V(z, y_A) = log(p(Yes|V(z,y_A)) / p(No|V(z,y_A)))`
- **G-V Gap**: Pearson correlation ρ between l_G and l_V over all (question, answer) pairs

Low correlation = large gap = inconsistent model.

---

## RankAlign: The Training Method

### Key Insight
If generator prefers answer A over B (higher probability), validator should too (higher "Yes" probability).

### Loss Function (G2V — Generator to Validator)
Train validator to match generator's rankings:

```
L_G2V = -E[log σ(β[log p(Yes|x_Vw) - log p(Yes|x_Vl)])]
```

Where x_Vw is the validator prompt for the "winner" (higher generator probability) and x_Vl for the "loser."

This is **pairwise logistic loss** — pushes P(Yes|winner) > P(Yes|loser).

### Variants
- **RankAlign-V2G**: Train generator to match validator rankings (less effective)
- **RankAlign-α**: Convex combination of both (α=0.5)

### Why Not Just DPO?
DPO aligns preferences *for a fixed prompt*. RankAlign aligns preferences *across prompts for a fixed completion* ("Yes").

---

## Results

### Main Findings
- **31.8% average improvement** in ρ-all across models and tasks
- Works on: QA (TriviaQA), Lexical semantics (Hypernymy, SWORDS), Next-word prediction (LAMBADA)
- Models tested: Gemma-2-2B, Llama-3.2-3B, Llama-3.1-8B

### Specific Results (Gemma-2-2B on Hypernymy)
- Base: ρ-all = 65.7
- RankAlign: ρ-all = 94.2 (nearly closed!)

### Generalization
- ✅ Cross-task: Training on Hypernymy improves SWORDS
- ✅ Lexical: No overlap in train/test vocabulary still works
- ✅ Prompt format: Different prompt templates still improve

### Accuracy Trade-off
- Mild degradation on task accuracy (acceptable)
- SFT maintains higher raw accuracy but doesn't close the gap

---

## Key Insights

### 1. Generator Is More Calibrated
RankAlign-G2V outperforms RankAlign-V2G. Hypothesis: Base LLM generator probabilities are better calibrated; validator behavior is more heavily induced by alignment (and may be poorly calibrated).

### 2. Gricean Pragmatics
Not all low-generator / high-validator cases are errors. "Dolphins are entities" is *true* but uninformative (Gricean violation). The paper focuses on cases where this doesn't apply.

### 3. Connection to Inside-Out
Paper cites **Gekhman et al. (2025)** — "Inside-Out: Hidden Factual Knowledge in LLMs" — noting:
> "LLMs encode significantly more factual knowledge in their parameters than they express in their outputs."

RankAlign provides a **mitigation method** for this gap.

---

## Relation to Dancer's Research

This complements the Inside-Out paper:
- **Inside-Out**: Diagnoses the gap (framework for measuring hidden vs. expressed knowledge)
- **RankAlign**: Mitigates the gap (training method to align generator/validator)

**Research angle**: Could combine these — use Inside-Out probing to identify problematic cases, then apply RankAlign-style training selectively.

---

## Questions / Future Directions

1. Does RankAlign work for long-form generation? (Paper focuses on short-form)
2. Can we selectively apply G2V vs V2G based on which is more accurate per-sample?
3. How does this interact with chain-of-thought or reasoning?
4. Mechanistic understanding: *why* does the gap exist in the first place?

---

## References to Chase

- Li et al. (2024b) — "Benchmarking and improving generator-validator consistency" (ICLR 2024)
- Gekhman et al. (2025) — "Inside-Out: Hidden Factual Knowledge in LLMs" (COLM 2025)
- West et al. (2024) — "The Generative AI Paradox" (ICLR 2024)
- Kadavath et al. (2022) — "Language models (mostly) know what they know"

---

*Notes by John P. Lake 🐟 — 2026-02-05*
