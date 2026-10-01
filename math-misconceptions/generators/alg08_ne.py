#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type NE (expression entry). Reference computed with sympy;
the typical wrong answer multiplies only the first term of the bracket."""
import random

import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "alg08_ne"
TID, CODE = "ALG-08", "NE"
x = sp.Symbol("x")
SAMPLES = [[-2], [0], [3]]


def fmt(expr):
    return str(sp.expand(expr)).replace("*", "").replace("-", "−")


def term(c):
    return "x" if c == 1 else f"{c}x"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8302)
    items = []
    for k in range(count):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        c = rng.randint(2, 5)
        d, e = rng.randint(2, 5), rng.randint(2, 6)
        if k == 0:
            level, prompt = "T", f"Avaa sulut ja sievennä: {a}(x + {b})"
            good, first = a * (x + b), a * x + b
            second = x + a * b
            steps = [f"{a} · x + {a} · {b}", fmt(good)]
        elif k == 1:
            level, prompt = "T", f"Avaa sulut ja sievennä: {a}({c}x {chr(0x2212)} {b})"
            good, first = a * (c * x - b), a * c * x - b
            second = c * x - a * b
            steps = [f"{a} · {c}x {chr(0x2212)} {a} · {b}", fmt(good)]
        elif k == 2:
            level, prompt = "T", f"Avaa sulut ja sievennä: {a}({b} + {c}x)"
            good, first = a * (b + c * x), a * b + c * x
            second = b + a * c * x
            steps = [f"{a} · {b} + {a} · {c}x", fmt(good)]
        elif k == 3:
            level = "H"
            prompt = (f"Pizzeria myy pizzoja hintaan x euroa kappale, ja jokaisesta pizzasta peritään {b} euroa kuljetusmaksua. "
                      f"Kirjoita {a} pizzan kokonaishinta sievennettynä.")
            good, first = a * (x + b), a * x + b
            second = x + a * b
            steps = [f"{a}(x + {b}) = {a} · x + {a} · {b}", fmt(good)]
        else:
            level = "H"
            prompt = f"Avaa sulut ja sievennä: {a}(x + {b}) + {d}(x {chr(0x2212)} {e})"
            good = a * (x + b) + d * (x - e)
            first = a * x + b + d * x - e
            second = x + a * b + x - d * e
            steps = [f"{a}x + {a * b} + {d}x {chr(0x2212)} {d * e}", fmt(good)]
        wrong = [(first, TID, f"Kerroin {a} kertoo myös sulun jälkimmäisen termin."),
                 (second, TID, "Kerroin kertoo myös sulun ensimmäisen termin.")]
        wl = []
        for w, m, fb in wrong:
            assert sp.expand(w - good) != 0
            if fmt(w) != fmt(good) and fmt(w) not in [t["match"] for t in wl]:
                wl.append({"match": fmt(w), "misconception": m, "feedback": fb})
        payload = {"answer": {"kind": "expression", "variables": ["x"], "reference": fmt(good), "samples": SAMPLES},
                   "wrong": wl, "input_hint": "Kirjoita esim. 2x + 6"}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, fmt(good),
                               "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin.", TEMPLATE,
                               {"a": a, "b": b, "c": c, "d": d, "e": e}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
