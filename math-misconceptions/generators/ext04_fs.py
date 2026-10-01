#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type FS. Every line is an equation with the same two solutions (checked by
verify.py); the blanked line is accepted by equivalence of solution sets, so a line that keeps only x = a is
rejected. The last line of each chain is the factored form (x - a)(x + a) = 0, which shows both roots."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "ext04_fs"
TID, CODE = "EXT-04", "FS"
GOOD = "Oikein: neliö ei erota lukua ja sen vastalukua, joten yhtälöllä on kaksi ratkaisua."
GENERIC = ("Tarkista välivaihe sijoittamalla: toteuttavatko sekä positiivinen että negatiivinen luku "
           "uuden rivin? Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1404)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a = rng.choice([4, 6, 9])
            lines = [f"x² {MINUS} {a * a} = 0", f"x² = {a * a}", f"(x {MINUS} {a})(x + {a}) = 0"]
            blank, level, params = 2, "T", {"a": a}
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}. "
                      "Siirrä luku oikealle puolelle.")
            steps = [f"Lisätään {a * a} molemmille puolille: {lines[1]}",
                     f"Tulon nollasääntö: x = {a} tai x = {MINUS}{a}"]
        elif k == 1:
            a = rng.choice([5, 7, 8])
            lines = [f"x² {MINUS} {a * a} = 0", f"x² = {a * a}", f"(x {MINUS} {a})(x + {a}) = 0"]
            blank, level, params = 3, "T", {"a": a}
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, {lines[1]}, □. "
                      f"Kirjoita yhtälö tulomuodossa (x {MINUS} luku)(x + luku) = 0.")
            steps = [f"x² {MINUS} {a * a} = (x {MINUS} {a})(x + {a})", f"Tulon nollasääntö: x = {a} tai x = {MINUS}{a}"]
        elif k == 2:
            a, p = rng.choice([(3, 4), (5, 2)])
            lines = [f"{p}x² = {p * a * a}", f"x² = {a * a}", f"(x {MINUS} {a})(x + {a}) = 0"]
            blank, level, params = 2, "T", {"a": a, "p": p}
            prompt = f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}. Jaa yhtälön molemmat puolet luvulla {p}."
            steps = [f"Jaetaan luvulla {p}: {lines[1]}", f"Tulon nollasääntö: x = {a} tai x = {MINUS}{a}"]
        elif k == 3:
            a, p = 4, 3
            lines = [f"{p}x² {MINUS} {p * a * a} = 0", f"{p}x² = {p * a * a}", f"x² = {a * a}",
                     f"(x {MINUS} {a})(x + {a}) = 0"]
            blank, level, params = 3, "H", {"a": a, "p": p}
            prompt = f"Täydennä puuttuva rivi: {lines[0]}, {lines[1]}, □, {lines[3]}. Jaa molemmat puolet luvulla {p}."
            steps = [f"Siirretään luku: {lines[1]}", f"Jaetaan luvulla {p}: {lines[2]}",
                     f"Tulon nollasääntö: x = {a} tai x = {MINUS}{a}"]
        else:
            a, p, c = 5, 2, 9
            lines = [f"{p}x² + {c} = {p * a * a + c}", f"{p}x² = {p * a * a}", f"x² = {a * a}",
                     f"(x {MINUS} {a})(x + {a}) = 0"]
            blank, level, params = 2, "H", {"a": a, "p": p, "c": c}
            prompt = (f"Täydennä puuttuva rivi: {lines[0]}, □, {lines[2]}, {lines[3]}. "
                      f"Vähennä molemmilta puolilta luku {c}.")
            steps = [f"Vähennetään {c} molemmilta puolilta: {lines[1]}", f"Jaetaan luvulla {p}: {lines[2]}",
                     f"Tulon nollasääntö: x = {a} tai x = {MINUS}{a}"]
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        ref = lines[blank - 1]
        answer = {"kind": "equation", "reference": ref, "variable": "x", "solutions": [-a, a]}
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, prompt, payload, steps, ref,
                               GOOD, TEMPLATE, {**params, "blank": blank}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
