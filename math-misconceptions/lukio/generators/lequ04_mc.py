#!/usr/bin/env python3
"""LEQU-04 MC (lukio level): the square root is taken across a quadratic inequality.
Correct options are computed with sympy; distractors carry misconception tags."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options

TEMPLATE = "lequ04_mc"
TID, CODE = "LEQU-04", "MC"
X = sp.Symbol("x", real=True)
GENERIC = "√(x²) = |x|, ei x. Ratkaise |x| < a tai siirrä kaikki vasemmalle ja tekijöi."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1104)
    items = []

    def add(n, g, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, ["MAA2.06"], [g], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    assert sp.solve_univariate_inequality(X ** 2 < 16, X, relational=False) == sp.Interval.open(-4, 4)
    add(start, "G4", "T", "Ratkaise epäyhtälö x² < 16.",
        ("−4 < x < 4", "Oikein."),
        [("x < 4", TID, "Kokeile x = −5: (−5)² = 25, ei pienempi kuin 16."),
         ("x < −4 tai x > 4", None, "Kokeile x = 5: 25 ei ole pienempi kuin 16."),
         ("x < 16", None, "Kokeile x = 10: 100 ei ole pienempi kuin 16.")],
        ["x² − 16 < 0, eli (x − 4)(x + 4) < 0.", "−4 < x < 4."], "−4 < x < 4", {"a": 16})
    assert sp.solve_univariate_inequality(X ** 2 > 49, X, relational=False) == sp.Union(sp.Interval.open(-sp.oo, -7), sp.Interval.open(7, sp.oo))
    add(start + 1, "G4", "T", "Ratkaise epäyhtälö x² > 49.",
        ("x < −7 tai x > 7", "Oikein."),
        [("x > 7", TID, "Myös x = −8 toteuttaa epäyhtälön: (−8)² = 64 > 49."),
         ("−7 < x < 7", None, "Kokeile x = 0: 0 ei ole suurempi kuin 49."),
         ("x > 49", None, "Kokeile x = 10: 100 > 49, mutta 10 < 49.")],
        ["x² − 49 > 0, eli (x − 7)(x + 7) > 0.", "x < −7 tai x > 7."], "x < −7 tai x > 7", {"a": 49})
    assert sp.solve_univariate_inequality((X + 2) ** 2 <= 9, X, relational=False) == sp.Interval(-5, 1)
    add(start + 2, "G4", "H", "Ratkaise epäyhtälö (x + 2)² ≤ 9.",
        ("−5 ≤ x ≤ 1", "Oikein: |x + 2| ≤ 3."),
        [("x ≤ 1", TID, "Esimerkiksi x = −10: (−8)² = 64 > 9."),
         ("−1 ≤ x ≤ 5", None, "Siirto meni väärään suuntaan: x + 2 on välillä −3...3."),
         ("−3 ≤ x ≤ 3", None, "Tämä ratkaisee epäyhtälön x² ≤ 9, ei (x + 2)² ≤ 9.")],
        ["Merkitse t = x + 2: t² ≤ 9, joten −3 ≤ t ≤ 3.", "−5 ≤ x ≤ 1."], "−5 ≤ x ≤ 1", {"shift": 2, "a": 9})
    add(start + 3, "G4", "H", "Oppilas ratkaisi epäyhtälön x² < 9 ja sai x < 3. Millä testiluvulla virhe paljastuu?",
        ("x = −5, sillä −5 < 3, mutta (−5)² = 25 ei ole pienempi kuin 9.", "Oikein."),
        [("x = 2, sillä 2² = 4 < 9.", None, "Tämä luku toteuttaa sekä epäyhtälön että oppilaan vastauksen, joten se ei paljasta virhettä."),
         ("x = 0, sillä 0 < 9.", None, "Tämä luku toteuttaa sekä epäyhtälön että oppilaan vastauksen."),
         ("Mikään testiluku ei paljasta virhettä, koska x < 3 on oikea ratkaisu.", TID, "Oppilaan vastaus päästää läpi esimerkiksi luvun −5, jonka neliö on 25.")],
        ["x = −5 toteuttaa x < 3.", "(−5)² = 25 > 9, joten −5 ei ole ratkaisu."], "x = −5", {"a": 9})
    add(start + 4, "G4", "H", "Oppilas otti epäyhtälön x² < 4 molemmilta puolilta neliöjuuren ja sai x < 2. Mikä on virheen perustelu?",
        ("√(x²) = |x|, ei x, joten saadaan |x| < 2 eli −2 < x < 2.", "Oikein."),
        [("Neliöjuurta ei saa ottaa epäyhtälön molemmilta puolilta lainkaan.", None, "Se on sallittu, kun molemmat puolet ovat ei-negatiivisia, mutta tulos on |x| < 2."),
         ("√4 = ±2, joten ratkaisu on x < 2 tai x < −2.", TID, "√4 = 2. Ratkaisu on |x| < 2, eli −2 < x < 2."),
         ("Oikea ratkaisu on x < −2 tai x > 2.", None, "Kokeile x = 3: 9 ei ole pienempi kuin 4.")],
        ["√(x²) = |x|.", "|x| < 2, joten −2 < x < 2."], "|x| < 2, eli −2 < x < 2", {"a": 4})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
