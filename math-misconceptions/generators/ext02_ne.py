#!/usr/bin/env python3
"""EXT-02 (integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2), type NE. Answers are computed with Fractions; the typical
wrong answers read the power as a product, a⁰ as 0 and a negative exponent as a negative number."""
import random
from fractions import Fraction

from gen_common import base_item, cli, num

TEMPLATE = "ext02_ne"
TID, CODE = "EXT-02", "NE"
BAD = ("Potenssi on toistettu kertolasku, a⁰ = 1 ja negatiivinen eksponentti tarkoittaa käänteislukua: "
       "a⁻ⁿ = 1/aⁿ.")


def c(x):
    """Decimal comma display text for a Fraction with a finite decimal expansion."""
    f = float(x)
    assert Fraction(str(f)) == x
    return num(str(f).rstrip("0").rstrip(".") if f == int(f) else str(f)).replace(".", ",")


SUP = {1: "¹", 2: "²", 3: "³"}


def make_items(run, date, count=5, start=1):
    rng = random.Random(1204)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, n = rng.choice([(2, 3), (3, 3), (5, 3), (4, 3), (2, 4)])
            ans, wrong = a ** n, [a * n]
            prompt = f"Laske {a}{'¹²³⁴'[n - 1]}."
            steps = [" · ".join([str(a)] * n) + f" = {a ** n}"]
            params = {"a": a, "n": n}
        elif k == 1:
            a, b = rng.choice([(7, 4), (5, 3), (9, 2), (6, 8)])
            ans, wrong = 1 + b, [b]
            prompt = f"Laske {a}⁰ + {b}."
            steps = [f"{a}⁰ = 1", f"1 + {b} = {ans}"]
            params = {"a": a, "b": b}
        elif k == 2:
            a, n = rng.choice([(2, 1), (2, 2), (5, 1), (10, 1), (5, 2), (10, 2)])
            val = Fraction(1, a ** n)
            ans, wrong = val, [-(a ** n)]
            prompt = f"Laske {a}⁻{SUP[n]} desimaalilukuna."
            steps = [f"{a}⁻{SUP[n]} = 1/{a}{SUP[n]} = 1/{a ** n}", f"= {c(val)}"]
            params = {"a": a, "n": n}
        elif k == 3:
            a, b, m = rng.choice([(3, 2, 3), (5, 2, 2), (4, 2, 2)])
            ans = 1 + Fraction(1, b) + m ** 3 if False else 1 + Fraction(1, b) + a ** m
            wrong = [0 + (-b) + a ** m, 1 + (-b) + a ** m, 0 + Fraction(1, b) + a ** m]
            prompt = f"Laske {a}⁰ + {b}⁻¹ + {a}{SUP[m]}."
            steps = [f"{a}⁰ = 1", f"{b}⁻¹ = 1/{b} = {c(Fraction(1, b))}", f"{a}{SUP[m]} = {a ** m}", f"summa = {c(ans)}"]
            params = {"a": a, "b": b, "m": m}
        else:
            a, m, n = rng.choice([(2, 3, 2), (3, 2, 1), (5, 2, 1), (2, 4, 2)])
            ans = Fraction(a) ** (m - n)
            wrong = [-(a ** m) * (a ** n)]
            prompt = f"Laske {a}{'¹²³⁴'[m - 1]} · {a}⁻{SUP[n]}."
            steps = [f"{a}{SUP.get(m, '⁴')} = {a ** m}", f"{a}⁻{SUP[n]} = 1/{a ** n}", f"{a ** m} · 1/{a ** n} = {c(ans)}"]
            params = {"a": a, "m": m, "n": n}
        ans, wrong = Fraction(ans), [Fraction(w) for w in wrong]
        assert all(w != ans for w in wrong)
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "EXT-02", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S2.11"], ["T10", "T11"], 8, "T" if k < 3 else "H", prompt,
                               payload, steps, c(ans), "Oikein: potenssi on toistettu kertolasku, a⁰ = 1 ja a⁻ⁿ = 1/aⁿ.",
                               TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
