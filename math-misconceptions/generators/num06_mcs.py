#!/usr/bin/env python3
"""NUM-06 (no number between 0,3 and 0,4), type MC select-all (a reverse problem).
The pupil ticks every equation whose solution is the number x that lies between two decimals (their midpoint, or a
quarter or tenth of the way from one to the other). Correct equations compute that point; wrong ones add the
decimals, take their difference, slip on the order of operations or put x on an endpoint, as if nothing lay
between. Decimals are written as exact tenths or hundredths so that sympy compares solution sets without float error."""
import random
from decimal import Decimal

from gen_common import base_item, cli
from gen_decimal import fmt
from gen_select import pretty, select_all

TEMPLATE = "num06_mcs"
TID, CODE = "NUM-06", "MC"


def tenths(x, places):
    """Decimal with `places` decimals and a decimal comma, e.g. 0,3 and 2,0."""
    return f"{x:.{places}f}".replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(702)
    items, seen = [], set()
    for k in range(count):
        if k < 3:
            a = [Decimal("0.3"), Decimal(rng.randint(11, 59)) / 10, Decimal(rng.randint(1, 8)) / 100][k]
            b = a + (Decimal("0.01") if k == 2 else Decimal("0.1"))
            m = (a + b) / 2
            level = "T"
            A, B = tenths(a, 2 if k == 2 else 1), tenths(b, 2 if k == 2 else 1)
            prompt = (f"Luku x on täsmälleen lukujen {fmt(a)} ja {fmt(b)} puolivälissä. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {fmt(m)}.")
            valid = [f"x = ({A} + {B}) / 2", f"2x = {A} + {B}"]
            invalid = [(f"x = {A} + {B}", None), (f"x = {B} - {A}", None), (f"x = {A}", TID)]
            steps = [f"Puoliväli on keskiarvo: x = ({fmt(a)} + {fmt(b)}) / 2", f"x = {fmt(m)}"]
        else:
            a = Decimal(rng.randint(1, 8)) / 10
            b = a + Decimal("0.1")
            q = 4 if k == 3 else 10
            m = a + (b - a) / q
            level = "H"
            A, B = tenths(a, 1), tenths(b, 1)
            word = "neljäsosan" if k == 3 else "kymmenesosan"
            prompt = (f"Luku x on {word} matkan päässä luvusta {fmt(a)} kohti lukua {fmt(b)}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {fmt(m)}.")
            valid = [f"x = {A} + ({B} - {A}) / {q}", f"{q}x = {q} * {A} + {B} - {A}"]
            invalid = [(f"x = {A} + {B} / {q}", None), (f"x = ({B} - {A}) / {q}", None),
                       (f"x = {B} - {A} / {q}", None), (f"x = {A}", TID)]
            steps = [f"Väli on {fmt(b)} − {fmt(a)} = {fmt(b - a)}", f"x = {fmt(a)} + {fmt(b - a)} / {q} = {fmt(m)}"]
        assert a < m < b
        key = (a, b, k)
        assert key not in seen
        seen.add(key)
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", float(m), valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S2.08"], ["T12"], 8, level, prompt, payload, steps,
                               "; ".join(pretty(v) for v in valid), "Lukujen välissä on aina uusia lukuja, ja ne voi laskea.",
                               TEMPLATE, {"a": fmt(a), "b": fmt(b), "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
