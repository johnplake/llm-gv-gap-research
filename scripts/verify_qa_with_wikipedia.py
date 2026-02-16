#!/usr/bin/env python3
"""Verify (question, answer) pairs against online sources in a crash-safe way.

Design goals:
- Simple + robust
- Processes EVERY row
- Writes results incrementally to a CSV (append per answer)
- Restartable / idempotent (skip already processed (id, answer))

Current implementation uses Wikipedia's public APIs as the primary online lookup
(source selection is deterministic and rate-limited).

Input format (CSV): columns: id, question, Num answers, Answers
- Answers are separated by ';'

Output CSV columns:
- id, question, answer, verdict, confidence, evidence_url, evidence_text

Verdict meanings:
- supported: evidence strongly suggests the answer is correct
- unsupported: evidence suggests the answer is wrong / different
- unknown: could not resolve confidently (needs manual review or richer search)

NOTE: This is not a perfect fact checker; it is meant to be a conservative,
transparent verifier that records citations.
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


def simple_verify(question: str, answer: str, ev: Evidence) -> Tuple[str, float]:
    """Heuristic verifier.

    We intentionally keep this conservative:
    - supported if answer (or close variant) appears in summary text
    - unsupported if summary contains a conflicting phrase like "is ..." with different entity?
      (we do NOT do deep NLI here)
    - otherwise unknown
    """
    ans_vars = answer_variants(answer)
    hay = norm_text(ev.text)

    for v in ans_vars:
        if norm_text(v) and norm_text(v) in hay:
            # confidence boosted for longer matches
            conf = 0.65 + min(0.25, len(v) / 100.0)
            return "supported", float(conf)

    # If we couldn't even find the answer string in the summary, we usually can't confidently
    # call it wrong; mark unknown.
    return "unknown", 0.3


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
        ])


def append_result(out_csv: str, *, key: str, qid: str, question: str, answer: str,
                  verdict: str, confidence: float, evidence: Optional[Evidence]):
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
        ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input CSV path")
    ap.add_argument("--output", default="outputs/results.csv", help="Output CSV path")
    ap.add_argument("--sleep", type=float, default=0.2, help="Sleep between network calls (seconds)")
    ap.add_argument("--max-summary-chars", type=int, default=600, help="Truncate evidence text")
    args = ap.parse_args()

    ensure_out_header(args.output)
    done = load_done_keys(args.output)

    session = requests.Session()
    session.headers.update({"User-Agent": "openclaw-v2g-verifier/0.1 (contact: local)"})

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
                              verdict="unknown", confidence=0.0, evidence=None)
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

            try:
                title = wiki_search(query, session)
                time.sleep(args.sleep)
                if title:
                    evidence = wiki_summary(title, session)
                    time.sleep(args.sleep)
                    if evidence and evidence.text:
                        verdict, conf = simple_verify(question, ans, evidence)
            except Exception as e:
                # Record the failure as unknown, but do not stop the run.
                verdict = "unknown"
                conf = 0.0
                evidence = Evidence(url="", text=f"ERROR: {type(e).__name__}: {e}")

            if evidence and evidence.text and len(evidence.text) > args.max_summary_chars:
                evidence = Evidence(url=evidence.url, text=evidence.text[: args.max_summary_chars] + "…")

            append_result(args.output, key=k, qid=qid, question=question, answer=ans,
                          verdict=verdict, confidence=conf, evidence=evidence)
            done.add(k)

        if n_q % 100 == 0:
            print(f"processed_questions={n_q} processed_answers={n_ans} skipped={n_skipped} out={args.output}", file=sys.stderr)

    print(f"DONE: questions={n_q} answers={n_ans} skipped={n_skipped} out={args.output}")


if __name__ == "__main__":
    main()
