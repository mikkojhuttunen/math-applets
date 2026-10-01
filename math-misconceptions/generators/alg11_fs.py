#!/usr/bin/env python3
"""ALG-11 (minus sign not distributed), type FS (fill in the missing step). Every line is equivalent to line 1
(checked by verify.py); the blanked line is accepted by equivalence to the reference expression."""
import random

from gen_common import MINUS, base_item, cli, lin, num

TEMPLATE = "alg11_fs"
TID, CODE = "ALG-11", "FS"
SAMPLES = [[1], [2], [3]]
GENERIC = ("Tarkista rivi sijoittamalla x = 1: onko uuden rivin arvo sama kuin edellisen? "
           "Sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1106)
    items = []
    for k in range(count):
        a, b, c, e = rng.randint(3, 7), rng.randint(2, 6), rng.randint(8, 15), rng.randint(2, 4)
        ctx = ""
        if k == 0:
            level = "T"
            lines = [f"{c} {MINUS} (x + {b})", f"{c} {MINUS} x {MINUS} {b}", lin(-1, c - b)]
            blank, how = 2, "Avaa sulku."
        elif k == 1:
            level = "T"
            lines = [f"{c} {MINUS} ({a}x {MINUS} {b})", f"{c} {MINUS} {a}x + {b}", lin(-a, c + b)]
            blank, how = 2, "Avaa sulku."
        elif k == 2:
            level = "T"
            a = rng.randint(a + 1, 9)
            lines = [f"({a}x + {c}) {MINUS} ({e}x + {b})", f"{a}x + {c} {MINUS} {e}x {MINUS} {b}", lin(a - e, c - b)]
            blank, how = 2, "Avaa jälkimmäinen sulku."
        elif k == 3:
            level = "H"
            lines = [f"{MINUS}({a}x {MINUS} {b}) {MINUS} (x + {c})", f"{MINUS}{a}x + {b} {MINUS} x {MINUS} {c}",
                     lin(-(a + 1), b - c)]
            blank, how = 3, "Kirjoita sievennetty lauseke."
        else:
            level = "H"
            ctx = (f"Tilillä on {c} euroa. Siitä vähennetään lasku, jonka suuruus on x {MINUS} {b} euroa. "
                   f"Jäljelle jäävä rahamäärä sievennetään rivi riviltä. ")
            lines = [f"{c} {MINUS} (x {MINUS} {b})", f"{c} {MINUS} x + {b}", f"{c + b} {MINUS} x"]
            blank, how = 2, "Avaa sulku."
        shown = [lines[i] if i != blank - 1 else "□" for i in range(len(lines))]
        prompt = f"{ctx}Täydennä puuttuva rivi: {', '.join(shown)}. {how}"
        ref = lines[blank - 1]
        payload = {"lines": lines, "blank_index": blank,
                   "answer": {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}}
        items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, prompt, payload,
                               [f"Rivi {blank}: {ref}", f"Lopputulos: {lines[-1]}"], ref,
                               "Oikein: sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "e": e}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
