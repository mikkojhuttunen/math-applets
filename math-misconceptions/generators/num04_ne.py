#!/usr/bin/env python3
"""NUM-04 (multiplication always makes bigger), type NE. Answers come from Decimal/Fraction comparisons."""
import random
from decimal import Decimal
from fractions import Fraction

from gen_common import base_item, cli
from gen_decimal import fmt as _fmt


def fmt(d):
    return _fmt(d.normalize() if isinstance(d, Decimal) and d != 0 else d)

TEMPLATE = "num04_ne"
TID, CODE = "NUM-04", "NE"
BAD = ("Kertolasku ei aina suurenna. Kun kerroin on pienempi kuin 1, tulo on pienempi kuin toinen tekijä "
       "(esimerkiksi 0,5 × 8 = 4).")


def make_items(run, date, count=5, start=1):
    rng = random.Random(602)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n = rng.choice([8, 12, 15])
            f = Decimal(rng.choice(["0.5", "0.25", "0.4"]))
            p = f * n
            prompt = f"Kumpi on suurempi, {n} vai {fmt(f)} × {n}? Kirjoita suurempi luku."
            ans, wrong = Decimal(n), [p]
            steps = [f"{fmt(f)} × {n} = {fmt(p)}", f"{n} > {fmt(p)}"]
            params = {"factor": fmt(f), "n": n}
        elif k == 1:
            n = rng.choice([15, 20, 35])
            f = Decimal(rng.choice(["0.6", "0.8", "0.9"]))
            p = f * n
            prompt = f"Kirjoita pienempi luvuista {n} ja {fmt(f)} × {n}."
            ans, wrong = p, [Decimal(n)]
            steps = [f"{fmt(f)} × {n} = {fmt(p)}", f"{fmt(p)} < {n}"]
            params = {"factor": fmt(f), "n": n}
        elif k == 2:
            n = rng.choice([12, 18, 24])
            fs = [Decimal(x) for x in ["0.5", "1.5", "2"]]
            prompt = (f"Lasketaan tulot {', '.join(fmt(f) + ' × ' + str(n) for f in fs)}. "
                      f"Mikä tulo on pienin? Kirjoita sen arvo.")
            ans, wrong = min(f * n for f in fs), [Decimal(n)]
            steps = [f"{fmt(f)} × {n} = {fmt(f * n)}" for f in fs] + [f"Pienin on {fmt(ans)}"]
            params = {"factors": [fmt(f) for f in fs], "n": n}
        elif k == 3:
            n = 30
            fs = [Decimal(x) for x in rng.sample(["0.4", "0.9", "1.2", "2", "0.75", "1.5"], 4)]
            ans = sum(1 for f in fs if f * n > n)
            if ans == 0 or ans == 4:
                fs = [Decimal(x) for x in ["0.4", "1.2", "0.9", "2"]]
                ans = 2
            prompt = (f"Montako tuloista {', '.join(fmt(f) + ' × ' + str(n) for f in fs)} on suurempia kuin {n}? Kirjoita lukumäärä.")
            wrong = [4]
            assert ans != 4
            steps = [f"{fmt(f)} × {n} = {fmt(f * n)} {'>' if f * n > n else '<'} {n}" for f in fs]
            params = {"factors": [fmt(f) for f in fs], "n": n}
        else:
            n = 24
            fs = rng.sample([Fraction(1, 4), Fraction(3, 2), Fraction(5, 6), Fraction(7, 4), Fraction(2, 3)], 4)
            ans = sum(1 for f in fs if f * n < n)
            prompt = (f"Montako luvuista {', '.join(f'{f.numerator}/{f.denominator} × {n}' for f in fs)} on pienempiä kuin {n}? Kirjoita lukumäärä.")
            wrong = [0]
            assert 0 < ans < 4 or ans == 4
            if ans == 0:
                raise SystemExit("bad sample")
            steps = [f"{f.numerator}/{f.denominator} × {n} = {f * n} {'<' if f * n < n else '>'} {n}" for f in fs]
            params = {"factors": [str(f) for f in fs], "n": n}
        assert all(Decimal(str(w)) != Decimal(str(ans)) for w in wrong)
        key = json_key = str(params)
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "NUM-04", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        final = fmt(ans) if isinstance(ans, Decimal) else str(ans)
        items.append(base_item(TID, CODE, start + k, ["S2.03", "S2.06"], ["T11"], 7, "T" if k < 3 else "H", prompt,
                               payload, steps, final, "Oikein: kerroin alle 1 pienentää tuloa.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
