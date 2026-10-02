#!/usr/bin/env python3
"""LEQU-01 NE (lukio level): dividing both sides by an expression that can be zero (a root is lost).
Roots computed with sympy; the wrong answer is what the division would give."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "lequ01_ne"
TID, CODE = "LEQU-01", "NE"
X = sp.Symbol("x", real=True)
GENERIC = "Yhtälön molempia puolia saa jakaa vain lausekkeella, joka ei voi olla nolla. Siirrä muuten kaikki yhdelle puolelle ja tekijöi."


def roots(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, g, level, prompt, value, wrong, wfb, steps, final, params):
        assert float(value) != float(wrong)
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt,
                               {"answer": {"kind": "number", "value": float(value), "tolerance": 0.01},
                                "wrong": [{"match": float(wrong), "misconception": TID, "feedback": wfb}],
                                "input_hint": "Kirjoita luku"}, steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    r = roots(sp.Eq(X ** 2, 7 * X))
    add(start, ["MAA2.05"], "MAA", ["G4"], "T", "Ratkaise yhtälö x² = 7x. Kirjoita ratkaisuista pienempi.", r[0], r[1],
        "7 on vain toinen ratkaisu. Jakaminen x:llä hävittää ratkaisun x = 0.", ["x² − 7x = 0.", "x(x − 7) = 0, joten x = 0 tai x = 7."], "0", {"a": 7})
    r = roots(sp.Eq(6 * X ** 2, 18 * X))
    add(start + 1, ["MAB2.04"], "MAB", ["G4"], "T", "Kuinka monta ratkaisua yhtälöllä 6x² = 18x on?", len(r), 1,
        "Jakaminen x:llä jättää vain ratkaisun x = 3. Ratkaisu x = 0 toteuttaa myös yhtälön.", ["6x² − 18x = 0.", "6x(x − 3) = 0, joten x = 0 tai x = 3."], "2", {"c": 6, "a": 18})
    r = roots(sp.Eq(X ** 3, 9 * X))
    add(start + 2, ["MAA2.05"], "MAA", ["G4"], "H", "Kuinka monta ratkaisua yhtälöllä x³ = 9x on?", len(r), 2,
        "Jakaminen x:llä jättää vain ratkaisut x = 3 ja x = −3. Ratkaisu x = 0 toteuttaa myös yhtälön.", ["x³ − 9x = 0.", "x(x − 3)(x + 3) = 0, joten ratkaisuja on kolme."], "3", {"n": 3, "a": 9})
    r = roots(sp.Eq(X * (X + 4), 3 * X))
    prod = sp.prod(r)
    assert prod == 0
    add(start + 3, ["MAB2.04"], "MAB", ["G4"], "H", "Ratkaise yhtälö x(x + 4) = 3x. Mikä on ratkaisujen tulo?", prod, -1,
        "−1 on vain ratkaisu x = −1, joka saadaan jakamalla x:llä. Ratkaisu x = 0 puuttuu, joten tulo on 0.", ["x(x + 4) − 3x = 0.", "x(x + 1) = 0, joten x = 0 tai x = −1.", "Tulo on 0 · (−1) = 0."], "0", {"a": 4, "b": 3})
    r = roots(sp.Eq((X - 1) * (X + 2), 4 * (X - 1)))
    s = sum(r)
    add(start + 4, ["MAA2.05", "MAA2.04"], "MAA", ["G4"], "H", "Elias ratkaisee yhtälön (x − 1)(x + 2) = 4(x − 1) jakamalla tekijällä x − 1 ja arvioi ratkaisujen summaksi 2. Laske ratkaisujen summa ja tarkista arvio.", s, 2,
        "2 on vain ratkaisu x = 2. Kun x = 1, molemmat puolet ovat nolla, joten myös x = 1 on ratkaisu.", ["(x − 1)(x + 2 − 4) = 0, joten (x − 1)(x − 2) = 0.", "Ratkaisut ovat 1 ja 2, summa on 3."], "3", {"a": 1, "b": 2, "c": 4})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
