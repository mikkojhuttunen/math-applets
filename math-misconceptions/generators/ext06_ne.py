#!/usr/bin/env python3
"""EXT-06 (sine read as a length; adjacent and opposite leg mixed up), type NE. Ratios and lengths are computed with
exact fractions from Pythagorean triples whose ratios are terminating decimals. Tagged wrong answers are a side
length given as the sine, or the ratio taken with the adjacent leg."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "ext06_ne"
TID, CODE = "EXT-06", "NE"
BAD = ("Sini on suhdeluku: vastainen kateetti jaettuna hypotenuusalla. Tarkista, ettet anna sivun pituutta "
       "etkä käytä viereistä kateettia.")
GOOD = "Oikein: sini lasketaan jakamalla vastainen kateetti hypotenuusalla."
TRIPLES = [(3, 4, 5), (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25), (7, 24, 25)]


def c(f):
    """Decimal comma text of a terminating fraction."""
    v = float(f)
    assert Fraction(str(v)) == f
    return str(v).replace(".", ",").removesuffix(",0")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1707)
    items, seen = [], set()
    for k in range(count):
        a, b, h = rng.choice([t for t in TRIPLES if t not in seen])
        seen.add((a, b, h))
        assert a * a + b * b == h * h
        sin, cos = Fraction(a, h), Fraction(b, h)
        assert sin != cos
        if k == 0:
            level = "T"
            prompt = (f"Suorakulmaisen kolmion kateetit ovat {a} cm ja {b} cm ja hypotenuusa {h} cm. "
                      f"Kulman α vastainen kateetti on {a} cm. Laske sin α desimaalilukuna.")
            ans, wrong = sin, [(a, "pituus"), (cos, "viereinen")]
            steps = [f"sin α = {a} / {h}", f"= {c(sin)}"]
        elif k == 1:
            level = "T"
            prompt = (f"Suorakulmaisen kolmion kateetit ovat {a} cm ja {b} cm ja hypotenuusa {h} cm. "
                      f"Kulman β vastainen kateetti on {b} cm. Laske sin β desimaalilukuna.")
            ans, wrong = cos, [(b, "pituus"), (sin, "viereinen")]
            steps = [f"sin β = {b} / {h}", f"= {c(cos)}"]
        elif k == 2:
            level = "T"
            prompt = (f"Suorakulmaisessa kolmiossa kulman α viereinen kateetti on {b} cm, vastainen kateetti {a} cm ja "
                      f"hypotenuusa {h} cm. Laske cos α desimaalilukuna.")
            ans, wrong = cos, [(sin, "vastainen"), (b, "pituus")]
            steps = [f"cos α = viereinen / hypotenuusa = {b} / {h}", f"= {c(cos)}"]
        elif k == 3:
            level = "H"
            prompt = (f"Tikkaat ovat {h} m pitkät ja ne yltävät {a} m korkeudelle seinällä. Laske sen kulman sini, "
                      f"jonka tikkaat muodostavat maan kanssa. Kulman vastainen kateetti on korkeus {a} m.")
            ans, wrong = sin, [(a, "pituus"), (cos, "viereinen")]
            steps = [f"sin α = {a} / {h}", f"= {c(sin)}"]
        else:
            level = "H"
            prompt = (f"Suorakulmaisessa kolmiossa sin α = {c(sin)} ja hypotenuusa on {h} cm. "
                      f"Kuinka monta senttimetriä pitkä on kulman α vastainen kateetti?")
            ans, wrong = Fraction(a), [(b, "viereinen"), (sin, "sini")]
            steps = [f"vastainen = sin α · hypotenuusa = {c(sin)} · {h}", f"= {a}"]
        assert all(Fraction(w[0]) != ans for w in wrong)
        payload = {"answer": {"kind": "number", "value": float(ans), "tolerance": 0},
                   "wrong": [{"match": float(Fraction(w[0])), "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku" + (" desimaalipilkulla" if ans.denominator != 1 else "")}
        final = c(ans)
        items.append(base_item(TID, CODE, start + k, ["S5.10"], ["T17"], 9, level, prompt, payload, steps, final,
                               GOOD, TEMPLATE, {"legs": [a, b], "hyp": h}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
