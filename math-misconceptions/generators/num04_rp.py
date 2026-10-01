#!/usr/bin/env python3
"""NUM-04 (multiplication always makes bigger), type RP. Valid and invalid equations are built from the same numbers; verify.py checks their solution sets."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "num04_rp"
TID, CODE = "NUM-04", "RP"


def c(x):
    """Decimal comma display text."""
    return str(x).replace(".", ",")


def d(x):
    """Exact fraction text, so the checker compares rationals (no floats)."""
    f = Fraction(str(x))
    return f"({f.numerator}/{f.denominator})"


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
            prompt = f"Luku {q} kerrotaan luvulla {c(p)}. Kirjoita yhtälö, jonka ratkaisu on x = {v}."
            valid = [f"x = {q} * {d(p)}", f"{d(p)} * {q} = x"]
            invalid = [f"x = {q} / {d(p)}", f"x = {q} + {d(p)}", f"x = {q} * {d(1 + p)}"]
            steps = [f"{c(p)} × {q} = {v}", f"x = {q} × {c(p)}"]
            value = v
        elif k == 1:
            level = "T"
            n = rng.choice([2, 4, 5])
            v = q // n if q % n == 0 else None
            if v is None:
                q = n * 6
                v = 6
            prompt = f"Luku {q} kerrotaan murtoluvulla 1/{n}. Kirjoita yhtälö, jonka ratkaisu on x = {v}."
            valid = [f"x = {q} * 1/{n}", f"x = {q} / {n}"]
            invalid = [f"x = {q} * {n}", f"x = {q} + 1/{n}", f"x = {q}"]
            steps = [f"{q} × 1/{n} = {v}", f"x = {q} × 1/{n}"]
            value = v
        elif k == 2:
            level = "T"
            prompt = (f"Kilo omenoita maksaa {q} €. Ostat {c(p)} kiloa. Kirjoita yhtälö, jossa x on maksettava hinta euroina "
                      f"ja jonka ratkaisu on x = {v}.")
            valid = [f"x = {q} * {d(p)}", f"x = {d(p)} * {q}"]
            invalid = [f"x = {q}", f"x = {q} + {d(p)}", f"x = {q} * {d(1 + p)}"]
            steps = [f"Hinta = kilohinta × määrä = {q} × {c(p)}", f"x = {v}"]
            value = v
        elif k == 3:
            level = "H"
            prompt = (f"Luku {q} kerrotaan ensin luvulla {c(p)} ja saatu tulos kerrotaan vielä luvulla {c(p)}. "
                      f"Kirjoita yhtälö, jonka ratkaisu on x, kun x on lopputulos.")
            value = Fraction(str(p)) * Fraction(str(p)) * q
            value = float(value)
            valid = [f"x = {q} * {d(p)} * {d(p)}", f"x = ({q} * {d(p)}) * {d(p)}"]
            invalid = [f"x = {q} * {d(p)}", f"x = {q} + {d(p)} + {d(p)}", f"x = {q}"]
            steps = [f"{q} × {c(p)} = {c(q * p)}", f"{c(q * p)} × {c(p)} = {c(value)}", f"x = {q} × {c(p)} × {c(p)}"]
        else:
            level = "H"
            prompt = (f"Kun tuntematon luku x kerrotaan luvulla {c(p)}, tulos on {v}. "
                      f"Kirjoita yhtälö, jonka ratkaisu on x = {q}.")
            valid = [f"{d(p)} * x = {v}", f"x = {v} / {d(p)}"]
            invalid = [f"{d(p)} * x = {q}", f"x = {v} * {d(p)}", f"x = {v}"]
            steps = [f"Tulo on pienempi kuin x, joten x on suurempi kuin {v}", f"{c(p)} × x = {v}", f"x = {v} / {c(p)} = {q}"]
            value = q
        if isinstance(value, float) and value == int(value):
            value = int(value)
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S2.03"], ["T11"], 7, level, prompt, payload, steps,
                               f"x = {c(value)}",
                               "Oikein: kun kerrotaan luvulla, joka on pienempi kuin 1, tulos on pienempi kuin alkuperäinen luku.",
                               TEMPLATE, {"p": p, "q": q, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
