#!/usr/bin/env python3
"""ALG-11 (minus sign not distributed), type NE (expression entry). Reference computed with sympy; the typical
wrong answer applies the minus sign before a bracket to the first term only."""
import random

import sympy as sp

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg11_ne"
TID, CODE = "ALG-11", "NE"
x = sp.Symbol("x")
SAMPLES = [[-2], [0], [3]]
FIRST = "Miinusmerkki sulun edessä koskee kaikkia sulun sisällä olevia termejä, ei vain ensimmäistä."


def fmt(expr):
    return str(sp.expand(expr)).replace("*", "").replace("-", MINUS)


def make_items(run, date, count=5, start=1):
    rng = random.Random(1102)
    items = []
    for k in range(count):
        a, b, c, d = rng.randint(2, 7), rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 6)
        if k == 0:
            level, prompt = "T", f"Sievennä: {MINUS}(x {MINUS} {b})"
            good, first = -(x - b), -x - b
        elif k == 1:
            level, prompt = "T", f"Sievennä: {MINUS}({a}x + {b})"
            good, first = -(a * x + b), -a * x + b
        elif k == 2:
            level, prompt = "T", f"Sievennä: {c} {MINUS} ({a}x {MINUS} {b})"
            good, first = c - (a * x - b), c - a * x - b
        elif k == 3:
            level, prompt = "H", f"Sievennä: {MINUS}({a}x {MINUS} {b}) {MINUS} (x + {d})"
            good, first = -(a * x - b) - (x + d), -a * x - b - x - d
        else:
            level = "H"
            prompt = (f"Tilillä on {c + b} euroa. Siitä maksetaan lasku, jonka hinta on x euroa, mutta laskusta saa {b} euron "
                      f"alennuksen. Kirjoita jäljelle jäävä rahamäärä sievennettynä lausekkeena.")
            good, first = (c + b) - (x - b), c + b - x - b
        steps = [f"Muutetaan sulun sisällä olevien termien merkit: {fmt(good)}"]
        assert sp.expand(first - good) != 0
        wl = [{"match": fmt(first), "misconception": TID, "feedback": FIRST}]
        payload = {"answer": {"kind": "expression", "variables": ["x"], "reference": fmt(good), "samples": SAMPLES},
                   "wrong": wl, "input_hint": "Kirjoita esim. −x + 5"}
        items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, prompt, payload, steps, fmt(good),
                               "Oikein: sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
