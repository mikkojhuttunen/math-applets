#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type NE (number entry). Answers computed from the same numbers."""
import random
from fractions import Fraction

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg07_ne"
TID, CODE = "ALG-07", "NE"
SIGN = "Siirrettäessä termi yhtälön toiselle puolelle sen merkki vaihtuu."
ONE = "Tee jokainen laskutoimitus yhtälön molemmille puolille, myös kaikille termeille."


def txt(v):
    v = Fraction(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(919)
    items = []
    for k in range(count):
        a, b, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
        if k == 0:
            level, c = "T", a * x + b
            prompt = f"Ratkaise yhtälö {a}x + {b} = {c}. Kirjoita x:n arvo."
            wrong = [(Fraction(c + b, a), SIGN), (c - b, ONE)]
            steps = [f"{a}x = {c} {MINUS} {b} = {c - b}", f"x = {c - b} / {a} = {x}"]
        elif k == 1:
            level, c = "T", a * x - b
            prompt = f"Ratkaise yhtälö {a}x {MINUS} {b} = {c}. Kirjoita x:n arvo."
            wrong = [(Fraction(c - b, a), SIGN), (c + b, ONE)]
            steps = [f"{a}x = {c} + {b} = {c + b}", f"x = {c + b} / {a} = {x}"]
        elif k == 2:
            level, c = "T", b + a * x
            prompt = f"Ratkaise yhtälö {b} + {a}x = {c}. Kirjoita x:n arvo."
            wrong = [(Fraction(c + b, a), SIGN), (c - b, ONE)]
            steps = [f"{a}x = {c} {MINUS} {b} = {c - b}", f"x = {c - b} / {a} = {x}"]
        elif k == 3:
            level = "H"
            a = max(a, 3)
            e = rng.randint(2, a - 1)
            d2 = (a - e) * x
            prompt = f"Ratkaise yhtälö {a}x = {e}x + {d2}. Kirjoita x:n arvo."
            wrong = [(Fraction(d2, a + e), SIGN), (Fraction(d2, a), ONE)]
            steps = [f"Vähennetään {e}x molemmilta puolilta: {a - e}x = {d2}", f"x = {d2} / {a - e} = {x}"]
        else:
            level, c = "H", a * x + b
            prompt = (f"Kauppa myy kahvia: pakkaus maksaa {a} euroa ja kertamaksu pussista on {b} euroa. "
                      f"Asiakas maksoi {c} euroa. Montako pakkausta x hän osti? Yhtälö on {a}x + {b} = {c}.")
            wrong = [(Fraction(c + b, a), SIGN), (c - b, ONE)]
            steps = [f"{a}x = {c} {MINUS} {b} = {c - b}", f"x = {c - b} / {a} = {x}"]
        assert all(Fraction(w) != x for w, _ in wrong) and len({Fraction(w) for w, _ in wrong}) == 2
        payload = {"answer": {"kind": "number", "value": x},
                   "wrong": [{"match": txt(w), "misconception": TID, "feedback": fb} for w, fb in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps, str(x),
                               "Oikein: yhtälön molempien puolten on pysyttävä yhtä suurina.", TEMPLATE,
                               {"a": a, "b": b, "x": x}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
