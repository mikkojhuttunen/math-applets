#!/usr/bin/env python3
"""LEQU-02 NE (lukio level): zero-product rule used when the product is not zero.
Answers are numbers computed with sympy; the wrong answer applies the rule with the non-zero value."""
import sympy as sp

from gen_common import base_item, cli, num

TEMPLATE = "lequ02_ne"
TID, CODE = "LEQU-02", "NE"
X = sp.Symbol("x", real=True)
GENERIC = "Tulon nollasääntö toimii vain, kun tulo on 0. Siirrä ensin kaikki vasemmalle, kerro auki ja tekijöi uudelleen."


def sols(eq):
    return sorted(sp.solveset(eq, X, sp.S.Reals), key=float)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, value, wrong, wfb, steps, params):
        assert float(value) != float(wrong)
        ans = {"kind": "number", "value": float(value), "tolerance": 0.01}
        items.append(base_item(TID, CODE, n, ["MAA2.05"], ["G4"], "MAA", level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": float(wrong), "misconception": TID, "feedback": wfb}],
                                "input_hint": "Kirjoita luku"}, steps, num(value), "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: larger root of (x-3)(x-4) = 12
    s = sols(sp.Eq((X - 3) * (X - 4), 12))
    w = max(sols(sp.Eq(X - 3, 12)) + sols(sp.Eq(X - 4, 12)))
    add(start, "T", "Ratkaise yhtälö (x − 3)(x − 4) = 12. Kirjoita suurempi ratkaisu.", s[-1], w,
        f"Tulon nollasääntö ei päde, kun tulo on 12. Tarkista: ({num(w)} − 3)({num(w)} − 4) ≠ 12.",
        ["x² − 7x + 12 = 12.", "x(x − 7) = 0.", f"Suurempi ratkaisu on {num(s[-1])}."], {"k": 12})
    # 2: smaller root of x(x-5) = 14
    s = sols(sp.Eq(X * (X - 5), 14))
    w = min(sols(sp.Eq(X, 14)) + sols(sp.Eq(X - 5, 14)))
    add(start + 1, "T", "Ratkaise yhtälö x(x − 5) = 14. Kirjoita pienempi ratkaisu.", s[0], w,
        "Tulon nollasääntö ei päde, kun tulo on 14. Siirrä 14 vasemmalle ja tekijöi.",
        ["x² − 5x − 14 = 0.", "(x − 7)(x + 2) = 0.", f"Pienempi ratkaisu on {num(s[0])}."], {"k": 14})
    # 3: larger root of (x+1)(x-2) = 10
    s = sols(sp.Eq((X + 1) * (X - 2), 10))
    w = max(sols(sp.Eq(X + 1, 10)) + sols(sp.Eq(X - 2, 10)))
    add(start + 2, "H", "Ratkaise yhtälö (x + 1)(x − 2) = 10. Kirjoita suurempi ratkaisu.", s[-1], w,
        "Tulon nollasääntö ei päde, kun tulo on 10. Kerro auki ja siirrä 10 vasemmalle.",
        ["x² − x − 2 = 10.", "x² − x − 12 = 0, eli (x − 4)(x + 3) = 0.", f"Suurempi ratkaisu on {num(s[-1])}."], {"k": 10})
    # 4: sum of solutions of x(x-6) = 16
    s = sols(sp.Eq(X * (X - 6), 16))
    w = sum(sols(sp.Eq(X, 16)) + sols(sp.Eq(X - 6, 16)))
    add(start + 3, "H", "Laske yhtälön x(x − 6) = 16 ratkaisujen summa.", sum(s), w,
        "Tulon nollasääntö ei päde, kun tulo on 16. Ratkaise yhtälö x² − 6x − 16 = 0.",
        ["x² − 6x − 16 = 0.", "(x − 8)(x + 2) = 0.", f"Ratkaisut ovat {num(s[1])} ja {num(s[0])}, summa {num(sum(s))}."], {"k": 16})
    # 5: sum of solutions of (x-3)(x+2) = -6, with a check by substitution
    s = sols(sp.Eq((X - 3) * (X + 2), -6))
    w = sum(sols(sp.Eq(X - 3, -6)) + sols(sp.Eq(X + 2, -6)))
    add(start + 4, "H", "Laske yhtälön (x − 3)(x + 2) = −6 ratkaisujen summa. Tarkista ratkaisut sijoittamalla alkuperäiseen yhtälöön.", sum(s), w,
        "Tulon nollasääntö ei päde, kun tulo on −6. Sijoita ratkaisusi: tulon pitää olla −6.",
        ["x² − x − 6 = −6.", "x(x − 1) = 0, joten x = 0 tai x = 1.", "Tarkistus: (0 − 3)(0 + 2) = −6 ja (1 − 3)(1 + 2) = −6.", f"Summa on {num(sum(s))}."], {"k": -6})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
