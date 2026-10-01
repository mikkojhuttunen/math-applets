#!/usr/bin/env python3
"""NUM-05 (division always makes smaller), type NE. Answers come from Decimal/Fraction arithmetic;
the typical wrong answer is the smaller number the pupil expects (the product with the divisor)."""
import random
from decimal import Decimal
from fractions import Fraction

from gen_common import base_item, cli
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)


TEMPLATE = "num05_ne"
TID, CODE = "NUM-05", "NE"
BAD = ("Jakolasku ei aina pienennä. Kun jakaja on pienempi kuin 1, osamäärä on suurempi kuin jaettava "
       "(esimerkiksi 8 ÷ 0,5 = 16).")


def make_items(run, date, count=5, start=1):
    rng = random.Random(702)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n, f = rng.choice([8, 12, 15]), Decimal(rng.choice(["0.5", "0.25", "0.2"]))
            ans, wrong = n / f, [n * f]
            prompt = f"Laske {n} ÷ {fmt(f)}."
            steps = [f"Luvussa {n} on {fmt(ans)} kertaa {fmt(f)}", f"{n} ÷ {fmt(f)} = {fmt(ans)}"]
            params = {"n": n, "divisor": fmt(f)}
        elif k == 1:
            n, f = rng.choice([18, 24, 30]), Decimal(rng.choice(["0.6", "0.3", "0.5"]))
            q = n / f
            prompt = f"Kirjoita suurempi luvuista {n} ja {n} ÷ {fmt(f)}."
            ans, wrong = q, [Decimal(n)]
            steps = [f"{n} ÷ {fmt(f)} = {fmt(q)}", f"{fmt(q)} > {n}"]
            params = {"n": n, "divisor": fmt(f)}
        elif k == 2:
            n, f = rng.choice([3, 5, 6]), Decimal(rng.choice(["0.25", "0.5", "0.2"]))
            ans, wrong = n / f, [n * f]
            prompt = f"Nauhaa on {n} metriä. Siitä leikataan {fmt(f)} metrin pituisia pätkiä. Montako pätkää saadaan?"
            steps = [f"{n} ÷ {fmt(f)} = {fmt(ans)}"]
            params = {"n": n, "piece": fmt(f)}
        elif k == 3:
            n = 12
            ds = [Decimal(x) for x in rng.sample(["0.5", "0.25", "2", "3", "0.4", "4"], 4)]
            ans = sum(1 for d in ds if n / d > n)
            if ans in (0, 4):
                ds = [Decimal(x) for x in ["0.5", "2", "0.25", "3"]]
                ans = 2
            prompt = f"Montako osamääristä {', '.join(str(n) + ' ÷ ' + fmt(d) for d in ds)} on suurempia kuin {n}? Kirjoita lukumäärä."
            wrong = [0]
            steps = [f"{n} ÷ {fmt(d)} = {fmt(n / d)} {'>' if n / d > n else '<'} {n}" for d in ds]
            params = {"divisors": [fmt(d) for d in ds], "n": n}
        else:
            n = rng.choice([6, 8, 9])
            fs = rng.sample([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 2), Fraction(3, 1)], 4)
            ans = sum(1 for f in fs if n / f > n)
            prompt = (f"Montako osamääristä {', '.join(str(n) + ' ÷ ' + str(f.numerator) + '/' + str(f.denominator) if f.denominator != 1 else str(n) + ' ÷ ' + str(f.numerator) for f in fs)} "
                      f"on suurempia kuin {n}? Kirjoita lukumäärä.")
            assert 0 < ans < 4
            wrong = [0]
            steps = [f"{n} ÷ {f} = {n / f} {'>' if n / f > n else '<'} {n}" for f in fs]
            params = {"divisors": [str(f) for f in fs], "n": n}
        assert all(Decimal(str(w)) != Decimal(str(ans)) for w in wrong)
        key = str(params)
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "NUM-05", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        final = fmt(ans) if isinstance(ans, Decimal) else str(ans)
        items.append(base_item(TID, CODE, start + k, ["S2.03", "S2.06"], ["T11"], 7, "T" if k < 3 else "H", prompt,
                               payload, steps, final, "Oikein: jakaja alle 1 suurentaa osamäärää.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
