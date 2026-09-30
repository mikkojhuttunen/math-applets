#!/usr/bin/env python3
"""NUM-06 (no number between 0,3 and 0,4), type RP: write an equation whose solution lies between two decimals.
Equations are listed with exact fractions; verify.py checks their solution sets with sympy."""
import random
from fractions import Fraction
from decimal import Decimal

from gen_common import base_item, cli
from gen_decimal import fmt

TEMPLATE = "num06_rp"
TID, CODE = "NUM-06", "RP"


def d(x):
    """Exact fraction text, so that sympy compares solution sets without float error."""
    f = Fraction(x)
    return f"({f.numerator}/{f.denominator})" if f.denominator != 1 else str(f.numerator)


def make_items(run, date, count=5, start=1):
    rng = random.Random(702)
    items, seen = [], set()
    for k in range(count):
        if k < 3:
            a = [Decimal("0.3"), Decimal(rng.randint(11, 59)) / 10, Decimal(rng.randint(1, 8)) / 100][k]
            b = a + (Decimal("0.01") if k == 2 else Decimal("0.1"))
            m = (a + b) / 2
            level = "T"
            prompt = (f"Luku x on täsmälleen lukujen {fmt(a)} ja {fmt(b)} puolivälissä. "
                      f"Kirjoita yhtälö, jonka ratkaisu on x.")
            valid = [f"x = ({d(a)} + {d(b)}) / 2", f"2 * x = {d(a)} + {d(b)}"]
            invalid = [f"x = {d(a)} + {d(b)}", f"x = {d(b)} - {d(a)}", f"x = {d(a)}"]
            steps = [f"Puoliväli on keskiarvo: x = ({fmt(a)} + {fmt(b)}) / 2", f"x = {fmt(m)}"]
        else:
            a = Decimal(rng.randint(1, 8)) / 10
            b = a + Decimal("0.1")
            q = 4 if k == 3 else 10
            m = a + (b - a) / q
            level = "H"
            word = "neljäsosan" if k == 3 else "kymmenesosan"
            prompt = (f"Luku x on {word} matkan päässä luvusta {fmt(a)} kohti lukua {fmt(b)}. "
                      f"Kirjoita yhtälö, jonka ratkaisu on x.")
            valid = [f"x = {d(a)} + ({d(b)} - {d(a)}) / {q}", f"{q} * x = {q} * {d(a)} + {d(b)} - {d(a)}"]
            invalid = [f"x = {d(a)} + {d(b)} / {q}", f"x = ({d(b)} - {d(a)}) / {q}", f"x = {d(b)} - {d(a)} / {q}"]
            steps = [f"Väli on {fmt(b)} − {fmt(a)} = {fmt(b - a)}", f"x = {fmt(a)} + {fmt(b - a)} / {q} = {fmt(m)}"]
        assert a < m < b
        key = (a, b, k)
        assert key not in seen
        seen.add(key)
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": float(m)},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S2.08"], ["T12"], 8, level, prompt, payload, steps,
                               f"x = {fmt(m)}", "Oikein: lukujen välissä on aina uusia lukuja, ja ne voi laskea.",
                               TEMPLATE, {"a": fmt(a), "b": fmt(b), "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
