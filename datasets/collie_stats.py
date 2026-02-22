"""Compute basic COLLIE dataset stats from collie_repo/data/all_data.dill.

This script is intentionally self-contained for environments without pip.
It relies on the local clone at:
  Projects/v2g/datasets/collie_repo/
which vendors dill and provides stubs for nltk/rich.

Usage:
  python3 Projects/v2g/datasets/collie_stats.py
"""

from __future__ import annotations

import re
import collections
from pathlib import Path


def main():
    repo = Path(__file__).resolve().parent / "collie_repo"

    import sys

    sys.path.insert(0, str(repo / "fake_deps"))
    sys.path.insert(0, str(repo / "third_party" / "dill-0.3.8"))
    sys.path.insert(0, str(repo))

    import dill  # type: ignore
    from collie.constraints import Constraint  # type: ignore

    obj = dill.load(open(repo / "data" / "all_data.dill", "rb"))

    instances = []
    for k, lst in obj.items():
        for inst in lst:
            inst["_collie_split"] = k
            instances.append(inst)

    print(f"total_instances {len(instances)}")

    # Source + constraint_id counts
    cid_counts = collections.Counter()
    source_counts = collections.Counter()
    for inst in instances:
        sp = inst["_collie_split"]
        m = re.match(r"(.*)_(c\d+[a-z]?)$", sp)
        if m:
            source, cid = m.group(1), m.group(2)
        else:
            source, cid = sp, sp
        cid_counts[cid] += 1
        source_counts[source] += 1

    print("sources", dict(source_counts))
    print("constraint_ids", len(cid_counts), dict(sorted(cid_counts.items())))

    # Atomic constraints per instance
    def count_atomic(constr):
        if isinstance(constr, Constraint):
            return 1
        if hasattr(constr, "callables"):
            return sum(count_atomic(c) for c in constr.callables)
        if hasattr(constr, "callable_1") and hasattr(constr, "callable_2"):
            return count_atomic(constr.callable_1) + count_atomic(constr.callable_2)
        return 1

    atomic_counts = [count_atomic(inst["constraint"]) for inst in instances]
    mean_atomic = sum(atomic_counts) / len(atomic_counts)
    print(
        "atomic_constraints_per_instance",
        {
            "mean": mean_atomic,
            "min": min(atomic_counts),
            "max": max(atomic_counts),
        },
    )


if __name__ == "__main__":
    main()
