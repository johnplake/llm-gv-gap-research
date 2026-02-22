# Draft report: COLLIE (ICLR 2024) dataset/code inspection for V2G

## TL;DR
COLLIE provides constrained text-generation prompts paired with **executable constraint objects** (Python) + corresponding **targets**, enabling direct automatic validation: `constraint(generation, targets) -> bool`.

Dataset `all_data.dill` contains **2080** instances across **13** constraint templates (`c01..c14` with `c06a`). Average **2.15 atomic constraints** per instance (min 1, max 4).

This makes it well-suited to generate (via LLM sampling) many candidate completions per prompt and then filter into **positive** (satisfies constraints) and **negative** (violates constraints) sets for V2G.

---

## Where the data lives
In the official repo (`princeton-nlp/Collie`), the main artifact is:

- `data/all_data.dill`

This is a dill-serialized Python dict mapping split-keys like `wiki_c14` to lists of instances.

Each instance has:
- `prompt: str`
- `example: str` (known-good completion)
- `constraint: Constraint | All | And | Or ...` (callable)
- `targets: Any` (ints/strings/lists; aligns with constraint tree)
- `metadata: dict` (source info)

Validation is one line:

```python
ok = x["constraint"](y, x["targets"])
```

---

## Dataset stats
### Total size
- **2080** instances

### Sources
- wiki: 649
- guten: 613
- ccnews: 613
- english: 205

### Constraint template counts
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

### Constraints per instance
Counting atomic `Constraint(...)` objects in the logical tree:
- mean: **2.153**
- min: 1
- max: 4

---

## How to get ~10 correct / ~10 incorrect candidates per prompt (V2G adaptation)
### Positives (correct)
Use **rejection sampling**:
1. sample completion(s) from model for the prompt (temperature>0)
2. keep those with `constraint(y, targets) == True`
3. repeat until ~10 positives or attempt budget exceeded

Seed with the dataset’s stored `example` (already valid) to guarantee at least one positive.

### Negatives (incorrect)
Two good options:

**1) Simple negatives:**
- sample from model and keep where `constraint(y, targets) == False`
- fast but can produce “easy” negatives (ignoring constraints)

**2) Hard/near-miss negatives (recommended):**
- start from a valid completion (example or model-found positive)
- apply targeted edits designed to break **exactly one** atomic constraint
- re-check until `constraint(y_bad, targets) == False`

Common break operations by constraint family:
- last-sentence equality: edit/remove the last sentence of one paragraph
- sentence-count constraints: delete/merge sentences
- must-include (`in`): delete a required token
- must-not-include (`not in`): insert a forbidden token
- position constraints: swap the word at the required position
- exact counts: add/remove one token/character

This yields negatives close to the boundary, useful for discriminative modeling.

---

## Practical notes / tooling
The dill file depends on the COLLIE Python classes (and imports like nltk/rich). In this workspace we avoided pip by vendoring dill + small stubs; long-term V2G code should either:

- install dependencies normally in a proper Python env, or
- vendor the minimal code needed to unpickle + validate

(See `Projects/v2g/datasets/collie.md` for the detailed inspection notes + the exact stub approach used here.)
