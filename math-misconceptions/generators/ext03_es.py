#!/usr/bin/env python3
"""EXT-03 (inequality sign not reversed when multiplying or dividing by a negative number), type ES (error
spotting). Lines before the error line have the same solution set as line 1; the error line divides by a negative
number and keeps the sign, which changes the solution set (checked by verify.py)."""
import random

from gen_common import MINUS, base_item, cli, lin, num

TEMPLATE = "ext03_es"
TID, CODE = "EXT-03", "ES"
FLIP = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
INTRO = "Oppilas ratkaisee epäyhtälön rivi riviltä. "
GENERIC = ("Tarkista rivi kerrallaan, onko uusi epäyhtälö sama kuin edellinen. "
           "Kun jaetaan tai kerrotaan negatiivisella luvulla, epäyhtälömerkin suunta kääntyy.")
GOOD = "Oikein: negatiivisella luvulla jaettaessa epäyhtälömerkin suunta kääntyy."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1303)
    items, seen = [], set()
    for k in range(count):
        ctx, var = "", "x"
        if k == 0:
            a, r, q, rel = 2, rng.choice([-3, 4]), rng.choice([3, 5]), ">"
            rhs0 = -a * r + q
            lines = [f"{lin(-a, q)} {rel} {num(rhs0)}", f"{lin(-a, 0)} {rel} {num(-a * r)}", f"x {rel} {num(r)}"]
            err, level = 3, "T"
            fix = f"Rivillä 3 jaetaan luvulla {num(-a)}, joten merkki kääntyy: x {FLIP[rel]} {num(r)}."
            params = {"a": a, "r": r, "q": q}
        elif k == 1:
            a, r, q, rel = 3, rng.choice([2, -2]), rng.choice([4, 7]), "≤"
            rhs0 = -a * r + q
            lines = [f"{q} {MINUS} {a}x {rel} {num(rhs0)}", f"{lin(-a, 0)} {rel} {num(-a * r)}", f"x {rel} {num(r)}"]
            err, level = 3, "T"
            fix = f"Rivillä 3 jaetaan luvulla {num(-a)}, joten merkki kääntyy: x {FLIP[rel]} {num(r)}."
            params = {"a": a, "r": r, "q": q}
        elif k == 2:
            t0, a, r = 5, 3, 3
            var = "t"
            ctx = (f"Lämpötila on aluksi {t0} °C ja laskee {a} astetta tunnissa. "
                   f"Milloin lämpötila on alle {num(t0 - a * r)} °C? ")
            lines = [f"{t0} {MINUS} {a}t < {num(t0 - a * r)}", f"{MINUS}{a}t < {num(-a * r)}", f"t < {r}"]
            err, level = 3, "T"
            fix = f"Rivillä 3 jaetaan luvulla {num(-a)}, joten merkki kääntyy: t > {r}."
            params = {"t0": t0, "a": a, "r": r}
        elif k == 3:
            a, b, r, rel = 2, 3, rng.choice([2, 4]), "<"
            d = -a * r - a * b
            lines = [f"{MINUS}{a}(x + {b}) {rel} {num(d)}", f"{MINUS}{a}x {MINUS} {a * b} {rel} {num(d)}",
                     f"{MINUS}{a}x {rel} {num(d + a * b)}", f"x {rel} {num(r)}"]
            err, level = 4, "H"
            fix = (f"Rivit 2 ja 3 ovat oikein. Rivillä 4 jaetaan luvulla {num(-a)}, joten merkki kääntyy: "
                   f"x {FLIP[rel]} {num(r)}.")
            params = {"a": a, "b": b, "r": r}
        else:
            p1, p2, q1, r, rel = 1, 4, 2, 3, ">"
            q2 = q1 + (p1 - p2) * r
            lines = [f"{lin(p1, q1)} {rel} {lin(p2, q2)}", f"{num(p1 - p2)}x {rel} {num(q2 - q1)}", f"x {rel} {num(r)}"]
            err, level = 3, "H"
            fix = (f"Rivi 2 on oikein. Rivillä 3 jaetaan luvulla {num(p1 - p2)}, joten merkki kääntyy: "
                   f"x {FLIP[rel]} {num(r)}.")
            params = {"p1": p1, "p2": p2, "q1": q1, "r": r}
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"lines": lines, "error_line": err, "error_type": "inequality_sign_not_reversed"}
        items.append(base_item(TID, CODE, start + k, ["S3.07"], ["T14"], 9, level, INTRO + ctx + ASK, payload,
                               [fix], f"Virhe on rivillä {err}", GOOD, TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
