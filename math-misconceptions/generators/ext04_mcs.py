#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type MC select-all (a reverse problem). The pupil ticks every equation whose
only solution is the given number. A square equation has a single solution only as a double root, so the correct
equations are forms of (x − a)² = 0. The wrong equations are built from the same numbers and have two solutions
(a and −a, as x² = a² does), another pair of solutions, or none; verify.py checks the solution sets."""
import random

from gen_common import MINUS, base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "ext04_mcs"
TID, CODE = "EXT-04", "MC"
GOOD = "Yhtälöllä, jonka ainoa ratkaisu on a, täytyy olla kaksoisjuuri, esimerkiksi (x − a)² = 0."
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
            prompt = f"Valitse kaikki yhtälöt, joissa x on toiseen potenssiin ja joiden ainoa ratkaisu on x = {a}."
            valid = [f"(x {MINUS} {a})² = 0", f"x² {MINUS} {2 * a}x + {s} = 0"]
            invalid = [(f"x² = {s}", TID), (f"x² {MINUS} {s} = 0", TID), (f"x² = {a}", None)]
            steps = [f"Kaksoisjuuri: (x {MINUS} {a})² = 0", f"Vain x = {a}, koska x {MINUS} {a} = 0"]
        elif k == 1:
            value = -a
            prompt = f"Valitse kaikki yhtälöt, joissa x on toiseen potenssiin ja joiden ainoa ratkaisu on x = {MINUS}{a}."
            valid = [f"(x + {a})² = 0", f"x² + {2 * a}x + {s} = 0"]
            invalid = [(f"x² = {s}", TID), (f"x² {MINUS} {s} = 0", TID), (f"x² = {MINUS}{a}", None)]
            steps = [f"Kaksoisjuuri: (x + {a})² = 0", f"Vain x = {MINUS}{a}, koska x + {a} = 0"]
        elif k == 2:
            p = rng.choice([2, 3, 5])
            value = a
            prompt = f"Valitse kaikki yhtälöt, joiden ainoa ratkaisu on x = {a}."
            valid = [f"{p}(x {MINUS} {a})² = 0", f"{p}(x {MINUS} {a})(x {MINUS} {a}) = 0"]
            invalid = [(f"{p}(x {MINUS} {a})(x + {a}) = 0", TID), (f"{p}x² = {p * s}", TID),
                       (f"{p}(x {MINUS} {a}) = {s}", None)]
            steps = [f"Kerrotaan sama tekijä kahdesti: {p}(x {MINUS} {a})² = 0", f"Vain x = {a}"]
        elif k == 3:
            level = "H"
            value = a
            prompt = f"Valitse kaikki yhtälöt, joiden ainoa ratkaisu on x = {a}."
            valid = [f"(x {MINUS} {a})² = 0", f"0 = (x {MINUS} {a})²"]
            invalid = [(f"x² = {s}", TID), (f"(x {MINUS} {a})² = 1", None), (f"(x {MINUS} {a})² = {s}", None),
                       (f"(x {MINUS} {a})² = {a}", None)]
            steps = ["Neliö on nolla vain, kun luku itse on nolla",
                     f"Oikea puoli on 0, ja x {MINUS} {a} = 0 antaa x = {a}"]
        else:
            level = "H"
            p = rng.choice([2, 3, 4])
            value = a
            prompt = f"Valitse kaikki yhtälöt, joiden ainoa ratkaisu on x = {a}."
            valid = [f"{p}(x {MINUS} {a})² = 0", f"{p}x² {MINUS} {2 * p * a}x + {p * s} = 0"]
            invalid = [(f"{p}x² = {p * s}", TID), (f"{p}x² {MINUS} {p * s} = 0", TID), (f"{p}(x + {a})² = 0", None)]
            steps = [f"{p}(x {MINUS} {a})² = 0", f"x {MINUS} {a} = 0, joten x = {a}"]
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", value, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, prompt, payload, steps,
                               "; ".join(pretty(v) for v in valid), GOOD, TEMPLATE, {"a": a, "p": p}, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
