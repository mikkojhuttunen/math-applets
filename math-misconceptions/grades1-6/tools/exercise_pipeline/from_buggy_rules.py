"""Turn items from tools/buggy_rules into the exercise schema and write a batch file.

Usage (from the repository root):
    python tools/exercise_pipeline/from_buggy_rules.py --n 12 --seed 20260930 \
        --out exercises/grades1-6/batch-20260930-0600.json

Templates covered: 3-digit subtraction (NUM-10), fraction addition (NUM-03),
unit-fraction comparison (NUM-12). All answers and wrong answers are computed by code.
Every item is written with status "draft". Only a human reviewer sets "reviewed".
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "buggy_rules"))
import buggy_rules as br  # noqa: E402


def to_schema(item: dict, goal: str, level: str, item_id: str) -> dict:
    p = item["params"]
    out = {
        "id": item_id,
        "goal": goal,
        "level": level,
        "type": item["type"],
        "stem_fi": item["stem_fi"],
        "answer": item["answer"],
        "workbook": item["workbook"],
        "source": "template",
        "status": "draft",
    }
    if item["template"] == "sub_multidigit_v1":
        out["answer_expr"] = f"{p['minuend']} - {p['subtrahend']}"
    elif item["template"] == "frac_add_v1":
        out["answer_expr"] = f"{p['a']}/{p['b']} + {p['c']}/{p['d']}"
    elif item["template"] == "frac_compare_unit_v1":
        out["options"] = item["options"]
    else:
        raise ValueError(f"unknown template {item['template']}")
    out["misconceptions"] = {t: {"answer": m["answer"]} for t, m in item["misconceptions"].items()}
    return out


def existing_stems(pattern: str) -> set[str]:
    stems = set()
    for path in glob.glob(pattern):
        with open(path, encoding="utf-8") as f:
            for it in json.load(f):
                stems.add(" ".join(str(it.get("stem_fi", "")).split()).lower())
    return stems


def make_batch(n: int, seed: int, stamp: str, avoid: set[str] | None = None) -> list[dict]:
    rng = random.Random(seed)
    makers = [
        ("sub", lambda: br.make_subtraction_item(rng, 3, 3), "A36.S2.04", "T"),
        ("fadd", lambda: br.make_fraction_add_item(rng), "A36.S2.12", "T"),
        ("fcmp", lambda: br.make_fraction_compare_item(rng), "A36.S2.11", "P"),
    ]
    batch, seen = [], set(avoid or ())
    i = 0
    while len(batch) < n and i < n * 50:
        name, make, goal, level = makers[i % len(makers)]
        i += 1
        item = make()
        key = " ".join(item["stem_fi"].split()).lower()
        if key in seen:
            continue
        seen.add(key)
        batch.append(to_schema(item, goal, level, f"{goal}-{name}-{stamp}-{len(batch) + 1:03d}"))
    return batch


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--stamp", default=None, help="short label used in item ids, default = seed")
    ap.add_argument("--avoid-glob", default="exercises/grades1-6/*.json",
                    help="stems already used in these files are skipped (default: all batches)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    batch = make_batch(a.n, a.seed, a.stamp or str(a.seed), existing_stems(a.avoid_glob))
    if len(batch) < a.n:
        print(f"warning: only {len(batch)} of {a.n} new items possible without repeating a stem")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {len(batch)} items to {a.out}")
