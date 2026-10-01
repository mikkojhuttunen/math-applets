#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type FS (fill in the missing step). Every line is equivalent
to line 1 (checked by verify.py); the blanked line is accepted by equivalence to the reference expression."""
import random

from gen_common import MINUS, base_item, cli, lin

TEMPLATE = "alg08_fs"
TID, CODE = "ALG-08", "FS"
SAMPLES = [[1], [2], [3]]
GENERIC = ("Tarkista rivi sijoittamalla x = 1: onko uuden rivin arvo sama kuin edellisen? "
           "Kerroin kertoo kaikki sulun sisällä olevat termit, ei vain ensimmäistä.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(8304)
    items = []
    for k in range(count):
        a, b, c, d = rng.randint(2, 7), rng.randint(2, 8), rng.randint(2, 6), rng.randint(2, 5)
        level, ctx = "T", ""
        if k == 0:
            lines = [f"{a}(x + {b}) + {c}x", f"{a}x + {a * b} + {c}x", lin(a + c, a * b)]
            blank, how = 2, "Avaa sulut."
        elif k == 1:
            lines = [f"{a}(x {MINUS} {b}) + {c}", f"{a}x {MINUS} {a * b} + {c}", lin(a, c - a * b)]
            blank, how = 2, "Avaa sulut."
        elif k == 2:
            c = rng.randint(d // a + 2, 7)
            lines = [f"{a}({b} + {c}x) {MINUS} {d}x", f"{a * b} + {a * c}x {MINUS} {d}x", lin(a * c - d, a * b)]
            blank, how = 2, "Avaa sulut."
        elif k == 3:
            level = "H"
            lines = [f"{a}(x + {b}) + {c}(x + {d})", f"{a}x + {a * b} + {c}x + {c * d}", lin(a + c, a * b + c * d)]
            blank, how = 3, "Kirjoita sievennetty lauseke."
        else:
            level = "H"
            ctx = (f"Kioski pakkaa {a} pussia. Jokaiseen pussiin tulee x grammaa lakritsia ja {b} grammaa suklaata, "
                   f"ja lisäksi {c} grammaa pakkausmateriaalia. Kokonaispaino lasketaan rivi riviltä. ")
            lines = [f"{a}(x + {b}) + {c}", f"{a}x + {a * b} + {c}", lin(a, a * b + c)]
            blank, how = 2, "Avaa sulut."
        shown = [lines[i] if i != blank - 1 else "□" for i in range(len(lines))]
        prompt = f"{ctx}Täydennä puuttuva rivi: {', '.join(shown)}. {how}"
        ref = lines[blank - 1]
        payload = {"lines": lines, "blank_index": blank,
                   "answer": {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload,
                               [f"Rivi {blank}: {ref}", f"Lopputulos: {lines[-1]}"], ref,
                               "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
