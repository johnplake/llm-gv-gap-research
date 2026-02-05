# Dataset Structure: Positive/Negative Examples per Prompt

For G-V gap research, we need datasets with clear positive AND negative examples per prompt/question. This table summarizes the structure.

---

## Summary Table

| Dataset | Pos per Q | Neg per Q | Total Examples | Structure | Notes |
|---------|-----------|-----------|----------------|-----------|-------|
| **LAMA/TREx** | 1 | 0 (implicit) | ~34K | Cloze completion | Only correct answer provided; negatives = all other tokens |
| **CommonsenseQA** | 1 | 4 | 12,102 | 5-way MCQ | Clean structure for G-V |
| **TruthfulQA** | 1-4 | 1-4 | 817 | Variable MCQ or binary | Binary version: 1 correct, 1 "best incorrect" |
| **HellaSwag** | 1 | 3 | ~10K | 4-way MCQ | Adversarially constructed negatives |
| **SWAG** | 1 | 3 | 113K | 4-way MCQ | Predecessor to HellaSwag |
| **SNLI** | ~1 | ~2 | 570K | 3-class per pair | 1 entailment, 1 contradiction, 1 neutral per premise |
| **MNLI** | ~1 | ~2 | 433K | 3-class per pair | Multi-genre version of SNLI |
| **SWORDS** | Variable | Variable | ~27K substitutes | Graded ratings | Avg 4.1 substitutes per target; ratings indicate quality |
| **THINGS (Hypernymy)** | 1 | 1 | Balanced | Binary per pair | Explicitly balanced pos/neg by Rodriguez et al. |
| **WinoGrande** | 1 | 1 | ~44K | Binary choice | Two options per sentence, one correct |
| **BoolQ** | 1 | 0 | 15,942 | Yes/No per passage | ~62% Yes, 38% No (imbalanced across dataset) |
| **TriviaQA** | 1+ | 0 (implicit) | 95K | Open-ended QA | Multiple answer aliases; no explicit negatives |
| **LAMBADA** | 1 | 0 (implicit) | 10K | Word completion | Single correct final word |
| **GSM8K** | 1 | 0 (implicit) | 8.5K | Math word problems | Single correct numeric answer |

---

## Detailed Notes

### Tier 1: Best for G-V Research (explicit pos/neg per question)

**CommonsenseQA**
- Structure: Question → 5 choices (1 correct, 4 distractors)
- Perfect for G-V: Can compare P(generate correct) vs P(validate each choice)
- Distractors from ConceptNet, semantically related but wrong

**HellaSwag / SWAG**
- Structure: Context → 4 completions (1 correct, 3 adversarial)
- Negatives specifically designed to fool models
- Great for probing the gap on "should know" cases

**THINGS (Hypernymy)**
- Structure: (hyponym, hypernym) pairs, balanced pos/neg
- Already proven in RankAlign paper
- Negatives are semantically similar non-hypernyms

**WinoGrande**
- Structure: Sentence with blank → 2 options
- Binary choice, balanced
- Tests commonsense pronoun resolution

### Tier 2: Good with some adaptation

**SNLI/MNLI**
- Structure: Premise → Hypothesis → {entailment, contradiction, neutral}
- For G-V: Given premise, can model generate entailed hypothesis? Does it validate correctly?
- **Key insight**: Each premise has ~3 hypotheses (one per class), giving natural pos/neg
- Rich human disagreement data available (5 annotators per example)

**TruthfulQA**
- Binary version: 1 correct + 1 "best incorrect" answer per question
- MCQ version: Variable choices (standardized to 4 in some versions)
- Specifically targets cases where models should know truth but generate falsehoods

**SWORDS**
- Structure: (context, target word) → multiple substitutes with graded ratings
- Avg 4.1 substitutes per target
- Can threshold ratings to create pos/neg splits
- Already proven in RankAlign paper

### Tier 3: Requires negative construction

**LAMA/TREx**
- Only provides correct answers
- Negatives must be constructed (e.g., other entities of same type, random tokens)
- Can use entity type constraints for meaningful negatives

**TriviaQA / LAMBADA / GSM8K**
- Only correct answers provided
- Need to sample incorrect answers (from model, from corpus, etc.)
- RankAlign paper did this by sampling model generations

**BoolQ**
- Each question has single Yes/No answer
- Not naturally paired pos/neg
- Could construct by pairing semantically similar questions with opposite answers

---

## Recommendations for G-V Research

### Best bets (no modification needed):
1. **CommonsenseQA** — Clean 5-way MCQ, 12K examples
2. **HellaSwag** — Adversarial 4-way, ~10K examples  
3. **THINGS** — Balanced binary hypernymy, proven in RankAlign
4. **WinoGrande** — Binary commonsense, ~44K examples
5. **TruthfulQA (binary)** — Targets the exact problem, 817 examples

### Good with grouping/adaptation:
6. **SNLI/MNLI** — Group by premise to get pos/neg hypothesis pairs
7. **SWORDS** — Threshold ratings for pos/neg

### Require negative sampling:
8. **LAMA** — Sample negatives from same entity type
9. **TriviaQA** — Sample wrong answers from model or similar questions
10. **GSM8K** — Sample wrong numeric answers (or wrong reasoning paths)

---

## Key Insight: What Makes a Good G-V Dataset

For studying the generator-validator gap, you need:

1. **Explicit positives AND negatives per question** — to measure both directions of the gap
2. **Semantically meaningful negatives** — random wrong answers don't probe "knows but doesn't say"
3. **Multiple candidates per question** — to measure correlation, not just binary agreement
4. **Difficulty stratification** — to isolate where the gap is largest

CommonsenseQA and HellaSwag hit all four criteria. LAMA/TriviaQA require work to add negatives.

---

*Compiled by John P. Lake 🐟 — 2026-02-05*
