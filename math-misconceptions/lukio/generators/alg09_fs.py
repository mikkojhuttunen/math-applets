#!/usr/bin/env python3
"""ALG-09 FS (lukio level): square of a sum. The blanked line is the step where the binomial square is
opened with its middle term. All lines are checked by the verifier for equivalence."""
import sympy as sp

from gen_common import base_item, cli

TEMPLATE = "alg09_fs"
TID, CODE = "ALG-09", "FS"
X = sp.Symbol("x")
GENERIC = "(a + b)² on (a + b)(a + b), ja siinä on myös keskimmäinen tulo 2ab. Kokeile lukuarvoilla, esim. a = 1, b = 1."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, lines, blank, answer, steps, final, params, fb="Oikein."):
        items.append(base_item(TID, CODE, n, lops, ["G2"], syll, level, "none", prompt,
                               {"lines": lines, "blank_index": blank, "answer": answer}, steps, final, fb,
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    def expr(ref):
        return {"kind": "expression", "variables": ["x"], "reference": ref, "samples": [[1], [2], [3]]}

    add(start, ["MAA2.01"], "MAA", "P", "Täydennä puuttuva rivi: kirjoita neliö tulona.",
        ["(x + 7)²", "(x + 7)(x + 7)", "x² + 14x + 49"], 2, expr("(x + 7)(x + 7)"),
        ["(x + 7)² = (x + 7)(x + 7).", "Kerrotaan auki: x² + 7x + 7x + 49 = x² + 14x + 49."], "(x + 7)(x + 7)", {"b": 7})
    add(start + 1, ["MAA2.01"], "MAA", "T", "Täydennä puuttuva rivi: kirjoita binomikaavan kolme termiä.",
        ["(2x − 3)²", "(2x)² − 2 · 2x · 3 + 3²", "4x² − 12x + 9"], 2, expr("(2x)² − 2 · 2x · 3 + 3²"),
        ["(a − b)² = a² − 2ab + b², kun a = 2x ja b = 3.", "= 4x² − 12x + 9."], "(2x)² − 2 · 2x · 3 + 3²", {"a": "2x", "b": 3})
    assert (1 + sp.Rational(4, 100)) ** 2 == sp.Rational(10816, 10000)
    add(start + 2, ["MAB2.07"], "MAB", "T",
        "Hinta nousee kaksi vuotta peräkkäin 4 % vuodessa. Täydennä puuttuva rivi: kirjoita (1 + 0,04)² binomikaavalla kolmena termenä.",
        ["(1 + 0,04)²", "1 + 2 · 0,04 + 0,04²", "1,0816"], 2, expr("1 + 2 · 0,04 + 0,04²"),
        ["(1 + 0,04)² = 1² + 2 · 1 · 0,04 + 0,04².", "= 1 + 0,08 + 0,0016 = 1,0816."], "1 + 2 · 0,04 + 0,04²", {"rate": "4/100"},
        "Oikein: kokonaiskerroin on 1,0816, eli hinta nousee 8,16 %.")
    assert sp.solveset(sp.Eq((X + 3) ** 2, 25), X, sp.S.Reals) == sp.FiniteSet(-8, 2)
    add(start + 3, ["MAA2.01"], "MAA", "H", "Täydennä puuttuva rivi: kirjoita yhtälö, jossa vasen puoli on kerrottu auki.",
        ["(x + 3)² = 25", "x² + 6x + 9 = 25", "x² + 6x − 16 = 0", "(x + 8)(x − 2) = 0"], 2,
        {"kind": "equation", "reference": "x² + 6x + 9 = 25", "variable": "x", "solutions": [-8, 2], "equivalents": ["25 = x² + 6x + 9"]},
        ["(x + 3)² = x² + 6x + 9.", "Siirretään 25 vasemmalle: x² + 6x − 16 = 0, joka on (x + 8)(x − 2) = 0."], "x² + 6x + 9 = 25", {"c": 25})
    add(start + 4, ["MAB2.07"], "MAB", "H",
        "Neliön sivu on x metriä. Sivua pidennetään 5 metrillä. Täydennä puuttuva rivi: kirjoita pinta-alan lisäys ennen supistamista.",
        ["(x + 5)² − x²", "x² + 10x + 25 − x²", "10x + 25"], 2, expr("x² + 10x + 25 − x²"),
        ["(x + 5)² = x² + 10x + 25.", "Lisäys on x² + 10x + 25 − x² = 10x + 25 (m²)."], "x² + 10x + 25 − x²", {"d": 5},
        "Oikein: lisäys 10x + 25 sisältää kaksi suorakaidetta ja pienen neliön.")
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
