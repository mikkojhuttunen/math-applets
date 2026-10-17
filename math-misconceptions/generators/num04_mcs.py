#!/usr/bin/env python3
"""NUM-04 (multiplication always makes bigger), type MC select-all (a reverse problem). The pupil ticks every
equation whose solution is the result of multiplying by a number below 1. Correct equations multiply by that number
(written as an exact fraction, which the prompt names); wrong ones divide by it instead, as a pupil does who thinks a
smaller result cannot come from multiplying, or add it, or multiply by a number above 1. verify.py checks the
solution sets."""
import random
from decimal import Decimal
from fractions import Fraction

from gen_common import base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "num04_mcs"
TID, CODE = "NUM-04", "MC"


def c(x):
    """Decimal comma display text."""
    return str(x).replace(".", ",")


def d(x):
    """Decimal with a decimal comma; the checker reads it as an exact fraction."""
    f = Fraction(str(x))
    return str(Decimal(f.numerator) / Decimal(f.denominator)).replace(".", ",")



def make_items(run, date, count=5, start=1):
    rng = random.Random(613)
    items, seen = [], set()
    for k in range(count):
        while True:
            p = rng.choice([0.5, 0.25, 0.2, 0.1, 0.75])
            q = rng.choice([8, 12, 16, 20, 24, 40])
            if (p, q) not in seen and (Fraction(str(p)) * q).denominator == 1:
                break
        seen.add((p, q))
        v = int(Fraction(str(p)) * q)
        if k == 0:
            level = "T"
            prompt = (f"Luku {q} kerrotaan luvulla {c(p)}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on tulo x = {v}.")
            valid = [f"x = {q} * {d(p)}", f"{d(p)} * {q} = x"]
            invalid = [(f"x = {q} / {d(p)}", TID), (f"x = {q} + {d(p)}", None), (f"x = {q} * {d(1 + p)}", None)]
            steps = [f"{c(p)} × {q} = {v}", f"x = {q} × {c(p)}"]
            value = v
        elif k == 1:
            level = "T"
            n = rng.choice([2, 4, 5])
            v = q // n if q % n == 0 else None
            if v is None:
                q = n * 6
                v = 6
            prompt = f"Luku {q} kerrotaan murtoluvulla 1/{n}. Valitse kaikki yhtälöt, joiden ratkaisu on tulo x = {v}."
            valid = [f"x = {q} * 1/{n}", f"x = {q} / {n}"]
            invalid = [(f"x = {q} * {n}", TID), (f"x = {q} + 1/{n}", None), (f"x = {q}", None)]
            steps = [f"{q} × 1/{n} = {v}", f"x = {q} × 1/{n}"]
            value = v
        elif k == 2:
            level = "T"
            prompt = (f"Kilo omenoita maksaa {q} €. Ostat {c(p)} kiloa, ja maksettava hinta on x euroa. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on oikea hinta x = {v}.")
            valid = [f"x = {q} * {d(p)}", f"x = {d(p)} * {q}"]
            invalid = [(f"x = {q} / {d(p)}", TID), (f"x = {q}", None), (f"x = {q} + {d(p)}", None),
                       (f"x = {q} * {d(1 + p)}", None)]
            steps = [f"Hinta = kilohinta × määrä = {q} × {c(p)}", f"x = {v}"]
            value = v
        elif k == 3:
            level = "H"
            value = Fraction(str(p)) * Fraction(str(p)) * q
            value = float(value)
            prompt = (f"Luku {q} kerrotaan ensin luvulla {c(p)} ja saatu tulos kerrotaan vielä luvulla {c(p)}. "
                      f"Lopputulos on x. Valitse kaikki yhtälöt, joiden ratkaisu on x = {c(value)}.")
            valid = [f"x = {q} * {d(p)} * {d(p)}", f"x = ({q} * {d(p)}) * {d(p)}"]
            invalid = [(f"x = {q} / {d(p)} / {d(p)}", TID), (f"x = {q} * {d(p)}", None),
                       (f"x = {q} + {d(p)} + {d(p)}", None), (f"x = {q}", None)]
            mid = q * p if q * p != int(q * p) else int(q * p)
            steps = [f"{q} × {c(p)} = {c(mid)}", f"{c(mid)} × {c(p)} = {c(value)}", f"x = {q} × {c(p)} × {c(p)}"]
        else:
            level = "H"
            prompt = (f"Kun tuntematon luku x kerrotaan luvulla {c(p)}, tulos on {v}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {q}.")
            valid = [f"{d(p)} * x = {v}", f"x = {v} / {d(p)}"]
            invalid = [(f"x = {v} * {d(p)}", TID), (f"{d(p)} * x = {q}", None), (f"x = {v}", None)]
            steps = [f"Tulo on pienempi kuin x, joten x on suurempi kuin {v}", f"{c(p)} × x = {v}", f"x = {v} / {c(p)} = {q}"]
            value = q
        if isinstance(value, float) and value == int(value):
            value = int(value)
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", value, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S2.03"], ["T11"], 7, level, prompt, payload, steps,
                               "; ".join(pretty(e) for e in valid),
                               "Kun kerrotaan luvulla, joka on pienempi kuin 1, tulos on pienempi kuin alkuperäinen luku.",
                               TEMPLATE, {"p": p, "q": q, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
