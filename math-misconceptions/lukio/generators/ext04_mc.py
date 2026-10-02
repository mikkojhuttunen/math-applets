#!/usr/bin/env python3
"""EXT-04 MC (lukio level): x^2 = a gives only the positive root. Solutions computed with sympy."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, num, show

TEMPLATE = "ext04_mc"
TID, CODE = "EXT-04", "MC"
X = sp.Symbol("x")
GENERIC = "Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0: x = √a ja x = −√a. Tarkista sijoittamalla."


def sols(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def both(s):
    return " tai ".join(f"x = {show(v)}" for v in s)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2704)
    items = []

    def add(n, lops, syll, level, prompt, s, wrongs, steps, params, extra_correct=None):
        correct = (extra_correct or both(s), "Oikein: sekä positiivinen että negatiivinen juuri toteuttavat yhtälön.")
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, "none", prompt, {"options": opts, "correct": [cid]},
                               steps, correct[0], "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    s = sols(sp.Eq(X ** 2, 49))
    add(start, ["MAA2.04"], "MAA", "T", "Ratkaise yhtälö x² = 49.", s,
        [("x = 7", TID, "Myös (−7)² = 49, joten x = −7 on ratkaisu."),
         ("x = −7", None, "Myös 7² = 49, joten x = 7 on ratkaisu."),
         ("x = 24,5", None, "x² = 49 ei tarkoita 2x = 49. Ota neliöjuuri.")],
        ["x = ±√49.", f"{both(s)}."], {"a": 49})
    s = sols(sp.Eq(X ** 2, sp.Rational(9, 4)))
    add(start + 1, ["MAB2.04"], "MAB", "T", "Neliön muotoisen laatan pinta-ala on 2,25 m². Yhtälö sivun pituudelle x on x² = 2,25. Mitkä ovat yhtälön ratkaisut?", s,
        [("x = 1,5", TID, "Yhtälöllä on myös ratkaisu x = −1,5, koska (−1,5)² = 2,25. (Sivun pituudeksi kelpaa vain positiivinen.)"),
         ("x = 1,125", None, "x² = 2,25 ei tarkoita 2x = 2,25. Ota neliöjuuri."),
         ("x = −1,5", None, "Myös 1,5² = 2,25, joten x = 1,5 on ratkaisu.")],
        ["x = ±√2,25 = ±1,5.", "Sivun pituudeksi kelpaa vain 1,5 m, mutta yhtälön ratkaisut ovat ±1,5."], {"a": 2.25})
    s = sols(sp.Eq((X - 2) ** 2, 9))
    add(start + 2, ["MAA2.04"], "MAA", "H", "Ratkaise yhtälö (x − 2)² = 9.", s,
        [("x = 5", TID, "Myös x − 2 = −3 toteuttaa yhtälön, joten x = −1 on ratkaisu."),
         ("x = 1 tai x = −5", None, "Luvut x − 2 = ±3 antavat x = 2 ± 3, ei x = −2 ± 3."),
         ("x = 11", None, "Neliöstä ei päästä pois lisäämällä 2 ja neliöimällä; ota neliöjuuri: x − 2 = ±3.")],
        ["x − 2 = 3 tai x − 2 = −3.", f"{both(s)}."], {"c": 2, "a": 9})
    s = sols(sp.Eq(2 * X ** 2, 50))
    add(start + 3, ["MAB2.04"], "MAB", "H", "Ratkaise yhtälö 2x² = 50.", s,
        [("x = 5", TID, "Myös x = −5 toteuttaa yhtälön: 2 · (−5)² = 50."),
         ("x = ±25", None, "Jaa ensin 2:lla: x² = 25. Sen jälkeen ota neliöjuuri."),
         ("x = ±10", None, "Sekä jakaminen että neliöjuuri tarvitaan: x² = 25, x = ±5.")],
        ["Jaetaan 2:lla: x² = 25.", f"{both(s)}."], {"c": 2, "a": 50})
    add(start + 4, ["MAA2.04"], "MAA", "H", "Ville ratkaisi yhtälön x² = 64 ja sai vastaukseksi x = 8. Mikä perustelu osoittaa vastauksen vajaaksi?",
        sols(sp.Eq(X ** 2, 64)),
        [("Yhtälö x² = 64 on määritelty vain positiivisille luvuille, joten x = 8 riittää.", TID, "Yhtälö on määritelty kaikille reaaliluvuille. Myös negatiivinen luku voi toteuttaa sen."),
         ("Koska 8² = 64, riittää löytää yksi ratkaisu.", TID, "Yhtälön kaikki ratkaisut pitää löytää. Tarkista, toteuttaako vastaluku yhtälön."),
         ("Vastaus on väärä, koska neliöjuuri 64 ei ole kokonaisluku.", None, "√64 = 8 on kokonaisluku, vika on muualla.")],
        ["(−8)² = 64, joten x = −8 on myös ratkaisu.", "Ratkaisut ovat x = 8 ja x = −8."], {"a": 64},
        extra_correct="Myös (−8)² = 64, joten x = −8 on toinen ratkaisu ja vastaus oli vajaa.")
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
