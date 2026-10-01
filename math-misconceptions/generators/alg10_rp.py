#!/usr/bin/env python3
"""ALG-10 (reversal error), type RP (reverse problem: write an equation with a given solution).
Valid and invalid example equations are computed so that their solution sets are checked by verify.py."""
import random

from gen_common import base_item, cli

TEMPLATE = "alg10_rp"
TID, CODE = "ALG-10", "RP"
CTX = [
    ("oppilaita", "opettajia", "o", "t"),
    ("pelaajia", "valmentajia", "p", "v"),
    ("kirjoja", "lehtiä", "k", "l"),
    ("kyyhkysiä", "harakoita", "k", "h"),
    ("kahvikuppeja", "teekuppeja", "k", "t"),
]


def make_items(run, date, count=5, start=1):
    rng = random.Random(302)
    items = []
    for k in range(count):
        many, few, m, f = CTX[k]
        n = rng.randint(3, 9)
        q = rng.randint(4, 15)  # quantity of the smaller group (or bigger for the reverse form)
        if k < 3:
            level, ops, tt = "T", ["S1.04"], ["T14", "T7"]
            value = n * q
            prompt = (f"Koululla on {n} kertaa enemmän {many} kuin {few}. {few.capitalize()} on {q}. "
                      f"Kirjoita yhtälö, jonka ratkaisu on {many} lukumäärä {m}.")
            valid = [f"{m} = {n} * {q}", f"{m}/{n} = {q}"]
            invalid = [f"{n}{m} = {q}", f"{m} = {q}/{n}", f"{m} = {q} + {n}"]
            steps = [f"{m} on {n} kertaa {few}n määrä", f"{m} = {n} · {q}", f"{m} = {value}"]
        elif k == 3:
            level, ops, tt = "H", ["S1.04"], ["T14", "T4"]
            value = q
            big = n * q
            prompt = (f"{many.capitalize()} on {big}, ja se on {n} kertaa enemmän kuin {few}. "
                      f"Kirjoita yhtälö, jonka ratkaisu on {few} lukumäärä {f}.")
            valid = [f"{n}{f} = {big}", f"{f} = {big}/{n}"]
            invalid = [f"{f} = {n} * {big}", f"{n}{big} = {f}", f"{f} + {n} = {big}"]
            steps = [f"{many.capitalize()} on {n} · {f}", f"{n}{f} = {big}", f"{f} = {big} / {n} = {value}"]
        else:
            level, ops, tt = "K", ["S1.04", "S3.05"], ["T14", "T4"]
            c, d = rng.randint(2, 4), rng.randint(2, 9)
            value = c * q + d
            prompt = (f"{many.capitalize()} on {d} enemmän kuin {c}-kertainen määrä {few}. {few.capitalize()} on {q}. "
                      f"Kirjoita yhtälö, jonka ratkaisu on {many} lukumäärä {m}.")
            valid = [f"{m} = {c} * {q} + {d}", f"{m} - {d} = {c} * {q}"]
            invalid = [f"{c}{m} + {d} = {q}", f"{m} = {c} * ({q} + {d})", f"{m} = {c} * {q} - {d}"]
            steps = [f"Kerrotaan ensin: {c} · {q} = {c * q}", f"Lisätään {d}: {m} = {c * q} + {d}", f"{m} = {value}"]
        payload = {"constraint": {"type": "solution_equals", "variable": m if k != 3 else f, "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        final = f"{payload['constraint']['variable']} = {value}"
        items.append(base_item(TID, CODE, start + k, ops, tt, 7 if k < 3 else 8, level, prompt, payload,
                               steps, final, "Oikein: yhtälön ratkaisu on pyydetty luku.", TEMPLATE,
                               {"n": n, "q": q, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
