# QA Verification Instructions

## Overview

You are verifying question-answer pairs. For each pair, you will:
1. Search the web to check if the answer is correct
2. Make a judgment: `supported`, `unsupported`, or `unknown`
3. Record your confidence and evidence

## Workflow

### Step 1: Prepare Batch
Run this command:
```bash
cd /home/node/.openclaw/workspace/Projects/v2g && python scripts/prepare_batch.py
```

This creates `/tmp/qa_batch.json` with items to verify.

**If output says "STATUS: COMPLETE"** → All done! Send Telegram message "QA COMPLETE" and stop.

### Step 2: Read the Batch
Read `/tmp/qa_batch.json`. It looks like:
```json
{
  "batch_number": 1,
  "offset": 0,
  "count": 20,
  "items": [
    {"id": "trivia_422", "question": "What is the common name for the femur?", "answer": "Bowie"},
    {"id": "webq_1596", "question": "What was the name of the last batman movie?", "answer": "The Batman Part II"}
  ]
}
```

### Step 3: Verify Each Item
For EACH item in the batch:

1. **Search**: Use `web_search` with a query like:
   - `"What is the common name for the femur?"`
   - Or: `"femur common name thighbone"`

2. **Judge**: Based on search results, decide:
   - `supported` = Answer is correct according to sources
   - `unsupported` = Answer is incorrect according to sources
   - `unknown` = Can't determine from search results

3. **Record**:
   - `verdict`: supported / unsupported / unknown
   - `confidence`: 0.0 to 1.0 (how sure are you?)
   - `url`: Best source URL
   - `snippet`: Brief quote supporting your verdict

### Step 4: Write Results
Write your results to `/tmp/qa_results.json` in this EXACT format:
```json
{
  "results": [
    {
      "id": "trivia_422",
      "question": "What is the common name for the femur?",
      "answer": "Bowie",
      "verdict": "unsupported",
      "confidence": 0.95,
      "url": "https://en.wikipedia.org/wiki/Femur",
      "snippet": "The femur is commonly known as the thighbone"
    },
    {
      "id": "webq_1596",
      "question": "What was the name of the last batman movie?",
      "answer": "The Batman Part II",
      "verdict": "supported",
      "confidence": 0.85,
      "url": "https://en.wikipedia.org/wiki/The_Batman_Part_II",
      "snippet": "The Batman Part II is an upcoming superhero film"
    }
  ]
}
```

**IMPORTANT**: Include ALL items from the batch. Match the `id` and `answer` exactly.

### Step 5: Save Results
Run this command:
```bash
cd /home/node/.openclaw/workspace/Projects/v2g && python scripts/save_results.py
```

This appends your results to `outputs/plausibleqa-verified2.csv` and updates the offset.

### Step 6: Report Progress
Send a Telegram message to chat `-1003700767295` (threadId `1`) with:
```
QA Batch X complete: Y verified. Remaining: Z
```

## Summary Checklist

1. [ ] Run `prepare_batch.py` → check if COMPLETE
2. [ ] Read `/tmp/qa_batch.json`
3. [ ] For each item: web_search → judge → record
4. [ ] Write `/tmp/qa_results.json` (exact format!)
5. [ ] Run `save_results.py`
6. [ ] Send Telegram progress update

## DO NOT

- Do NOT parse CSV files yourself
- Do NOT write to CSV files directly
- Do NOT use `edit` tool on any files
- Do NOT skip items or change the batch

## Example Verdicts

| Question | Answer | Verdict | Why |
|----------|--------|---------|-----|
| "Capital of France?" | "Paris" | supported | Matches all sources |
| "Capital of France?" | "London" | unsupported | Sources say Paris |
| "Who directed Movie X?" | "John Smith" | unknown | Can't find reliable info |
