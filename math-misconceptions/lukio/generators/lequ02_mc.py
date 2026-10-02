#!/usr/bin/env python3
"""LEQU-02 MC (lukio level): zero-product rule used when the product is not zero.
Solutions computed with sympy; the typical wrong answer sets each factor equal to the non-zero value."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lequ02_mc"
TID, CODE = "LEQU-02", "MC"
X = sp.Symbol("x", real=True)
GENERIC = "Tulon nollasääntö toimii vain, kun tulo on 0. Siirrä ensin kaikki vasemmalle, kerro auki ja tekijöi uudelleen."


def sols(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def both(s):
    return " tai ".join(f"x = {show(a)}" for a in s)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2702)
    items = []

    def add(n, level, prompt, correct, wrongs, steps, params, cfb="Oikein: yhtälö on ensin saatava muotoon, jossa tulo on 0."):
        opts, cid = mc_options(rng, (correct, cfb), wrongs)
        items.append(base_item(TID, CODE, n, ["MAA2.05"], ["G4"], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, correct, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    def factor_wrong(a, b, c, d, k):
        """Typical wrong answer: each factor of (ax + b)(cx + d) = k set equal to k."""
        return sols(sp.Eq(a * X + b, k)) + sols(sp.Eq(c * X + d, k))

    # 1: (x - 2)(x - 3) = 6
    s = sols(sp.Eq((X - 2) * (X - 3), 6))
    w = factor_wrong(1, -2, 1, -3, 6)
    add(start, "T", "Ratkaise yhtälö (x − 2)(x − 3) = 6.", both(s),
        [(both(w), TID, "Tulon nollasääntö ei päde, kun tulo on 6. Tekijät voivat olla esimerkiksi 2 ja 3."),
         ("x = 2 tai x = 3", None, "Nämä ratkaisevat yhtälön (x − 2)(x − 3) = 0, eivät yhtälöä, jossa tulo on 6."),
         ("x = 5", None, "Yhtälöllä on kaksi ratkaisua: kerro auki ja siirrä 6 vasemmalle.")],
        ["x² − 5x + 6 = 6.", "x² − 5x = 0, eli x(x − 5) = 0.", f"{both(s)}."], {"k": 6})
    # 2: x(x + 4) = 5
    s = sols(sp.Eq(X * (X + 4), 5))
    w = factor_wrong(1, 0, 1, 4, 5)
    add(start + 1, "T", "Ratkaise yhtälö x(x + 4) = 5.", both(s),
        [(both(w), TID, "Tulon nollasääntö ei päde, kun tulo on 5. Tekijä voi olla mikä tahansa luku, kunhan tulo on 5."),
         ("x = 0 tai x = −4", None, "Nämä ratkaisevat yhtälön x(x + 4) = 0."),
         ("x = 1", None, "Myös x = −5 toteuttaa yhtälön: −5 · (−1) = 5.")],
        ["x² + 4x − 5 = 0.", "(x + 5)(x − 1) = 0.", f"{both(s)}."], {"k": 5})
    # 3: (2x - 1)(x + 3) = 4
    s = sols(sp.Eq((2 * X - 1) * (X + 3), 4))
    w = factor_wrong(2, -1, 1, 3, 4)
    add(start + 2, "H", "Ratkaise yhtälö (2x − 1)(x + 3) = 4.", both(s),
        [(both(w), TID, "Tulon nollasääntö ei päde, kun tulo on 4. Kerro auki ja siirrä 4 vasemmalle."),
         ("x = 1/2 tai x = −3", None, "Nämä ratkaisevat yhtälön (2x − 1)(x + 3) = 0."),
         ("x = 1 tai x = 7/2", None, "Merkkivirhe: 2x² + 5x − 7 = 0 antaa tekijät (2x + 7)(x − 1).")],
        ["2x² + 5x − 3 = 4.", "2x² + 5x − 7 = 0, eli (2x + 7)(x − 1) = 0.", f"{both(s)}."], {"k": 4})
    # 4: check a solution by substitution
    s = sols(sp.Eq((X - 1) * (X - 2), 12))
    w = factor_wrong(1, -1, 1, -2, 12)
    assert w == [13, 14] and s == [-2, 5]
    add(start + 3, "H", "Oppilas ratkaisi yhtälön (x − 1)(x − 2) = 12 ja sai x = 13 tai x = 14. Mikä tarkistus paljastaa nopeimmin, että vastaus on väärä?",
        "Sijoitetaan x = 13 alkuperäiseen yhtälöön: (13 − 1)(13 − 2) = 12 · 11 = 132, joka ei ole 12.",
        [("Tarkistetaan vain tekijät: 13 − 1 = 12 ja 14 − 2 = 12, joten molemmat ratkaisut ovat oikein.", TID, "Tarkistuksessa on laskettava koko tulo. Pelkkä toinen tekijä ei kerro, onko tulo 12."),
         ("Yhtälön ratkaisujen pitää olla pienempiä kuin 12, joten 13 ja 14 ovat väärin.", None, "Ratkaisun suuruudelle ei ole tällaista rajaa. Oikea ratkaisu on x = 5 tai x = −2, mutta syy on sijoituksessa."),
         ("Ratkaisuja pitää olla kolme, koska yhtälö on toista astetta.", None, "Toisen asteen yhtälöllä on enintään kaksi ratkaisua.")],
        ["Sijoitus x = 13: 12 · 11 = 132 ≠ 12, joten x = 13 ei ole ratkaisu.", f"Oikea ratkaisu: x² − 3x + 2 = 12, (x − 5)(x + 2) = 0, {both(s)}."], {"k": 12, "check": "substitution"})
    # 5: when may the zero-product rule be used
    add(start + 4, "H", "Missä yhtälössä tulon nollasääntöä saa käyttää suoraan ilman, että yhtälöä ensin muokataan?",
        "(x − 4)(x + 1) = 0",
        [("(x − 4)(x + 1) = 1", TID, "Tulon nollasääntö vaatii, että tulo on 0. Tässä tulo on 1."),
         ("x(x − 4) = 4", TID, "Oikealla puolella on 4, ei 0. Siirrä 4 vasemmalle ja tekijöi uudelleen."),
         ("(x − 4) + (x + 1) = 0", None, "Tämä on summa, ei tulo. Tulon nollasääntö koskee tuloa.")],
        ["Sääntö: ab = 0 täsmälleen silloin, kun a = 0 tai b = 0.", "Vain yhtälössä (x − 4)(x + 1) = 0 on tulo, joka on yhtä suuri kuin 0."], {"case": "which_equation"})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
