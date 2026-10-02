#!/usr/bin/env python3
"""Reference generator: LTRI-01 (trigonometric equation has one solution), type NE,
answer kind periodic.

Shows the pattern every lukio generator should follow:
  * fixed random seed, so the same call always gives the same items
  * the base solutions are COMPUTED with sympy (solveset over one period), never typed
  * the typical wrong answer ("only the calculator value") is computed from the
    misconception rule: the first base solution alone
  * items mix radians and degrees and levels T and H, and state level and tools
Prints the wrapper JSON; tests/run_tests.py checks that it verifies.
The routine writes its own generators; this one is a model, not a matrix cell.
"""
import random

import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "example_ltri01_ne"
TID, CODE = "LTRI-01", "NE"
X = sp.Symbol("x")
VALUES = [sp.Rational(1, 2), sp.sqrt(2) / 2, sp.sqrt(3) / 2]
GENERIC = "Yksikköympyrällä sama sinin tai kosinin arvo saadaan yleensä kahdessa kohdassa, ja ratkaisut toistuvat jakson välein."


def base_solutions(func, k, a, unit):
    """Sorted solutions of func(k x) = a in one period, in the item's unit."""
    period = 2 * sp.pi / k
    sols = sp.solveset(sp.Eq(func(k * X), a), X, sp.Interval.Ropen(0, period))
    sols = sorted(sols, key=float)
    if unit == "deg":
        return [sp.nsimplify(s * 180 / sp.pi) for s in sols], sp.nsimplify(period * 180 / sp.pi)
    return sols, period


def fmt(v, unit):
    return f"{show(v)}°" if unit == "deg" else show(v)


def make_items(run, date, count=5, start=1):
    rng = random.Random(5104)
    plan = [("sin", 1, 1, "rad", "T"), ("cos", 1, 1, "deg", "T"), ("sin", 1, -1, "rad", "H"),
            ("sin", 2, 1, "rad", "H"), ("cos", 1, -1, "deg", "H")]
    items = []
    for n, (fname, k, sign, unit, level) in enumerate(plan[:count]):
        func = {"sin": sp.sin, "cos": sp.cos}[fname]
        a = sign * rng.choice(VALUES)
        base, period = base_solutions(func, k, a, unit)
        arg = "x" if k == 1 else f"{k}x"
        eq_text = f"{fname} {arg} = {show(a)}"
        ref = f"{fname}({k}*x) = {a}"
        unit_text = "asteina" if unit == "deg" else "radiaaneina"
        branches = " tai ".join(f"x = {fmt(b, unit)} + n · {fmt(period, unit)}" for b in base)
        payload = {
            "answer": {"kind": "periodic", "variable": "x", "reference": ref, "unit": unit,
                       "base": [str(b) for b in base], "period": str(period)},
            "wrong": [{"match": str(base[0]), "misconception": TID,
                       "feedback": f"x = {fmt(base[0], unit)} on vain yksi ratkaisu. Etsi toinen kohta yksikköympyrältä ja lisää jakso."}],
            "input_hint": f"esim. x = {fmt(base[0], unit)} + n · {fmt(period, unit)}",
        }
        steps = [f"Välillä [0, {fmt(period, unit)}) yhtälön {eq_text} ratkaisut ovat {', '.join(fmt(b, unit) for b in base)}.",
                 f"Jakso on {fmt(period, unit)}."]
        items.append(base_item(TID, CODE, start + n, ["MAA5.04"], ["G4"], "MAA", level, "none",
                               f"Ratkaise yhtälö {eq_text}. Anna kaikki ratkaisut {unit_text}.", payload,
                               steps, f"{branches}, n ∈ ℤ",
                               "Oikein: kaikki ratkaisuhaarat ja jakso ovat mukana.",
                               TEMPLATE, {"func": fname, "k": k, "a": str(a), "unit": unit}, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
