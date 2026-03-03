#!/usr/bin/env python3
"""Verify (question, answer) pairs against online sources in a crash-safe way.

Design goals:
- Simple + robust
- Processes EVERY row
- Writes results incrementally to a CSV (append per answer)
- Restartable / idempotent (skip already processed (id, answer))

Online lookup:
- Uses Wikipedia's public APIs to retrieve a *citation* (page + summary text).

Decision:
- Uses an LLM (Anthropic) to judge whether the provided answer is supported by
  the retrieved evidence.

Input format (CSV): columns: id, question, Num answers, Answers
- Answers are separated by ';'

Output CSV columns:
- key, id, question, answer, verdict, confidence, evidence_url, evidence_text, llm_output

Verdict meanings:
- supported: evidence supports that the answer is correct
- unsupported: evidence contradicts the answer
- unknown: evidence is insufficient/ambiguous

NOTE: This is still not a perfect fact checker (web sources can be wrong; some
questions won't be covered by Wikipedia). But it is transparent and conservative
and records citations + the LLM's structured decision.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

import requests

# Optional: Anthropic LLM for verification (recommended)
try:
    from anthropic import Anthropic
except Exception:  # pragma: no cover
    Anthropic = None

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_REST_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"


def norm_text(s: str) -> str:
    s = s.strip().lower()
    # normalize punctuation/whitespace
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[\"“”‘’]", "'", s)
    return s


def answer_variants(ans: str) -> list[str]:
    """Generate a few cheap variants for matching."""
    a = ans.strip()
    vs = {a, a.lower(), a.strip("\"'")}
    # remove parenthetical qualifiers
    vs.add(re.sub(r"\s*\([^)]*\)\s*", "", a).strip())
    # collapse whitespace
    vs = {re.sub(r"\s+", " ", v).strip() for v in vs if v.strip()}
    # very small normalization of trailing punctuation
    vs = {v.rstrip(".?!,;:") for v in vs}
    # drop empty
    return [v for v in sorted(vs, key=len, reverse=True) if v]


@dataclass
class Evidence:
    url: str
    text: str


def wiki_search(query: str, session: requests.Session, timeout: float = 20.0) -> Optional[str]:
    """Return the best-matching Wikipedia page title, or None."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
        "format": "json",
    }
    r = session.get(WIKI_API, params=params, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    hits = data.get("query", {}).get("search", [])
    if not hits:
        return None
    return hits[0].get("title")


def wiki_summary(title: str, session: requests.Session, timeout: float = 20.0) -> Optional[Evidence]:
    """Fetch REST summary text for a title."""
    # REST endpoint needs URL-encoded title
    from urllib.parse import quote

    url = WIKI_REST_SUMMARY.format(quote(title.replace(" ", "_"), safe=""))
    r = session.get(url, timeout=timeout, headers={"Accept": "application/json"})
    if r.status_code == 404:
        return None
    r.raise_for_status()
    j = r.json()
    extract = j.get("extract") or ""
    page_url = (j.get("content_urls", {})
                .get("desktop", {})
                .get("page")) or f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
    if not extract:
        return Evidence(url=page_url, text="")
    return Evidence(url=page_url, text=extract)


def llm_verify(question: str, answer: str, ev: Evidence, client: Anthropic, model: str) -> Tuple[str, float, str]:
    """LLM-based verifier.

    Returns (verdict, confidence, llm_output_json_text).
    """

    prompt = f"""
You are verifying whether a proposed answer is correct for a question.
You MUST base your decision ONLY on the provided evidence text and URL.
If the evidence is insufficient or ambiguous, say UNKNOWN.

Return JSON with keys: verdict, confidence, short_reason, quote.
- verdict must be one of: SUPPORTED, UNSUPPORTED, UNKNOWN
- confidence must be a number from 0 to 1
- quote should be a short direct quote from the evidence that supports the verdict (or empty if none)

QUESTION: {question}
PROPOSED_ANSWER: {answer}
EVIDENCE_URL: {ev.url}
EVIDENCE_TEXT:
{ev.text}
""".strip()

    msg = client.messages.create(
        model=model,
        max_tokens=250,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    # Anthropic SDK returns content blocks
    out = "".join(getattr(b, "text", "") for b in msg.content)
    out_s = out.strip()

    verdict = "unknown"
    confidence = 0.0
    try:
        import json

        j = json.loads(out_s)
        v = (j.get("verdict") or "").strip().upper()
        if v in {"SUPPORTED", "UNSUPPORTED", "UNKNOWN"}:
            verdict = v.lower()
        c = j.get("confidence")
        if isinstance(c, (int, float)):
            confidence = float(c)
    except Exception:
        # If parsing fails, record raw output; keep unknown
        verdict = "unknown"
        confidence = 0.0

    return verdict, confidence, out_s


def iter_input_rows(path: str) -> Iterable[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def parse_answers_field(s: str) -> list[str]:
    # split on ';' with trimming
    parts = [p.strip() for p in (s or "").split(";")]
    return [p for p in parts if p]


def load_done_keys(out_csv: str) -> set[str]:
    """Keys are sha1(id + '\t' + answer)."""
    done = set()
    if not os.path.exists(out_csv):
        return done
    with open(out_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            k = (row.get("key") or "").strip()
            if k:
                done.add(k)
    return done


def key_for(qid: str, answer: str) -> str:
    h = hashlib.sha1()
    h.update((qid + "\t" + answer).encode("utf-8"))
    return h.hexdigest()


def ensure_out_header(out_csv: str):
    if os.path.exists(out_csv) and os.path.getsize(out_csv) > 0:
        return
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "key",
            "id",
            "question",
            "answer",
            "verdict",
            "confidence",
            "evidence_url",
            "evidence_text",
            "llm_output",
        ])


def append_result(out_csv: str, *, key: str, qid: str, question: str, answer: str,
                  verdict: str, confidence: float, evidence: Optional[Evidence], llm_output: str = ""):
    with open(out_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            key,
            qid,
            question,
            answer,
            verdict,
            f"{confidence:.3f}",
            (evidence.url if evidence else ""),
            (evidence.text if evidence else ""),
            llm_output,
        ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input CSV path")
    ap.add_argument("--output", default="outputs/results.csv", help="Output CSV path")
    ap.add_argument("--sleep", type=float, default=0.2, help="Sleep between network calls (seconds)")
    ap.add_argument("--max-summary-chars", type=int, default=600, help="Truncate evidence text")
    ap.add_argument("--model", default="claude-3-5-sonnet-latest", help="Anthropic model name")
    ap.add_argument("--no-llm", action="store_true", help="Disable LLM verification (NOT recommended)")
    args = ap.parse_args()

    ensure_out_header(args.output)
    done = load_done_keys(args.output)

    session = requests.Session()
    session.headers.update({"User-Agent": "openclaw-v2g-verifier/0.2 (contact: local)"})

    llm_client = None
    if not args.no_llm:
        if Anthropic is None:
            raise RuntimeError("anthropic python package not installed; install it or pass --no-llm")
        llm_client = Anthropic()  # reads ANTHROPIC_API_KEY from env

    n_q = 0
    n_ans = 0
    n_skipped = 0

    for row in iter_input_rows(args.input):
        n_q += 1
        qid = (row.get("id") or "").strip()
        question = (row.get("question") or "").strip()
        answers = parse_answers_field(row.get("Answers") or "")

        # If answers field is empty, still record a row so we can assert we processed the question.
        if not answers:
            k = key_for(qid, "")
            if k in done:
                n_skipped += 1
            else:
                append_result(args.output, key=k, qid=qid, question=question, answer="",
                              verdict="unknown", confidence=0.0, evidence=None, llm_output="")
                done.add(k)
            continue

        for ans in answers:
            n_ans += 1
            k = key_for(qid, ans)
            if k in done:
                n_skipped += 1
                continue

            # Query strategy: use both question and answer terms.
            query = f"{question} {ans}".strip()

            evidence = None
            verdict = "unknown"
            conf = 0.0
            llm_out = ""

            try:
                title = wiki_search(query, session)
                time.sleep(args.sleep)
                if title:
                    evidence = wiki_summary(title, session)
                    time.sleep(args.sleep)

                if evidence and evidence.text and len(evidence.text) > args.max_summary_chars:
                    evidence = Evidence(url=evidence.url, text=evidence.text[: args.max_summary_chars] + "…")

                if llm_client is not None and evidence and evidence.text:
                    verdict, conf, llm_out = llm_verify(question, ans, evidence, llm_client, args.model)

            except Exception as e:
                # Record the failure as unknown, but do not stop the run.
                verdict = "unknown"
                conf = 0.0
                evidence = Evidence(url="", text=f"ERROR: {type(e).__name__}: {e}")
                llm_out = ""

            append_result(args.output, key=k, qid=qid, question=question, answer=ans,
                          verdict=verdict, confidence=conf, evidence=evidence, llm_output=llm_out)
            done.add(k)

        if n_q % 100 == 0:
            print(f"processed_questions={n_q} processed_answers={n_ans} skipped={n_skipped} out={args.output}", file=sys.stderr)

    print(f"DONE: questions={n_q} answers={n_ans} skipped={n_skipped} out={args.output}")


if __name__ == "__main__":
    main()
