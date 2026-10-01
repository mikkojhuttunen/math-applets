#!/usr/bin/env python3
"""NUM-03 (whole-number bias in fraction addition), type ME. Equivalence flags are computed with Fraction from the same numbers."""
import random
from fractions import Fraction
from math import lcm

from gen_common import base_item, cli

TEMPLATE = "num03_me"
TID, CODE = "NUM-03", "ME"


def fr(a, b):
    return f"{a}/{b}"


def pick(rng, unlike=True):
    while True:
        b, d = rng.sample([2, 3, 4, 5, 6, 8, 9], 2)
        if unlike and (b % d == 0 or d % b == 0):
            continue
        a, c = rng.randint(1, b - 1), rng.randint(1, d - 1)
        s = Fraction(a, b) + Fraction(c, d)
        if s < 1 and Fraction(a + c, b + d) != s and Fraction(a * c, b * d) != s:
            return a, b, c, d


def make_items(run, date, count=5, start=1):
    rng = random.Random(503)
    items = []
    for n in range(count):
        a, b, c, d = pick(rng)
        L = lcm(b, d)
        x, y = a * (L // b), c * (L // d)
        s = Fraction(a, b) + Fraction(c, d)
        ref = f"{fr(a, b)} + {fr(c, d)}"
        eq = [f"{fr(x, L)} + {fr(y, L)}", f"{fr(x + y, L)}", f"{fr(c, d)} + {fr(a, b)}"]
        if n >= 3:
            eq[2] = f"1 - {fr(L - x - y, L)}"
        bad = [(f"{fr(a + c, b + d)}", TID), (f"{fr(a + c, L)}", None), (f"{fr(a * c, b * d)}", None)]
        if n == 4:
            bad.append((f"({a} + {c})/({b} + {d})", TID))
            bad[0] = (f"{fr(a + c, b * d)}", None)
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        opts = [o for i, o in enumerate(opts) if o[0] not in [p[0] for p in opts[:i]]]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m} for i, (t, e, m) in enumerate(opts)]
        level = "T" if n < 3 else "H"
        if n == 0:
            prompt = f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref}."
        elif n == 3:
            prompt = (f"Pullossa on {fr(a, b)} l mehua ja toisessa pullossa {fr(c, d)} l mehua. "
                      "Valitse kaikki lausekkeet, joiden arvo on mehun yhteismäärä litroina.")
        else:
            prompt = f"Valitse kaikki lausekkeet, joiden arvo on {fr(s.numerator, s.denominator)}, kun lasket {ref}."
        if n == 1:
            prompt = f"Mitkä seuraavista ovat yhtä suuria kuin {ref}? Valitse kaikki oikeat."
        steps = [f"{ref} = {fr(x, L)} + {fr(y, L)}", f"= {fr(x + y, L)}"]
        payload = {"reference": ref, "variables": ["x"], "samples": [[1], [2], [3]], "options": options}
        it = base_item(TID, CODE, start + n, ["S2.02"], ["T11"], 7, level, prompt, payload, steps, f"{fr(x + y, L)}",
                       "Oikein: lausekkeet ovat yhtä suuria, kun ne sieventyvät samaan arvoon samannimisillä murtoluvuilla.",
                       TEMPLATE, {"a": a, "b": b, "c": c, "d": d, "common": L}, date, run,
                       generic_wrong="Nimittäjiä ei lasketa yhteen. Muuta murtoluvut samannimisiksi ja laske vain osoittajat yhteen.")
        items.append(it)
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
