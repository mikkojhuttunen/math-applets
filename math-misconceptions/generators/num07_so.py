#!/usr/bin/env python3
"""NUM-07 (wrong base in reverse percentage), type SO (step ordering). Every line is an equation with the same
solution as line 1 (the original amount x); lines are listed in the correct order and shuffled by the app."""
import random
from decimal import Decimal

from gen_common import MINUS, base_item, cli
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num07_so"
TID, CODE = "NUM-07", "SO"
ASK = "Järjestä rivit oikeaan järjestykseen niin, että alkuperäinen määrä ratkeaa vaihe vaiheelta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(810)
    items, seen = [], set()
    for k in range(count):
        while True:
            orig = Decimal(rng.choice([40, 60, 80, 120, 160, 200, 240]))
            p = Decimal(rng.choice([10, 20, 25]))
            if k == 4:
                p = Decimal(50)
            if (orig, p) not in seen:
                break
        seen.add((orig, p))
        r = p / 100
        up = k in (0, 2, 4)
        new = orig * (1 + r) if up else orig * (1 - r)
        sign, f = ("+", 1 + r) if up else (MINUS, 1 - r)
        # the final numeric line is left out: a decimal line 1 and an integer last line compare unequal in verify.py
        lines = [f"x {sign} {fmt(r)}x = {fmt(new)}", f"{fmt(f)}x = {fmt(new)}", f"x = {fmt(new)} / {fmt(f)}"]
        if k >= 3:
            lines = lines[:2] + [f"{fmt(f)}x / {fmt(f)} = {fmt(new)} / {fmt(f)}"] + lines[2:]
        ctx = [
            f"Pelin hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. ",
            f"Takin hinta aleni {fmt(p)} % ja on nyt {fmt(new)} €. ",
            f"Bussilipun hinta nousi {fmt(p)} % ja on nyt {fmt(new)} €. ",
            f"Kengät maksavat {fmt(p)} %:n alennuksen jälkeen {fmt(new)} €. ",
            f"Vuokra nousi {fmt(p)} % ja on nyt {fmt(new)} €/kk. ",
        ][k]
        ask = ASK if k < 3 else ASK.replace("rivit", "rivit (alkuperäinen määrä x)")
        level = "T" if k < 3 else "H"
        expl = (f"Alkuperäinen määrä x on 100 %, joten uusi määrä on {fmt(f)}x. Jaetaan luvulla {fmt(f)}.")
        items.append(base_item(TID, CODE, start + k, ["S2.10"], ["T13"], 8, level, ctx + ask,
                               {"lines": lines, "accept": "exact"}, [expl, f"Alkuperäinen määrä on {fmt(orig)}"],
                               f"x = {fmt(new)} / {fmt(f)} = {fmt(orig)}",
                               "Oikein: perusarvo x on alkuperäinen määrä, ja uusi määrä on (1 ± prosentti) · x.",
                               TEMPLATE, {"orig": fmt(orig), "percent": fmt(p), "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
