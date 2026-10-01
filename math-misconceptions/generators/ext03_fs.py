#!/usr/bin/env python3
"""EXT-03 (inequality sign not reversed when multiplying or dividing by a negative number), type FS. Every line
is an inequality with the same solution set (checked by verify.py); the blanked line is accepted by equivalence
of solution sets, so keeping the sign in a division by a negative number is rejected. The answer is stored as kind
expression with an inequality reference because the equation kind needs a finite solution set."""
import random

from gen_common import MINUS, base_item, cli, lin, num

TEMPLATE = "ext03_fs"
TID, CODE = "EXT-03", "FS"
FLIP = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
SAMPLES = [[1], [2], [3]]
GOOD = "Oikein: negatiivisella luvulla jaettaessa tai kerrottaessa epäyhtälömerkin suunta kääntyy."
GENERIC = ("Tarkista välivaihe sijoittamalla jokin luku: toteuttaako se sekä edellisen että uuden rivin? "
           "Kun jaetaan tai kerrotaan negatiivisella luvulla, epäyhtälömerkin suunta kääntyy.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1304)
    items, seen = [], set()
    for k in range(count):
        ctx = ""
        if k == 0:
            a, r, q, rel = 2, rng.choice([3, 5]), rng.choice([4, 7]), ">"
            lines = [f"{lin(-a, q)} {rel} {num(-a * r + q)}", f"{lin(-a, 0)} {rel} {num(-a * r)}",
                     f"x {FLIP[rel]} {num(r)}"]
            blank, level, params = 3, "T", {"a": a, "r": r, "q": q}
            prompt = f"Täydennä puuttuva rivi: {lines[0]}, {lines[1]}, □. Jaa molemmat puolet luvulla {num(-a)}."
            steps = [f"Vähennetään {q} molemmilta puolilta: {lines[1]}",
                     f"Jaetaan luvulla {num(-a)}, merkki kääntyy: {lines[2]}"]
        elif k == 1:
            a, r, rel = 3, rng.choice([2, 4]), "≤"
            lines = [f"{MINUS}{a}x + 1 {rel} {num(-a * r + 1)}", f"{MINUS}{a}x {rel} {num(-a * r)}",
                     f"x {FLIP[rel]} {num(r)}"]
            blank, level, params = 3, "T", {"a": a, "r": r}
            prompt = f"Täydennä puuttuva rivi: {lines[0]}, {lines[1]}, □. Ratkaise x."
            steps = [f"Vähennetään 1 molemmilta puolilta: {lines[1]}",
                     f"Jaetaan luvulla {num(-a)}, merkki kääntyy: {lines[2]}"]
        elif k == 2:
            t0, a, r = 8, 2, 3
            ctx = (f"Vesisäiliössä on {t0} litraa vettä, ja siitä valuu {a} litraa minuutissa. "
                   f"Milloin vettä on alle {num(t0 - a * r)} litraa? ")
            lines = [f"{t0} {MINUS} {a}t < {num(t0 - a * r)}", f"{MINUS}{a}t < {num(-a * r)}", f"t > {r}"]
            blank, level, params = 3, "T", {"t0": t0, "a": a, "r": r}
            prompt = ctx + f"Täydennä puuttuva rivi: {lines[0]}, {lines[1]}, □."
            steps = [f"Vähennetään {t0} molemmilta puolilta: {lines[1]}",
                     f"Jaetaan luvulla {num(-a)}, merkki kääntyy: {lines[2]}"]
        elif k == 3:
            a, b, r, rel = 2, 3, rng.choice([2, 4]), "<"
            d = -a * r - a * b
            lines = [f"{MINUS}{a}(x + {b}) {rel} {num(d)}", f"{MINUS}{a}x {MINUS} {a * b} {rel} {num(d)}",
                     f"{MINUS}{a}x {rel} {num(d + a * b)}", f"x {FLIP[rel]} {num(r)}"]
            blank, level, params = 2, "H", {"a": a, "b": b, "r": r}
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}, {lines[3]}. "
                      "Avaa sulut. Merkkiä ei vielä käännetä.")
            steps = [f"Avataan sulut: {lines[1]}", f"Siirretään luku oikealle: {lines[2]}",
                     f"Jaetaan luvulla {num(-a)}, merkki kääntyy: {lines[3]}"]
        else:
            p1, p2, q1, r, rel = 1, 4, 2, 3, ">"
            q2 = q1 + (p1 - p2) * r
            lines = [f"{lin(p1, q1)} {rel} {lin(p2, q2)}", f"{num(p1 - p2)}x {rel} {num(q2 - q1)}",
                     f"x {FLIP[rel]} {num(r)}"]
            blank, level, params = 2, "H", {"p1": p1, "p2": p2, "q1": q1, "r": r}
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}. "
                      "Siirrä x-termit vasemmalle ja luvut oikealle. Merkkiä ei vielä käännetä.")
            steps = [f"Siirretään termit: {lines[1]}", f"Jaetaan luvulla {num(p1 - p2)}, merkki kääntyy: {lines[2]}"]
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        ref = lines[blank - 1]
        answer = {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S3.07"], ["T14"], 9, level, prompt, payload, steps, ref,
                               GOOD, TEMPLATE, {**params, "blank": blank}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
