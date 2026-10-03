#!/usr/bin/env python3
"""LEQU-05 NE (lukio level): absolute value read as "drop the minus sign", so the negative
case of |f(x)| = a is lost. Roots are computed with sympy; the wrong answer is the root from the
positive case only."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "lequ05_ne"
TID, CODE = "LEQU-05", "NE"
X = sp.Symbol("x", real=True)
GENERIC = "Itseisarvo |a| on luvun a etäisyys nollasta. Yhtälö |f(x)| = a tarkoittaa f(x) = a tai f(x) = −a (kun a ≥ 0). Tarkista sijoittamalla."


def roots(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, value, wrongs, steps, final, params):
        for w, _ in wrongs:
            assert float(w) != float(value)
        ans = {"kind": "number", "value": float(value), "tolerance": 0.01}
        items.append(base_item(TID, CODE, n, ["MAA4.06"], ["G4"], "MAA", level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": float(w), "misconception": TID, "feedback": f} for w, f in wrongs],
                                "input_hint": "Kirjoita luku"}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    r = roots(sp.Eq(sp.Abs(X - 3), 5))
    add(start, "T", "Ratkaise yhtälö |x − 3| = 5. Kirjoita ratkaisuista pienempi.", r[0], [(r[1], "8 on suurempi ratkaisu. Myös x − 3 = −5 toteuttaa yhtälön, koska |−5| = 5.")],
        ["x − 3 = 5 tai x − 3 = −5.", "x = 8 tai x = −2; pienempi on −2."], "−2", {"a": 3, "b": 5})
    r = roots(sp.Eq(sp.Abs(2 * X - 1), 7))
    add(start + 1, "T", "Kuinka monta ratkaisua yhtälöllä |2x − 1| = 7 on?", len(r), [(1, "Yhtälöllä on myös negatiivinen tapaus 2x − 1 = −7, joten ratkaisuja on kaksi.")],
        ["2x − 1 = 7 antaa x = 4.", "2x − 1 = −7 antaa x = −3.", "Ratkaisuja on 2."], "2", {"a": 2, "b": -1, "c": 7})
    r = roots(sp.Eq(sp.Abs(X + 4), 6))
    s = sum(r)
    add(start + 2, "T", "Ratkaise yhtälö |x + 4| = 6 ja laske ratkaisujen summa.", s, [(r[1], "2 on vain toinen ratkaisu. Myös x + 4 = −6 antaa ratkaisun x = −10.")],
        ["x + 4 = 6 antaa x = 2.", "x + 4 = −6 antaa x = −10.", "Summa on 2 + (−10) = −8."], "−8", {"a": 4, "c": 6})
    r = roots(sp.Eq(sp.Abs(3 * X - 2), sp.Abs(X + 6)))
    add(start + 3, "H", "Ratkaise yhtälö |3x − 2| = |x + 6|. Kirjoita ratkaisuista pienempi.", r[0], [(r[1], "4 saadaan tapauksesta 3x − 2 = x + 6. Myös 3x − 2 = −(x + 6) on mahdollinen.")],
        ["3x − 2 = x + 6 antaa x = 4.", "3x − 2 = −(x + 6) antaa 4x = −4, eli x = −1.", "Pienempi ratkaisu on −1."], "−1", {"a": 3, "b": -2, "c": 1, "d": 6})
    assert roots(sp.Eq(sp.Abs(X - 1), -2)) == []
    add(start + 4, "H", "Matti ratkaisi yhtälön |x − 1| = −2 ja sai x = 3. Kuinka monta ratkaisua yhtälöllä oikeasti on? Tarkista Matin vastaus sijoittamalla.", 0,
        [(1, "Matin ratkaisu x = 3 ei kelpaa: |3 − 1| = 2, ei −2. Itseisarvo ei voi olla negatiivinen."),
         (2, "Sijoita x = 3: |3 − 1| = 2, ei −2. Mikään luku ei anna negatiivista itseisarvoa.")],
        ["Itseisarvo on aina ≥ 0.", "Oikea puoli −2 on negatiivinen, joten ratkaisuja ei ole.", "Tarkistus: |3 − 1| = 2 ≠ −2."], "0", {"a": -2, "b": 1})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
