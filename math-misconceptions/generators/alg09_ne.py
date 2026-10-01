#!/usr/bin/env python3
"""ALG-09 (square of a sum), type NE (expression entry). Reference computed with sympy; the typical wrong
answer distributes the power over the sum."""
import random

import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "alg09_ne"
TID, CODE = "ALG-09", "NE"
x = sp.Symbol("x")
SAMPLES = [[-2], [0], [3]]
M = chr(0x2212)


def fmt(expr):
    return str(sp.expand(expr)).replace("**2", "²").replace("*", "").replace("-", M)


def make_items(run, date, count=5, start=1):
    rng = random.Random(9302)
    items = []
    for k in range(count):
        b = rng.randint(2, 9)
        c = rng.randint(2, 4)
        if k == 0:
            level, prompt, good = "T", f"Avaa sulut ja sievennä: (x + {b})²", (x + b) ** 2
            wrong = [(x**2 + b**2, "Potenssi ei jakaudu summan yli. Kirjoita (x + " + f"{b})(x + {b}) ja kerro."),
                     (x**2 + b * x + b**2, "Keskitermejä on kaksi: x · " + f"{b} + {b} · x.")]
        elif k == 1:
            level, prompt, good = "T", f"Avaa sulut ja sievennä: (x {M} {b})²", (x - b) ** 2
            wrong = [(x**2 - b**2, "Potenssi ei jakaudu erotuksen yli. Kirjoita (x " + M + f" {b})(x {M} {b}) ja kerro."),
                     (x**2 - 2 * b * x - b**2, f"Viimeinen termi on ({M}{b})² = {b**2}.")]
        elif k == 2:
            level, prompt, good = "T", f"Avaa sulut ja sievennä: ({c}x + {b})²", (c * x + b) ** 2
            wrong = [(c**2 * x**2 + b**2, "Potenssi ei jakaudu summan yli: keskitermi 2 · " + f"{c}x · {b} puuttuu."),
                     (c * x**2 + 2 * b * c * x + b**2 if False else c**2 * x**2 + b * c * x + b**2, "Keskitermejä on kaksi.")]
        elif k == 3:
            level = "H"
            prompt = (f"Neliön muotoisen laatan sivu on (x + {b}) cm. Kirjoita laatan pinta-ala sievennettynä.")
            good = (x + b) ** 2
            wrong = [(x**2 + b**2, "Pinta-ala jakautuu neliöön x², kahteen suorakulmioon ja neliöön " + f"{b}²."),
                     (x**2 + 2 * b * x, f"Pieni neliö {b}² = {b**2} puuttuu.")]
        else:
            level = "H"
            prompt = f"Sievennä: (x + {b})² {M} x²"
            good = (x + b) ** 2 - x**2
            wrong = [(sp.Integer(b**2), "Potenssi ei jakaudu summan yli: (x + " + f"{b})² = x² + {2 * b}x + {b**2}."),
                     (sp.Integer(b**2) + b * x, "Keskitermejä on kaksi: 2 · " + f"{b}x.")]
        wl = []
        for w, fb in wrong:
            assert sp.expand(w - good) != 0
            wl.append({"match": fmt(w), "misconception": TID, "feedback": fb})
        steps = [f"Avataan neliö: {fmt((x + b) ** 2) if k in (0, 3, 4) else fmt(good)}", fmt(good)]
        payload = {"answer": {"kind": "expression", "variables": ["x"], "reference": fmt(good), "samples": SAMPLES},
                   "wrong": wl, "input_hint": "Kirjoita esim. x² + 6x + 9"}
        items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, prompt, payload, steps, fmt(good),
                               "Oikein: (a + b)² = a² + 2ab + b².", TEMPLATE, {"b": b, "c": c}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
