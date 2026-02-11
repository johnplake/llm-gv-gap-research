# V2G Research: Complete Paper Analysis
## All 40 Papers with Datasets, Results, and Code

**Goal:** Train a generator to match a validator's ranking over candidate outputs (V2G/RankAlign approach).  
For each paper: (1) Why we care for V2G, (2) Key datasets/results/methods, (3) Code & data links.

---

## Section 1: Generator-Validator Inconsistency (9 papers)

### 1.1 RankAlign: A Ranking View of the Generator-Validator Gap
**Rodriguez et al., COLM 2025** | [Paper](https://arxiv.org/abs/2504.11381) | [Code](https://github.com/juand-r/rankalign)

**Why This Matters for V2G:**
- **FOUNDATIONAL** - This IS our project's starting point and closest ancestor
- Formalizes G-V gap as **ranking correlation mismatch** (not just binary accuracy)
- Proposes ranking-based training that closes gap by **31.8% average**
- Shows listwise ranking > pairwise training for G-V alignment

**Key Results:**
- Large gaps exist even in strong models across multiple domains
- Generalizes to out-of-domain tasks and unseen lexical items
- Methodologically relevant: sampling candidate sets, listwise/pairwise losses, correlation-based evaluation

**Datasets:**
- CommonsenseQA, TriviaQA (question answering)
- Hypernymy detection (lexical semantics)
- Next-word prediction tasks

**Code & Data:**
- ✅ Full implementation: https://github.com/juand-r/rankalign
- Includes RankAlign training, evaluation scripts, G-V gap measurement tools
- Longform branch has mode="g" for V2G direction

---

### 1.2 Inside-Out: Hidden Factual Knowledge in LLMs
**Gekhman et al., COLM 2025** | [Paper](https://arxiv.org/abs/2503.15299)

**Why This Matters for V2G:**
- **STRONG MOTIVATION** - Proves knowledge exists internally but isn't expressed in generation
- **40% relative gap** between internal and external knowledge
- Some answers "deeply hidden" - never generated despite 1000 samples
- V2G training can help **externalize internally-represented truth signals**

**Key Results:**
- LLMs consistently encode more knowledge than they express
- Internal knowledge can be perfect while generation fails completely
- Fundamental limitation in generation that validators can detect

**Datasets:**
- Closed-book QA setup
- Multiple factual knowledge datasets
- Large-scale sampling (1000 answers per question)

**Code & Data:**
- 🔍 Very recent (2025) - no official repo located yet
- Paper includes detailed methodology for measuring hidden knowledge

---

### 1.3 The Generative AI Paradox: "What It Can Create, It May Not Understand"
**West et al., ICLR 2024** | [Paper](https://arxiv.org/abs/2311.00059)

**Why This Matters for V2G:**
- **EMPIRICAL FOUNDATION** - Systematically shows generation ≠ discrimination
- Models outperform humans at generation but underperform at discrimination
- **Different scaling curves** for each capability
- V2G relies on validator being "ahead" or differently capable than generator

**Key Results:**
- Generation and discrimination follow different capability curves
- Models can generate content they cannot reliably evaluate
- Gap persists across domains (language, vision) even in SOTA models

**Datasets:**
- Custom discrimination tests
- Multiple generation benchmarks
- Cross-domain evaluation suite

**Code & Data:**
- ❌ No public code (OpenReview submission, no canonical repo)

---

### 1.4 Language Models (Mostly) Know What They Know
**Kadavath et al., 2022** | [Paper](https://arxiv.org/abs/2207.05221)

**Why This Matters for V2G:**
- **CALIBRATION BASELINE** - Shows LLMs have internal knowledge representations
- P(True) and P(IK) methods provide **validator signals we can leverage**
- Larger models = better calibrated = more reliable validation
- Format matters for eliciting calibration

**Key Results:**
- Large models well-calibrated on multiple choice when properly formatted
- Models can predict which questions they'll answer correctly (P(IK))
- Calibration generalizes across tasks (with limitations)

**Datasets:**
- TriviaQA, Natural Questions
- Multiple choice variants
- Custom calibration test sets

**Code & Data:**
- 🔍 No canonical Anthropic repo found (many downstream replications exist)

---

### 1.5 Self-critiquing Models for Assisting Human Evaluators
**Saunders et al., 2022** | [Report](https://cdn.openai.com/papers/critiques.pdf)

**Why This Matters for V2G:**
- **EARLY G-D GAP WORK** - First explicit formulation of generation-discrimination gap
- **"Recognition easier than avoidance"** principle validates V2G direction
- Natural language critiques = rich validator signal
- Can use critique quality to train better generators

**Key Results:**
- Models can effectively critique their own outputs
- Critique ability doesn't require generation ability
- Human-model collaboration improves evaluation

**Datasets:**
- Summarization tasks
- Custom evaluation sets

**Code & Data:**
- ❌ OpenAI technical report, no public training code

---

### 1.6 Benchmarking and Improving Generator-Validator Consistency
**Li et al., ICLR 2024** | [Paper](https://arxiv.org/abs/2310.01846) | [OpenReview](https://openreview.net/forum?id=phBS6YpTzC)

**Why This Matters for V2G:**
- **COMPLEMENTARY FRAMEWORK** - Different lens on G-V inconsistency
- Provides **GV-consistency metrics and benchmarks** we can use for evaluation
- Shows joint training can improve both sides: **16% generator, 6.3% validator improvement**
- Systematic evaluation across multiple task types

**Key Results:**
- Inconsistency is widespread across tasks
- Different training strategies have different tradeoffs
- Multi-task evaluation reveals robustness

**Datasets:**
- Math questions (GSM8K, MATH)
- Knowledge-intensive QA
- Instruction following tasks

**Code & Data:**
- 🔍 No official repo found quickly (check paper PDF for link)

---

### 1.7 Self-[In]Correct: LLMs Struggle with Discriminating Self-Generated Responses
**Huang et al., 2024** | [Paper](https://arxiv.org/abs/2404.04298)

**Why This Matters for V2G:**
- **CHALLENGES ASSUMPTIONS** - Self-evaluation isn't reliable across most tasks
- Discrimination not consistently better than generation
- Motivates using **external/stronger validators** (not just self-evaluation)
- V2G provides framework beyond simple self-correction

**Key Results:**
- Unified framework comparing generation vs discrimination capabilities
- Models not reliably better at discriminating self-generated options
- Self-improvement through self-evaluation is limited

**Datasets:**
- Multiple task types for comparison
- Self-generated vs external responses

**Code & Data:**
- 🔍 No official repo found

---

### 1.8 Shrinking the Generation-Verification Gap with Weak Verifiers
**Saad-Falcon et al., 2025** | [Paper](https://arxiv.org/abs/2506.18203) | [Code](https://github.com/HazyResearch/scaling-verification)

**Why This Matters for V2G:**
- **WEAK SUPERVISION** - Shows aggregating weak validators helps
- LM judges are noisy/biased/poorly calibrated individually
- **Weaver method** for combining validators into stronger signal
- Could combine: aggregate weak validators → train with V2G

**Key Results:**
- Learned weighting/aggregation approaches strong-oracle verification
- Addresses calibration issues in individual judges
- Improves over single verifiers significantly

**Datasets:**
- Multiple verification tasks
- Weak verifier outputs for aggregation

**Code & Data:**
- ✅ Weaver implementation: https://github.com/HazyResearch/scaling-verification

---

### 1.9 Constitutional AI: Harmlessness from AI Feedback
**Bai et al., 2022** | [Paper](https://arxiv.org/abs/2212.08073)

**Why This Matters for V2G:**
- **AI-AS-VALIDATOR** - Uses model self-critique for training (RLAIF)
- Constitution provides structured validator signal
- V2G formalizes validator signal as ranking
- Demonstrates large-scale AI feedback for alignment

**Key Results:**
- Can train harmless assistants with minimal human labels
- Self-critique → revision → preference learning pipeline
- Reduces evasive responses while maintaining helpfulness

**Datasets:**
- Red teaming prompts
- Constitutional principles as evaluation criteria

**Code & Data:**
- 🔍 Anthropic - no full public implementation

---

## Section 2: Hidden/Latent Knowledge and Probing (7 papers)

### 2.1 LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations
**Orgad et al., ICLR 2025** | [Paper](https://arxiv.org/abs/2410.02707) | [Code](https://github.com/technion-cs-nlp/LLMsKnow)

**Why This Matters for V2G:**
- **INTERNAL TRUTHFULNESS** - Representations encode truth even when outputs lie
- Information is there but not expressed in generation
- V2G can train models to **externalize internal knowledge**
- Validates that validators have signal generators lack

**Key Results:**
- Probing internal states reveals truthfulness information
- Works across different model families
- Even hallucinated outputs have truthful internal representations

**Datasets:**
- TruthfulQA and variants
- Custom hallucination detection sets

**Code & Data:**
- ✅ Official repo: https://github.com/technion-cs-nlp/LLMsKnow
- ✅ Reproduction: https://github.com/sriharshapy/LLM-knows-more-than-they-show (medical domain extension)

---

### 2.2 The Internal State of an LLM Knows When It's Lying
**Azaria & Mitchell, EMNLP Findings 2023** | [Paper](https://arxiv.org/abs/2304.13734) | [Code](https://github.com/sisinflab/HidingInTheHiddenStates)

**Why This Matters for V2G:**
- **PROBING TRUTHFULNESS** - **71-83% accuracy** detecting lies from hidden states
- Internal state reveals what external generation doesn't
- Probes work on both provided and self-generated statements
- V2G could use this signal during training as lightweight validator

**Key Results:**
- Linear probes on hidden activations predict truthfulness
- Generalizes across topics
- Works for both factual and opinion statements

**Datasets:**
- True/false statement pairs
- Multiple topics and domains

**Code & Data:**
- ✅ Related implementation: https://github.com/sisinflab/HidingInTheHiddenStates
- ✅ Base code: https://github.com/balevinstein/Probes

---

### 2.3 The Geometry of Truth: Emergent Linear Structure in LLM Representations
**Marks & Tegmark, COLM 2024** | [Paper](https://arxiv.org/abs/2310.06824) | [Code](https://github.com/saprmarks/geometry-of-truth)

**Why This Matters for V2G:**
- **LINEAR STRUCTURE** - Truth represented as linear directions at scale
- Simple difference-in-mean probes find "truth directions"
- Transfers across topics and datasets
- **Ranking-based training can leverage this geometry**

**Key Results:**
- Emergent property at sufficient scale
- Linear probes generalize remarkably well across datasets
- Mathematical foundation for truth representation

**Datasets:**
- Multiple true/false datasets
- Cross-topic evaluation

**Code & Data:**
- ✅ Full implementation: https://github.com/saprmarks/geometry-of-truth
- Includes probe training and evaluation

---

### 2.4 Discovering Latent Knowledge in Language Models Without Supervision
**Burns et al., ICLR 2023** | [Paper](https://arxiv.org/abs/2212.03827) | [Code](https://github.com/collin-burns/discovering_latent_knowledge)

**Why This Matters for V2G:**
- **UNSUPERVISED KNOWLEDGE** - Contrast-Consistent Search (CCS) finds knowledge without labels
- Uses contrast pairs (statement + negation)
- Recovers knowledge even when outputs are misleading
- Complementary to V2G: CCS finds knowledge, V2G trains to express it

**Key Results:**
- Works without supervision using invariances across prompt variants
- Finds latent knowledge across diverse datasets
- Can outperform zero-shot prompting

**Datasets:**
- IMDB sentiment
- AG News
- Factual statements with negations

**Code & Data:**
- ✅ Full CCS implementation: https://github.com/collin-burns/discovering_latent_knowledge
- Includes algorithm and evaluation code

---

### 2.5 Representation Engineering: A Top-Down Approach to AI Transparency
**Zou et al., 2023** | [Paper](https://arxiv.org/abs/2310.01405) | [Code](https://github.com/andyzoujm/representation-engineering)

**Why This Matters for V2G:**
- **ACTIVATION STEERING** - RepE improves truthfulness via activation manipulation
- Steering "truthfulness" direction improves TruthfulQA by **up to 30 percentage points**
- Inference-time intervention; **V2G achieves similar goals through training**
- Could combine: use RepE to identify directions, V2G to make them default

**Key Results:**
- Can control multiple behaviors (truthfulness, sentiment, etc.)
- Works by manipulating activation differences
- Generalizes across prompts

**Datasets:**
- TruthfulQA
- Custom behavior evaluation sets

**Code & Data:**
- ✅ RepE implementation: https://github.com/andyzoujm/representation-engineering

---

### 2.6 Inference-Time Intervention: Eliciting Truthful Answers from a Language Model
**Li et al., NeurIPS 2023** | [Paper](https://arxiv.org/abs/2306.03341) | [Code](https://github.com/likenneth/honest_llama)

**Why This Matters for V2G:**
- **ITI METHOD** - Shifts activations during inference for truthfulness
- Uses only **few hundred examples**
- Shows internal truth representations exist before generation
- **V2G: bake these improvements into the model** (no inference cost)

**Key Results:**
- Significant TruthfulQA improvements
- Minimal training data needed
- Persistent across prompts

**Datasets:**
- TruthfulQA
- Small calibration set (few hundred examples)

**Code & Data:**
- ✅ Full ITI implementation: https://github.com/likenneth/honest_llama
- Includes ITI intervention and evaluation

---

### 2.7 Patchscopes: A Unifying Framework for Inspecting Hidden Representations
**Ghandeharioun et al., 2024** | [Paper](https://arxiv.org/abs/2401.06102) | [Project](https://pair-code.github.io/interpretability/patchscopes/)

**Why This Matters for V2G:**
- **INTERPRETABILITY FRAMEWORK** - Unifies probing, vocabulary projection, etc.
- Decode representations into natural language
- **Diagnose** what validators respond to and what generators learn
- Useful for debugging when generator learns superficial "judge hacks"

**Key Results:**
- Single framework for multiple interpretability methods
- Can decode internal representations
- Shows how to inspect early vs late layers

**Datasets:**
- Multiple tasks for demonstration

**Code & Data:**
- 🔍 Project page: https://pair-code.github.io/interpretability/patchscopes/

---

## Section 3: Preference Learning and Alignment (9 papers)

### 3.1 Training Language Models to Follow Instructions with Human Feedback (InstructGPT)
**Ouyang et al., NeurIPS 2022** | [Paper](https://arxiv.org/abs/2203.02155)

**Why This Matters for V2G:**
- **FOUNDATIONAL RLHF** - Establishes preference learning paradigm
- SFT → Reward Model → PPO pipeline
- **1.3B InstructGPT preferred over 175B GPT-3**
- V2G extends this: uses **validator rankings** instead of human preferences

**Key Results:**
- Dramatic improvements from RLHF
- Smaller aligned model > larger unaligned
- Defines modern alignment approach

**Datasets:**
- Prompt dataset for SFT
- Human preference comparisons
- Evaluation suite

**Code & Data:**
- ❌ OpenAI - no public code for full pipeline (many open-source reimplementations exist)

---

### 3.2 Direct Preference Optimization: Your Language Model is Secretly a Reward Model
**Rafailov et al., NeurIPS 2023** | [Paper](https://arxiv.org/abs/2305.18290) | [Code](https://github.com/eric-mitchell/direct-preference-optimization)

**Why This Matters for V2G:**
- **PAIRWISE BASELINE** - Eliminates reward model, direct optimization
- **V2G extends from pairwise to listwise rankings** (more information per prompt)
- Simpler than PPO, more stable training
- Our ranking loss builds on DPO's direct optimization approach

**Key Results:**
- Matches or exceeds PPO-based RLHF
- Much simpler to implement
- More stable training

**Datasets:**
- Anthropic HH dataset
- Reddit TL;DR summarization

**Code & Data:**
- ✅ Reference implementation: https://github.com/eric-mitchell/direct-preference-optimization
- ✅ Also in Hugging Face TRL: https://github.com/huggingface/trl

---

### 3.3 SimPO: Simple Preference Optimization with a Reference-Free Reward
**Meng et al., NeurIPS 2024** | [Paper](https://arxiv.org/abs/2405.14734) | [Code](https://github.com/princeton-nlp/SimPO)

**Why This Matters for V2G:**
- **REFERENCE-FREE DPO** - Uses length-normalized log-likelihood as reward
- Removes reference model requirement (simpler than DPO)
- Outperforms DPO on AlpacaEval 2, MT-Bench, Arena-Hard
- Suggests **reference-free ranking objectives** may be preferable for V2G

**Key Results:**
- Strong empirical performance across benchmarks
- Simpler architecture (no reference model)
- Alternative objective formulation

**Datasets:**
- AlpacaEval 2
- MT-Bench
- Arena-Hard

**Code & Data:**
- ✅ Full implementation: https://github.com/princeton-nlp/SimPO
- Includes training scripts and model checkpoints

---

### 3.4 KTO: Model Alignment as Prospect Theoretic Optimization
**Ethayarajh et al., 2024** | [Paper](https://arxiv.org/abs/2402.01078) | [Code](https://github.com/ContextualAI/HALOs)

**Why This Matters for V2G:**
- **UNPAIRED PREFERENCES** - Doesn't require pairwise comparisons
- Applies prospect theory to preference learning
- Works with simpler feedback (thumbs up/down)
- Suggests ranking objectives might benefit from **asymmetric penalties**

**Key Results:**
- Works without paired preferences
- Prospect theory provides theoretical foundation
- Competitive with preference methods at scale

**Datasets:**
- Binary feedback (good/bad)
- No paired comparisons needed

**Code & Data:**
- ✅ HALOs library: https://github.com/ContextualAI/HALOs
- ✅ Also in Hugging Face TRL: https://github.com/huggingface/trl

---

### 3.5 LiPO: Listwise Preference Optimization through Learning-to-Rank
**Liu et al., NAACL 2025** | [Paper](https://arxiv.org/abs/2402.01878)

**Why This Matters for V2G:**
- **DIRECTLY RELATED** - Explicitly **listwise alignment** using learning-to-rank
- LiPO-λ uses **DCG-weighted listwise losses** 
- Same core insight as RankAlign: listwise > pairwise
- Provides candidate listwise losses to borrow directly

**Key Results:**
- Listwise objectives outperform pairwise
- Learning-to-rank principles apply to LLMs
- Weighting top-of-list mistakes more helps

**Datasets:**
- Preference ranking datasets
- Multiple response candidates per prompt

**Code & Data:**
- 🔍 No official repo found quickly (check paper PDF)

---

### 3.6 Self-Rewarding Language Models
**Yuan et al., ICML 2024** | [Paper](https://arxiv.org/abs/2401.10020) | [Code](https://github.com/lucidrains/self-rewarding-lm-pytorch)

**Why This Matters for V2G:**
- **SELF-IMPROVEMENT** - LLM as both generator and judge
- Llama 2 70B outperforms Claude 2, Gemini Pro, GPT-4 on AlpacaEval
- V2G must avoid **degenerate feedback loops** if generator and validator too coupled
- Use frozen/stronger validators or ensembles

**Key Results:**
- Self-generated rewards enable improvement
- Iterative training compounds gains
- Beats much larger models

**Datasets:**
- AlpacaEval 2.0
- Self-generated training data

**Code & Data:**
- 🔍 No official Meta repo found
- ✅ Third-party implementation: https://github.com/lucidrains/self-rewarding-lm-pytorch

---

### 3.7 Scaling Laws for Reward Model Overoptimization
**Gao et al., ICML 2023** | [Paper](https://arxiv.org/abs/2210.10760)

**Why This Matters for V2G:**
- **OVEROPTIMIZATION WARNING** - Gold reward initially increases then decreases
- Proxy reward models can be exploited (reward hacking)
- Scaling laws predict when overoptimization occurs
- **V2G must monitor**: ranking losses may be more robust but not immune

**Key Results:**
- Coefficients scale with reward model size
- Predictable overoptimization dynamics
- Larger RMs delay but don't eliminate overoptimization

**Datasets:**
- Anthropic HH dataset
- Reddit TL;DR

**Code & Data:**
- 🔍 No official repo found

---

### 3.8 On Calibration of Modern Neural Networks
**Guo et al., ICML 2017** | [Paper](https://arxiv.org/abs/1706.04599)

**Why This Matters for V2G:**
- **CALIBRATION FOUNDATIONS** - Modern networks are overconfident
- Temperature scaling as post-hoc fix
- Expected Calibration Error (ECE) as standard metric
- V2G could improve calibration through alignment with validators

**Key Results:**
- Larger models more overconfident
- Temperature scaling effective
- Calibration ≠ accuracy

**Datasets:**
- CIFAR, ImageNet (originally)
- Applies to any classification

**Code & Data:**
- ✅ Widely implemented, standard technique

---

### 3.9 Can LLMs Express Their Uncertainty? An Empirical Evaluation
**Xiong et al., ICLR 2024** | [Paper](https://arxiv.org/abs/2306.13063)

**Why This Matters for V2G:**
- **UNCERTAINTY ELICITATION** - Tests multiple confidence extraction methods
- Verbalized confidence often poorly calibrated
- Consistency-based methods work better
- **V2G training could improve self-consistency** → better calibration

**Key Results:**
- Verbalized confidence unreliable
- Sampling consistency more reliable
- Method choice matters greatly

**Datasets:**
- TriviaQA, MMLU, others
- Multiple confidence elicitation formats

**Code & Data:**
- 🔍 No official repo found

---

## Section 4: Self-Consistency and Self-Evaluation (4 papers)

### 4.1 Self-Consistency Improves Chain of Thought Reasoning
**Wang et al., ICLR 2023** | [Paper](https://arxiv.org/abs/2203.11171)

**Why This Matters for V2G:**
- **INFERENCE-TIME CONSISTENCY** - Sample multiple paths, majority vote
- **+17.9% on GSM8K** from consistency alone
- V2G aims to **improve consistency through training** (not just inference)
- Could combine: V2G training + self-consistency inference

**Key Results:**
- Works across reasoning tasks (math, commonsense)
- Emergent with scale
- Simple but highly effective

**Datasets:**
- GSM8K (math word problems)
- CommonsenseQA
- StrategyQA

**Code & Data:**
- ✅ Many implementations available (simple to implement)

---

### 4.2 Chain-of-Thought Prompting Elicits Reasoning
**Wei et al., NeurIPS 2022** | [Paper](https://arxiv.org/abs/2201.11903)

**Why This Matters for V2G:**
- **REASONING FOUNDATION** - Intermediate steps improve complex tasks
- Emergent ability with scale
- **V2G can help models better select among CoT outputs**
- Validator can rank different reasoning chains

**Key Results:**
- Dramatic improvements on reasoning
- Requires sufficient scale
- Works across diverse tasks

**Datasets:**
- Math word problems
- Commonsense reasoning
- Symbolic reasoning

**Code & Data:**
- ✅ Standard technique, many implementations

---

### 4.3 Large Language Models Can Self-Improve
**Huang et al., 2022** | [Paper](https://arxiv.org/abs/2210.11610)

**Why This Matters for V2G:**
- **SELF-IMPROVEMENT** - Models improve via self-generated rationales
- **Limited without external signals**
- V2G provides framework using ranking signals
- Self-generation + validator ranking = improvement path

**Key Results:**
- Self-improvement possible but bounded
- Benefits from scale
- External feedback helps more

**Datasets:**
- Reasoning tasks
- Self-generated training data

**Code & Data:**
- 🔍 No official repo found

---

### 4.4 When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey
**Huang et al., TACL 2024** | [Paper](https://arxiv.org/abs/2305.14483)

**Why This Matters for V2G:**
- **CRITICAL ANALYSIS** - Self-correction only works when verification is easy
- Most methods don't work without external feedback
- **Motivates V2G**: if self-correction is hard, train to internalize corrections
- Ranking-based training = internalized correction signal

**Key Results:**
- Self-correction overestimated in literature
- Requires easy verification
- External signals necessary for real improvement

**Datasets:**
- Multiple self-correction benchmarks

**Code & Data:**
- 🔍 Survey/analysis paper

---

## Section 5: Instruction Following and Evaluation (5 papers)

### 5.1 COLLIE: Systematic Construction of Constrained Text Generation Tasks
**Yao et al., ICLR 2024** | [Paper](https://arxiv.org/abs/2307.08689) | [Code](https://github.com/princeton-nlp/Collie) | [Project](https://collie-benchmark.github.io/)

**Why This Matters for V2G:**
- **CHALLENGING BENCHMARK** - 2,080 instances, 13 constraint structures
- Even GPT-4 struggles with complex constraints
- **Perfect testbed for V2G**: validators can check constraints precisely
- Constrained generation = ideal setting where discrimination > generation

**Key Results:**
- Systematic framework for constraint generation
- Complexity increases with constraint combinations
- Automatic verification possible (deterministic validator signal)

**Datasets:**
- ✅ COLLIE-v1: 2,080 constrained generation tasks
- 13 constraint types
- Verifiable constraints

**Code & Data:**
- ✅ Full framework: https://github.com/princeton-nlp/Collie
- ✅ Project page: https://collie-benchmark.github.io/
- Includes constraint spec language, generators, evaluators

---

### 5.2 Evaluating LLMs at Evaluating Instruction Following (LLMBar)
**Zeng et al., ICLR 2024** | [Paper](https://arxiv.org/abs/2310.07641) | [Code](https://github.com/princeton-nlp/LLMBar)

**Why This Matters for V2G:**
- **META-EVALUATION** - Tests LLMs as judges
- LLMs can be biased/inconsistent judges
- **Validator quality affects V2G training effectiveness**
- Helps select validators and detect systematic errors

**Key Results:**
- LLM judges have systematic biases
- Position bias, length bias, etc.
- Some judges better than others

**Datasets:**
- LLMBar benchmark
- Adversarial test cases for judges

**Code & Data:**
- ✅ LLMBar: https://github.com/princeton-nlp/LLMBar

---

### 5.3 Instruction-Following Evaluation for LLMs (IFEval)
**Zhou et al., 2023** | [Paper](https://arxiv.org/abs/2311.07911) | [Code](https://github.com/EleutherAI/lm-evaluation-harness)

**Why This Matters for V2G:**
- **VERIFIABLE INSTRUCTIONS** - Straightforward evaluation criteria
- Even strong models have significant room for improvement
- **Clear validator signal** for V2G training
- Instruction following benefits from G-V alignment

**Key Results:**
- Simple, verifiable instructions
- Significant model differences
- Deterministic constraint checking

**Datasets:**
- IFEval benchmark
- Verifiable instruction following

**Code & Data:**
- ✅ Implemented in lm-eval-harness: https://github.com/EleutherAI/lm-evaluation-harness
- Task: ifeval

---

### 5.4 InFoBench: Evaluating Instruction Following Ability
**Qin et al., ACL Findings 2024** | [Paper](https://arxiv.org/abs/2401.03601)

**Why This Matters for V2G:**
- **FINE-GRAINED EVALUATION** - Decomposed Requirements Following Ratio (DRFR)
- Breaking down instructions reveals nuanced capabilities
- **Granular validator signal** for V2G
- Can train on specific requirement types

**Key Results:**
- Instruction decomposition useful
- Models vary on different requirement types
- More diagnostic than aggregate scores

**Datasets:**
- InFoBench with decomposed requirements

**Code & Data:**
- 🔍 No official repo found

---

### 5.5 Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
**Zheng et al., NeurIPS 2023** | [Paper](https://arxiv.org/abs/2306.05685)

**Why This Matters for V2G:**
- **LLM JUDGES** - Strong LLMs as scalable evaluators
- High agreement with human preferences
- Can provide **validator signal for V2G training**
- MT-Bench = standard evaluation

**Key Results:**
- LLM judges correlate well with humans
- GPT-4 as strong judge
- Scalable alternative to human eval

**Datasets:**
- MT-Bench (multi-turn conversations)
- Chatbot Arena (pairwise battles)

**Code & Data:**
- ✅ FastChat repo includes MT-Bench

---

## Section 6: Decoding and Inference-Time Methods (3 papers)

### 6.1 DoLa: Decoding by Contrasting Layers Improves Factuality
**Chuang et al., ICLR 2024** | [Paper](https://arxiv.org/abs/2309.03883) | [Code](https://github.com/voidism/DoLa)

**Why This Matters for V2G:**
- **INFERENCE-TIME ALTERNATIVE** - Contrast layer outputs for factuality
- **+12-17% absolute** on TruthfulQA
- V2G achieves similar goals through **training** (persistent, no inference cost)
- Could potentially combine both approaches

**Key Results:**
- Later layers - earlier layers = factual signal
- Works across model families (LLaMA, etc.)
- No training required

**Datasets:**
- TruthfulQA
- StrategyQA
- GSM8K

**Code & Data:**
- ✅ Full implementation: https://github.com/voidism/DoLa
- Includes DoLa decoding and evaluation

---

### 6.2 Contrastive Decoding: Open-ended Text Generation as Optimization
**Li et al., ACL 2023** | [Paper](https://arxiv.org/abs/2210.15097) | [Code](https://github.com/XiangLi1999/ContrastiveDecoding)

**Why This Matters for V2G:**
- **EXPERT-AMATEUR CONTRAST** - Large model - small model improves generation
- Uses model differences as signal (like validator-generator gap)
- Reduces repetition, improves coherence
- **V2G: distill contrastive signal into generator weights**

**Key Results:**
- Outperforms nucleus sampling
- Reduces degeneration
- Simple to implement at inference

**Datasets:**
- WikiText, news articles
- Long-form generation

**Code & Data:**
- ✅ Contrastive Decoding: https://github.com/XiangLi1999/ContrastiveDecoding

---

### 6.3 Alleviating Hallucinations through Induced Hallucinations
**Zhang et al., 2023** | [Paper](https://arxiv.org/abs/2312.15710) | [Code](https://github.com/HillZhang1999/ICD)

**Why This Matters for V2G:**
- **HALLUCINATION CONTRAST** - Create weak model, contrast against it
- Induce-then-Contrast Decoding (ICD)
- For V2G: use induced-hallucination model to generate **hard negatives**
- Validator ranks; train generator away from hallucinated candidates

**Key Results:**
- Inducing hallucinations helps identify truthful outputs
- Training-free method
- Improves factuality metrics

**Datasets:**
- Factual QA tasks
- Hallucination detection

**Code & Data:**
- ✅ ICD implementation: https://github.com/HillZhang1999/ICD

---

## Section 7: Benchmarks (1 paper)

### 7.1 TruthfulQA: Measuring How Models Mimic Human Falsehoods
**Lin et al., ACL 2022** | [Paper](https://arxiv.org/abs/2109.07958) | [Code](https://github.com/sylinrl/TruthfulQA) | [HF](https://huggingface.co/datasets/domenicrosati/TruthfulQA)

**Why This Matters for V2G:**
- **STANDARD BENCHMARK** - 817 questions designed to elicit falsehoods
- Tests whether models repeat misconceptions
- Key setting where "validator knows better than generator"
- Central evaluation for V2G improvements

**Key Results:**
- Models mimic human falsehoods
- Larger models were less truthful initially (scaling ≠ truthfulness)
- 38 categories covering diverse topics

**Datasets:**
- ✅ 817 questions with correct/incorrect answers
- Multiple choice and generation formats
- Publicly available

**Code & Data:**
- ✅ Official dataset: https://github.com/sylinrl/TruthfulQA
- ✅ HF mirror: https://huggingface.co/datasets/domenicrosati/TruthfulQA
- Evaluation code included

---

## Section 8: Additional Key Papers (3 papers)

### 8.1 A Survey of Confidence Estimation and Calibration in LLMs
**Geng et al., 2024** | [Paper](https://arxiv.org/abs/2311.08298)

**Why This Matters for V2G:**
- **COMPREHENSIVE OVERVIEW** - Catalogs methods to build better validators
- Calibration, uncertainty, selective prediction
- Can become ranking objectives in V2G
- No universal solution yet

**Datasets:**
- Survey covers multiple benchmarks

**Code & Data:**
- 🔍 Survey paper - references many implementations

---

### 8.2 Large Language Models Must Be Taught to Know What They Don't Know
**Banda et al., NeurIPS 2024** | [Paper](https://arxiv.org/abs/2406.08391)

**Why This Matters for V2G:**
- **CALIBRATION TUNING** - Off-the-shelf LLMs poor at expressing uncertainty
- Explicit training needed for good calibration
- **V2G is a form of calibration tuning** using ranking signals
- Fine-tuning significantly improves uncertainty expression

**Datasets:**
- Calibration training data
- Multiple evaluation benchmarks

**Code & Data:**
- 🔍 No official repo found

---

### 8.3 Representation/Probing Papers (Survey Note)
Multiple papers demonstrate that:
- Truth is linearly separable in representations
- Internal states encode knowledge not expressed
- Probing can recover hidden knowledge

**Implications for V2G:**
- Validators can access these signals
- Training can help externalize them
- Linear structure suggests ranking objectives are well-suited

---

## Summary: Complete Resource Map

### 🔥 Core V2G Papers (Must Read)
1. **RankAlign** - THE foundational paper | [Code](https://github.com/juand-r/rankalign)
2. **Inside-Out** - Hidden knowledge evidence (40% gap)
3. **LiPO** - Listwise ranking for LLMs
4. **GV Consistency** - Benchmarking framework

### ✅ Top Code Repositories (20+ found)

**Core Training:**
- RankAlign: https://github.com/juand-r/rankalign
- DPO: https://github.com/eric-mitchell/direct-preference-optimization
- SimPO: https://github.com/princeton-nlp/SimPO
- HALOs (KTO): https://github.com/ContextualAI/HALOs
- TRL (DPO/KTO): https://github.com/huggingface/trl

**Hidden Knowledge & Probing:**
- LLMsKnow: https://github.com/technion-cs-nlp/LLMsKnow
- Geometry of Truth: https://github.com/saprmarks/geometry-of-truth
- CCS: https://github.com/collin-burns/discovering_latent_knowledge
- Lying Detection: https://github.com/sisinflab/HidingInTheHiddenStates
- RepE: https://github.com/andyzoujm/representation-engineering
- ITI: https://github.com/likenneth/honest_llama

**Validators & Evaluation:**
- Weaver: https://github.com/HazyResearch/scaling-verification
- COLLIE: https://github.com/princeton-nlp/Collie
- LLMBar: https://github.com/princeton-nlp/LLMBar
- IFEval (lm-eval): https://github.com/EleutherAI/lm-evaluation-harness

**Inference Methods (Baselines):**
- DoLa: https://github.com/voidism/DoLa
- Contrastive Decoding: https://github.com/XiangLi1999/ContrastiveDecoding
- ICD: https://github.com/HillZhang1999/ICD

**Benchmarks:**
- TruthfulQA: https://github.com/sylinrl/TruthfulQA

### 📊 Best Datasets for V2G

**Verifiable Constraints (Strong Validators):**
1. **COLLIE** - 2,080 constrained tasks, 13 types
2. **IFEval** - Verifiable instruction following
3. **InFoBench** - Decomposed requirements

**Factuality (Hidden Knowledge):**
1. **TruthfulQA** - 817 questions, 38 categories
2. Custom true/false pairs for probing

**Reasoning (Self-Consistency):**
1. **GSM8K** - Math word problems
2. **CommonsenseQA** - Commonsense reasoning

**Preference Learning:**
1. Anthropic HH dataset
2. Reddit TL;DR summaries
3. AlpacaEval 2, MT-Bench

### 🎯 Key Research Insights for V2G

**Strongest Evidence:**
1. **Hidden knowledge exists** - 40% gap (Inside-Out), linear structure (Geometry)
2. **G-V gap is real** - RankAlign, Paradox, multiple papers confirm
3. **Ranking > pairwise** - 31.8% improvement (RankAlign), LiPO confirms
4. **Training > inference-time** - V2G for persistent gains vs. DoLa/ITI/CD

**Critical Warnings:**
1. **Overoptimization** - Monitor gold metrics, use holdout validators
2. **Judge quality matters** - LLMBar shows biases; use ensembles (Weaver)
3. **Self-correction limited** - Need external validators (SELF-[IN]CORRECT)

**Best Practices:**
1. **Listwise training** when possible (RankAlign, LiPO)
2. **Verifiable constraints** anchor rankings (COLLIE, IFEval)
3. **Ensemble validators** reduce noise (Weaver)
4. **Frozen/strong validators** avoid collapse (Self-Rewarding caution)
5. **Weight top-of-list** errors more (LiPO-λ, DCG)

### 📝 Research Gaps V2G Addresses

1. **Training-time alignment** (most work is inference-time: DoLa, ITI, CD)
2. **Listwise ranking signals** (most work uses pairwise: DPO)
3. **Surfacing hidden knowledge** (evidence exists: Inside-Out, Geometry; V2G surfaces it)
4. **Persistent improvements** (vs. inference-time interventions)
5. **Systematic G-V gap closure** (framework + method)

---

**Last updated:** 2026-02-10  
**Total papers:** 40  
**Code repositories:** 20+  
**Datasets identified:** 15+

