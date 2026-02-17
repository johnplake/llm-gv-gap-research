"""Download QASC and ASQA from Hugging Face and materialize to disk.

Why this exists:
- Our repo has a top-level `datasets/` directory, which can shadow the Hugging Face
  `datasets` python package if you run `python ...` from the repo root.
- The intended invocation uses `uv run --no-project --with datasets ...` so we get
  the correct dependencies without needing to manage a local venv here.

Example:
  cd Projects/v2g
  ~/.openclaw/workspace/bin/uv run --no-project \
    --with datasets --with pyarrow --with pandas \
    -- python3 scripts/qasc_asqa_download.py --out-dir datasets/raw
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def _import_hf_datasets():
    # Avoid importing the local `datasets/` directory as a python module.
    cwd = os.getcwd()
    if "" in os.sys.path:
        os.sys.path.remove("")
    if cwd in os.sys.path:
        os.sys.path.remove(cwd)

    from datasets import load_dataset  # type: ignore

    return load_dataset


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="datasets/raw", help="Base output directory")
    ap.add_argument(
        "--formats",
        default="save_to_disk,jsonl",
        help="Comma-separated: save_to_disk,jsonl (jsonl is per-split)",
    )
    args = ap.parse_args()

    formats = {s.strip() for s in args.formats.split(",") if s.strip()}
    out_dir = Path(args.out_dir)

    load_dataset = _import_hf_datasets()

    targets = [
        ("allenai/qasc", "qasc"),
        ("din0s/asqa", "asqa"),
    ]

    for hf_id, short_name in targets:
        print(f"==> Loading {hf_id}")
        ds_dict = load_dataset(hf_id)

        # Write a lightweight manifest.
        manifest = {
            "hf_id": hf_id,
            "splits": {k: len(v) for k, v in ds_dict.items()},
            "columns": {k: v.column_names for k, v in ds_dict.items()},
        }
        _write_json(out_dir / short_name / "manifest.json", manifest)

        for split, ds in ds_dict.items():
            split_dir = out_dir / short_name / split
            split_dir.mkdir(parents=True, exist_ok=True)

            if "save_to_disk" in formats:
                # Arrow-based, preserves full structure.
                ds.save_to_disk(str(split_dir / "hf_datasets"))

            if "jsonl" in formats:
                # Materialize a JSONL for quick grepping/inspection.
                # (Keep it simple: one object per line.)
                jsonl_path = split_dir / "data.jsonl"
                with jsonl_path.open("w", encoding="utf-8") as f:
                    for ex in ds:
                        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

        print(f"✅ Wrote {short_name} to {out_dir/short_name}")


if __name__ == "__main__":
    main()
