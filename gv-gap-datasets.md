# Tasks & Datasets for Generator-Validator Gap Research

Curated for exploring the "knows but doesn't say" phenomenon.

---

## 1. Factual Knowledge Probing

### LAMA (LAnguage Model Analysis)
- **What:** Subject-relation-object triples as cloze prompts
- **Source:** Facebook Research (https://github.com/facebookresearch/LAMA)
- **Why good for G-V:** Natural generator (fill mask) vs validator (is X the answer?) setup
- **Subsets:** T-REx (Wikidata triples), Google-RE, ConceptNet, SQuAD

### LAMA-TREx Variants
- **LAMA-TREx_UHN:** Removes "easy" examples (unhelpful names filtered)
- **LAMA-easy / LAMA-hard:** Partitioned by difficulty
- **Good for:** Studying where internal knowledge exists but generation fails

### PopQA / EntityQuestions
- **What:** Entity-centric factual questions with popularity metadata
- **Why good:** Can stratify by entity frequency — rare entities may show larger gaps

---

## 2. Commonsense Reasoning

### CommonsenseQA
- **What:** 12K multiple-choice questions requiring commonsense knowledge
- **Source:** https://huggingface.co/datasets/tau/commonsense_qa
- **Why good for G-V:** Can compare generation (open-ended) vs selection (MCQ)

### HellaSwag / SWAG
- **What:** Sentence completion with adversarial distractors
- **Why good:** Discriminator task by design — easy to probe generator probability of correct completion

### WinoGrande
- **What:** Pronoun resolution requiring commonsense
- **Why good:** Binary choice enables clean validator formulation

### PIQA (Physical Intuition QA)
- **What:** Physical commonsense reasoning (which action achieves goal?)
- **Why good:** Tests implicit physical knowledge

### SIQA (Social Intelligence QA)
- **What:** Social/emotional commonsense
- **Why good:** Models may "know" social norms but not express them

---

## 3. Natural Language Inference (NLI)

### SNLI / MNLI
- **What:** Premise-hypothesis pairs labeled entailment/neutral/contradiction
- **Source:** Stanford NLI, Multi-Genre NLI
- **Why good for G-V:** 
  - Generator: Given premise, generate entailed hypothesis
  - Validator: Does this hypothesis follow from premise?
- **Bonus:** Human disagreement data available (graded judgments)

### ANLI (Adversarial NLI)
- **What:** Adversarially constructed NLI examples
- **Why good:** Specifically targets model failures — likely shows gaps

---

## 4. Lexical Semantics

### SWORDS (used in RankAlign)
- **What:** Lexical substitution — can word X replace word Y in context?
- **Why good:** Already proven to show G-V gap

### WiC (Words in Context)
- **What:** Binary — do two uses of a word have same sense?
- **Source:** SuperGLUE
- **Why good for G-V:** Validator task; can construct generator version

### Word Sense Disambiguation (WSD)
- **Datasets:** SemCor, SemEval, CoarseWSD-20, hardEN
- **Why good:** Models may internally represent sense distinctions they don't generate

### THINGS (used in RankAlign)
- **What:** Hypernymy — IS-A relations with graded similarity
- **Why good:** Already proven to show G-V gap

---

## 5. Reading Comprehension / QA

### TriviaQA (used in RankAlign)
- **What:** Open-domain QA from trivia sources
- **Already shown:** G-V gap exists

### SQuAD / SQuAD 2.0
- **What:** Extractive QA from Wikipedia
- **Why good:** Can compare span extraction (generator) vs verification (validator)

### Natural Questions
- **What:** Real Google queries with Wikipedia answers
- **Why good:** Naturalistic distribution of difficulty

### BoolQ
- **What:** Yes/No questions about passages
- **Why good:** Already in validator format; can construct generator version

---

## 6. Cloze / Language Modeling

### LAMBADA (used in RankAlign)
- **What:** Final word prediction requiring long-range context
- **Already shown:** G-V gap exists

### Children's Book Test (CBT)
- **What:** Cloze task over children's stories
- **Why good:** Named entities vs common nouns show different patterns

---

## 7. Generation Quality / Consistency

### TruthfulQA
- **What:** Questions designed to elicit false answers
- **Why good:** Models may "know" the truth but generate falsehoods

### HaluEval
- **What:** Hallucination evaluation benchmark
- **Why good:** Directly targets cases where internal knowledge diverges from output

### FActScore
- **What:** Fine-grained atomic fact scoring for biographies
- **Why good:** Can probe internal knowledge of each atomic fact

---

## 8. Math / Reasoning

### GSM8K
- **What:** Grade school math word problems
- **Why good:** Models may verify correct answers they can't generate (P vs NP intuition)

### MATH
- **What:** Competition-level math
- **Why good:** Extreme version of above

---

## Recommended Priority for G-V Research

**Tier 1 (directly applicable, proven gaps):**
1. LAMA / LAMA-TREx — canonical knowledge probing
2. TriviaQA — already studied in RankAlign
3. CommonsenseQA — clean MCQ format
4. SWORDS / THINGS — lexical, already proven

**Tier 2 (high potential, needs adaptation):**
5. SNLI/MNLI — rich for G-V formulation
6. TruthfulQA — targets the core problem
7. HellaSwag — adversarial, discriminative
8. BoolQ — natural validator format

**Tier 3 (interesting extensions):**
9. GSM8K — math reasoning
10. WSD benchmarks — lexical ambiguity
11. FActScore — fine-grained factuality

---

## Key Criteria for Task Selection

1. **Natural generator/validator formulations** — can easily construct both prompts
2. **Graded or probabilistic answers** — not just binary correct/incorrect
3. **Known model weaknesses** — tasks where models underperform relative to capability
4. **Difficulty stratification** — can isolate "hard" cases where gap is largest
5. **Human baseline available** — to calibrate what "should know" means

---

*Compiled by John P. Lake 🐟 — 2026-02-05*
