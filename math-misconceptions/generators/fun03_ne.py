#!/usr/bin/env python3
"""FUN-03 (slope confused with visual steepness), type NE. Axis scales are described in words (no figure). The
slope is computed as dy/dx from the numbers; the tagged wrong answer is the value read from the apparent steepness."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "fun03_ne"
TID, CODE = "FUN-03", "NE"
BAD = ("Kuvan jyrkkyys riippuu myös akselien asteikoista. Kulmakerroin lasketaan lukuarvoista: "
       "kulmakerroin = y:n muutos / x:n muutos.")
GOOD = "Oikein: kulmakerroin = y:n muutos / x:n muutos, eikä se riipu siitä, miltä suora näyttää."


def val(x):
    x = Fraction(x)
    return int(x) if x.denominator == 1 else float(x)


def dec(x):
    return str(val(x)).replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1232)
    items = []
    for k in range(count):
        if k == 0:
            kk, m = rng.choice([(1, 2), (2, 3), (3, 2)])
            ans, wrong = Fraction(kk), [Fraction(kk * m)]
            prompt = (f"Suora y = {'' if kk == 1 else kk}x piirretään koordinaatistoon, jossa y-akselin yksikkö on {m} kertaa "
                      "x-akselin yksikön pituinen, joten suora näyttää jyrkemmältä. Mikä on suoran kulmakerroin?")
            steps = [f"Yhtälöstä y = {'' if kk == 1 else kk}x kulmakerroin on {kk}"]
            level, params = "T", {"k": kk, "m": m, "form": k}
        elif k == 1:
            p, s, m, c = rng.choice([(2, 3, 2, 1), (3, 2, 3, 4), (2, 4, 2, 0)])
            ans, wrong = Fraction(s), [Fraction(s * m)]
            prompt = (f"Suora kulkee pisteiden (0, {c}) ja ({p}, {c + s * p}) kautta. Se on piirretty koordinaatistoon, jossa "
                      f"y-akselin yksikkö on {m} kertaa x-akselin yksikön pituinen, joten suora näyttää jyrkemmältä. "
                      "Mikä on suoran kulmakerroin?")
            steps = [f"Muutos y: {c + s * p} − {c} = {s * p}", f"Muutos x: {p} − 0 = {p}", f"Kulmakerroin {s * p} / {p} = {s}"]
            level, params = "T", {"p": p, "s": s, "m": m, "c": c, "form": k}
        elif k == 2:
            r = rng.choice([2, 3, 4, 5])
            ans, wrong = Fraction(r), [Fraction(1)]
            prompt = (f"Suora näyttää kulkevan 45° kulmassa koordinaatistossa, jossa y-akselin yksikkö on {r} kertaa lyhyempi "
                      f"kuin x-akselin yksikkö. Mikä on suoran kulmakerroin?")
            steps = [f"1 cm oikealle on 1 yksikkö, 1 cm ylös on {r} yksikköä", f"Kulmakerroin = {r} / 1 = {r}"]
            level, params = "T", {"r": r, "form": k}
        elif k == 3:
            r, c = rng.choice([(2, 3), (3, 1), (4, 5)])
            ans, wrong = Fraction(3 * r + c), [Fraction(3 + c)]
            prompt = (f"Suora y = kx + {c} näyttää kulkevan 45° kulmassa koordinaatistossa, jossa y-akselin yksikkö on {r} kertaa "
                      f"lyhyempi kuin x-akselin yksikkö. Mikä on y:n arvo, kun x = 3?")
            steps = [f"Kulmakerroin k = {r}", f"y = {r} · 3 + {c} = {3 * r + c}"]
            level, params = "H", {"r": r, "c": c, "form": k}
        else:
            h, u = rng.choice([(2, Fraction(1, 2)), (3, Fraction(1, 2)), (1, Fraction(1, 4))])
            ans, wrong = h / u, [Fraction(h)]
            prompt = (f"Kuvassa suora nousee {h} cm jokaista yhtä oikealle kulkevaa senttimetriä kohti. x-akselin yksikkö on 1 cm "
                      f"ja y-akselin yksikkö {dec(u)} cm. Mikä on suoran kulmakerroin?")
            steps = [f"Oikealle 1 cm = 1 yksikkö", f"Ylös {h} cm = {h} / {dec(u)} = {dec(ans)} yksikköä", f"Kulmakerroin {dec(ans)}"]
            level, params = "H", {"h": h, "u": str(u), "form": k}
        wrong = [w for w in dict.fromkeys(wrong) if w != ans]
        payload = {"answer": {"kind": "number", "value": val(ans)},
                   "wrong": [{"match": val(w), "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S4.05"], ["T15"], 8, level, prompt, payload, steps,
                               dec(ans), GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
