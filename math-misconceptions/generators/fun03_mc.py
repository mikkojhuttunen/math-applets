#!/usr/bin/env python3
"""FUN-03 (slope confused with visual steepness), type MC. Axis scales are described in words (no figure). The
slope is computed as dy/dx from the numbers; the tagged wrong option reads the slope from how steep the line looks."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options

TEMPLATE = "fun03_mc"
TID, CODE = "FUN-03", "MC"
BAD = ("Kuvan jyrkkyys riippuu myös akselien asteikoista. Kulmakerroin lasketaan lukuarvoista: "
       "kulmakerroin = y:n muutos / x:n muutos.")
GOOD = "Oikein: kulmakerroin = y:n muutos / x:n muutos, eikä se riipu siitä, miltä suora näyttää."


def fr(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1231)
    items = []
    for k in range(count):
        if k == 0:
            kk, m = rng.choice([(1, 2), (2, 3), (1, 3)])
            prompt = (f"Suora y = {'' if kk == 1 else kk}x piirretään koordinaatistoon, jossa y-akselin yksikkö on {m} kertaa "
                      "x-akselin yksikön pituinen. Suora näyttää jyrkemmältä kuin 45°. Mikä on suoran kulmakerroin?")
            correct = (fr(kk), GOOD)
            wrongs = [(fr(kk * m), TID, BAD), (fr(Fraction(kk, m)), None, "Kulmakerroin luetaan yhtälöstä, ei kuvan mittasuhteista."),
                      ("45", None, "45° on kulma, ei kulmakerroin.")]
            steps = [f"Yhtälöstä y = {'' if kk == 1 else kk}x kulmakerroin on {kk}", "Asteikko venyttää kuvaa mutta ei muuta kulmakerrointa"]
            final, level, params = fr(kk), "T", {"k": kk, "m": m, "form": k}
        elif k == 1:
            kk, c = rng.choice([(3, 1), (2, 4), (4, 2)])
            prompt = (f"Funktion y = {kk}x + {c} kuvaaja piirretään kahteen koordinaatistoon. Toisessa y-akselin asteikko on "
                      "tihennetty, ja suora näyttää siinä loivemmalta. Mitä voi sanoa kulmakertoimista?")
            correct = (f"Ne ovat samat, {kk}", GOOD)
            wrongs = [(f"Tihennetyssä kuvassa kulmakerroin on pienempi, koska suora näyttää loivemmalta", TID, BAD),
                      ("Tihennetyssä kuvassa kulmakerroin on suurempi", None, "Asteikon tihentäminen ei muuta funktiota eikä kulmakerrointa."),
                      ("Kulmakertoimia ei voi vertailla ilman mittaviivainta", None, "Kulmakerroin voidaan lukea yhtälöstä.")]
            steps = [f"Molemmat kuvaajat esittävät funktiota y = {kk}x + {c}", f"Kulmakerroin on {kk}"]
            final, level, params = f"Samat, {kk}", "T", {"k": kk, "c": c, "form": k}
        elif k == 2:
            r = rng.choice([2, 3, 4])
            prompt = (f"Suora näyttää kulkevan 45° kulmassa koordinaatistossa, jossa y-akselin yksikkö on {r} kertaa lyhyempi "
                      f"kuin x-akselin yksikkö (1 cm vastaa x-akselilla yhtä yksikköä ja y-akselilla {r} yksikköä). "
                      "Mikä on suoran kulmakerroin?")
            correct = (fr(r), GOOD)
            wrongs = [("1", TID, BAD), (fr(Fraction(1, r)), None, "Muutos y-suunnassa on suurempi kuin x-suunnassa."), ("45", None, "45° on kulma, ei kulmakerroin.")]
            steps = [f"1 cm oikealle on 1 yksikkö, 1 cm ylös on {r} yksikköä", f"Kulmakerroin = {r} / 1 = {r}"]
            final, level, params = fr(r), "T", {"r": r, "form": k}
        elif k == 3:
            a, b, m = rng.choice([(4, 2, 3), (6, 3, 4), (5, 2, 4)])
            assert Fraction(a, m) < b and a > b
            prompt = (f"Suora A on y = {a}x ja suora B on y = {b}x. Suora A on piirretty koordinaatistoon, jossa y-akselin "
                      f"yksikkö on {m} kertaa lyhyempi kuin x-akselin yksikkö, ja suora B koordinaatistoon, jossa akselien "
                      f"yksiköt ovat yhtä pitkät. Suora B näyttää jyrkemmältä. Kumman kulmakerroin on suurempi?")
            correct = (f"Suoran A ({a} > {b})", GOOD)
            wrongs = [("Suoran B, koska se näyttää jyrkemmältä", TID, BAD), ("Ne ovat yhtä suuret", None, "Kulmakertoimet ovat eri suuret: tarkista yhtälöt."),
                      ("Sitä ei voi vertailla, koska asteikot ovat eri", None, "Kulmakertoimet voi vertailla yhtälöistä.")]
            steps = [f"A: kulmakerroin {a}, B: kulmakerroin {b}", f"{a} > {b}"]
            final, level, params = "Suoran A", "H", {"a": a, "b": b, "m": m, "form": k}
        else:
            prompt = "Miksi suoran kulmakerrointa ei voi päätellä pelkästä kuvan jyrkkyydestä?"
            correct = ("Koska jyrkkyys riippuu akselien asteikoista; kulmakerroin lasketaan lukuarvojen muutosten suhteena", GOOD)
            wrongs = [("Kuvan jyrkkyys kertoo aina kulmakertoimen", TID, BAD),
                      ("Koska kulmakerroin on aina 1", None, "Eri suorilla on eri kulmakerroin."),
                      ("Koska kulmakerroin mitataan asteina", None, "Kulmakerroin on suhdeluku, ei kulma.")]
            steps = ["Asteikon muuttaminen venyttää kuvaa", "Kulmakerroin = y:n muutos / x:n muutos"]
            final, level, params = "Jyrkkyys riippuu asteikoista", "H", {"form": k}
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S4.05"], ["T15"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
