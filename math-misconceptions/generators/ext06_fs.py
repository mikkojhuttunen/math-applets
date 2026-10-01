#!/usr/bin/env python3
"""EXT-06 (sine read as a length; adjacent and opposite leg mixed up), type FS. All lines are numeric expressions
equivalent to line 1 (a opposite, b adjacent, h hypotenuse); the blanked line is computed by code and verify.py checks
the chain for equivalence (the variable x is only a schema placeholder)."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "ext06_fs"
TID, CODE = "EXT-06", "FS"
SAMPLES = [[1], [2], [3]]
GOOD = "Oikein: sin α = vastainen kateetti / hypotenuusa ja cos α = viereinen kateetti / hypotenuusa."
GENERIC = "Tarkista, että sinin osoittajassa on vastainen kateetti ja kosinin osoittajassa viereinen kateetti. Jakajana on hypotenuusa."
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15)]


def fr(f):
    return f"{f.numerator}/{f.denominator}"


def build(k, a, b, h, m):
    tri = f"Suorakulmaisessa kolmiossa kulman α vastainen kateetti on {a} cm, viereinen kateetti {b} cm ja hypotenuusa {h} cm."
    if k == 0:
        lines = [f"{m} · {a}/{h}", f"{m * a}/{h}", fr(Fraction(m * a, h))]
        return tri, "T", f"Laske {m} · sin α. Kirjoita välivaihe, jossa osoittaja on sievennetty", lines
    if k == 1:
        lines = [f"{a}/{h} + {b}/{h}", f"({a} + {b})/{h}", fr(Fraction(a + b, h))]
        return tri, "T", "Laske sin α + cos α. Kirjoita välivaihe, jossa yhteinen nimittäjä on otettu pois", lines
    if k == 2:
        lines = [f"{a}/{h} · {h}", f"{a} · {h}/{h}", f"{a}"]
        return tri, "T", f"Laske sin α · {h}. Kirjoita välivaihe, jossa kertolasku on yhdistetty yhdeksi murtoluvuksi", lines
    if k == 3:
        lines = [f"({a}/{h}) / ({b}/{h})", f"{a}/{h} · {h}/{b}", fr(Fraction(a, b))]
        return tri, "H", "Laske sin α / cos α. Kirjoita välivaihe, jossa jakolasku on muutettu kertolaskuksi", lines
    lines = [f"{m * a}/{m * h}", f"{m} · {a}/({m} · {h})", fr(Fraction(a, h))]
    tri = (f"Kolmion sivut ovat {a} cm, {b} cm ja {h} cm, ja kulman α vastainen kateetti on {a} cm. "
           f"Kolmio suurennetaan {m}-kertaiseksi.")
    return tri, "H", "Laske suurennetun kolmion sin α. Kirjoita välivaihe, jossa tekijä on erotettu osoittajasta ja nimittäjästä", lines


def make_items(run, date, count=5, start=1):
    rng = random.Random(1722)
    items, seen = [], set()
    for k in range(count):
        while True:  # pick a triple whose three lines are all different (fractions that do not reduce would repeat)
            a, b, h = rng.choice([t for t in TRIPLES if t not in seen])
            m = rng.choice([2, 3, 5])
            tri, level, hint, lines = build(k, a, b, h, m)
            if len(set(lines)) == 3:
                break
        seen.add((a, b, h))
        assert a * a + b * b == h * h
        blank = 2
        ref = lines[blank - 1]
        prompt = f"Täydennä puuttuva rivi. {tri} {hint}: {lines[0]} = □ = {lines[2]}"
        answer = {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}
        steps = [f"{lines[i]} = {lines[i + 1]}" for i in range(len(lines) - 1)]
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S5.10"], ["T17"], 9, level, prompt, payload, steps, ref,
                               GOOD, TEMPLATE, {"triple": [a, b, h], "m": m, "blank": blank}, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
