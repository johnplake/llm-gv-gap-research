#!/usr/bin/env python3
"""
prepare_batch.py - Prepares the next batch of QA pairs for verification.

Reads:
  - outputs/plausibleqa-remaining.csv (source of pairs to verify)
  - outputs/qa_offset.txt (current position, created if missing)

Writes:
  - /tmp/qa_batch.json (batch for agent to verify)

Usage:
  python scripts/prepare_batch.py [--batch-size N]

Output format (/tmp/qa_batch.json):
{
  "batch_number": 1,
  "offset": 0,
  "count": 20,
  "items": [
    {"id": "trivia_422", "question": "What is the common name for the femur?", "answer": "Bowie"},
    ...
  ]
}
"""

import csv
import json
import argparse
from pathlib import Path

# Paths (relative to v2g project root)
PROJECT_ROOT = Path(__file__).parent.parent
REMAINING_CSV = PROJECT_ROOT / "outputs" / "plausibleqa-remaining.csv"
OFFSET_FILE = PROJECT_ROOT / "outputs" / "qa_offset.txt"
BATCH_OUTPUT = Path("/tmp/qa_batch.json")

DEFAULT_BATCH_SIZE = 20


def get_offset():
    """Read current offset, or 0 if file doesn't exist."""
    if OFFSET_FILE.exists():
        return int(OFFSET_FILE.read_text().strip())
    return 0


def read_batch(offset: int, batch_size: int):
    """Read batch_size rows from remaining.csv starting at offset."""
    items = []
    with open(REMAINING_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i < offset:
                continue
            if len(items) >= batch_size:
                break
            items.append({
                "id": row["id"],
                "question": row["question"],
                "answer": row["answer"]
            })
    return items


def main():
    parser = argparse.ArgumentParser(description="Prepare next batch of QA pairs")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE,
                        help=f"Number of pairs per batch (default: {DEFAULT_BATCH_SIZE})")
    args = parser.parse_args()

    # Get current offset
    offset = get_offset()
    
    # Read batch
    items = read_batch(offset, args.batch_size)
    
    if not items:
        # No more items to process
        output = {
            "batch_number": offset // args.batch_size + 1,
            "offset": offset,
            "count": 0,
            "items": [],
            "status": "COMPLETE",
            "message": "All pairs have been processed!"
        }
    else:
        output = {
            "batch_number": offset // args.batch_size + 1,
            "offset": offset,
            "count": len(items),
            "items": items,
            "status": "OK"
        }
    
    # Write output
    BATCH_OUTPUT.write_text(json.dumps(output, indent=2))
    
    # Print summary for agent
    print(f"=== BATCH PREPARED ===")
    print(f"Batch number: {output['batch_number']}")
    print(f"Offset: {offset}")
    print(f"Items in batch: {len(items)}")
    print(f"Output: {BATCH_OUTPUT}")
    if not items:
        print(f"STATUS: COMPLETE - No more pairs to verify!")
    else:
        print(f"STATUS: OK - Ready for verification")


if __name__ == "__main__":
    main()
