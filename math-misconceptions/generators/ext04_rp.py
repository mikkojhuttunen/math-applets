#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type RP (write an equation with a given solution). The target is a single
solution, which a square-equation can have only as a double root, (x − a)² = 0. Invalid equations are built from
the same numbers and have two solutions (a and −a) or none; verify.py checks the solution sets."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "ext04_rp"
TID, CODE = "EXT-04", "RP"
GOOD = "Oikein: yhtälöllä, jonka ainoa ratkaisu on a, täytyy olla kaksoisjuuri, esimerkiksi (x − a)² = 0."
GENERIC = ("Sijoita x:n paikalle sekä pyydetty luku että sen vastaluku. Yhtälöllä x² = a² on aina kaksi ratkaisua, "
           "joten sen ratkaisu ei ole vain yksi luku.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1408)
    items, seen = [], set()
    for k in range(count):
        while True:
            a = rng.randint(2, 9)
            if a not in seen:
                break
        seen.add(a)
        s = a * a
        level, p = "T", 1
        if k == 0:
            value = a
            prompt = f"Kirjoita yhtälö, jonka ainoa ratkaisu on x = {a} ja jossa x on toiseen potenssiin."
            valid = [f"(x {MINUS} {a})² = 0", f"x² {MINUS} {2 * a}x + {s} = 0"]
            invalid = [f"x² = {s}", f"x² {MINUS} {s} = 0", f"x² = {a}"]
            steps = [f"Kaksoisjuuri: (x {MINUS} {a})² = 0", f"Vain x = {a}, koska x {MINUS} {a} = 0"]
        elif k == 1:
            value = -a
            prompt = f"Kirjoita yhtälö, jonka ainoa ratkaisu on x = {MINUS}{a} ja jossa x on toiseen potenssiin."
            valid = [f"(x + {a})² = 0", f"x² + {2 * a}x + {s} = 0"]
            invalid = [f"x² = {s}", f"x² {MINUS} {s} = 0", f"x² = {MINUS}{a}"]
            steps = [f"Kaksoisjuuri: (x + {a})² = 0", f"Vain x = {MINUS}{a}, koska x + {a} = 0"]
        elif k == 2:
            p = rng.choice([2, 3, 5])
            value = a
            prompt = f"Kirjoita yhtälö, jonka ainoa ratkaisu on x = {a} ja jossa on tekijä x {MINUS} {a} ja kerroin {p}."
            valid = [f"{p}(x {MINUS} {a})² = 0", f"{p}(x {MINUS} {a})(x {MINUS} {a}) = 0"]
            invalid = [f"{p}(x {MINUS} {a})(x + {a}) = 0", f"{p}x² = {p * s}", f"{p}(x {MINUS} {a}) = {s}"]
            steps = [f"Kerrotaan sama tekijä kahdesti: {p}(x {MINUS} {a})² = 0", f"Vain x = {a}"]
        elif k == 3:
            level = "H"
            value = a
            prompt = f"Täydennä yhtälö (x {MINUS} {a})² = □ siten, että sen ainoa ratkaisu on x = {a}. Kirjoita koko yhtälö."
            valid = [f"(x {MINUS} {a})² = 0", f"0 = (x {MINUS} {a})²"]
            invalid = [f"(x {MINUS} {a})² = 1", f"(x {MINUS} {a})² = {s}", f"(x {MINUS} {a})² = {a}"]
            steps = ["Neliö on nolla vain, kun luku itse on nolla", f"□ = 0, ja x {MINUS} {a} = 0 antaa x = {a}"]
        else:
            level = "H"
            p = rng.choice([2, 3, 4])
            value = a
            prompt = (f"Kirjoita yhtälö, jonka vasen puoli on {p} kertaa neliö (x {MINUS} {a})² ja jonka "
                      f"ainoa ratkaisu on x = {a}.")
            valid = [f"{p}(x {MINUS} {a})² = 0", f"{p}x² {MINUS} {2 * p * a}x + {p * s} = 0"]
            invalid = [f"{p}x² = {p * s}", f"{p}x² {MINUS} {p * s} = 0", f"{p}(x + {a})² = 0"]
            steps = [f"{p}(x {MINUS} {a})² = 0", f"x {MINUS} {a} = 0, joten x = {a}"]
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        final = f"x = {str(value).replace('-', MINUS)}"
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, prompt, payload, steps, final,
                               GOOD, TEMPLATE, {"a": a, "p": p}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
