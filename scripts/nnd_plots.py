#!/usr/bin/env python3
"""NND dataset plotting + filtering counts.

Usage:
  ~/.openclaw/workspace/.uv/venvs/v2g-plot/bin/python Projects/v2g/scripts/nnd_plots.py \
    --nnd-data Projects/v2g/datasets/candidates/nnd_data \
    --out Projects/v2g/figures/nnd

This script:
- loads each available NND sub-dataset we have locally
- computes per-prompt counts of pos/neg candidates
- produces distribution plots (histograms + heatmaps)
- reports how many prompts remain after filtering for pos>=N1 and neg>=N2 for a grid of values

POS/NEG definitions:
- MT MQM: POS iff category==No-error and severity==No-error for that system on that segment.
- QA Challenge300: POS iff credit==1.0 (NEG credit==0.0)
- QGen QuizDesign: POS iff reason=="No error"
- Summ GPT3 (cnn/bbc): POS iff max score among {gpt3,t0,brio}, where score = (#best) - (#worst)

"""

import argparse
import os
import json
import csv
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def quantiles(x):
    if len(x) == 0:
        return dict(min=None, p50=None, p90=None, max=None)
    x = np.asarray(x)
    return dict(
        min=int(np.min(x)),
        p50=float(np.median(x)),
        p90=float(np.quantile(x, 0.9, method="nearest")),
        max=int(np.max(x)),
    )


def load_mqm(mqm_path: str) -> pd.DataFrame:
    # aggregate to segment+system level
    seg_sys = {}
    with open(mqm_path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            seg = (row["doc_id"], row["seg_id"], row["source"])
            sys = row["system"]
            key = (seg, sys)
            d = seg_sys.get(key)
            if d is None:
                d = {
                    "doc_id": row["doc_id"],
                    "seg_id": row["seg_id"],
                    "source": row["source"],
                    "system": sys,
                    "target": row["target"],
                    "cats": set(),
                    "sevs": set(),
                }
                seg_sys[key] = d
            d["cats"].add(row["category"])
            d["sevs"].add(row["severity"])

    rows = []
    for d in seg_sys.values():
        cats = d["cats"]
        sevs = d["sevs"]
        pos = (cats == {"No-error"} and sevs == {"No-error"})
        rows.append(
            {
                "dataset": "mt_mqm",
                "prompt_id": f"{d['doc_id']}:{d['seg_id']}:{abs(hash(d['source']))%10**12}",
                "prompt": d["source"],
                "candidate": d["target"],
                "system": d["system"],
                "pos": int(pos),
            }
        )
    return pd.DataFrame(rows)


def load_challenge300(c300_path: str) -> pd.DataFrame:
    model_names = [
        "Macaw-11B",
        "Macaw-answer-11B",
        "GPT3-davinci",
        "Jurassic-1-jumbo",
        "T5-XXL-SSM-NQ",
    ]
    rows = []
    with open(c300_path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            qid = row["id"]
            q = row["question"]
            for mn in model_names:
                credit_raw = row.get("credit-" + mn, "")
                if credit_raw == "":
                    continue
                credit = float(credit_raw)
                if credit not in (0.0, 1.0):
                    continue
                rows.append(
                    {
                        "dataset": "qa_challenge300",
                        "prompt_id": qid,
                        "prompt": q,
                        "candidate": row[mn],
                        "system": mn,
                        "pos": int(credit == 1.0),
                    }
                )
    return pd.DataFrame(rows)


def load_quizdesign(qd_path: str) -> pd.DataFrame:
    rows = []
    with open(qd_path, encoding="utf-8") as f:
        for line in f:
            g = json.loads(line)
            prompt_id = str(g["group_id"])
            prompt = f"ANSWER_SPAN: {g['answer_span']}\nCONTEXT: {g['context']}"
            for q in g["questions"]:
                rows.append(
                    {
                        "dataset": "qgen_quizdesign",
                        "prompt_id": prompt_id,
                        "prompt": prompt,
                        "candidate": q["question"],
                        "system": q.get("model_name", "unknown"),
                        "pos": int(q.get("reason") == "No error"),
                    }
                )
    return pd.DataFrame(rows)


def load_gpt3_summ(json_path: str, name: str) -> pd.DataFrame:
    data = json.load(open(json_path))
    rows = []
    for doc_id, doc in data.items():
        if "annotators" not in doc:
            continue
        scores = {k: 0 for k in ["gpt3", "t0", "brio"]}
        for anno in doc["annotators"]:
            scores[anno["best_summary"][0]] += 1
            scores[anno["worst_summary"][0]] -= 1
        mx = max(scores.values())
        for sys in ["gpt3", "t0", "brio"]:
            rows.append(
                {
                    "dataset": f"summ_gpt3_{name}",
                    "prompt_id": str(doc_id),
                    "prompt": doc["article"],
                    "candidate": doc[sys]["text"],
                    "system": sys,
                    "pos": int(scores[sys] == mx),
                }
            )
    return pd.DataFrame(rows)


def per_prompt_counts(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["dataset", "prompt_id"], as_index=False)["pos"].agg(["count", "sum"])
    g = g.reset_index()
    g.rename(columns={"count": "n_total", "sum": "n_pos"}, inplace=True)
    g["n_neg"] = g["n_total"] - g["n_pos"]
    return g


def plot_distributions(counts: pd.DataFrame, out_dir: str):
    ensure_dir(out_dir)

    for dataset, sub in counts.groupby("dataset"):
        sub = sub.copy()
        # histogram of total candidates
        plt.figure(figsize=(7, 4))
        sns.histplot(sub["n_total"], bins=30)
        plt.title(f"{dataset}: candidates per prompt")
        plt.xlabel("# candidates")
        plt.ylabel("# prompts")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{dataset}__hist_n_total.png"), dpi=200)
        plt.close()

        # histogram of pos/neg
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        sns.histplot(sub["n_pos"], bins=30, ax=ax[0])
        ax[0].set_title(f"{dataset}: #POS per prompt")
        sns.histplot(sub["n_neg"], bins=30, ax=ax[1])
        ax[1].set_title(f"{dataset}: #NEG per prompt")
        for a in ax:
            a.set_xlabel("count")
            a.set_ylabel("# prompts")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{dataset}__hist_pos_neg.png"), dpi=200)
        plt.close()

        # heatmap: n_pos x n_neg counts
        pivot = (
            sub.groupby(["n_pos", "n_neg"]).size().reset_index(name="n_prompts")
        )
        # cap to reasonable grid for readability
        max_pos = int(pivot["n_pos"].max())
        max_neg = int(pivot["n_neg"].max())
        grid = np.zeros((max_pos + 1, max_neg + 1), dtype=int)
        for _, r in pivot.iterrows():
            grid[int(r["n_pos"]), int(r["n_neg"])] = int(r["n_prompts"])
        plt.figure(figsize=(10, 6))
        sns.heatmap(grid, cmap="viridis")
        plt.title(f"{dataset}: #prompts by (n_pos, n_neg)")
        plt.xlabel("n_neg")
        plt.ylabel("n_pos")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{dataset}__heatmap_pos_vs_neg.png"), dpi=200)
        plt.close()


def filter_grid(counts: pd.DataFrame, n1_values, n2_values) -> pd.DataFrame:
    rows = []
    for dataset, sub in counts.groupby("dataset"):
        for n1 in n1_values:
            for n2 in n2_values:
                kept = ((sub["n_pos"] >= n1) & (sub["n_neg"] >= n2)).sum()
                rows.append(
                    {
                        "dataset": dataset,
                        "N1_min_pos": int(n1),
                        "N2_min_neg": int(n2),
                        "num_prompts_kept": int(kept),
                        "num_prompts_total": int(len(sub)),
                        "frac_kept": float(kept / len(sub)) if len(sub) else 0.0,
                    }
                )
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nnd-data", required=True, help="Path to nnd_data folder")
    ap.add_argument("--out", required=True, help="Output directory for plots")
    ap.add_argument("--write-csv", default=None, help="Optional CSV path for filter grid")
    args = ap.parse_args()

    nnd = args.nnd_data
    dfs = []

    mqm_path = os.path.join(nnd, "mqm_newstest2021_ende.tsv")
    if os.path.exists(mqm_path):
        dfs.append(load_mqm(mqm_path))

    c300 = os.path.join(nnd, "challenge300-outputs.tsv")
    if os.path.exists(c300):
        dfs.append(load_challenge300(c300))

    qd = os.path.join(nnd, "quiz_design_groups.jsonl")
    if os.path.exists(qd):
        dfs.append(load_quizdesign(qd))

    ha = os.path.join(nnd, "human_annotations_unzipped", "human_annotations")
    for name in ["cnn", "bbc"]:
        fp = os.path.join(ha, f"{name}_human.json")
        if os.path.exists(fp):
            dfs.append(load_gpt3_summ(fp, name))

    if not dfs:
        raise SystemExit("No datasets found under --nnd-data")

    df = pd.concat(dfs, ignore_index=True)
    counts = per_prompt_counts(df)

    # print summary stats
    print("Datasets loaded:", sorted(df["dataset"].unique()))
    for dataset, sub in counts.groupby("dataset"):
        pos_share = sub["n_pos"].sum() / sub["n_total"].sum()
        print(
            dataset,
            {
                "num_prompts": len(sub),
                "pos_share": float(pos_share),
                "n_total": quantiles(sub["n_total"].tolist()),
                "n_pos": quantiles(sub["n_pos"].tolist()),
                "n_neg": quantiles(sub["n_neg"].tolist()),
            },
        )

    plot_distributions(counts, args.out)

    # filter grid
    n1_values = [0, 1, 2, 3, 5, 10]
    n2_values = [0, 1, 2, 3, 5, 10]
    grid = filter_grid(counts, n1_values, n2_values)
    if args.write_csv:
        ensure_dir(os.path.dirname(args.write_csv))
        grid.to_csv(args.write_csv, index=False)
    else:
        # print a small slice
        print(grid.sort_values(["dataset", "N1_min_pos", "N2_min_neg"]).head(50))


if __name__ == "__main__":
    main()
