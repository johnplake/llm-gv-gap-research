#!/usr/bin/env python3
"""
save_results.py - Saves verified QA results and updates offset.

Reads:
  - /tmp/qa_results.json (agent's verification results)
  - /tmp/qa_batch.json (to get batch metadata)

Writes:
  - outputs/plausibleqa-verified2.csv (appends results)
  - outputs/qa_offset.txt (updates offset)

Usage:
  python scripts/save_results.py

Expected input format (/tmp/qa_results.json):
{
  "results": [
    {
      "id": "trivia_422",
      "question": "What is the common name for the femur?",
      "answer": "Bowie",
      "verdict": "unsupported",
      "confidence": 0.9,
      "url": "https://en.wikipedia.org/wiki/Femur",
      "snippet": "The femur is commonly called the thighbone"
    },
    ...
  ]
}
"""

import csv
import json
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
VERIFIED2_CSV = PROJECT_ROOT / "outputs" / "plausibleqa-verified2.csv"
OFFSET_FILE = PROJECT_ROOT / "outputs" / "qa_offset.txt"
BATCH_INPUT = Path("/tmp/qa_batch.json")
RESULTS_INPUT = Path("/tmp/qa_results.json")


def load_json(path):
    """Load JSON file."""
    return json.loads(path.read_text())


def save_offset(offset: int):
    """Save offset to file."""
    OFFSET_FILE.write_text(str(offset))


def append_results(results: list):
    """Append results to verified2.csv."""
    # Check if file exists (need to write header?)
    write_header = not VERIFIED2_CSV.exists()
    
    with open(VERIFIED2_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        if write_header:
            writer.writerow(['id', 'question', 'answer', 'verdict', 'confidence', 
                           'evidence_url', 'evidence_snippet', 'notes'])
        
        for r in results:
            writer.writerow([
                r.get('id', ''),
                r.get('question', ''),
                r.get('answer', ''),
                r.get('verdict', 'unknown'),
                r.get('confidence', 0.0),
                r.get('url', ''),
                r.get('snippet', ''),
                r.get('notes', '')
            ])


def main():
    # Load batch info
    batch = load_json(BATCH_INPUT)
    batch_count = batch.get('count', 0)
    old_offset = batch.get('offset', 0)
    
    # Load results
    results_data = load_json(RESULTS_INPUT)
    results = results_data.get('results', [])
    
    # Validate
    if len(results) != batch_count:
        print(f"WARNING: Expected {batch_count} results, got {len(results)}")
    
    # Append to CSV
    append_results(results)
    
    # Update offset
    new_offset = old_offset + batch_count
    save_offset(new_offset)
    
    # Count total verified
    if VERIFIED2_CSV.exists():
        with open(VERIFIED2_CSV) as f:
            total_lines = sum(1 for _ in f) - 1  # minus header
    else:
        total_lines = 0
    
    # Print summary
    print(f"=== RESULTS SAVED ===")
    print(f"Results saved: {len(results)}")
    print(f"Offset updated: {old_offset} → {new_offset}")
    print(f"Total in verified2.csv: {total_lines}")
    print(f"Remaining: {5569 - new_offset}")


if __name__ == "__main__":
    main()
