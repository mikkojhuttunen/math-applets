#!/usr/bin/env python3
"""NUM-07 (wrong base in reverse percentage), type ES. The lines are equations for the original amount x: lines before
the error line have the same solution as line 1 (checked by verify.py); the injected error takes the percentage of the
new (given) amount."""
import random
from decimal import Decimal

from gen_common import MINUS, base_item, cli
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num07_es"
TID, CODE = "NUM-07", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = ("Tarkista rivi kerrallaan: onko uuden rivin yhtälöllä sama ratkaisu kuin edellisellä? "
           "Prosentti lasketaan alkuperäisestä määrästä x, ei annetusta uudesta määrästä.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(809)
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
        l1 = f"x {sign} {fmt(r)}x = {fmt(new)}"
        l2 = f"{fmt(f)}x = {fmt(new)}"
        good = f"x = {fmt(new)} / {fmt(f)}"
        if k in (0, 1):
            # error at line 2: the percentage is taken of the new amount
            bad = f"x = {fmt(new)} {MINUS if up else '+'} {fmt(r)} · {fmt(new)}"
            wrong_val = new * (1 - r) if up else new * (1 + r)
            lines = [l1, bad, f"x = {fmt(wrong_val)}"]
            err, etype = 2, "percentage_of_new_amount"
            steps = [f"Rivi 2 on väärin: {fmt(r * 100)} % on laskettu uudesta määrästä {fmt(new)}", f"Oikein: {l2}, joten {good} = {fmt(orig)}"]
        elif k == 2:
            bad = f"x = {fmt(new)} · {fmt(1 - r)}"
            lines = [l1, l2, bad]
            err, etype = 3, "multiplies_new_amount_by_inverse_factor"
            steps = [f"Rivi 2 on oikein: {l2}", f"Rivi 3 on väärin: jaettava on {fmt(new)} ja jakaja {fmt(f)}, ei kertoimen {fmt(1 - r)} kertominen; {good} = {fmt(orig)}"]
        elif k == 3:
            bad = f"x = {fmt(new)} · {fmt(1 + r)}"
            lines = [l1, l2, bad]
            err, etype = 3, "multiplies_new_amount_by_inverse_factor"
            steps = [f"Rivi 2 on oikein: {l2}", f"Rivi 3 on väärin: jaetaan luvulla {fmt(f)}, {good} = {fmt(orig)}"]
        else:
            bad = f"x = {fmt(new)} {MINUS} {fmt(r)} · {fmt(new)}"
            lines = [l1, l2, bad, f"x = {fmt(new * (1 - r))}"]
            err, etype = 3, "percentage_of_new_amount"
            steps = [f"Rivi 2 on oikein: {l2}", f"Rivi 3 on väärin: {fmt(r * 100)} % on laskettu uudesta määrästä; oikein {good} = {fmt(orig)}"]
        ctxs = [
            f"Pelin hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. Oppilas laskee alkuperäisen hinnan x rivi riviltä. ",
            f"Takin hinta aleni {fmt(p)} % ja on nyt {fmt(new)} €. Oppilas laskee alkuperäisen hinnan x rivi riviltä. ",
            f"Bussilipun hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. Oppilas ratkaisee alkuperäisen hinnan x. ",
            f"Kengät maksavat {fmt(p)} %:n alennuksen jälkeen {fmt(new)} €. Oppilas ratkaisee alkuperäisen hinnan x. ",
            f"Vuokra nousi {fmt(p)} % ja on nyt {fmt(new)} €/kk. Oppilas laskee entisen vuokran x rivi riviltä. ",
        ]
        level = "T" if k < 3 else "H"
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, ctxs[k] + ASK, payload, steps,
                               f"Virhe on rivillä {err}",
                               "Oikein: perusarvo x on alkuperäinen määrä, ja uusi määrä on (1 ± prosentti) · x.",
                               TEMPLATE, {"orig": fmt(orig), "percent": fmt(p), "form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
