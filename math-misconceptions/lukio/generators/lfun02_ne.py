#!/usr/bin/env python3
"""LFUN-02 NE: linearity applied to every function (square root, squares of sums, sin).
Answers computed with sympy; the typical wrong answer is the linear misreading."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lfun02_ne"
TID, CODE = "LFUN-02", "NE"
X = sp.Symbol("x")
GENERIC = "Funktio ei yleensä jaa summaa: f(a + b) on eri asia kuin f(a) + f(b). Kokeile lukuarvoilla."


def disp(e):
    return show(e).replace(" · ", "")


def pretty(e):
    return show(sp.expand(e)).replace(" · ", "").replace("^2", "²")


def make_items(run, date, count=5, start=1):
    items = []
    # 1: sqrt(a^2 + b^2)
    a, b = 5, 12
    right = sp.sqrt(a**2 + b**2)
    assert right == 13
    items.append(base_item(TID, CODE, start, ["MAA2.01"], ["G2"], "MAA", "P", "none",
                           f"Laske √({a}² + {b}²).",
                           {"answer": {"kind": "number", "value": int(right)},
                            "wrong": [{"match": a + b, "misconception": TID,
                                       "feedback": "Neliöjuuri ei jaa summaa: √(a² + b²) ei ole a + b. Laske ensin juuren sisällä."}]},
                           [f"{a}² + {b}² = {a**2 + b**2}.", f"√{a**2 + b**2} = {right}."], str(right),
                           "Oikein.", TEMPLATE, {"a": a, "b": b}, date, run, generic_wrong=GENERIC))
    # 2, 3: expand a square, expression answers
    for k, (expr, lops, syll, level) in enumerate([(X + 7, ["MAA2.01"], "MAA", "T"), (3 * X - 2, ["MAB2.07"], "MAB", "P")]):
        right = sp.expand(expr**2)
        c, d = sp.Poly(expr, X).all_coeffs()
        lin = sp.expand(c**2 * X**2 + d**2)
        assert lin != right
        items.append(base_item(TID, CODE, start + 1 + k, lops, ["G2"], syll, level, "none",
                               f"Kerro auki ja sievennä ({disp(expr)})².",
                               {"answer": {"kind": "expression", "variables": ["x"], "reference": str(right),
                                           "samples": [[0], [1], [2], [-3]]},
                                "wrong": [{"match": pretty(lin).replace("²", "^2"), "misconception": TID,
                                           "feedback": "Neliö ei jaa summaan: puuttuu keskimmäinen tulo 2ab."}],
                                "input_hint": "esim. x^2 + 1"},
                               [f"({disp(expr)})² = ({disp(expr)})({disp(expr)}).", f"= {pretty(right)}."],
                               pretty(right), "Oikein.", TEMPLATE, {"expr": str(expr)}, date, run, generic_wrong=GENERIC))
    # 4: number (a + b)^2 with numbers, MAB
    a, b = 6, 2
    items.append(base_item(TID, CODE, start + 3, ["MAB2.07"], ["G2"], "MAB", "P", "none",
                           f"Laatan sivut ovat a = {a} m ja b = {b} m. Neliön muotoisen alueen sivu on a + b. Laske alueen pinta-ala (m²).",
                           {"answer": {"kind": "number", "value": (a + b) ** 2, "unit": "m²"},
                            "wrong": [{"match": a**2 + b**2, "misconception": TID,
                                       "feedback": "(a + b)² ei ole a² + b². Laske ensin sivu a + b ja korota se toiseen."}]},
                           [f"Sivu on {a} + {b} = {a + b} m.", f"Pinta-ala on {a + b}² = {(a + b) ** 2} m²."],
                           f"{(a + b) ** 2} m²", "Oikein.", TEMPLATE, {"a": a, "b": b}, date, run, generic_wrong=GENERIC))
    # 5: plausibility check, sin(a + b)
    right = sp.simplify(sp.sin(sp.pi / 6 + sp.pi / 3))
    lin = sp.simplify(sp.sin(sp.pi / 6) + sp.sin(sp.pi / 3))
    assert right == 1 and float(lin) > 1
    items.append(base_item(TID, CODE, start + 4, ["MAA2.01", "MAA5.03"], ["G3"], "MAA", "H", "none",
                           "Oppilas laski sin(π/6 + π/3) = sin(π/6) + sin(π/3) ≈ 1,37. Perustele, miksi tulos ei voi olla oikein, ja laske sitten oikea arvo.",
                           {"answer": {"kind": "number", "value": 1},
                            "wrong": [{"match": 1.37, "misconception": TID,
                                       "feedback": "Sinin arvo ei voi olla yli 1. Sini ei jaa summaa: laske ensin kulma π/6 + π/3 = π/2."}]},
                           ["Sini ei koskaan ylitä lukua 1, mutta 1,37 > 1.", "π/6 + π/3 = π/2 ja sin(π/2) = 1."], "1",
                           "Oikein.", TEMPLATE, {"a": "pi/6", "b": "pi/3"}, date, run, generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
