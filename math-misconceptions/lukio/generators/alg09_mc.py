#!/usr/bin/env python3
"""ALG-09 MC (lukio level): square of a sum, (a + b)^2 = a^2 + b^2. Answers computed with sympy."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "alg09_mc"
TID, CODE = "ALG-09", "MC"
X, A, B = sp.symbols("x a b")
GENERIC = "(a + b)² on (a + b)(a + b), ja siinä on myös keskimmäinen tulo 2ab. Kokeile lukuarvoilla, esim. a = 1, b = 1."


def poly(e):
    return show(sp.expand(e)).replace(" · ", "").replace("^2", "²")


def make_items(run, date, count=5, start=1):
    rng = random.Random(2909)
    items = []
    # 1: (x - 6)^2
    e = X - 6
    right, lin = sp.expand(e**2), X**2 + 36
    other = X**2 - 36
    assert len({right, lin, other}) == 3
    opts, cid = mc_options(rng, (poly(right), "Oikein: (x − 6)² = x² − 12x + 36."),
                           [(poly(lin), TID, "Keskimmäinen tulo −2 · 6x = −12x puuttuu."),
                            (poly(other), None, "Tämä on summan ja erotuksen tulo (x + 6)(x − 6), ei erotuksen neliö.")])
    items.append(base_item(TID, CODE, start, ["MAA2.01"], ["G2"], "MAA", "P", "none", "Sievennä (x − 6)².",
                           {"options": opts, "correct": [cid]}, ["(x − 6)² = (x − 6)(x − 6).", f"= {poly(right)}."], poly(right), "Oikein.",
                           TEMPLATE, {"e": str(e)}, date, run, generic_wrong=GENERIC))
    # 2: difference of two squares of sums
    d = sp.expand((2 * X + 5) ** 2 - (2 * X - 5) ** 2)
    zero = sp.expand((4 * X**2 + 25) - (4 * X**2 + 25))
    assert d == 40 * X and zero == 0
    opts, cid = mc_options(rng, (poly(d), "Oikein: neliöiden erotus on 40x."),
                           [("0", TID, "Jos neliöt jakautuisivat, molemmista tulisi 4x² + 25 ja erotus olisi 0. Keskimmäiset tulot ±20x eivät kumoudu."),
                            ("20x", None, "Keskimmäiset tulot ovat +20x ja −20x; erotuksessa ne eivät kumoudu vaan lasketaan yhteen.")])
    items.append(base_item(TID, CODE, start + 1, ["MAA2.01"], ["G2"], "MAA", "T", "none", "Sievennä (2x + 5)² − (2x − 5)².",
                           {"options": opts, "correct": [cid]},
                           ["(2x + 5)² = 4x² + 20x + 25 ja (2x − 5)² = 4x² − 20x + 25.", "Erotus on (20x) − (−20x) = 40x."],
                           poly(d), "Oikein.", TEMPLATE, {"a": 5}, date, run, generic_wrong=GENERIC))
    # 3: plot extended (MAB)
    right = sp.expand((X + 3) ** 2)
    lin = X**2 + 9
    mid = X**2 + 3 * X + 9
    assert len({right, lin, mid}) == 3
    opts, cid = mc_options(rng, (poly(right), "Oikein: pinta-ala on (x + 3)² = x² + 6x + 9."),
                           [(poly(lin), TID, "Puuttuu kaksi suorakaidetta, kummankin pinta-ala 3x."),
                            (poly(mid), None, "Suorakaiteita on kaksi, joten keskimmäinen termi on 6x.")])
    items.append(base_item(TID, CODE, start + 2, ["MAB2.07"], ["G2"], "MAB", "P", "none",
                           "Neliön muotoisen tontin sivu on x metriä. Tonttia laajennetaan niin, että sivu pitenee 3 metriä. Mikä lauseke antaa uuden tontin pinta-alan (m²)?",
                           {"options": opts, "correct": [cid]},
                           ["Uusi sivu on x + 3.", f"Pinta-ala (x + 3)² = {poly(right)}."], poly(right), "Oikein.", TEMPLATE, {"d": 3}, date, run, generic_wrong=GENERIC))
    # 4: a^2 + b^2 from a + b and ab (MAB)
    s, p = 7, 12
    right = s**2 - 2 * p
    assert right == 25 and sp.expand((A + B) ** 2 - 2 * A * B) == A**2 + B**2
    opts, cid = mc_options(rng, (f"{right} m²", "Oikein: a² + b² = (a + b)² − 2ab = 49 − 24 = 25."),
                           [(f"{s**2} m²", TID, "(a + b)² ei ole a² + b²; erotus on 2ab."),
                            (f"{s**2 + p} m²", None, "Keskimmäinen tulo on 2ab = 24 ja se vähennetään, ei ab:tä lisätä.")])
    items.append(base_item(TID, CODE, start + 3, ["MAB2.07"], ["G2"], "MAB", "T", "none",
                           f"Kahden neliön sivujen pituuksien summa on {s} m ja tulo {p} m². Kuinka suuri on neliöiden yhteenlaskettu pinta-ala?",
                           {"options": opts, "correct": [cid]},
                           [f"(a + b)² = a² + 2ab + b², joten a² + b² = {s}² − 2 · {p}.", f"= {s**2} − {2 * p} = {right}."], f"{right} m²", "Oikein.",
                           TEMPLATE, {"s": s, "p": p}, date, run, generic_wrong=GENERIC))
    # 5: counterexample justification
    ok = lambda v: (v + 3) ** 2 == v**2 + 9
    assert ok(0) and not ok(1)
    opts, cid = mc_options(rng, ("Väite on väärä: x = 1 antaa (1 + 3)² = 16, mutta 1² + 9 = 10. Yksi vastaesimerkki riittää.", "Oikein."),
                           [("Väite on oikea, koska se toimii kokeiltaessa x = 0.", TID, "Yksi onnistunut kokeilu ei todista yleistä väitettä; vastaesimerkki kumoaa sen."),
                            ("Väite on väärä, koska 9 ei ole neliöluku.", None, "9 = 3², mutta virhe on puuttuvassa keskimmäisessä tulossa 6x.")])
    items.append(base_item(TID, CODE, start + 4, ["MAA2.01"], ["G2"], "MAA", "H", "none",
                           "Oppilas väittää: ”(x + 3)² = x² + 9, sillä kun x = 0, molemmat puolet ovat 9.” Mikä perustelu arvioi väitteen oikein?",
                           {"options": opts, "correct": [cid]},
                           ["x = 1: (1 + 3)² = 16 ja 1² + 9 = 10.", "Vastaesimerkki kumoaa väitteen; oikein (x + 3)² = x² + 6x + 9."], "Väite on väärä", "Oikein.",
                           TEMPLATE, {"a": 3}, date, run, generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
