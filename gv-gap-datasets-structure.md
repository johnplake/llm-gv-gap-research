# Dataset Structure: Positive/Negative Examples per Prompt

For G-V gap research, we need datasets with MANY positives AND negatives per prompt/question. 

---

## 🌟 HIGH-DENSITY DATASETS (Many candidates per question)

These are the best for G-V gap research because they provide multiple graded candidates:

### PlausibleQA ⭐⭐⭐ (BEST FIND)
- **Structure:** 10K questions × 10 candidate answers = **100K total**
- **Positives:** 1 correct + multiple "plausible" answers with graded scores
- **Negatives:** Multiple implausible answers with graded scores
- **Bonus:** 900K pairwise comparison justifications
- **Paper:** SIGIR 2025, arXiv:2502.16358
- **GitHub:** https://github.com/DataScienceUIBK/PlausibleQA
- **Why perfect:** Explicit plausibility scores for each answer, designed for exactly this problem

### ChaosNLI ⭐⭐⭐
- **Structure:** 4,645 NLI examples × **100 annotations each** = 464K annotations
- **Source:** Subset of SNLI, MNLI, Abductive-NLI
- **Key insight:** 100 human judgments per example reveals natural disagreement
- **Labels:** Each annotator picks entailment/neutral/contradiction
- **Paper:** EMNLP 2020, arXiv:2010.03532
- **GitHub:** https://github.com/easonnie/ChaosNLI
- **Why perfect:** Distribution over labels gives graded pos/neg signal

### CoInCo (Concepts in Context) ⭐⭐
- **Structure:** ~15K target words, **6+ substitutes per target**
- **Type:** Lexical substitution (all-words annotation)
- **Source:** MASC corpus (news + fiction)
- **URL:** https://www.ims.uni-stuttgart.de/en/research/resources/corpora/coinco/
- **Why good:** Every content word annotated with multiple valid substitutes

### SWORDS ⭐⭐
- **Structure:** 1,132 targets × **~4.1 substitutes per target** (graded ratings)
- **Type:** Lexical substitution with quality ratings
- **Key feature:** Human ratings of substitute appropriateness (not binary)
- **Paper:** NAACL 2021
- **GitHub:** https://github.com/p-lambda/swords
- **Why good:** Already proven in RankAlign paper

### AmbigQA ⭐⭐
- **Structure:** Questions with **multiple valid answers** (inherently ambiguous)
- **Type:** Open-domain QA where ambiguity yields multiple correct answers
- **Example:** "When did the US enter WW2?" → multiple valid dates depending on interpretation
- **Paper:** EMNLP 2020
- **GitHub:** https://github.com/shmsw25/AmbigQA
- **Why good:** Multiple genuinely correct answers per question

### ALaSca (Large-Scale Lexical Substitution) ⭐⭐
- **Structure:** Large-scale, automatically constructed
- **Type:** Silver-standard substitutes for lexical substitution
- **URL:** https://sapienzanlp.github.io/alasca/
- **Why good:** Much larger scale than manually annotated datasets

---

## MODERATE-DENSITY DATASETS (4-5 choices per question)

These have fixed MCQ structure but fewer candidates:

| Dataset | Choices | Total Qs | Negative Quality |
|---------|---------|----------|------------------|
| CommonsenseQA | 1+4 | 12K | ConceptNet distractors |
| HellaSwag | 1+3 | 10K | Adversarial (model-generated) |
| SWAG | 1+3 | 113K | Adversarial |
| WinoGrande | 1+1 | 44K | Balanced binary |
| ARC (Easy/Challenge) | 1+3 | 7.8K | Science exam distractors |
| OpenBookQA | 1+3 | 6K | Requires reasoning |
| RACE | 1+3 | 100K | Human-written (exams) |
| SciQ | 1+3 | 13.7K | Science domain |
| QASC | 1+7 | 9.9K | **8 choices total** |
| MedMCQA | 1+3 | 194K | Medical domain |

---

## DATASETS REQUIRING CANDIDATE CONSTRUCTION

These only provide correct answers — negatives must be constructed:

| Dataset | Total | Notes on Negative Construction |
|---------|-------|-------------------------------|
| LAMA/TREx | 34K | Sample from same entity type |
| TriviaQA | 95K | Sample from similar questions |
| Natural Questions | 300K+ | Sample from corpus |
| LAMBADA | 10K | Sample other plausible words |
| SQuAD 2.0 | 150K | Has unanswerable Qs (partial negatives) |
| GSM8K | 8.5K | Sample wrong numeric answers |

---

## GRADED SIMILARITY/RELATEDNESS DATASETS

These provide continuous scores rather than binary labels:

| Dataset | Pairs | Scale | Notes |
|---------|-------|-------|-------|
| SimLex-999 | 999 | 0-10 | Similarity (not relatedness) |
| WordSim-353 | 353 | 0-10 | Relatedness |
| MEN | 3,000 | 0-50 | Relatedness |
| RG-65 | 65 | 0-4 | Classic word similarity |
| CoSimLex | 340 | 0-10 | Context-dependent similarity |

---

## RECOMMENDED PRIORITY FOR G-V RESEARCH

### Tier 1: Use immediately (high density, graded)
1. **PlausibleQA** — 10 candidates per Q with plausibility scores ⭐⭐⭐
2. **ChaosNLI** — 100 annotations per example, natural distribution ⭐⭐⭐
3. **CoInCo** — 6+ substitutes per target ⭐⭐

### Tier 2: Good with some processing
4. **SWORDS** — Graded substitute ratings, proven in RankAlign
5. **AmbigQA** — Multiple valid answers per question
6. **QASC** — 8 choices per question (more than typical MCQ)

### Tier 3: Standard MCQ (fewer candidates but high quality)
7. **CommonsenseQA** — 5 choices, semantic distractors
8. **HellaSwag** — 4 choices, adversarial

### Tier 4: Need to construct negatives
9. **LAMA** — Classic knowledge probing (must add negatives)
10. **TriviaQA** — Large scale (must add negatives)

---

## KEY INSIGHT

**For measuring G-V correlation, you want:**
- Many candidates per question (not just 4-5)
- Graded plausibility/quality scores (not just binary)
- Both positives AND negatives with varying degrees

**PlausibleQA is the gold standard** — it was literally designed for this:
> "a large-scale dataset comprising 10,000 questions and 100,000 candidate answers, each annotated with plausibility scores"

**ChaosNLI is great for NLI** — 100 human judgments per example reveals the true distribution of opinions, not just majority vote.

---

*Updated by John P. Lake 🐟 — 2026-02-05*
