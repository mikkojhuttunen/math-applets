#!/usr/bin/env python3
"""NUM-03 (whole-number bias in fraction addition), type FS. The blanked line is computed with Fraction; verify.py checks the chain for equivalence."""
import random
from fractions import Fraction
from math import lcm

from gen_common import base_item, cli

TEMPLATE = "num03_fs"
TID, CODE = "NUM-03", "FS"
SAMPLES = [[1], [2], [3]]


def make_items(run, date, count=5, start=1):
    rng = random.Random(612)
    items, seen = [], set()
    for k in range(count):
        level = "T" if k < 3 else "H"
        nfr = 3 if k == 3 else 2
        while True:
            ds = rng.sample([2, 3, 4, 5, 6, 8], nfr)
            ns = [rng.randint(1, d - 1) for d in ds]
            L = lcm(*ds)
            tot = sum(n * (L // d) for n, d in zip(ns, ds))
            if L <= 24 and tot != sum(ns) and Fraction(tot, L) < 2 and all(n * 2 <= d + 1 for n, d in zip(ns, ds)) \
                    and (tuple(ds), tuple(ns)) not in seen:
                break
        seen.add((tuple(ds), tuple(ns)))
        expr = " + ".join(f"{n}/{d}" for n, d in zip(ns, ds))
        common = " + ".join(f"{n * (L // d)}/{L}" for n, d in zip(ns, ds))
        total = f"{tot}/{L}"
        simple = Fraction(tot, L)
        lines = [expr, common, total]
        if simple.denominator != L:
            lines.append(f"{simple.numerator}/{simple.denominator}")
        blank = 4 if (k == 4 and len(lines) == 4) else (3 if k == 2 else 2)
        if k == 4 and len(lines) < 4:
            blank = 3
        ref = lines[blank - 1]
        if blank == 2:
            prompt = f"Täydennä puuttuva rivi. Kirjoita välivaihe, jossa murtoluvut on muutettu samannimisiksi: {expr} = □ = {total}"
        elif blank == 3:
            prompt = f"Täydennä puuttuva rivi. Laske samannimisten murtolukujen summa: {expr} = {common} = □"
        else:
            prompt = f"Täydennä puuttuva rivi. Sievennä summa: {expr} = {common} = {total} = □"
        if k == 1:
            prompt = (f"Kaksi sivua kirjasta luetaan: {ns[0]}/{ds[0]} ja {ns[1]}/{ds[1]} osaa kirjasta. Täydennä puuttuva rivi. "
                      f"Kirjoita välivaihe, jossa murtoluvut on muutettu samannimisiksi: {expr} = □ = {total}") if blank == 2 else prompt
        answer = {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}
        steps = [f"{expr} = {common}", f"{common} = {total}"] + ([f"{total} = {lines[3]}"] if len(lines) == 4 else [])
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S2.02"], ["T11"], 7, level, prompt, payload, steps, ref,
                               "Oikein: murtoluvut muutetaan samannimisiksi ja vain osoittajat lasketaan yhteen.",
                               TEMPLATE, {"denominators": ds, "numerators": ns, "common": L, "blank": blank}, date, run,
                               generic_wrong="Nimittäjiä ei lasketa yhteen. Muuta murtoluvut samannimisiksi ja laske vain osoittajat yhteen."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
