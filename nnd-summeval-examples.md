# SummEval: prompt → multiple candidates (POS vs NEG examples)

This file provides a few concrete **SummEval** examples in the style of the MT MQM examples: for each prompt (doc id), show a few candidate summaries labeled POS/NEG.

## Dataset file
- `datasets/candidates/nnd_data/summeval/model_annotations.aligned.jsonl`
- 100 prompts × 16 candidates each

## POS vs NEG rule (current in this repo)
This repo now uses a **non-arbitrary rule that mirrors the NND helper logic** (and avoids a hand-chosen cutoff):

For a given dimension (we focus on **consistency** here):
1. Use **only the 3 expert annotations** (`expert_annotations`).
2. Count how many experts give the max score **5** for that dimension.
3. **POS** iff a strict majority of experts give a 5.
   - With 3 experts, this means: **POS iff (# of 5s) ≥ 2**.
4. **NEG** otherwise.

This gives a binary label per (prompt, candidate) consistent with the intended “near-negative distinction” style: treat top-rated (by experts) as positives.

We keep this file’s examples in the **consistency** dimension.

---

## Example 1 (balanced: 8 POS / 8 NEG)
**id:** `dm-test-f26d8400ae49b90d109c165d0f44b8f6ca253c08`

**Reference (one):**
Naoki Ogane says that Chelsea have made an offer for Yoshinori Muto. The 22-year-old forward has one goal in 11 games for Japan. Muto admits that it is an 'honour' to receive an offer from the Blues. Chelsea have signed a £200m sponsorship deal with Yokohama Rubber. Muto graduated from university with an economics degree two weeks ago. He would become the first Japanese player to sign for Chelsea.

**POS (high mean consistency):**
- POS `M5`: “chelsea have made an offer for fc tokyo 's 22 - year - old forward yoshinori muto …”
- POS `M12`: “chelsea have made an offer for fc tokyo 's 22-year-old forward yoshinori muto …”
- POS `M15`: “chelsea have made an offer for fc tokyo 's 22-year-old forward yoshinori muto …”

**NEG:**
- NEG `M11`: “chelsea have made an offer for fc tokyo 's dutch partner yoshinori muto …”
- NEG `M10`: “chelsea have made an offer … not connected to the 200million deal …”
- NEG `M13`: “chelsea have made an offer …”

---

## Example 2 (POS-heavy: 13 POS / 3 NEG)
**id:** `cnn-test-b1c3fc03a2b74cf4c79844c1fe2fdce70a8a436e`

**Reference (one):**
The Italian coast guard says 8,480 migrants were rescued from Friday to Monday. Save the Children said Tuesday 400 migrants could be missing from a boat. The Italian coast guard cannot confirm that report.

**POS:**
- POS `M2` mean_cons=5.00: “from friday to monday , a total of 8,480 migrants were rescued … save the children …”
- POS `M0` mean_cons=5.00: “italy is coping with a rising wave … 8,480 migrants were rescued …”
- POS `M12` mean_cons=4.62: “italy is coping … a total of 8,480 migrants were rescued …”

**NEG:**
- NEG `M11` mean_cons=2.25: claims “400 migrants have died …” (not supported by reference)
- NEG `M20` mean_cons=2.75: adds extra stats/claims (likely hallucinated)
- NEG `M13` mean_cons=3.00: weaker / incomplete

---

## Example 3 (NEG-heavy: 4 POS / 12 NEG)
**id:** `dm-test-18243373494a1722ddcd162ec67b63dd749633ab`

**Reference (one):**
Roma win at home for the first time since November. Miralem Pjanic completes a counter-attack to put hosts ahead. Morgan de Sanctis produces stunning goalkeeping display. Napoli without a win for five matches after terrible run.

**POS:**
- POS `M23` mean_cons=4.50: “roma ended their four-month winless streak at home with a win over napoli …”
- POS `M14` mean_cons=4.25: similar, clean
- POS `M5` mean_cons=4.25: similar, clean

**NEG:**
- NEG `M11` mean_cons=2.50: repetitive/garbled + wrong extra claims
- NEG `M20` mean_cons=3.00: says “Roma beat Napoli 4-2” (contradicts reference)
- NEG `M8` mean_cons=3.12: also claims “4-2”
