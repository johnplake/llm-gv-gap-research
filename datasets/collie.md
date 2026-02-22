# COLLIE (ICLR 2024, Princeton NLP) — dataset inspection + adaptation notes

Repo: https://github.com/princeton-nlp/Collie (cloned locally under `Projects/v2g/datasets/collie_repo/`).

## What’s in `data/all_data.dill`
`data/all_data.dill` is a pickled (dill) Python object:

- **Top-level:** `dict[str, list[dict]]`
- **Keys:** dataset splits like `wiki_c14`, `guten_c10`, `ccnews_c06a`, `english_c12`, etc.
  - pattern: `<source>_<constraint_id>`
  - `constraint_id` ∈ {`c01`,`c02`,`c04`,`c05`,`c06a`,`c07`,`c08`,`c09`,`c10`,`c11`,`c12`,`c13`,`c14`} (13 types)
- **Each instance** is a `dict` with fields:
  - `prompt: str` — natural-language instruction specifying the constraints
  - `example: str` — a reference completion that *satisfies* the constraints
  - `constraint: collie.constraints.Constraint | collie.constraints.All | ...` — executable constraint object
  - `targets: Any` — target(s) consumed by the constraint object; often a mix of list(s)/int(s)/string(s)
  - `metadata: dict` — source metadata (e.g., `{'index': ..., 'title': ...}` for wiki)

### Minimal validation / scoring
To check whether a candidate completion `y` satisfies an instance `x`:

```python
ok = x["constraint"](y, x["targets"])  # bool
```

This is exactly what `collie/examples/validate.py` demonstrates.

### Example instance (from `wiki_c14`)
The `constraint` can be a **conjunction** of multiple atomic constraints, represented as `All(...)`.

For `wiki_c14[0]`, the constraint is:

- split completion into **paragraphs** (InputLevel(paragraph))
- per paragraph, split into **sentences** (TargetLevel(sentence))
- enforce:
  1) for each paragraph, **last sentence** equals a provided target sentence (target is a list of sentences)
  2) for each paragraph, **#sentences ≥ 2** (target is an integer)

The stored `example` satisfies: `x['constraint'](x['example'], x['targets']) == True`.

## Basic stats (computed from `all_data.dill`)
Total instances: **2080**.

Instances by source (from key prefix):
- `wiki`: 649
- `guten`: 613
- `ccnews`: 613
- `english`: 205

Instances by constraint_id (from key suffix):
- c10: 286
- c05: 279
- c09: 274
- c07: 267
- c12: 229
- c14: 228
- c04: 113
- c06a: 108
- c01: 100
- c02: 98
- c13: 98
- c11: 97
- c08: 3

### “How many constraints per instance?”
If we count **atomic** `Constraint(...)` objects inside the logical tree (e.g. an `All(a,b)` has 2), we get:

- mean: **2.153** atomic constraints / instance
- min: 1
- max: 4

### Atomic constraint “signatures” (rough)
Each atomic constraint can be summarized by:
`(input_level, target_level, transformation, relation, reduction, reduction_value)`.

We observed **16** distinct atomic signatures in this dataset; most common ones include:
- `(None, 'word', 'ForEach', 'not in', None, None)`  — 822 occurrences
- `(None, 'sentence', 'Count', '==', None, None)`    — 789
- `('sentence','word','ForEach','>=','all',None)`    — 341
- `('sentence','word','ForEach','<=','all',None)`    — 286
- `(None,'word','Count','==',None,None)`             — 279
- `(None,'word','Position','==',None,None)`          — 279
- `(None,'word','ForEach','in',None,None)`           — 267
- `('sentence','word','ForEach','==','all',None)`    — 265
- `('paragraph','sentence','ForEach','==','all',None)` — 228
- `('paragraph','sentence','ForEach','>=','all',None)` — 228

(These map fairly directly to the 13 “constraint_id” templates; many templates are conjunctions of 2 atomic constraints.)

## Generating multiple candidates per prompt + filtering
COLLIE itself is designed for **generate → validate** workflows.

### Correct candidates (~10 per prompt)
Use repeated sampling from an LLM, and **accept** only candidates that satisfy the constraints:

1. for i in 1..N_attempts:
   - sample completion y from model (use temperature > 0)
   - compute `ok = constraint(y, targets)`
   - if ok: keep
2. stop once you have ~10 ok candidates (or hit attempt budget)

This is plain **rejection sampling**.

Practical tips:
- Many constraints are quite strict; you may need higher attempt budget (e.g., 50–200) depending on model.
- Consider *structured prompting*: instruct the model to explicitly plan paragraphs/sentences/word counts.
- For word-level constraints, reduce variance by asking for shorter outputs.

### Incorrect candidates (~10 per prompt)
Options:

**A) Negative rejection sampling (simple):**
- sample y from model
- keep if `constraint(y, targets) == False`

Downside: negatives may be “trivially wrong” (completely ignore constraints) rather than near-miss.

**B) Adversarial/near-miss negatives (recommended):**
Start from a known-good completion (e.g., `example` or a model-found positive) and apply *targeted edits* that violate exactly one atomic constraint, then re-check.

Examples of systematic corruptions:
- If constraint requires a **specific last sentence per paragraph**: change or remove that last sentence in one paragraph.
- If constraint requires **≥k sentences per paragraph**: merge two sentences or delete one.
- If constraint requires **forbidden words** (`not in`): insert a forbidden token.
- If constraint requires **must-include words** (`in`): remove one required token.
- If constraint requires **position == target** (e.g., first/last word): replace that position word.
- If constraint is **count == n**: add/remove a token to change the count.

Then keep as negative if it fails validation.

This yields “hard negatives” close to the decision boundary.

## Adaptation plan for V2G: ~10 correct + ~10 incorrect per prompt
Suggested pipeline:

1. **Load** COLLIE instances (prompt, constraint, targets, example).
2. For each instance:
   - Seed positives with stored `example` (already valid).
   - Use LLM sampling to find additional positives via rejection sampling until you have 10.
   - Generate near-miss negatives by mutating positives; verify with constraint until you have 10.
3. Store V2G-ready record:
   - `prompt`
   - `constraint_id` (from key suffix)
   - `constraint_serialization` (optional: `str(constraint)` is human readable)
   - `targets`
   - `candidates_pos: list[str]`
   - `candidates_neg: list[str]`

Implementation detail: dill-unpickling requires the COLLIE python classes. If you don’t want to depend on their environment, you can keep their code vendored.

---

## Repro notes (this workspace)
This environment lacked pip/nltk/rich, so I used:
- vendored dill source under `collie_repo/third_party/dill-0.3.8/`
- lightweight stubs under `collie_repo/fake_deps/` for `nltk` tokenizers + `rich.print`

This is enough to load `all_data.dill` and run `constraint(text, targets)` for analysis.
