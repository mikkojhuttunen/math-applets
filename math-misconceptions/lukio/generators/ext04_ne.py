#!/usr/bin/env python3
"""EXT-04 NE (lukio level): x^2 = a gives only the positive root. Roots computed with sympy;
the wrong answer is the positive root."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "ext04_ne"
TID, CODE = "EXT-04", "NE"
X = sp.Symbol("x")
GENERIC = "Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0: x = √a ja x = −√a. Tarkista sijoittamalla."


def roots(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, value, unit, wrong, wfb, steps, final, params):
        assert float(value) != float(wrong)
        ans = {"kind": "number", "value": float(value), "tolerance": 0.01}
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": float(wrong), "misconception": TID, "feedback": wfb}],
                                "input_hint": "Kirjoita luku"}, steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    r = roots(sp.Eq(X ** 2, 121))
    add(start, ["MAA2.04"], "MAA", "T", "Ratkaise yhtälö x² = 121. Kirjoita negatiivinen ratkaisu.", r[0], None, r[1],
        "Yhtälön toinen ratkaisu on vastaluku: myös (−11)² = 121.", ["x = 11 tai x = −11.", "Negatiivinen ratkaisu on −11."], "−11", {"a": 121})
    r = roots(sp.Eq(3 * X ** 2, 75))
    add(start + 1, ["MAB2.04"], "MAB", "T", "Ratkaise yhtälö 3x² = 75. Kirjoita negatiivinen ratkaisu.", r[0], None, r[1],
        "Yhtälöllä on myös negatiivinen ratkaisu, koska 3 · (−5)² = 75.", ["Jaetaan 3:lla: x² = 25.", "x = ±5, negatiivinen ratkaisu on −5."], "−5", {"c": 3, "a": 75})
    r = roots(sp.Eq((X - 1) ** 2, 16))
    add(start + 2, ["MAA2.04"], "MAA", "H", "Ratkaise yhtälö (x − 1)² = 16. Kirjoita ratkaisuista pienempi.", r[0], None, r[1],
        "5 on yhtälön suurempi ratkaisu. Myös x − 1 = −4 toteuttaa yhtälön.", ["x − 1 = 4 tai x − 1 = −4.", "x = 5 tai x = −3; pienempi on −3."], "−3", {"c": 1, "a": 16})
    r = roots(sp.Eq(X ** 2 - 12, 37))
    add(start + 3, ["MAB2.04"], "MAB", "H", "Kuinka monta ratkaisua yhtälöllä x² − 12 = 37 on?", len(r), None, 1,
        "Yhtälöllä x² = 49 on kaksi ratkaisua, koska myös (−7)² = 49.", ["x² = 49.", "x = 7 tai x = −7, eli ratkaisuja on 2."], "2", {"c": -12, "a": 37})
    r = roots(sp.Eq(X ** 2, 20))
    s = sum(r)
    assert s == 0
    add(start + 4, ["MAA2.04"], "MAA", "H", "Yhtälön x² = 20 ratkaisujen summan arvioi Eeva olevan 4,47. Laske ratkaisujen summa ja tarkista Eevan arvio.", s, None, round(float(r[1]), 2),
        "4,47 on vain positiivinen ratkaisu √20. Yhtälöllä on myös ratkaisu −√20.", ["Ratkaisut ovat √20 ≈ 4,47 ja −√20 ≈ −4,47.", "Summa on 0, joten Eevan arvio ei täsmää."], "0", {"a": 20})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
