#!/usr/bin/env python3
"""ALG-12 (subtraction of a negative number), type ME (multi-select equivalence). Expressions are numeric (the
variable x is only a schema placeholder); equivalence flags are checked by verify.py and every distractor value is
asserted to differ from the reference. Tagged distractors subtract the absolute value: a - (-b) read as a - b."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "alg12_me"
TID, CODE = "ALG-12", "ME"
GOOD = "Oikein: negatiivisen luvun vähentäminen on sen vastaluvun lisäämistä, a − (−b) = a + b."
GENERIC = ("Laske jokaisen vaihtoehdon arvo erikseen ja vertaa viitelausekkeeseen. Muista, että "
           "a − (−b) = a + b.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1212)
    items, seen = [], set()
    for k in range(count):
        a, b, c = rng.sample(range(2, 10), 3)
        ctx = ""
        if k == 0:
            level, ref, val = "T", f"{a} {MINUS} ({MINUS}{b})", a + b
            eq = [f"{a} + {b}", f"{b} + {a}", f"{a + b}"]
            bad = [(f"{a} {MINUS} {b}", TID, a - b), (f"{MINUS}{a} {MINUS} {b}", None, -a - b), (f"{a} · {b}", None, a * b)]
            steps = [f"{a} {MINUS} ({MINUS}{b}) = {a} + {b} = {val}"]
        elif k == 1:
            level, ref, val = "T", f"{MINUS}{a} {MINUS} ({MINUS}{b})", b - a
            eq = [f"{b} {MINUS} {a}", f"{MINUS}{a} + {b}", f"{num(b - a)}"]
            bad = [(f"{MINUS}{a} {MINUS} {b}", TID, -a - b), (f"{a} {MINUS} {b}", None, a - b), (f"{a} + {b}", None, a + b)]
            steps = [f"{MINUS}{a} {MINUS} ({MINUS}{b}) = {MINUS}{a} + {b} = {num(val)}"]
        elif k == 2:
            level, ref, val = "T", f"{a} {MINUS} ({MINUS}{b}) {MINUS} ({MINUS}{c})", a + b + c
            eq = [f"{a} + {b} + {c}", f"{a} + {b} {MINUS} ({MINUS}{c})", f"{a} {MINUS} ({MINUS}{c}) + {b}"]
            bad = [(f"{a} {MINUS} {b} {MINUS} {c}", TID, a - b - c), (f"{a} + {b} {MINUS} {c}", TID, a + b - c),
                   (f"{MINUS}{a} {MINUS} {b} {MINUS} {c}", None, -a - b - c)]
            steps = [f"{a} + {b} + {c} = {val}"]
        elif k == 3:
            level, ref, val = "H", f"{a} {MINUS} ({MINUS}{b})", a + b
            ctx = (f"Lämpötila nousee arvosta {MINUS}{b} °C arvoon {a} °C. Valitse kaikki lausekkeet, joiden arvo on "
                   "lämpötilan muutos asteina (loppu miinus alku). ")
            eq = [f"{a} + {b}", f"{b} + {a}", f"{a + b}"]
            bad = [(f"{a} {MINUS} {b}", TID, a - b), (f"{b} {MINUS} {a}", None, b - a), (f"{MINUS}{a} {MINUS} {b}", None, -a - b)]
            steps = [f"Muutos on {a} {MINUS} ({MINUS}{b}) = {a} + {b} = {val}"]
        else:
            level, ref, val = "H", f"{c} {MINUS} ({MINUS}{a}) {MINUS} {b}", c + a - b
            eq = [f"{c} + {a} {MINUS} {b}", f"{c} + {a} + ({MINUS}{b})", f"{num(c + a - b)}"]
            bad = [(f"{c} {MINUS} {a} {MINUS} {b}", TID, c - a - b), (f"{c} {MINUS} {a} + {b}", TID, c - a + b),
                   (f"{c} + {a} + {b}", None, c + a + b)]
            steps = [f"{c} {MINUS} ({MINUS}{a}) = {c} + {a}", f"{c + a} {MINUS} {b} = {num(val)}"]
        assert all(v != val for _, _, v in bad), "distractor equals reference"
        key = (k, a, b, c)
        assert key not in seen
        seen.add(key)
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref}."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m, _ in bad]
        assert len({t for t, _, _ in opts}) == len(opts), "duplicate option texts"
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[1], [2], [3]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S2.01"], ["T10", "T11"], 7, level, prompt, payload,
                               steps, num(val), GOOD, TEMPLATE, {"a": a, "b": b, "c": c, "form": k}, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
