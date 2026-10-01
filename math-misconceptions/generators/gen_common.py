"""Shared helpers for the generators (not a template itself)."""
import argparse
import json
from pathlib import Path

MINUS = "−"


def num(n):
    """Integer as display text with a proper minus sign."""
    return str(n).replace("-", MINUS)


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


def base_item(tid, code, n, ops, t, grade, level, prompt, payload, steps, final,
              correct_fb, template, params, date, run, misconceptions=None, generic_wrong=None):
    fb = {"correct": correct_fb}
    if generic_wrong:
        fb["generic_wrong"] = generic_wrong
    return {
        "schema_version": "1.0",
        "id": f"{tid}-{code}-{n:03d}",
        "type": code,
        "status": "draft",
        "lang": "fi",
        "curriculum": {"ops": ops, "t": t, "grade": grade, "level": level},
        "misconceptions": misconceptions or [tid],
        "prompt": {"text": prompt},
        "payload": payload,
        "solution": {"steps": steps, "final": final},
        "feedback": fb,
        "provenance": {"template": template, "params": params, "generated": date,
                       "verified": True, "run": run},
    }


def cli(make_items, tid, code):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=int, default=1)
    ap.add_argument("--date", default="2026-09-30")
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--write", action="store_true", help=f"write exercises/{tid}/{code}.json")
    a = ap.parse_args()
    items = make_items(a.run, a.date, a.count)
    doc = {"schema_version": "1.0", "topic": tid, "type": code, "items": items}
    text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    if a.write:
        out = Path(__file__).resolve().parent.parent / "exercises" / tid / f"{code}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            raise SystemExit(f"{out} exists; appending needs manual numbering")
        out.write_text(text, encoding="utf-8")
    else:
        print(text)


def lin(p, q):
    """Linear expression p x + q as display text (proper minus sign, no 1x, no +0)."""
    if p == 0:
        return num(q)
    first = ("−" if p < 0 else "") + ("" if abs(p) == 1 else str(abs(p))) + "x"
    if q == 0:
        return first
    return f"{first} {'+' if q > 0 else MINUS} {abs(q)}"
