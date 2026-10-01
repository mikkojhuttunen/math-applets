#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type MC. Solutions and wrong answers are computed from the same numbers."""
import random
from fractions import Fraction

from gen_common import MINUS, base_item, cli, mc_options

TEMPLATE = "alg07_mc"
TID, CODE = "ALG-07", "MC"
SIGN = "Siirrettäessä termi yhtälön toiselle puolelle sen merkki vaihtuu: lisäys muuttuu vähennykseksi ja päinvastoin."
ONE = "Jokainen laskutoimitus on tehtävä yhtälön molemmille puolille, myös kaikille termeille."


def f(v):
    v = Fraction(v)
    return (str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}").replace("-", MINUS)


def make_items(run, date, count=5, start=1):
    rng = random.Random(918)
    items = []
    for k in range(count):
        a = rng.randint(2, 6)
        b = rng.randint(2, 9)
        x = rng.randint(2, 9)
        if k == 0:
            level = "T"
            c = a * x + b
            prompt = f"Ratkaise yhtälö {a}x + {b} = {c}."
            good = Fraction(x)
            wrongs = [(Fraction(c + b, a), TID, SIGN), (Fraction(c - b), TID, ONE), (Fraction(c, a) - b, TID, ONE)]
            steps = [f"{a}x = {c} {MINUS} {b} = {c - b}", f"x = {c - b} / {a} = {x}"]
        elif k == 1:
            level = "T"
            c = a * x - b
            prompt = f"Ratkaise yhtälö {a}x {MINUS} {b} = {c}."
            good = Fraction(x)
            wrongs = [(Fraction(c - b, a), TID, SIGN), (Fraction(c + b), TID, ONE), (Fraction(c, a) + b, TID, ONE)]
            steps = [f"{a}x = {c} + {b} = {c + b}", f"x = {c + b} / {a} = {x}"]
        elif k == 2:
            level = "T"
            c = a * x + b
            prompt = (f"Taksimatka maksaa aloitusmaksun {b} euroa ja lisäksi {a} euroa kilometriltä. Matka maksoi {c} euroa. "
                      f"Montako kilometriä x ajettiin? Yhtälö on {a}x + {b} = {c}.")
            good = Fraction(x)
            wrongs = [(Fraction(c + b, a), TID, SIGN), (Fraction(c - b), TID, ONE), (Fraction(c, a) - b, TID, ONE)]
            steps = [f"Vähennetään aloitusmaksu: {a}x = {c} {MINUS} {b} = {c - b}", f"x = {c - b} / {a} = {x}"]
        elif k == 3:
            level = "H"
            a = max(a, 3)
            e = rng.randint(2, a - 1)
            # a x = e x + d2  ->  (a - e) x = d2
            d2 = (a - e) * x
            prompt = f"Ratkaise yhtälö {a}x = {e}x + {d2}."
            good = Fraction(x)
            wrongs = [(Fraction(d2, a + e), TID, SIGN), (Fraction(d2, a) , TID, ONE), (Fraction(d2 + e, a), TID, ONE)]
            steps = [f"Vähennetään {e}x molemmilta puolilta: {a - e}x = {d2}", f"x = {d2} / {a - e} = {x}"]
        else:
            level = "H"
            c = a * x + b
            prompt = (f"Oppilas ratkaisee yhtälön {a}x + {b} = {c} ja kirjoittaa ensimmäiseksi riviksi {a}x = {c + b}. "
                      f"Mikä virhe rivillä on?")
            options, cid = mc_options(rng, (f"Luku {b} siirrettiin toiselle puolelle, mutta sen merkki ei vaihtunut: pitäisi olla {a}x = {c - b}",
                                            "Oikein: luku {} on vähennettävä molemmilta puolilta.".format(b)), [
                (f"Yhtälö jaettiin luvulla {a} vain vasemmalta puolelta", None, "Rivillä ei ole jakolaskua."),
                (f"Luku {b} pitää jättää vasemmalle puolelle, koska sen edessä on plusmerkki", TID, SIGN),
                (f"Rivi on oikein, koska luku {b} siirtyi sivulta toiselle", TID, SIGN),
            ])
            payload = {"options": options, "correct": [cid]}
            items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload,
                                   [f"{a}x + {b} = {c}", f"Vähennetään {b} molemmilta puolilta: {a}x = {c} {MINUS} {b} = {c - b}"],
                                   f"{a}x = {c - b}", "Oikein: termin siirto toiselle puolelle vaihtaa sen merkin.", TEMPLATE,
                                   {"a": a, "b": b, "x": x}, date, run))
            continue
        options, cid = mc_options(rng, (f"x = {f(good)}", "Oikein: toimitus tehtiin molemmille puolille ja merkit käsiteltiin oikein."),
                                  [(f"x = {f(v)}", m, fb) for v, m, fb in wrongs if v != good])
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps, f"x = {x}",
                               "Oikein: yhtälön molempien puolten on pysyttävä yhtä suurina.", TEMPLATE,
                               {"a": a, "b": b, "x": x}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
