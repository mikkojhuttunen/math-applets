#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type FS (fill in the missing step). Every line is an equation
with the same solution (checked by verify.py); the blanked line is accepted by equivalence of solution sets."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg07_fs"
TID, CODE = "ALG-07", "FS"
GENERIC = ("Tarkista vaihe sijoittamalla ratkaisu: onko uudella rivillä sama ratkaisu kuin edellisellä? "
           "Siirrettäessä termi toiselle puolelle sen merkki vaihtuu, ja jakaminen tehdään molemmille puolille.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(8203)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
            if (a, b, x) not in seen:
                break
        seen.add((a, b, x))
        level, ctx, e = "T", "", 0
        if k == 0:
            c = a * x + b
            lines = [f"{a}x + {b} = {c}", f"{a}x = {c - b}", f"x = {x}"]
            blank, equiv = 2, [f"{c - b} = {a}x"]
            prompt = f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}. Kirjoita rivi, jossa luku {b} on siirretty toiselle puolelle."
            steps = [f"Vähennetään {b} molemmilta puolilta: {a}x = {c} {MINUS} {b} = {c - b}"]
        elif k == 1:
            c = a * x - b
            lines = [f"{a}x {MINUS} {b} = {c}", f"{a}x = {c + b}", f"x = {x}"]
            blank, equiv = 2, [f"{c + b} = {a}x"]
            prompt = f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}. Kirjoita rivi, jossa luku {b} on siirretty toiselle puolelle."
            steps = [f"Lisätään {b} molemmille puolille: {a}x = {c} + {b} = {c + b}"]
        elif k == 2:
            c = b + a * x
            lines = [f"{b} + {a}x = {c}", f"{a}x = {c - b}", f"x = {x}"]
            blank, equiv = 3, []
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, {lines[1]}, □. Jaa yhtälön molemmat puolet luvulla {a}"
                      f" ja kirjoita ratkaisu.")
            steps = [f"Jaetaan molemmat puolet luvulla {a}: x = {c - b} / {a} = {x}"]
        elif k == 3:
            level = "H"
            a = max(a, 5)
            e = rng.randint(2, a - 2)
            d = b + (a - e) * x
            lines = [f"{a}x + {b} = {e}x + {d}", f"{a}x {MINUS} {e}x = {d} {MINUS} {b}", f"{a - e}x = {d - b}", f"x = {x}"]
            blank, equiv = 2, [f"{a}x {MINUS} {e}x = {d - b}"]
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}, {lines[3]}. "
                      f"Kirjoita rivi, jossa x-termit ovat vasemmalla ja luvut oikealla.")
            steps = [f"Vähennetään {e}x ja {b} molemmilta puolilta: {a}x {MINUS} {e}x = {d} {MINUS} {b}"]
            c = d
        else:
            level = "H"
            c = a * x - b
            ctx = (f"Koripallojoukkue maksaa pelipaidoista {a} euroa kappaleelta ja saa {b} euron alennuksen koko tilauksesta. "
                   f"Lasku on {c} euroa, ja paitojen määrä x ratkaistaan yhtälöstä. ")
            lines = [f"{a}x {MINUS} {b} = {c}", f"{a}x = {c + b}", f"x = {x}"]
            blank, equiv = 2, [f"{c + b} = {a}x"]
            prompt = ctx + f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}. Kirjoita rivi, jossa alennus on otettu huomioon."
            steps = [f"Lisätään alennus {b} euroa molemmille puolille: {a}x = {c} + {b} = {c + b}"]
        ref = lines[blank - 1]
        answer = {"kind": "equation", "reference": ref, "variable": "x", "solutions": [x]}
        if equiv:
            answer["equivalents"] = equiv
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload,
                               steps + [f"Ratkaisu: x = {x}"], ref,
                               "Oikein: molemmille puolille tehdään sama toimitus, ja siirrettäessä termin merkki vaihtuu.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "e": e, "x": x}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
