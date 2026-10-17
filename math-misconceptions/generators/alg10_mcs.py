#!/usr/bin/env python3
"""ALG-10 (reversal error), type MC select-all (a reverse problem).
The pupil ticks every equation whose solution is the asked quantity. Correct equations model the comparison
(o = 7 · 12, o/7 = 12); wrong ones come from the same numbers, and the tagged ones reverse the comparison
(7o = 12, the classic students-and-professors error)."""
import random

from gen_common import base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "alg10_mcs"
TID, CODE = "ALG-10", "MC"
CTX = [
    ("oppilaita", "opettajia", "o", "t", "oppilaiden", "opettajien"),
    ("pelaajia", "valmentajia", "p", "v", "pelaajien", "valmentajien"),
    ("kirjoja", "lehtiä", "k", "l", "kirjojen", "lehtien"),
    ("kyyhkysiä", "harakoita", "k", "h", "kyyhkysten", "harakoiden"),
    ("kahvikuppeja", "teekuppeja", "k", "t", "kahvikuppien", "teekuppien"),
]


def make_items(run, date, count=5, start=1):
    rng = random.Random(302)
    items = []
    for k in range(count):
        many, few, m, f, many_gen, few_gen = CTX[k]
        n = rng.randint(3, 9)
        q = rng.randint(4, 15)  # quantity of the smaller group (or bigger for the reverse form)
        if k < 3:
            level, ops, tt = "T", ["S1.04"], ["T14", "T7"]
            value = n * q
            prompt = (f"Koululla on {n} kertaa enemmän {many} kuin {few}. {few.capitalize()} on {q}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on {many_gen} lukumäärä {m}.")
            valid = [f"{m} = {n} * {q}", f"{m}/{n} = {q}"]
            invalid = [(f"{n}{m} = {q}", TID), (f"{m} = {q}/{n}", TID), (f"{m} = {q} + {n}", None)]
            steps = [f"{m} on {n} kertaa {few_gen} määrä", f"{m} = {n} · {q}", f"{m} = {value}"]
        elif k == 3:
            level, ops, tt = "H", ["S1.04"], ["T14", "T4"]
            value = q
            big = n * q
            prompt = (f"{many.capitalize()} on {big}, ja se on {n} kertaa enemmän kuin {few}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on {few_gen} lukumäärä {f}.")
            valid = [f"{n}{f} = {big}", f"{f} = {big}/{n}"]
            invalid = [(f"{f} = {n} * {big}", TID), (f"{f}/{n} = {big}", TID), (f"{f} + {n} = {big}", None)]
            steps = [f"{many.capitalize()} on {n} · {f}", f"{n}{f} = {big}", f"{f} = {big} / {n} = {value}"]
        else:
            level, ops, tt = "K", ["S1.04", "S3.05"], ["T14", "T4"]
            c, d = rng.randint(2, 4), rng.randint(2, 9)
            value = c * q + d
            prompt = (f"{many.capitalize()} on {d} enemmän kuin {c}-kertainen määrä {few}. {few.capitalize()} on {q}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on {many_gen} lukumäärä {m}.")
            valid = [f"{m} = {c} * {q} + {d}", f"{m} - {d} = {c} * {q}"]
            invalid = [(f"{c}{m} + {d} = {q}", TID), (f"{m} = {c} * ({q} + {d})", None), (f"{m} = {c} * {q} - {d}", None)]
            steps = [f"Kerrotaan ensin: {c} · {q} = {c * q}", f"Lisätään {d}: {m} = {c * q} + {d}", f"{m} = {value}"]
        payload = select_all(f"{TEMPLATE}-{start + k}", m if k != 3 else f, value, valid, invalid)
        final = "; ".join(pretty(e) for e in valid)
        items.append(base_item(TID, CODE, start + k, ops, tt, 7 if k < 3 else 8, level, prompt, payload,
                               steps, final, "Yhtälön ratkaisu on pyydetty luku.", TEMPLATE,
                               {"n": n, "q": q, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
