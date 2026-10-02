#!/usr/bin/env python3
"""LEQU-01 MC (lukio level): dividing both sides by an expression that can be zero (a root is lost).
Solutions computed with sympy."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lequ01_mc"
TID, CODE = "LEQU-01", "MC"
X, T = sp.symbols("x t", real=True)
GENERIC = "Yhtälön molempia puolia saa jakaa vain lausekkeella, joka ei voi olla nolla. Siirrä muuten kaikki yhdelle puolelle ja tekijöi."


def sols(eq, v=X):
    return sorted(sp.solveset(eq, v, sp.S.Reals), key=float)


def both(s, v="x", unit=""):
    return " tai ".join(f"{v} = {show(a)}{unit}" for a in s)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2701)
    items = []

    def add(n, lops, syll, g, level, prompt, correct, wrongs, steps, params):
        opts, cid = mc_options(rng, (correct, "Oikein: nollaksi sievenevä tekijä antaa myös ratkaisun."), wrongs)
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt, {"options": opts, "correct": [cid]},
                               steps, correct, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    s = sols(sp.Eq(X ** 2, 3 * X))
    add(start, ["MAA2.05"], "MAA", ["G4"], "T", "Ratkaise yhtälö x² = 3x.", both(s),
        [("x = 3", TID, "Jakaminen x:llä hävittää ratkaisun x = 0. Tarkista sijoittamalla: 0² = 3 · 0."),
         ("x = 0", None, "Myös x = 3 toteuttaa yhtälön: 3² = 3 · 3."),
         ("x = 3 tai x = −3", None, "x² = 3x ei ole sama kuin x² = 9. Siirrä 3x vasemmalle ja tekijöi.")],
        ["x² − 3x = 0.", "x(x − 3) = 0.", f"{both(s)}."], {"a": 3})
    s = sols(sp.Eq(12 * T - 3 * T ** 2, 0), T)
    add(start + 1, ["MAB2.04"], "MAB", ["G4"], "T", "Pallon korkeus metreinä heiton jälkeen on h = 12t − 3t², missä t on aika sekunteina. Milloin korkeus on 0 m?",
        both(s, "t", " s"),
        [("t = 4 s", TID, "Jakaminen t:llä hävittää hetken t = 0 s, jolloin pallo on heitettäessä maassa."),
         ("t = 0 s", None, "Pallo palaa maahan myös hetkellä t = 4 s."),
         ("t = 2 s", None, "t = 2 s on huipun hetki, jolloin korkeus on 12 m.")],
        ["12t − 3t² = 0.", "3t(4 − t) = 0.", f"{both(s, 't', ' s')}."], {"a": 12, "b": 3})
    s = sols(sp.Eq(X ** 3, 4 * X))
    add(start + 2, ["MAA2.05"], "MAA", ["G4"], "H", "Ratkaise yhtälö x³ = 4x.", both(s),
        [("x = 2 tai x = −2", TID, "Jakaminen x:llä hävittää ratkaisun x = 0."),
         ("x = 2", TID, "Jakaminen x:llä hävittää ratkaisun x = 0, ja neliöjuuresta jää pois ratkaisu x = −2."),
         ("x = 0 tai x = 4", None, "x³ = 4x antaa x(x² − 4) = 0, ja x² = 4 antaa x = ±2.")],
        ["x³ − 4x = 0.", "x(x − 2)(x + 2) = 0.", f"{both(s)}."], {"n": 3, "a": 4})
    s = sols(sp.Eq(X * (X - 5), 2 * X))
    add(start + 3, ["MAB2.04"], "MAB", ["G4"], "H", "Ratkaise yhtälö x(x − 5) = 2x.", both(s),
        [("x = 7", TID, "Jakaminen x:llä hävittää ratkaisun x = 0. Tarkista: 0 · (0 − 5) = 2 · 0."),
         ("x = 0", None, "Myös x = 7 toteuttaa yhtälön: 7 · 2 = 14."),
         ("x = 3", None, "Yhtälö x − 5 = 2 antaa x = 7, ei x = 3.")],
        ["x(x − 5) − 2x = 0.", "x(x − 7) = 0.", f"{both(s)}."], {"a": 5, "b": 2})
    s = sols(sp.Eq((X - 1) * (X + 2), 4 * (X - 1)))
    add(start + 4, ["MAA2.05", "MAA2.04"], "MAA", ["G3"], "H", "Yhtälössä (x − 1)(x + 2) = 4(x − 1) Liisa jakaa molemmat puolet tekijällä x − 1. Mikä perustelu osoittaa, että tämä on virhe?",
        "Kun x = 1, tekijä x − 1 on nolla, eikä nollalla voi jakaa. Luku 1 toteuttaa yhtälön, joten ratkaisu x = 1 katoaisi.",
        [("Jakaminen on virhe, koska yhtälössä ei saa jakaa mitään lauseketta.", TID, "Jakaminen on sallittua, kun jakaja ei voi olla nolla. Tässä jakaja voi olla nolla."),
         ("Jakaminen on sallittu, koska molemmilla puolilla on sama tekijä.", TID, "Sama tekijä ei riitä. Jos tekijä on nolla, jakaminen ei ole määritelty ja ratkaisu voi kadota."),
         ("Jakaminen on virhe, koska yhtälöllä ei ole ratkaisuja.", None, "Yhtälöllä on ratkaisut: x = 1 ja x = 2.")],
        ["Siirretään oikea puoli vasemmalle: (x − 1)(x + 2 − 4) = 0.", f"Ratkaisut: {both(s)}; jako olisi hävittänyt ratkaisun x = 1."], {"a": 1, "b": 2, "c": 4})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
