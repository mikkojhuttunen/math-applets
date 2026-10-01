#!/usr/bin/env python3
"""NUM-03 (whole-number bias in fraction addition), type ES. Correct lines use common denominators; the injected error adds numerators and denominators separately."""
import random
from fractions import Fraction
from math import lcm

from gen_common import base_item, cli

TEMPLATE = "num03_es"
TID, CODE = "NUM-03", "ES"


def frac(n, d):
    return f"{n}/{d}"


def pick(rng, k):
    while True:
        ds = rng.sample([2, 3, 4, 5, 6, 8], k)
        ns = [rng.randint(1, d - 1) for d in ds]
        L = lcm(*ds)
        tot = sum(n * (L // d) for n, d in zip(ns, ds))
        if L <= 24 and tot != sum(ns) and Fraction(tot, L) < 2 and all(n * 2 <= d + 1 for n, d in zip(ns, ds)):
            return ds, ns, L, tot


def make_items(run, date, count=5, start=1):
    rng = random.Random(611)
    items, seen = [], set()
    for k in range(count):
        level = "T" if k < 3 else "H"
        nfr = 3 if k == 3 else 2
        while True:
            ds, ns, L, tot = pick(rng, nfr)
            if (tuple(ds), tuple(ns)) not in seen:
                break
        seen.add((tuple(ds), tuple(ns)))
        expr = " + ".join(frac(n, d) for n, d in zip(ns, ds))
        common = " + ".join(frac(n * (L // d), L) for n, d in zip(ns, ds))
        sum_ok = frac(tot, L)
        if k in (0, 4):
            # error at line 2: numerators and denominators added separately
            wrong = frac(sum(ns), sum(ds))
            lines = [expr, wrong, frac(2 * sum(ns), 2 * sum(ds))]
            err, etype = 2, "adds_numerators_and_denominators"
            steps = [f"Rivi 2 on väärin: {expr} ≠ {wrong}", f"Oikein: {common} = {sum_ok}"]
        else:
            # error at line 3: correct common denominators, then the denominators are added
            wrong = frac(tot, L * nfr)
            lines = [expr, common, wrong]
            err, etype = 3, "adds_denominators_after_common_form"
            steps = [f"Rivi 2 on oikein: {common}", f"Rivi 3 on väärin: nimittäjää ei lasketa yhteen, {common} = {sum_ok}"]
        if k == 2:
            prompt = (f"Oppilas laskee, kuinka paljon mehua on yhteensä, kun ämpäriin kaadetaan {ns[0]}/{ds[0]} l ja {ns[1]}/{ds[1]} l. "
                      "Missä rivissä on ensimmäinen virhe? Napauta riviä.")
        elif k == 4:
            prompt = (f"Oppilas kirjoittaa muistiin laskun {expr} ja ratkaisee sen. Jokainen rivi on yhtä suuri kuin edellinen, "
                      "paitsi virheellinen rivi. Missä rivissä on ensimmäinen virhe? Napauta riviä.")
        else:
            prompt = f"Oppilas laskee yhteen murtoluvut rivi riviltä. Missä rivissä on ensimmäinen virhe? Napauta riviä."
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        items.append(base_item(TID, CODE, start + k, ["S2.02"], ["T11"], 7, level, prompt, payload, steps,
                               f"Virhe on rivillä {err}",
                               "Oikein: murtolukuja yhteenlaskettaessa nimittäjää ei lasketa yhteen, vaan käytetään yhteistä nimittäjää.",
                               TEMPLATE, {"denominators": ds, "numerators": ns, "common": L}, date, run,
                               generic_wrong="Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Murtolukujen nimittäjiä ei lasketa yhteen."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
