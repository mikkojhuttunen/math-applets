#!/usr/bin/env python3
"""EXT-03 (inequality sign not reversed when multiplying or dividing by a negative number), type NE. The answer is
the number of integers in a window that satisfy the inequality, counted by brute force; the tagged wrong answer is
the count obtained when the inequality sign is not reversed."""
import random

from gen_common import base_item, cli, lin, num

TEMPLATE = "ext03_ne"
TID, CODE = "EXT-03", "NE"
FLIP = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
HOLDS = {">": lambda u, v: u > v, "<": lambda u, v: u < v, "≥": lambda u, v: u >= v, "≤": lambda u, v: u <= v}
BAD = ("Epäyhtälömerkin suunta kääntyy, kun jaetaan negatiivisella luvulla. "
       "Tarkista sijoittamalla muutama luku alkuperäiseen epäyhtälöön.")
GOOD = "Oikein: negatiivisella luvulla jaettaessa merkki kääntyy, ja ratkaisut lasketaan oikealta puolelta rajaa."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1302)
    items, seen = [], set()
    for k in range(count):
        lo, hi = -10, 10
        ctx = ""
        if k == 0:
            a, r = rng.choice([(2, -3), (3, -4), (5, -2)])
            p, q, rel, rhs, level = -a, 0, ">", -a * r, "T"
        elif k == 1:
            a, r = rng.choice([(2, 4), (4, 3), (3, 5)])
            p, q, rel, rhs, level = -a, 0, "≤", -a * r, "T"
        elif k == 2:
            t0, a, lim = rng.choice([(5, 3, -4), (8, 2, -2), (10, 5, -5)])
            p, q, rel, rhs, level, lo, hi = -a, t0, "<", lim, "T", 0, 10
            ctx = (f"Lämpötila on aluksi {t0} °C ja laskee {a} astetta tunnissa, joten t tunnin kuluttua se on "
                   f"{lin(p, q).replace('x', 't')} °C. ")
        elif k == 3:
            c, a, rhs = rng.choice([(5, 2, -1), (7, 3, 1), (1, 4, -7)])
            p, q, rel, level = -a, c, ">", "H"
        else:
            c, a, rhs = rng.choice([(3, 2, -5), (2, 3, -7), (4, 5, 9)])
            p, q, rel, level = -a, c, "≥", "H"
        assert (rhs - q) % p == 0
        r = (rhs - q) // p
        correct = sum(1 for x in range(lo, hi + 1) if HOLDS[rel](p * x + q, rhs))
        wrong = sum(1 for x in range(lo, hi + 1) if HOLDS[rel](x, r))  # sign not reversed
        assert wrong != correct and correct == sum(1 for x in range(lo, hi + 1) if HOLDS[FLIP[rel]](x, r))
        var = "t" if k == 2 else "x"
        if k == 2:
            prompt = ctx + f"Kuinka monta kokonaislukua t väliltä {lo}…{hi} on sellaisia, että lämpötila on alle {num(rhs)} °C?"
        else:
            prompt = f"Kuinka monta kokonaislukua väliltä {num(lo)}…{hi} toteuttaa epäyhtälön {lin(p, q)} {rel} {num(rhs)}?"
        steps = ([f"{lin(p, 0).replace('x', var)} {rel} {num(rhs - q)}"] if q else []) + \
                [f"Jaetaan luvulla {num(p)}, ja merkki kääntyy: {var} {FLIP[rel]} {num(r)}",
                 f"Ratkaisuja on {correct} kappaletta"]
        params = {"p": p, "q": q, "rhs": rhs, "rel": rel, "window": [lo, hi]}
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": correct},
                   "wrong": [{"match": wrong, "misconception": TID, "feedback": BAD}],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + k, ["S3.07"], ["T14"], 9, level, prompt, payload, steps,
                               str(correct), GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
