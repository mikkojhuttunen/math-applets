#!/usr/bin/env python3
"""NUM-07 (wrong base in reverse percentage), type FS (fill in the missing step). Every line is an equation for the
original amount x with the same solution (checked by verify.py); the blanked line is accepted by equivalence of
solution sets."""
import random
from decimal import Decimal

from gen_common import MINUS, base_item, cli
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num07_fs"
TID, CODE = "NUM-07", "FS"
GENERIC = ("Tarkista rivi sijoittamalla ratkaisu: onko uudella rivillä sama ratkaisu kuin edellisellä? "
           "Prosentti lasketaan alkuperäisestä määrästä x, joten uusi määrä on (1 ± prosentti) · x.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(8107)
    items, seen = [], set()
    for k in range(count):
        while True:
            orig = Decimal(rng.choice([40, 60, 80, 120, 160, 200, 240]))
            p = Decimal(rng.choice([10, 20, 25]))
            if k == 3:
                orig, p = Decimal(rng.choice([80, 120, 160, 240])), Decimal(25)
            if k == 4:
                p = Decimal(50)
            if (orig, p) not in seen:
                break
        seen.add((orig, p))
        r = p / 100
        up = k in (0, 2, 4)
        new = orig * (1 + r) if up else orig * (1 - r)
        sign, f = ("+", 1 + r) if up else (MINUS, 1 - r)
        # hundredths instead of decimals, so the checker compares exact rationals
        rh, fh = f"{fmt(p)}/100", f"{fmt(f * 100)}/100"
        l1 = f"x {sign} {rh} · x = {fmt(new)}"
        l2 = f"{fh} · x = {fmt(new)}"
        l3 = f"x = {fmt(orig)}"
        lines = [l1, l2, l3]
        level, ctx, how = "T", "", ""
        if k in (0, 1):
            blank, equiv = 2, []
            how = " Kirjoita rivi, jossa x:n termit on yhdistetty yhdeksi kertoimeksi."
            ctx = (f"Pelin hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. " if up else
                   f"Takin hinta aleni {fmt(p)} % ja on nyt {fmt(new)} €. ")
            ctx += "Alkuperäinen hinta x ratkaistaan rivi riviltä. "
            steps = [f"x {sign} {rh} · x = {fh} · x", f"Rivi 2: {l2}"]
            ref = l2
        elif k in (2, 3):
            blank = 3
            equiv = [f"x = {fmt(new)} / ({fh})"]
            how = " Jaa yhtälön molemmat puolet kertoimella ja kirjoita ratkaisu."
            ctx = ("Bussilipun hinta nousi " + f"{fmt(p)} % ja on nyt {fmt(new)} €. " if up else
                   f"Kengät maksavat {fmt(p)} %:n alennuksen jälkeen {fmt(new)} €. ")
            ctx += "Alkuperäinen hinta x ratkaistaan rivi riviltä. "
            steps = [f"Jaetaan molemmat puolet kertoimella {fh} = {fmt(f)}: x = {fmt(new)} / {fmt(f)} = {fmt(orig)}", f"Rivi 3: {l3}"]
            ref = l3
            if k == 3:
                level = "H"
        else:
            level, blank, equiv = "H", 2, []
            ctx = (f"Vuokra nousi {fmt(p)} % ja on nyt {fmt(new)} €/kk. Entinen vuokra x ratkaistaan rivi riviltä. ")
            how = " Kirjoita rivi, jossa x:n termit on yhdistetty yhdeksi kertoimeksi."
            steps = [f"x + {rh} · x = {fh} · x", f"Rivi 2: {l2}"]
            ref = l2
        shown = [lines[i] if i != blank - 1 else "□" for i in range(3)]
        prompt = f"{ctx}Täydennä puuttuva rivi: {', '.join(shown)}.{how}"
        answer = {"kind": "equation", "reference": ref, "variable": "x", "solutions": [float(orig)]}
        if equiv:
            answer["equivalents"] = equiv
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, prompt, payload, steps, ref,
                               "Oikein: perusarvo x on alkuperäinen määrä, ja uusi määrä on (1 ± prosentti) · x.",
                               TEMPLATE, {"orig": fmt(orig), "percent": fmt(p), "form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
