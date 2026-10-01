#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type ES (error spotting). Lines before the error line are
equivalent to line 1 and the error line breaks equivalence (both checked by verify.py)."""
import random
from fractions import Fraction

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg07_es"
TID, CODE = "ALG-07", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = "Tarkista rivi kerrallaan: onko uuden rivin yhtälöllä sama ratkaisu kuin edellisellä? Sijoita ratkaisu yhtälöön."


def q(v):
    v = Fraction(v)
    return (str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}").replace("-", MINUS)


def make_items(run, date, count=5, start=1):
    rng = random.Random(8201)
    items = []
    for k in range(count):
        a, b, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
        ctx = "Oppilas ratkaisee yhtälön rivi riviltä. "
        if k == 0:
            level, err, etype = "T", 2, "sign_not_changed"
            c = a * x + b
            lines = [f"{a}x + {b} = {c}", f"{a}x = {c + b}", f"x = {q(Fraction(c + b, a))}"]
            fix = f"Luku {b} siirretään toiselle puolelle vähentämällä: {a}x = {c} {MINUS} {b} = {c - b}."
        elif k == 1:
            level, err, etype = "T", 2, "sign_not_changed"
            c = a * x - b
            lines = [f"{a}x {MINUS} {b} = {c}", f"{a}x = {c - b}", f"x = {q(Fraction(c - b, a))}"]
            fix = f"Luku {b} siirretään toiselle puolelle lisäämällä: {a}x = {c} + {b} = {c + b}."
        elif k == 2:
            level, err, etype = "T", 3, "one_sided_operation"
            c = a * x + b
            lines = [f"{b} + {a}x = {c}", f"{a}x = {c - b}", f"x = {c - b}"]
            fix = f"Rivi 2 on oikein. Jakaminen luvulla {a} on tehtävä molemmille puolille: x = {c - b} / {a} = {x}."
        elif k == 3:
            level, err, etype = "H", 2, "sign_not_changed"
            a = max(a, 5)
            e = rng.randint(2, a - 2)
            d = b + (a - e) * x
            lines = [f"{a}x + {b} = {e}x + {d}", f"{a}x {MINUS} {e}x = {d + b}", f"{a - e}x = {d + b}"]
            fix = (f"Luku {b} siirretään vasemmalta oikealle vähentämällä: {a}x {MINUS} {e}x = {d} {MINUS} {b} = {d - b}, "
                   f"joten {a - e}x = {d - b} ja x = {x}.")
        else:
            level, err, etype = "H", 2, "sign_not_changed"
            c = a * x - b
            ctx = (f"Koripallojoukkue maksaa pelipaidoista {a} euroa kappaleelta ja saa {b} euron alennuksen koko tilauksesta. "
                   f"Lasku on {c} euroa, ja paitojen määrä x saadaan yhtälöstä. Oppilas ratkaisee yhtälön rivi riviltä. ")
            lines = [f"{a}x {MINUS} {b} = {c}", f"{a}x = {c - b}", f"x = {q(Fraction(c - b, a))}"]
            fix = f"Alennuksen {b} euroa lisätään molemmille puolille: {a}x = {c} + {b} = {c + b}, joten x = {x}."
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, ctx + ASK, payload,
                               [fix, f"Oikea ratkaisu: x = {x}"], f"Virhe on rivillä {err}",
                               "Oikein: yhtälön molemmille puolille tehdään sama toimitus, ja siirrettäessä termin merkki vaihtuu.",
                               TEMPLATE, {"a": a, "b": b, "x": x}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
