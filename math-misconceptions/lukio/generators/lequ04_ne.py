#!/usr/bin/env python3
"""LEQU-04 NE (lukio level): the square root is taken across a quadratic inequality (x^2 < a gives
x < sqrt(a)). Interval answers are computed with sympy."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "lequ04_ne"
TID, CODE = "LEQU-04", "NE"
X = sp.Symbol("x", real=True)
GENERIC = "Neliöjuuri ei säilytä epäyhtälöä näin: √(x²) = |x|. Ratkaise |x| < a tai siirrä kaikki vasemmalle ja tekijöi."


def ivs(rel):
    s = sp.solve_univariate_inequality(rel, X, relational=False)
    parts = list(s.args) if isinstance(s, sp.Union) else [s]
    parts.sort(key=lambda p: float(p.inf) if p.inf != -sp.oo else -1e18)
    return [{"lo": None if p.inf == -sp.oo else str(p.inf), "hi": None if p.sup == sp.oo else str(p.sup),
             "lo_closed": bool((not p.left_open) and p.inf != -sp.oo), "hi_closed": bool((not p.right_open) and p.sup != sp.oo)}
            for p in parts]


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, g, level, prompt, ref_text, rel, wrong_text, wfb, steps, final, params):
        ans = {"kind": "interval", "variable": "x", "reference": ref_text, "intervals": ivs(rel)}
        items.append(base_item(TID, CODE, n, ["MAA2.06"], [g], "MAA", level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": wrong_text, "misconception": TID, "feedback": wfb}]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    add(start, "G4", "T", "Ratkaise epäyhtälö x² < 4.", "x² < 4", X ** 2 < 4, "x < 2",
        "Esimerkiksi x = −5 toteuttaa epäyhtälön x < 2, mutta (−5)² = 25, joka ei ole pienempi kuin 4.",
        ["x² − 4 < 0, eli (x − 2)(x + 2) < 0.", "Tulo on negatiivinen, kun tekijät ovat erimerkkiset: −2 < x < 2."], "−2 < x < 2", {"a": 4})
    add(start + 1, "G4", "T", "Ratkaise epäyhtälö x² > 9.", "x² > 9", X ** 2 > 9, "x > 3",
        "Myös x = −4 toteuttaa epäyhtälön: (−4)² = 16 > 9. Tämä ratkaisu puuttuu.",
        ["x² − 9 > 0, eli (x − 3)(x + 3) > 0.", "Tulo on positiivinen, kun molemmat tekijät ovat samanmerkkiset: x < −3 tai x > 3."], "x < −3 tai x > 3", {"a": 9})
    add(start + 2, "G4", "T", "Ratkaise epäyhtälö x² ≤ 25. Tarkista tulos sijoittamalla x = −4.", "x² ≤ 25", X ** 2 <= 25, "x ≤ 5",
        "Epäyhtälöä x ≤ 5 toteuttaa myös x = −10, mutta (−10)² = 100 > 25. Alaraja −5 puuttuu.",
        ["x² − 25 ≤ 0, eli (x − 5)(x + 5) ≤ 0.", "−5 ≤ x ≤ 5.", "Tarkistus: (−4)² = 16 ≤ 25."], "−5 ≤ x ≤ 5", {"a": 25})
    add(start + 3, "G4", "H", "Ratkaise epäyhtälö (x − 1)² < 4.", "(x − 1)² < 4", (X - 1) ** 2 < 4, "x < 3",
        "Epäyhtälö (x − 1)² < 4 tarkoittaa |x − 1| < 2, eli myös x − 1 > −2. Esimerkiksi x = −5: (−6)² = 36 > 4.",
        ["Merkitse t = x − 1: t² < 4, joten −2 < t < 2.", "Siis −2 < x − 1 < 2, eli −1 < x < 3."], "−1 < x < 3", {"shift": 1, "a": 4})
    add(start + 4, "G4", "H", "Ratkaise epäyhtälö 2x² ≥ 18.", "2x² ≥ 18", 2 * X ** 2 >= 18, "x ≥ 3",
        "Myös x = −5 toteuttaa epäyhtälön: 2 · 25 = 50 ≥ 18. Ratkaisu x ≤ −3 puuttuu.",
        ["Jaa kahdella: x² ≥ 9, eli (x − 3)(x + 3) ≥ 0.", "Tulo on ei-negatiivinen, kun x ≤ −3 tai x ≥ 3."], "x ≤ −3 tai x ≥ 3", {"c": 2, "a": 18})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
