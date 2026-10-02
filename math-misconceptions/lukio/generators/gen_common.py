"""Shared helpers for the lukio generators (not a template itself).

Copied from ../../generators/gen_common.py (7-9) and adapted: lukio curriculum
block (lops, g, syllabus, level, tools), LU- item IDs, schema_version lukio-1.0.
Run a generator from math-misconceptions/lukio/:
  python generators/<template>.py                 print the wrapper JSON
  python generators/<template>.py --write --run N --date YYYY-MM-DD
"""
import argparse
import json
import re
from fractions import Fraction
from pathlib import Path

SCHEMA_VERSION = "lukio-1.0"
MINUS = "−"


def num(n):
    """Integer or decimal as display text: proper minus sign, decimal comma."""
    return str(n).replace("-", MINUS).replace(".", ",")


def frac(v):
    """Fraction as display text, e.g. −5/12 or 3."""
    v = Fraction(v)
    return num(v.numerator) if v.denominator == 1 else f"{num(v.numerator)}/{v.denominator}"


def mc_options(rng, correct, wrongs):
    """correct = (text, feedback); wrongs = [(text, misconception|None, feedback)].
    Returns (options, correct_id) with deterministic shuffling and ids a, b, c..."""
    pool = [(correct[0], None, correct[1], True)] + [(t, m, f, False) for t, m, f in wrongs]
    assert len({p[0].lower() for p in pool}) == len(pool), "duplicate option texts"
    rng.shuffle(pool)
    options, cid = [], None
    for i, (t, m, f, ok) in enumerate(pool):
        oid = "abcdefgh"[i]
        options.append({"id": oid, "text": t, "misconception": m, "feedback": f})
        if ok:
            cid = oid
    return options, cid


def base_item(tid, code, n, lops, g, syllabus, level, tools, prompt, payload, steps, final,
              correct_fb, template, params, date, run, misconceptions=None, generic_wrong=None):
    fb = {"correct": correct_fb}
    if generic_wrong:
        fb["generic_wrong"] = generic_wrong
    return {
        "schema_version": SCHEMA_VERSION,
        "id": f"LU-{tid}-{code}-{n:03d}",
        "type": code,
        "status": "draft",
        "lang": "fi",
        "curriculum": {"lops": lops, "g": g, "syllabus": syllabus, "level": level, "tools": tools},
        "misconceptions": misconceptions or [tid],
        "prompt": {"text": prompt},
        "payload": payload,
        "solution": {"steps": steps, "final": final},
        "feedback": fb,
        "provenance": {"template": template, "params": params, "generated": date,
                       "verified": True, "run": run},
    }


def wrapper(tid, code, items):
    return {"schema_version": SCHEMA_VERSION, "topic": tid, "type": code, "items": items}


def cli(make_items, tid, code):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=int, default=1)
    ap.add_argument("--date", default="2026-10-02")
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--write", action="store_true", help=f"write exercises/{tid}/{code}.json")
    a = ap.parse_args()
    text = json.dumps(wrapper(tid, code, make_items(a.run, a.date, a.count)), ensure_ascii=False, indent=2) + "\n"
    if a.write:
        out = Path(__file__).resolve().parent.parent / "exercises" / tid / f"{code}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            raise SystemExit(f"{out} exists; appending needs manual numbering")
        out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def show(expr):
    """sympy expression or number as display text: π, ·, ^, proper minus sign, decimal comma."""
    s = re.sub(r"sqrt\((\d+|[a-z])\)", r"√\1", str(expr)).replace("sqrt", "√").replace("*pi", "π").replace("pi", "π").replace("**", "^").replace("*", " · ")
    return num(s)
