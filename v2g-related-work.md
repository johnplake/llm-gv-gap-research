# Related Work: Generator-Validator Gap and V2G Research

This document provides a comprehensive literature review for research on improving LLM generators by training them to match validator rankings (V2G direction).

---

## 1. Generator-Validator Inconsistency

This section covers papers that directly study the gap between LLMs' generation capabilities and their discrimination/validation abilities.

### Core Papers

#### RankAlign: A Ranking View of the Generator-Validator Gap in Large Language Models
**Rodriguez et al., COLM 2025** [[arXiv:2504.11381](https://arxiv.org/abs/2504.11381)]

- **Key Contribution:** Introduces a ranking-based view of the generator-validator gap, measuring correlation between log-odds assigned by generators and validators. Proposes RankAlign, a ranking-based training method.
- **Key Finding:** Shows that a large gap exists in various settings (QA, lexical semantics, next-word prediction). RankAlign closes the gap by 31.8% on average.
- **Relation to Our Work:** This is the foundational paper for the V2G research direction. Our work builds on and extends this framework.

#### Inside-Out: Hidden Factual Knowledge in LLMs
**Gekhman et al., COLM 2025** [[arXiv:2503.15299](https://arxiv.org/abs/2503.15299)]

- **Key Contribution:** Presents a framework for assessing whether LLMs encode more factual knowledge internally than they express in outputs. Demonstrates that some knowledge is "deeply hidden" and never generated despite repeated sampling.
- **Key Finding:** LLMs encode significantly more factual knowledge in their parameters than what they express in their outputs.
- **Relation to Our Work:** Provides strong evidence for the existence of latent knowledge that V2G methods could help surface.

#### The Generative AI Paradox: "What It Can Create, It May Not Understand"
**West et al., ICLR 2024** [[arXiv:2311.00059](https://arxiv.org/abs/2311.00059)]

- **Key Contribution:** Formulates and tests the hypothesis that generative models acquire generative capabilities not contingent upon understanding. Shows models outperform humans in generation but fall short in discrimination.
- **Key Finding:** Generation and discrimination follow different capability curves; models can generate content they cannot reliably evaluate.
- **Relation to Our Work:** Provides empirical foundation for the generation-discrimination gap. Our V2G approach addresses this by leveraging validation capabilities during training.

#### Language Models (Mostly) Know What They Know
**Kadavath et al., 2022** [[arXiv:2207.05221](https://arxiv.org/abs/2207.05221)]

- **Key Contribution:** Studies whether LLMs can evaluate validity of their own claims and predict which questions they can answer correctly. Introduces P(True) and P(IK) ("I Know") approaches.
- **Key Finding:** Larger models are well-calibrated on multiple choice questions when provided in the right format. Models can partially generalize P(IK) across tasks.
- **Relation to Our Work:** Foundational evidence that LLMs have internal representations of their own uncertainty/knowledge, which V2G methods can leverage.

### Related Papers on Generation-Discrimination Gap

#### Self-critiquing Models for Assisting Human Evaluators
**Saunders et al., 2022** [[OpenAI Technical Report](https://cdn.openai.com/papers/critiques.pdf)]

- **Key Contribution:** Proposes fine-tuning LLMs to generate natural language critiques. Introduces the concept of generation-discrimination gap (G-D gap).
- **Key Finding:** Recognition of errors may be easier than avoiding them. Models can generate outputs they "know" have flaws.
- **Relation to Our Work:** Early formulation of the G-D gap that motivates V2G training approaches.

#### Benchmarking and Improving Generator-Validator Consistency of Language Models
**Li et al., ICLR 2024** [[arXiv:2310.01846](https://arxiv.org/abs/2310.01846)]

- **Key Contribution:** Proposes a framework for measuring consistency between generation and validation. Develops approaches to improve this inconsistency.
- **Key Finding:** Inconsistency between generating and validating answers is prevalent in LLMs and erodes trust.
- **Relation to Our Work:** Provides benchmarks and methods complementary to our ranking-based V2G approach.

#### Self-[In]Correct: LLMs Struggle with Discriminating Self-Generated Responses
**Huang et al., 2024** [[arXiv:2404.04298](https://arxiv.org/abs/2404.04298)]

- **Key Contribution:** Unified framework comparing generative and discriminative capabilities. Challenges the assumption that LLMs can self-improve through self-evaluation.
- **Key Finding:** LLMs do not reliably perform better at discrimination than generation across most tasks.
- **Relation to Our Work:** Highlights the difficulty of leveraging self-evaluation, motivating external validator signals.

#### Shrinking the Generation-Verification Gap with Weak Verifiers
**Saad-Falcon et al., 2025** [[arXiv:2506.18203](https://arxiv.org/abs/2506.18203)]

- **Key Contribution:** Proposes Weaver, a method that leverages weak supervision to combine multiple weak verifiers.
- **Key Finding:** LM-based judges produce noisy, biased, and poorly calibrated scores; aggregation helps.
- **Relation to Our Work:** Complementary approach that could be combined with V2G training.

---

## 2. Knowledge in LLMs: Hidden/Latent Knowledge and Probing

### Probing and Internal Representations

#### LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations
**Orgad et al., ICLR 2025** [[arXiv:2410.02707](https://arxiv.org/abs/2410.02707)]

- **Key Contribution:** Reveals that internal representations encode much more information about truthfulness than previously recognized. Shows LLMs can distinguish correct from hallucinated content internally.
- **Key Finding:** The internal states of LLMs encode truthfulness information even when outputs are incorrect.
- **Relation to Our Work:** Demonstrates the information is there to be exploited; V2G training can help surface this knowledge.

#### The Internal State of an LLM Knows When It's Lying
**Azaria & Mitchell, EMNLP Findings 2023** [[arXiv:2304.13734](https://arxiv.org/abs/2304.13734)]

- **Key Contribution:** Trains classifiers on LLM hidden layer activations to predict statement truthfulness. Achieves 71-83% accuracy.
- **Key Finding:** LLM internal state can reveal truthfulness of both provided and self-generated statements.
- **Relation to Our Work:** Evidence that validation signals exist internally; V2G can help externalize this through ranking loss.

#### The Geometry of Truth: Emergent Linear Structure in LLM Representations
**Marks & Tegmark, COLM 2024** [[arXiv:2310.06824](https://arxiv.org/abs/2310.06824)]

- **Key Contribution:** Shows that at sufficient scale, LLMs linearly represent truth/falsehood of factual statements. Probes generalize across datasets.
- **Key Finding:** Simple difference-in-mean probes identify "truth directions" that transfer across topics.
- **Relation to Our Work:** The linear structure suggests ranking-based training could effectively leverage this geometry.

#### Discovering Latent Knowledge in Language Models Without Supervision
**Burns et al., ICLR 2023** [[arXiv:2212.03827](https://arxiv.org/abs/2212.03827)]

- **Key Contribution:** Introduces Contrast-Consistent Search (CCS) for finding latent knowledge without supervision using contrast pairs.
- **Key Finding:** Can recover diverse knowledge from activations even when outputs are misleading.
- **Relation to Our Work:** Unsupervised approach to accessing latent knowledge; V2G provides a training-time alternative.

### Representation Engineering

#### Representation Engineering: A Top-Down Approach to AI Transparency
**Zou et al., 2023** [[arXiv:2310.01405](https://arxiv.org/abs/2310.01405)]

- **Key Contribution:** Introduces representation engineering (RepE) for reading and controlling LLM behavior through activation manipulation.
- **Key Finding:** Steering "truthfulness" direction increases TruthfulQA accuracy by up to 30 percentage points.
- **Relation to Our Work:** Inference-time intervention; V2G achieves similar goals through training-time alignment.

#### Inference-Time Intervention: Eliciting Truthful Answers from a Language Model
**Li et al., NeurIPS 2023** [[arXiv:2306.03341](https://arxiv.org/abs/2306.03341)]

- **Key Contribution:** ITI shifts model activations during inference to enhance truthfulness using only a few hundred examples.
- **Key Finding:** LLMs have internal representations of truthfulness even as they produce falsehoods on the surface.
- **Relation to Our Work:** ITI modifies inference; V2G modifies training to achieve persistent improvements.

#### Patchscopes: A Unifying Framework for Inspecting Hidden Representations
**Ghandeharioun et al., 2024** [[arXiv:2401.06102](https://arxiv.org/abs/2401.06102)]

- **Key Contribution:** Unifies various interpretability methods (probing, vocabulary projection) into a single framework.
- **Key Finding:** Representations can be decoded into natural language explanations.
- **Relation to Our Work:** Provides tools for understanding what knowledge is hidden that V2G could surface.

---

## 3. Preference Learning and Alignment

### Foundational Methods

#### Training Language Models to Follow Instructions with Human Feedback (InstructGPT)
**Ouyang et al., NeurIPS 2022** [[arXiv:2203.02155](https://arxiv.org/abs/2203.02155)]

- **Key Contribution:** Introduces RLHF pipeline: SFT → Reward Model → PPO. Creates InstructGPT.
- **Key Finding:** 1.3B InstructGPT preferred over 175B GPT-3; RLHF dramatically improves instruction following.
- **Relation to Our Work:** Establishes the preference learning paradigm that V2G extends with ranking objectives.

#### Direct Preference Optimization: Your Language Model is Secretly a Reward Model
**Rafailov et al., NeurIPS 2023** [[arXiv:2305.18290](https://arxiv.org/abs/2305.18290)]

- **Key Contribution:** Eliminates explicit reward modeling by reparameterizing the RL objective into a classification loss on preferences.
- **Key Finding:** DPO matches or exceeds PPO-based RLHF while being simpler to implement.
- **Relation to Our Work:** DPO uses pairwise preferences; V2G/RankAlign extends to listwise ranking objectives for richer signal.

#### Constitutional AI: Harmlessness from AI Feedback
**Bai et al., 2022** [[arXiv:2212.08073](https://arxiv.org/abs/2212.08073)]

- **Key Contribution:** Introduces RLAIF (RL from AI Feedback) using a constitution of principles. Model critiques and revises its own outputs.
- **Key Finding:** Can train harmless, non-evasive assistants with minimal human labels.
- **Relation to Our Work:** Uses AI as validator; V2G formalizes the validator signal as ranking.

### DPO Variants and Extensions

#### SimPO: Simple Preference Optimization with a Reference-Free Reward
**Meng et al., NeurIPS 2024** [[arXiv:2405.14734](https://arxiv.org/abs/2405.14734)]

- **Key Contribution:** Removes reference model requirement from DPO using length-normalized log-likelihood as reward.
- **Key Finding:** Outperforms DPO on AlpacaEval 2, MT-Bench, and Arena-Hard.
- **Relation to Our Work:** Alternative objective formulation; V2G's ranking approach is complementary.

#### KTO: Model Alignment as Prospect Theoretic Optimization
**Ethayarajh et al., 2024**

- **Key Contribution:** Applies prospect theory to preference optimization, allowing unpaired preference data.
- **Key Finding:** Works well even without paired preferences.
- **Relation to Our Work:** Different approach to extracting signal from preferences.

#### LiPO: Listwise Preference Optimization through Learning-to-Rank
**Liu et al., NAACL 2025** [[arXiv:2402.01878](https://arxiv.org/abs/2402.01878)]

- **Key Contribution:** Formulates LM alignment as a listwise ranking problem. Introduces LiPO-λ using DCG-weighted listwise loss.
- **Key Finding:** Listwise objectives can be more effective than pairwise objectives for preference optimization.
- **Relation to Our Work:** Directly related; V2G/RankAlign uses similar ranking-based training insights.

### Self-Improvement and Reward Modeling

#### Self-Rewarding Language Models
**Yuan et al., ICML 2024** [[arXiv:2401.10020](https://arxiv.org/abs/2401.10020)]

- **Key Contribution:** LLMs serve as both generator and judge, iteratively improving through self-evaluation.
- **Key Finding:** Llama 2 70B fine-tuned this way outperforms Claude 2, Gemini Pro, GPT-4 on AlpacaEval 2.0.
- **Relation to Our Work:** Uses self-validation; V2G leverages the validator more systematically through ranking.

#### Scaling Laws for Reward Model Overoptimization
**Gao et al., ICML 2023** [[arXiv:2210.10760](https://arxiv.org/abs/2210.10760)]

- **Key Contribution:** Studies how optimizing against proxy reward models leads to reward hacking. Derives scaling laws.
- **Key Finding:** Gold reward initially increases then decreases with optimization; coefficients scale with RM size.
- **Relation to Our Work:** V2G training must be careful about over-optimization; ranking losses may be more robust.

---

## 4. Calibration and Uncertainty

#### On Calibration of Modern Neural Networks
**Guo et al., ICML 2017**

- **Key Contribution:** Shows modern neural networks are poorly calibrated (overconfident). Introduces temperature scaling.
- **Key Finding:** Expected Calibration Error (ECE) is standard metric; temperature scaling is effective post-hoc.
- **Relation to Our Work:** Foundational work on calibration; LLM calibration is a related but distinct problem.

#### Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
**Xiong et al., ICLR 2024** [[arXiv:2306.13063](https://arxiv.org/abs/2306.13063)]

- **Key Contribution:** Evaluates various methods for eliciting confidence from LLMs (verbalized, consistency-based, etc.).
- **Key Finding:** Verbalized confidence is often poorly calibrated; consistency-based methods work better.
- **Relation to Our Work:** V2G training could improve self-consistency and calibration through ranking alignment.

#### A Survey of Confidence Estimation and Calibration in Large Language Models
**Geng et al., 2024** [[arXiv:2311.08298](https://arxiv.org/abs/2311.08298)]

- **Key Contribution:** Comprehensive survey of confidence estimation methods for LLMs.
- **Key Finding:** Different methods work for different settings; no universal solution.
- **Relation to Our Work:** V2G may help close the gap between internal and expressed confidence.

#### Large Language Models Must Be Taught to Know What They Don't Know
**Banda et al., NeurIPS 2024**

- **Key Contribution:** Shows LLMs need explicit training to express uncertainty well; proposes calibration tuning.
- **Key Finding:** Off-the-shelf LLMs struggle with uncertainty; fine-tuning helps significantly.
- **Relation to Our Work:** V2G training is a form of calibration tuning using ranking signals.

---

## 5. Self-Consistency and Self-Evaluation

#### Self-Consistency Improves Chain of Thought Reasoning in Language Models
**Wang et al., ICLR 2023** [[arXiv:2203.11171](https://arxiv.org/abs/2203.11171)]

- **Key Contribution:** Proposes sampling multiple reasoning paths and selecting the most consistent answer via majority voting.
- **Key Finding:** Substantial improvements on arithmetic and commonsense reasoning (e.g., +17.9% on GSM8K).
- **Relation to Our Work:** Self-consistency at inference time; V2G aims to improve consistency through training.

#### Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
**Wei et al., NeurIPS 2022** [[arXiv:2201.11903](https://arxiv.org/abs/2201.11903)]

- **Key Contribution:** Shows that including intermediate reasoning steps dramatically improves performance on complex tasks.
- **Key Finding:** CoT is an emergent ability that appears with scale.
- **Relation to Our Work:** CoT improves generation quality; V2G training could help models better select among CoT outputs.

#### Large Language Models Can Self-Improve
**Huang et al., 2022** [[arXiv:2210.11610](https://arxiv.org/abs/2210.11610)]

- **Key Contribution:** Shows LLMs can improve through self-generated rationales without external supervision.
- **Key Finding:** Self-improvement is possible but limited without external signals.
- **Relation to Our Work:** V2G provides a framework for self-improvement using ranking rather than binary signals.

#### When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey
**Huang et al., TACL 2024**

- **Key Contribution:** Critically examines self-correction claims, finding many methods don't work without external feedback.
- **Key Finding:** Self-correction is only effective when verification is exceptionally easy.
- **Relation to Our Work:** Motivates V2G: if self-correction is hard, training to internalize corrections is valuable.

---

## 6. Instruction Following and Evaluation

#### COLLIE: Systematic Construction of Constrained Text Generation Tasks
**Yao et al., ICLR 2024** [[arXiv:2307.08689](https://arxiv.org/abs/2307.08689)]

- **Key Contribution:** Framework for systematically constructing constrained generation tasks. Creates COLLIE-v1 with 2,080 instances across 13 constraint structures.
- **Key Finding:** Even strong models like GPT-4 struggle with complex constraint combinations.
- **Relation to Our Work:** Provides challenging instruction-following benchmarks where V2G improvements could be measured.

#### Evaluating Large Language Models at Evaluating Instruction Following (LLMBar)
**Zeng et al., ICLR 2024** [[arXiv:2310.07641](https://arxiv.org/abs/2310.07641)]

- **Key Contribution:** Meta-evaluation benchmark testing LLMs' ability to judge instruction-following quality.
- **Key Finding:** LLMs can be biased judges; evaluator quality matters for preference learning.
- **Relation to Our Work:** Quality of validator signal affects V2G training effectiveness.

#### Instruction-Following Evaluation for Large Language Models (IFEval)
**Zhou et al., 2023** [[arXiv:2311.07911](https://arxiv.org/abs/2311.07911)]

- **Key Contribution:** Straightforward benchmark with verifiable instruction-following criteria.
- **Key Finding:** Even strong models have significant room for improvement on precise instructions.
- **Relation to Our Work:** Benchmark for measuring V2G improvements on instruction following.

#### InFoBench: Evaluating Instruction Following Ability
**Qin et al., ACL Findings 2024**

- **Key Contribution:** Introduces Decomposed Requirements Following Ratio (DRFR) for fine-grained evaluation.
- **Key Finding:** Breaking down instructions into components reveals nuanced model capabilities.
- **Relation to Our Work:** V2G could be applied to improve following of decomposed requirements.

#### Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
**Zheng et al., NeurIPS 2023** [[arXiv:2306.05685](https://arxiv.org/abs/2306.05685)]

- **Key Contribution:** Proposes using strong LLMs as judges for evaluation. Introduces MT-Bench and Chatbot Arena.
- **Key Finding:** LLM judges achieve high agreement with human preferences; scalable alternative to human eval.
- **Relation to Our Work:** LLM-as-a-Judge can provide validator signal for V2G training.

---

## 7. Decoding and Inference-Time Methods

#### DoLa: Decoding by Contrasting Layers Improves Factuality
**Chuang et al., ICLR 2024** [[arXiv:2309.03883](https://arxiv.org/abs/2309.03883)]

- **Key Contribution:** Obtains next-token distribution by contrasting logits from later vs. earlier layers.
- **Key Finding:** Improves TruthfulQA by 12-17% absolute points on LLaMA models.
- **Relation to Our Work:** Inference-time approach; V2G achieves similar goals through training.

#### Contrastive Decoding: Open-ended Text Generation as Optimization
**Li et al., ACL 2023**

- **Key Contribution:** Contrasts large "expert" model with small "amateur" to improve generation quality.
- **Key Finding:** Reduces repetition and improves coherence in long-form generation.
- **Relation to Our Work:** Uses model differences as signal; V2G uses ranking differences.

#### Alleviating Hallucinations of Large Language Models through Induced Hallucinations
**Zhang et al., 2023** [[arXiv:2312.15710](https://arxiv.org/abs/2312.15710)]

- **Key Contribution:** Creates "factually weak" LLM by inducing hallucinations, then uses contrastive decoding.
- **Key Finding:** Contrasting against hallucination-prone model improves factuality.
- **Relation to Our Work:** Training-free method; V2G provides persistent improvements.

---

## 8. Benchmarks

#### TruthfulQA: Measuring How Models Mimic Human Falsehoods
**Lin et al., ACL 2022** [[arXiv:2109.07958](https://arxiv.org/abs/2109.07958)]

- **Key Contribution:** 817 questions spanning 38 categories designed to elicit imitative falsehoods.
- **Key Finding:** Larger models were less truthful; models mimic common misconceptions.
- **Relation to Our Work:** Standard benchmark for measuring truthfulness improvements from V2G.

---

## Summary: Gaps Our Work Addresses

Based on this literature review, the V2G research direction addresses several key gaps:

1. **Training-Time vs. Inference-Time:** Most methods for leveraging validation capabilities operate at inference time (ITI, DoLa, contrastive decoding). V2G provides training-time alignment for persistent improvements.

2. **Pairwise vs. Listwise:** DPO and most preference methods use pairwise comparisons. V2G/RankAlign leverages richer listwise ranking signals from validators.

3. **Hidden Knowledge Utilization:** Papers show LLMs have hidden knowledge (Inside-Out, LLMs Know More Than They Show). V2G provides a mechanism to surface this knowledge into generation.

4. **Self-Consistency Through Training:** Self-consistency methods operate at inference time. V2G trains models to be more self-consistent.

5. **Systematic Evaluation of Gap:** While papers document the G-D gap, V2G provides a principled framework for closing it through ranking alignment.

---

## Citation Statistics (as of February 2026)

| Paper | Year | Venue | Topic |
|-------|------|-------|-------|
| RankAlign | 2025 | COLM | Generator-Validator Gap |
| Inside-Out | 2025 | COLM | Hidden Knowledge |
| Generative AI Paradox | 2024 | ICLR | G-D Gap |
| Kadavath et al. | 2022 | arXiv | Self-Knowledge |
| DPO | 2023 | NeurIPS | Preference Learning |
| RLHF/InstructGPT | 2022 | NeurIPS | Alignment |
| Self-Consistency | 2023 | ICLR | Reasoning |
| TruthfulQA | 2022 | ACL | Benchmark |

---

*Literature review compiled for V2G research, February 2026*
