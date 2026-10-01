#!/usr/bin/env python3
"""ALG-04 (conjoining terms), type NE (expression entry). Reference and wrong answers computed with sympy."""
import random

import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "alg04_ne"
TID, CODE = "ALG-04", "NE"
x, y = sp.symbols("x y")
OP = "Plusmerkki ei pyydä yhdistämään kaikkea yhdeksi termiksi. Sievennä vain samanmuotoiset termit."


def fmt(e):
    return str(sp.expand(e)).replace("*", "").replace("-", "−")


def make_items(run, date, count=5, start=1):
    rng = random.Random(312)
    items = []
    for k in range(count):
        a, b, c, d = (rng.randint(2, 7) for _ in range(4))
        while c == a:
            c = rng.randint(2, 7)
        if k == 0:
            level, vars_, samples = "T", ["x"], [[-2], [0], [3]]
            expr = a * x + b
            prompt = f"Sievennä lauseke {a}x + {b}. Jos se ei sievene, kirjoita se sellaisenaan."
            wrong = [((a + b) * x, TID, OP), (a * b * x, TID, OP)]
            steps = [f"{a}x ja {b} ovat eri muotoisia termejä", f"{a}x + {b}"]
        elif k == 1:
            level, vars_, samples = "T", ["x"], [[-2], [0], [3]]
            given = f"{a}x + {b} + {c}x"
            expr = (a + c) * x + b
            prompt = f"Sievennä lauseke {given}."
            wrong = [((a + b + c) * x, TID, OP), ((a + c + b), None, "Kirjain x ei saa kadota.")]
            steps = [f"{a}x + {c}x = {a + c}x", f"{a + c}x + {b}"]
        elif k == 2:
            level, vars_, samples = "T", ["x"], [[-2], [0], [3]]
            given = f"{b} + {a}x + {d}"
            expr = a * x + b + d
            prompt = f"Sievennä lauseke {given}."
            wrong = [((a + b + d) * x, TID, OP), (a * (b + d) * x, TID, OP)]
            steps = [f"Luvut: {b} + {d} = {b + d}", f"{a}x + {b + d}"]
        elif k == 3:
            level, vars_, samples = "H", ["x", "y"], [[1, 2], [2, -1], [-3, 4]]
            given = f"{a}x + {b}y + {c}x + {d}y"
            expr = (a + c) * x + (b + d) * y
            prompt = f"Sievennä lauseke {given}."
            wrong = [((a + b + c + d) * x, TID, OP), ((a + c + b + d) * x * y, TID, OP)]
            steps = [f"x-termit: {a}x + {c}x = {a + c}x", f"y-termit: {b}y + {d}y = {b + d}y", f"{a + c}x + {b + d}y"]
        else:
            level, vars_, samples = "H", ["x"], [[-2], [0], [3]]
            given = f"{a}x + {b} + {c}x {chr(0x2212)} {d}"
            expr = (a + c) * x + b - d
            prompt = f"Sievennä lauseke {given}."
            wrong = [((a + b + c - d) * x, TID, OP), ((a + c) * x + b + d, None, f"Tarkista luvun {d} merkki.")]
            steps = [f"x-termit: {a}x + {c}x = {a + c}x", f"Luvut: {b} {chr(0x2212)} {d} = {b - d}", fmt(expr)]
        ref = fmt(expr)
        wr = []
        for w, m, fb in wrong:
            wt = fmt(w) if not isinstance(w, int) else str(w)
            wr.append({"match": wt, "misconception": m, "feedback": fb})
        payload = {"answer": {"kind": "expression", "variables": vars_, "reference": ref, "samples": samples},
                   "wrong": wr, "input_hint": "Kirjoita esim. 5x + 3"}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, ref,
                               "Oikein: vain samanmuotoiset termit lasketaan yhteen.", TEMPLATE,
                               {"a": a, "b": b, "c": c, "d": d}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
