# V2G Papers: Quick Reference with Code/Data Links

## Core V2G Papers

### 🔥 RankAlign (Rodriguez et al., 2025)
**Paper:** https://arxiv.org/abs/2504.11381  
**Code:** https://github.com/juand-r/rankalign  
**Why:** THE foundational paper - defines ranking-based training for G-V gap. 31.8% gap closure.

### 🔥 Inside-Out (Gekhman et al., 2025)
**Paper:** https://arxiv.org/abs/2503.15299  
**Code:** 🔍 Searching (very recent)  
**Why:** Proves 40% hidden knowledge gap - strong motivation for V2G approach.

### 🔥 Generative AI Paradox (West et al., 2024)
**Paper:** https://arxiv.org/abs/2311.00059  
**Code:** No public code  
**Why:** Empirical foundation showing generation ≠ discrimination systematically.

### 🔥 G-V Consistency Benchmark (Li et al., 2024)
**Paper:** https://arxiv.org/abs/2310.01846  
**Code:** 🔍 Searching  
**Why:** Complementary framework, shows 16% generator + 6.3% validator improvements.

---

## Probing & Hidden Knowledge

### Geometry of Truth (Marks & Tegmark, 2024)
**Paper:** https://arxiv.org/abs/2310.06824  
**Code:** https://github.com/saprmarks/geometry-of-truth  
**Why:** Linear structure of truth in representations → ranking training can leverage this.

### LLMs Know More (Orgad et al., 2024)
**Paper:** https://arxiv.org/abs/2410.02707  
**Code:** https://github.com/sriharshapy/LLM-knows-more-than-they-show (reproduction)  
**Why:** Internal representations encode truthfulness even when outputs are wrong.

### CCS (Burns et al., 2023)
**Paper:** https://arxiv.org/abs/2212.03827  
**Code:** https://github.com/collin-burns/discovering_latent_knowledge  
**Why:** Unsupervised latent knowledge extraction using contrast pairs.

### LLM Lying (Azaria & Mitchell, 2023)
**Paper:** https://arxiv.org/abs/2304.13734  
**Code:** https://github.com/sisinflab/HidingInTheHiddenStates (related impl)  
**Why:** 71-83% accuracy in detecting lies from hidden states.

---

## Preference Learning & Alignment

### DPO (Rafailov et al., 2023)
**Paper:** https://arxiv.org/abs/2305.18290  
**Code:** https://github.com/eric-mitchell/direct-preference-optimization  
**Why:** Pairwise preferences baseline - V2G extends to listwise rankings.

### SimPO (Meng et al., 2024)
**Paper:** https://arxiv.org/abs/2405.14734  
**Code:** https://github.com/princeton-nlp/SimPO  
**Why:** Reference-free alternative to DPO - complementary approach.

### InstructGPT/RLHF (Ouyang et al., 2022)
**Paper:** https://arxiv.org/abs/2203.02155  
**Code:** No public code (OpenAI)  
**Why:** Foundation of preference learning paradigm that V2G extends.

---

## Instruction Following

### COLLIE (Yao et al., 2024)
**Paper:** https://arxiv.org/abs/2307.08689  
**Code:** https://github.com/princeton-nlp/Collie  
**Data:** 2,080 constrained generation instances  
**Why:** Challenging evaluation benchmark for V2G improvements.

---

## More Papers Coming...

Sub-agent is compiling comprehensive summaries for all 40 papers. Check `v2g-paper-summaries.md` when complete.

Key patterns across papers:
- **Hidden knowledge exists** (Inside-Out, Geometry of Truth, LLMs Know More)
- **G-V gap is real** (RankAlign, Paradox, Kadavath)
- **Ranking > pairwise** (RankAlign, LiPO)
- **Training > inference-time fixes** (V2G vs. DoLa/ITI)

