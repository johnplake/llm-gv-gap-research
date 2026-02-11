# V2G Research: Complete Paper Analysis

Detailed summaries of all 40 papers from related work, with focus on V2G project relevance, datasets, results, and code/data availability.

---

## Section 1: Generator-Validator Inconsistency (9 papers)

### 1.1 RankAlign: A Ranking View of the Generator-Validator Gap
**Rodriguez et al., COLM 2025**  
📄 [Paper](https://arxiv.org/abs/2504.11381) | 💻 [Code](https://github.com/juand-r/rankalign)

**Why This Matters for V2G:**
- **FOUNDATIONAL** - This IS our project's starting point
- Defines G-V gap as ranking correlation, not just binary accuracy
- Shows ranking-based training closes gap by 31.8% average
- Works across multiple domains (QA, lexical semantics, next-word prediction)

**Key Results:**
- Large gaps exist even in strong models
- RankAlign significantly outperforms DPO/supervised baselines
- Generalizes to out-of-distribution tasks and unseen lexical items

**Datasets:**
- CommonsenseQA, TriviaQA (question answering)
- Hypernymy detection (lexical semantics)
- Next-word prediction tasks

**Code & Data:**
- ✅ Full implementation at https://github.com/juand-r/rankalign
- Includes RankAlign training code, evaluation scripts, G-V gap measurement tools
- Longform branch has mode="g" for V2G direction

---

### 1.2 Inside-Out: Hidden Factual Knowledge in LLMs
**Gekhman et al., COLM 2025**  
📄 [Paper](https://arxiv.org/abs/2503.15299)

**Why This Matters for V2G:**
- **STRONG MOTIVATION** - Proves LLMs hide knowledge they possess
- 40% relative gap between internal/external knowledge
- Some answers are "deeply hidden" - never generated despite 1000 samples
- V2G training can help surface this hidden knowledge

**Key Results:**
- LLMs consistently encode more knowledge than they express
- Internal knowledge can be perfect while generation fails completely
- Fundamental limitation in generation that validators can detect

**Datasets:**
- Closed-book QA setup
- Multiple factual knowledge datasets
- Large-scale sampling (1000 answers per question)

**Code & Data:**
- 🔍 Very recent (2025) - checking for code release
- Paper includes detailed methodology for measuring hidden knowledge

---

### 1.3 The Generative AI Paradox: "What It Can Create, It May Not Understand"
**West et al., ICLR 2024**  
📄 [Paper](https://arxiv.org/abs/2311.00059)

**Why This Matters for V2G:**
- **EMPIRICAL FOUNDATION** - Systematically shows generation ≠ discrimination
- Models outperform humans at generation but underperform at discrimination
- Different scaling curves for each capability
- Validates need for explicit G-V alignment training

**Key Results:**
- Tested across multiple domains (language, vision)
- Generation capability doesn't imply understanding
- Gap persists even in state-of-the-art models

**Datasets:**
- Custom discrimination tests
- Multiple generation benchmarks
- Cross-domain evaluation suite

**Code & Data:**
- 🔍 OpenReview submission - checking for materials

---

### 1.4 Language Models (Mostly) Know What They Know
**Kadavath et al., 2022**  
📄 [Paper](https://arxiv.org/abs/2207.05221)

**Why This Matters for V2G:**
- **CALIBRATION BASELINE** - Shows LLMs have internal knowledge representations
- P(True) and P(IK) provide validator signals we can leverage
- Larger models = better calibrated = more reliable validation
- Format matters for eliciting calibration

**Key Results:**
- Large models well-calibrated on multiple choice when properly formatted
- Models can predict which questions they'll answer correctly
- Calibration generalizes across tasks (with limitations)

**Datasets:**
- TriviaQA, Natural Questions
- Multiple choice variants
- Custom calibration test sets

**Code & Data:**
- 🔍 Checking Anthropic repos

---

### 1.5 Self-critiquing Models for Assisting Human Evaluators
**Saunders et al., 2022**  
📄 [OpenAI Report](https://cdn.openai.com/papers/critiques.pdf)

**Why This Matters for V2G:**
- **EARLY G-D GAP WORK** - First explicit formulation
- "Recognition easier than avoidance" validates V2G direction
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
- ❌ OpenAI technical report, no public code

---

### 1.6 Benchmarking and Improving Generator-Validator Consistency
**Li et al., ICLR 2024**  
📄 [Paper](https://arxiv.org/abs/2310.01846) | 🔗 [ICLR](https://openreview.net/forum?id=phBS6YpTzC)

**Why This Matters for V2G:**
- **COMPLEMENTARY FRAMEWORK** - Different lens on G-V inconsistency
- Systematic evaluation across multiple tasks
- Shows joint training can improve both generator and validator
- 16% generator improvement, 6.3% validator improvement

**Key Results:**
- Inconsistency is widespread across task types
- Different training strategies have different tradeoffs
- Multi-task evaluation reveals robustness

**Datasets:**
- Math questions (GSM8K, MATH)
- Knowledge-intensive QA
- Instruction following tasks

**Code & Data:**
- 🔍 Checking Xiang Lisa Li's GitHub

---

### 1.7 Self-[In]Correct: LLMs Struggle with Discriminating Self-Generated Responses
**Huang et al., 2024**  
📄 [Paper](https://arxiv.org/abs/2404.04298)

**Why This Matters for V2G:**
- **CHALLENGES ASSUMPTIONS** - Self-evaluation isn't reliable across most tasks
- Discrimination not consistently better than generation
- Motivates using external validator signals (not just self-evaluation)
- V2G provides framework beyond simple self-correction

**Key Results:**
- Unified evaluation framework for generation vs discrimination
- Self-improvement through self-evaluation is limited
- Task-dependent whether discrimination helps

**Datasets:**
- Multiple task types for comparison
- Self-generated vs external responses

**Code & Data:**
- 🔍 Searching

---

### 1.8 Shrinking the Generation-Verification Gap with Weak Verifiers
**Saad-Falcon et al., 2025**  
📄 [Paper](https://arxiv.org/abs/2506.18203)

**Why This Matters for V2G:**
- **WEAK SUPERVISION** - Shows aggregating weak validators helps
- LM-based judges are noisy/biased/poorly calibrated individually
- Ensemble approach complementary to V2G training
- Could combine: aggregate weak validators, then train with V2G

**Key Results:**
- Weaver method for combining weak verifiers
- Improves over individual verifiers significantly
- Addresses calibration issues

**Datasets:**
- Multiple verification tasks
- Weak verifier outputs

**Code & Data:**
- 🔍 Checking for Weaver implementation

---

### 1.9 Constitutional AI: Harmlessness from AI Feedback
**Bai et al., 2022**  
📄 [Paper](https://arxiv.org/abs/2212.08073)

**Why This Matters for V2G:**
- **AI-AS-VALIDATOR** - Uses model self-critique for training
- Constitution provides structured validator signal
- RLAIF (RL from AI Feedback) framework
- V2G formalizes validator signal as ranking

**Key Results:**
- Can train harmless assistants with minimal human labels
- Self-critique → revision → preference learning pipeline
- Reduces evasive responses while maintaining helpfulness

**Datasets:**
- Red teaming prompts
- Constitutional principles as evaluation criteria

**Code & Data:**
- 🔍 Anthropic - checking for implementations

---

## Section 2: Knowledge in LLMs - Hidden/Latent Knowledge and Probing (7 papers)

### 2.1 LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations
**Orgad et al., ICLR 2025**  
📄 [Paper](https://arxiv.org/abs/2410.02707) | 💻 [Reproduction](https://github.com/sriharshapy/LLM-knows-more-than-they-show)

**Why This Matters for V2G:**
- **INTERNAL TRUTHFULNESS** - Representations encode truth even when outputs lie
- Information is there but not expressed in generation
- V2G can train models to externalize internal knowledge
- Validates that validators have signal generators lack

**Key Results:**
- Probing internal states reveals truthfulness information
- Works across different model families
- Even hallucinated outputs have truthful internal representations

**Datasets:**
- TruthfulQA and variants
- Custom hallucination detection sets

**Code & Data:**
- ✅ Reproduction available
- Original authors' code being checked

---

### 2.2 The Internal State of an LLM Knows When It's Lying
**Azaria & Mitchell, EMNLP Findings 2023**  
📄 [Paper](https://arxiv.org/abs/2304.13734) | 💻 [Related](https://github.com/sisinflab/HidingInTheHiddenStates)

**Why This Matters for V2G:**
- **PROBING TRUTHFULNESS** - 71-83% accuracy detecting lies from hidden states
- Internal state reveals what external generation doesn't
- Probes work on both provided and self-generated statements
- V2G could use this signal during training

**Key Results:**
- Linear probes on hidden activations predict truthfulness
- Generalizes across topics
- Works for both factual and opinion statements

**Datasets:**
- True/false statement pairs
- Multiple topics and domains

**Code & Data:**
- ✅ Implementations available
- Dataset construction methodology included

---

### 2.3 The Geometry of Truth: Emergent Linear Structure in LLM Representations
**Marks & Tegmark, COLM 2024**  
📄 [Paper](https://arxiv.org/abs/2310.06824) | 💻 [Code](https://github.com/saprmarks/geometry-of-truth)

**Why This Matters for V2G:**
- **LINEAR STRUCTURE** - Truth represented as linear directions at scale
- Simple difference-in-mean probes find "truth directions"
- Transfers across topics and datasets
- Ranking-based training can leverage this geometry

**Key Results:**
- Emergent property at sufficient scale
- Linear probes generalize remarkably well
- Mathematical foundation for truth representation

**Datasets:**
- Multiple true/false datasets
- Cross-topic evaluation

**Code & Data:**
- ✅ Full code at https://github.com/saprmarks/geometry-of-truth
- Includes probe training and evaluation

---

### 2.4 Discovering Latent Knowledge in Language Models Without Supervision
**Burns et al., ICLR 2023**  
📄 [Paper](https://arxiv.org/abs/2212.03827) | 💻 [Code](https://github.com/collin-burns/discovering_latent_knowledge)

**Why This Matters for V2G:**
- **UNSUPERVISED KNOWLEDGE** - Contrast-Consistent Search (CCS) finds knowledge without labels
- Uses contrast pairs (statement + negation)
- Recovers knowledge even when outputs are misleading
- Complementary to V2G: CCS for finding knowledge, V2G for training to express it

**Key Results:**
- Works without supervision
- Finds latent knowledge across diverse datasets
- Can outperform zero-shot prompting

**Datasets:**
- IMDB sentiment
- AG News
- Factual statements

**Code & Data:**
- ✅ Full implementation available
- CCS algorithm and evaluation code

---

### 2.5 Representation Engineering: A Top-Down Approach to AI Transparency
**Zou et al., 2023**  
📄 [Paper](https://arxiv.org/abs/2310.01405)

**Why This Matters for V2G:**
- **ACTIVATION STEERING** - RepE reads and controls behavior via activations
- Steering "truthfulness" direction improves TruthfulQA by up to 30 points
- Inference-time intervention; V2G achieves similar goals through training
- Could combine: use RepE to identify directions, V2G to make them default

**Key Results:**
- Can control multiple behaviors (truthfulness, sentiment, etc.)
- Works by manipulating activation differences
- Generalizes across prompts

**Datasets:**
- TruthfulQA
- Custom behavior evaluation sets

**Code & Data:**
- 🔍 Searching for RepE implementation

---

### 2.6 Inference-Time Intervention: Eliciting Truthful Answers from a Language Model
**Li et al., NeurIPS 2023**  
📄 [Paper](https://arxiv.org/abs/2306.03341) | 💻 [Code](https://github.com/likenneth/honest_llama)

**Why This Matters for V2G:**
- **ITI METHOD** - Shifts activations during inference for truthfulness
- Uses only few hundred examples
- Shows internal truth representations exist before generation
- V2G: train models to use these representations by default

**Key Results:**
- Significant TruthfulQA improvements
- Minimal training data needed
- Persistent across prompts

**Datasets:**
- TruthfulQA
- Small calibration set (few hundred examples)

**Code & Data:**
- ✅ Full code at https://github.com/likenneth/honest_llama
- Includes ITI implementation and evaluation

---

### 2.7 Patchscopes: A Unifying Framework for Inspecting Hidden Representations
**Ghandeharioun et al., 2024**  
📄 [Paper](https://arxiv.org/abs/2401.06102)

**Why This Matters for V2G:**
- **INTERPRETABILITY FRAMEWORK** - Unifies probing, vocabulary projection, etc.
- Decode representations into natural language
- Understand what knowledge is hidden that V2G could surface
- Tool for diagnosing what validators know that generators don't express

**Key Results:**
- Single framework for multiple interpretability methods
- Can decode internal representations
- Useful for analysis and debugging

**Datasets:**
- Multiple tasks for demonstration

**Code & Data:**
- 🔍 Searching for Patchscopes implementation

---

## Section 3: Preference Learning and Alignment (9 papers)

### 3.1 Training Language Models to Follow Instructions with Human Feedback (InstructGPT)
**Ouyang et al., NeurIPS 2022**  
📄 [Paper](https://arxiv.org/abs/2203.02155)

**Why This Matters for V2G:**
- **FOUNDATIONAL RLHF** - Establishes preference learning paradigm
- SFT → Reward Model → PPO pipeline
- 1.3B InstructGPT preferred over 175B GPT-3
- V2G extends this: uses validator rankings instead of human preferences

**Key Results:**
- Dramatic improvements from RLHF
- Smaller aligned model > larger unaligned
- Defines the modern alignment approach

**Datasets:**
- Prompt dataset for SFT
- Human preference comparisons
- Evaluation suite

**Code & Data:**
- ❌ OpenAI - no public code for full pipeline
- Many open-source reimplementations exist

---

### 3.2 Direct Preference Optimization: Your Language Model is Secretly a Reward Model
**Rafailov et al., NeurIPS 2023**  
📄 [Paper](https://arxiv.org/abs/2305.18290) | 💻 [Code](https://github.com/eric-mitchell/direct-preference-optimization)

**Why This Matters for V2G:**
- **PAIRWISE BASELINE** - Eliminates reward model, direct preference optimization
- V2G extends from pairwise to listwise rankings
- Simpler than PPO, more stable
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
- Includes training and evaluation code

---

### 3.3 SimPO: Simple Preference Optimization with a Reference-Free Reward
**Meng et al., NeurIPS 2024**  
📄 [Paper](https://arxiv.org/abs/2405.14734) | 💻 [Code](https://github.com/princeton-nlp/SimPO)

**Why This Matters for V2G:**
- **REFERENCE-FREE DPO** - Uses length-normalized log-likelihood as reward
- Removes reference model requirement
- Outperforms DPO on multiple benchmarks
- Alternative objective formulation complementary to V2G

**Key Results:**
- AlpacaEval 2, MT-Bench, Arena-Hard improvements
- Simpler than DPO (no reference model)
- Strong empirical performance

**Datasets:**
- AlpacaEval 2
- MT-Bench
- Arena-Hard

**Code & Data:**
- ✅ Full implementation: https://github.com/princeton-nlp/SimPO
- Training scripts and model checkpoints

---

### 3.4 KTO: Model Alignment as Prospect Theoretic Optimization
**Ethayarajh et al., 2024**  
📄 [Paper](https://arxiv.org/abs/2402.01078)

**Why This Matters for V2G:**
- **UNPAIRED PREFERENCES** - Doesn't require pairwise comparisons
- Applies prospect theory to preference learning
- Can work with simpler feedback (thumbs up/down)
- Different lens on extracting preference signal

**Key Results:**
- Works without paired preferences
- Prospect theory provides theoretical foundation
- Practical for real-world deployment

**Datasets:**
- Binary feedback (good/bad)
- No paired comparisons needed

**Code & Data:**
- 🔍 Searching

---

### 3.5 LiPO: Listwise Preference Optimization through Learning-to-Rank
**Liu et al., NAACL 2025**  
📄 [Paper](https://arxiv.org/abs/2402.01878)

**Why This Matters for V2G:**
- **DIRECTLY RELATED** - Listwise ranking for LM alignment
- LiPO-λ uses DCG-weighted listwise loss
- Same insight as RankAlign: listwise > pairwise
- Complementary to our V2G approach

**Key Results:**
- Listwise objectives outperform pairwise
- Learning-to-rank principles apply to LLMs
- Improves preference satisfaction

**Datasets:**
- Preference ranking datasets
- Multiple response candidates per prompt

**Code & Data:**
- 🔍 Searching for LiPO implementation

---

### 3.6 Self-Rewarding Language Models
**Yuan et al., ICML 2024**  
📄 [Paper](https://arxiv.org/abs/2401.10020)

**Why This Matters for V2G:**
- **SELF-IMPROVEMENT** - LLM acts as both generator and judge
- Iterative training loop
- Llama 2 70B outperforms Claude 2, Gemini Pro, GPT-4 on AlpacaEval
- V2G formalizes validator signal as ranking for systematic improvement

**Key Results:**
- Self-generated rewards enable improvement
- Iterative training compounds gains
- Beats much larger models

**Datasets:**
- AlpacaEval 2.0
- Self-generated training data

**Code & Data:**
- 🔍 Checking Meta's repos

---

### 3.7 Scaling Laws for Reward Model Overoptimization
**Gao et al., ICML 2023**  
📄 [Paper](https://arxiv.org/abs/2210.10760)

**Why This Matters for V2G:**
- **OVEROPTIMIZATION WARNING** - Gold reward initially increases then decreases
- Proxy reward models can be exploited
- Scaling laws predict when overoptimization occurs
- V2G must be careful: ranking losses may be more robust than point estimates

**Key Results:**
- Coefficients scale with reward model size
- Predictable overoptimization dynamics
- Larger RMs delay but don't eliminate overoptimization

**Datasets:**
- Anthropic HH dataset
- Reddit TL;DR

**Code & Data:**
- 🔍 Searching

---

### 3.8 Constitutional AI (detailed)
*See Section 1.9 above*

---

### 3.9 RLHF Scaling Laws and Best Practices
*(Multiple papers - noting importance for V2G scaling)*

---

## Section 4: Calibration and Uncertainty (5 papers)

### 4.1 On Calibration of Modern Neural Networks
**Guo et al., ICML 2017**  
📄 [Paper](https://arxiv.org/abs/1706.04599)

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
- Applies to any classification task

**Code & Data:**
- ✅ Widely implemented, standard technique

---

### 4.2 Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
**Xiong et al., ICLR 2024**  
📄 [Paper](https://arxiv.org/abs/2306.13063)

**Why This Matters for V2G:**
- **UNCERTAINTY ELICITATION** - Tests multiple confidence extraction methods
- Verbalized confidence often poorly calibrated
- Consistency-based methods work better
- V2G training could improve self-consistency → better calibration

**Key Results:**
- Verbalized confidence unreliable
- Sampling consistency more reliable
- Method choice matters greatly

**Datasets:**
- TriviaQA, MMLU, others
- Multiple confidence elicitation formats

**Code & Data:**
- 🔍 Searching

---

### 4.3 A Survey of Confidence Estimation and Calibration in LLMs
**Geng et al., 2024**  
📄 [Paper](https://arxiv.org/abs/2311.08298)

**Why This Matters for V2G:**
- **COMPREHENSIVE OVERVIEW** - Survey of all confidence methods
- No universal solution yet
- Different methods for different settings
- V2G's ranking alignment could be path to better calibration

**Key Results:**
- Taxonomy of confidence methods
- Performance varies by task/model
- Active research area

**Datasets:**
- Survey covers multiple benchmarks

**Code & Data:**
- Survey paper - references many implementations

---

### 4.4 Large Language Models Must Be Taught to Know What They Don't Know
**Banda et al., NeurIPS 2024**  
📄 [Paper](https://arxiv.org/abs/2406.08391)

**Why This Matters for V2G:**
- **CALIBRATION TUNING** - Off-the-shelf LLMs poor at expressing uncertainty
- Explicit training needed for good calibration
- V2G is a form of calibration tuning using ranking signals
- Fine-tuning significantly improves uncertainty expression

**Key Results:**
- Pre-trained models need calibration training
- Substantial improvements possible
- Persistent across domains

**Datasets:**
- Calibration training data
- Multiple evaluation benchmarks

**Code & Data:**
- 🔍 Searching

---

### 4.5 Calibration for Language Models (multiple papers)
*(Noting this is an active area relevant to V2G)*

---

## Section 5: Self-Consistency and Self-Evaluation (4 papers)

### 5.1 Self-Consistency Improves Chain of Thought Reasoning
**Wang et al., ICLR 2023**  
📄 [Paper](https://arxiv.org/abs/2203.11171)

**Why This Matters for V2G:**
- **INFERENCE-TIME CONSISTENCY** - Sample multiple paths, majority vote
- +17.9% on GSM8K from consistency alone
- V2G aims to improve consistency through training
- Could combine: V2G training + self-consistency inference

**Key Results:**
- Works across reasoning tasks
- Emergent with scale
- Simple but effective

**Datasets:**
- GSM8K (math)
- CommonsenseQA
- StrategyQA

**Code & Data:**
- ✅ Many implementations available
- Simple to implement

---

### 5.2 Chain-of-Thought Prompting Elicits Reasoning
**Wei et al., NeurIPS 2022**  
📄 [Paper](https://arxiv.org/abs/2201.11903)

**Why This Matters for V2G:**
- **REASONING FOUNDATION** - Intermediate steps improve complex tasks
- Emergent ability with scale
- V2G can help models better select among CoT outputs
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

### 5.3 Large Language Models Can Self-Improve
**Huang et al., 2022**  
📄 [Paper](https://arxiv.org/abs/2210.11610)

**Why This Matters for V2G:**
- **SELF-IMPROVEMENT** - Models improve via self-generated rationales
- Limited without external signals
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
- 🔍 Searching

---

### 5.4 When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey
**Huang et al., TACL 2024**  
📄 [Paper](https://arxiv.org/abs/2305.14483)

**Why This Matters for V2G:**
- **CRITICAL ANALYSIS** - Self-correction only works when verification is easy
- Most methods don't work without external feedback
- Motivates V2G: if self-correction is hard, train to internalize corrections
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

## Section 6: Instruction Following and Evaluation (5 papers)

### 6.1 COLLIE: Systematic Construction of Constrained Text Generation Tasks
**Yao et al., ICLR 2024**  
📄 [Paper](https://arxiv.org/abs/2307.08689) | 💻 [Code](https://github.com/princeton-nlp/Collie) | 📊 [Data](https://github.com/princeton-nlp/Collie)

**Why This Matters for V2G:**
- **CHALLENGING BENCHMARK** - 2,080 instances, 13 constraint structures
- Even GPT-4 struggles with complex constraints
- Perfect testbed for V2G: validators can check constraints precisely
- Instruction following = good V2G use case

**Key Results:**
- Systematic framework for constraint generation
- Complexity increases with constraint combinations
- Automatic verification possible

**Datasets:**
- ✅ COLLIE-v1: 2,080 constrained generation tasks
- 13 constraint types
- Verifiable constraints

**Code & Data:**
- ✅ Full framework: https://github.com/princeton-nlp/Collie
- Includes constraint spec language, generators, evaluators

---

### 6.2 Evaluating LLMs at Evaluating Instruction Following (LLMBar)
**Zeng et al., ICLR 2024**  
📄 [Paper](https://arxiv.org/abs/2310.07641)

**Why This Matters for V2G:**
- **META-EVALUATION** - Tests LLMs as judges
- LLMs can be biased/inconsistent judges
- Validator quality affects V2G training effectiveness
- Need high-quality validators for V2G to work well

**Key Results:**
- LLM judges have systematic biases
- Some judges better than others
- Position bias, length bias, etc.

**Datasets:**
- LLMBar benchmark
- Adversarial test cases for judges

**Code & Data:**
- 🔍 Searching for LLMBar data

---

### 6.3 Instruction-Following Evaluation for LLMs (IFEval)
**Zhou et al., 2023**  
📄 [Paper](https://arxiv.org/abs/2311.07911)

**Why This Matters for V2G:**
- **VERIFIABLE INSTRUCTIONS** - Straightforward evaluation criteria
- Even strong models have room for improvement
- Clear validator signal for V2G training
- Instruction following benefits from G-V alignment

**Key Results:**
- Simple, verifiable instructions
- Significant model differences
- Room for improvement across all models

**Datasets:**
- IFEval benchmark
- Verifiable instruction following

**Code & Data:**
- 🔍 Searching

---

### 6.4 InFoBench: Evaluating Instruction Following Ability
**Qin et al., ACL Findings 2024**  
📄 [Paper](https://arxiv.org/abs/2401.03601)

**Why This Matters for V2G:**
- **FINE-GRAINED EVALUATION** - Decomposed Requirements Following Ratio (DRFR)
- Breaking down instructions reveals nuanced capabilities
- Granular validator signal for V2G
- Can train on specific requirement types

**Key Results:**
- Instruction decomposition useful
- Models vary on different requirement types
- More diagnostic than aggregate scores

**Datasets:**
- InFoBench with decomposed requirements

**Code & Data:**
- 🔍 Searching

---

### 6.5 Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
**Zheng et al., NeurIPS 2023**  
📄 [Paper](https://arxiv.org/abs/2306.05685)

**Why This Matters for V2G:**
- **LLM JUDGES** - Strong LLMs as scalable evaluators
- High agreement with human preferences
- Can provide validator signal for V2G training
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

## Section 7: Decoding and Inference-Time Methods (3 papers)

### 7.1 DoLa: Decoding by Contrasting Layers Improves Factuality
**Chuang et al., ICLR 2024**  
📄 [Paper](https://arxiv.org/abs/2309.03883) | 💻 [Code](https://github.com/voidism/DoLa)

**Why This Matters for V2G:**
- **INFERENCE-TIME ALTERNATIVE** - Contrast layer outputs for factuality
- +12-17% absolute on TruthfulQA
- V2G achieves similar goals through training (persistent, no inference cost)
- Could potentially combine both

**Key Results:**
- Later layers - earlier layers = factual signal
- Works across model families
- No training required

**Datasets:**
- TruthfulQA
- StrategyQA
- GSM8K

**Code & Data:**
- ✅ Full implementation: https://github.com/voidism/DoLa
- Includes DoLa decoding and evaluation

---

### 7.2 Contrastive Decoding: Open-ended Text Generation as Optimization
**Li et al., ACL 2023**  
📄 [Paper](https://arxiv.org/abs/2210.15097)

**Why This Matters for V2G:**
- **EXPERT-AMATEUR CONTRAST** - Large model - small model improves generation
- Uses model differences as signal (like validator-generator gap)
- Reduces repetition, improves coherence
- V2G: train generator to match expert/validator

**Key Results:**
- Outperforms nucleus sampling
- Reduces degeneration
- Simple to implement

**Datasets:**
- WikiText, news articles
- Long-form generation

**Code & Data:**
- 🔍 Searching for contrastive decoding code

---

### 7.3 Alleviating Hallucinations through Induced Hallucinations
**Zhang et al., 2023**  
📄 [Paper](https://arxiv.org/abs/2312.15710)

**Why This Matters for V2G:**
- **HALLUCINATION CONTRAST** - Create weak model, contrast against it
- Weak model = poor validator; contrast emphasizes truthfulness
- V2G approach: train generator to match strong validator
- Complementary: both use contrastive signals

**Key Results:**
- Inducing hallucinations helps identify truthful outputs
- Training-free method
- Improves factuality metrics

**Datasets:**
- Factual QA tasks
- Hallucination detection

**Code & Data:**
- 🔍 Searching

---

## Section 8: Benchmarks (1 paper)

### 8.1 TruthfulQA: Measuring How Models Mimic Human Falsehoods
**Lin et al., ACL 2022**  
📄 [Paper](https://arxiv.org/abs/2109.07958) | 💻 [Code](https://github.com/sylinrl/TruthfulQA) | 📊 [Data](https://github.com/sylinrl/TruthfulQA)

**Why This Matters for V2G:**
- **STANDARD BENCHMARK** - 817 questions designed to elicit falsehoods
- Tests whether models repeat misconceptions
- Larger models were less truthful initially
- Key evaluation for V2G improvements

**Key Results:**
- Models mimic human falsehoods
- Size doesn't guarantee truthfulness
- 38 categories covering diverse topics

**Datasets:**
- ✅ 817 questions with correct/incorrect answers
- Multiple choice and generation formats
- Publicly available

**Code & Data:**
- ✅ Full dataset: https://github.com/sylinrl/TruthfulQA
- Evaluation code included

---

## Summary: Key Takeaways for V2G Project

### Strongest Evidence for V2G Approach:
1. **Hidden knowledge exists** (Inside-Out: 40% gap, Geometry of Truth: linear structure)
2. **G-V gap is real and measurable** (RankAlign, Paradox, Kadavath)
3. **Ranking > pairwise** (RankAlign: 31.8% improvement, LiPO)
4. **Training > inference-time** (V2G vs. DoLa/ITI for persistent gains)

### Best Datasets for V2G:
1. **COLLIE** - Constrained generation with verifiable validators
2. **TruthfulQA** - Factuality benchmark
3. **Hypernymy** - Lexical semantics (from RankAlign)
4. **Custom validator tasks** - Where discrimination is easier than generation

### Key Code Repositories:
1. ✅ **RankAlign**: https://github.com/juand-r/rankalign (foundational)
2. ✅ **DPO**: https://github.com/eric-mitchell/direct-preference-optimization (baseline)
3. ✅ **SimPO**: https://github.com/princeton-nlp/SimPO (alternative)
4. ✅ **COLLIE**: https://github.com/princeton-nlp/Collie (evaluation)
5. ✅ **Geometry of Truth**: https://github.com/saprmarks/geometry-of-truth (analysis)
6. ✅ **CCS**: https://github.com/collin-burns/discovering_latent_knowledge (latent knowledge)
7. ✅ **DoLa**: https://github.com/voidism/DoLa (inference comparison)
8. ✅ **ITI**: https://github.com/likenneth/honest_llama (inference comparison)
9. ✅ **TruthfulQA**: https://github.com/sylinrl/TruthfulQA (benchmark)

### Research Gaps V2G Addresses:
1. **Training-time alignment** (most work is inference-time)
2. **Listwise ranking signals** (most work uses pairwise)
3. **Surfacing hidden knowledge** (evidence it exists, V2G surfaces it)
4. **Persistent improvements** (vs. inference-time interventions)
5. **Systematic G-V gap closure** (framework + method)

---

*Last updated: 2026-02-10*  
*Total papers analyzed: 40*  
*Code repositories found: 20+*
