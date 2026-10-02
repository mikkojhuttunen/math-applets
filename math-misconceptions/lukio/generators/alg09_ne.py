#!/usr/bin/env python3
"""ALG-09 NE (lukio level): square of a sum. Answers computed with sympy."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "alg09_ne"
TID, CODE = "ALG-09", "NE"
X = sp.Symbol("x")
GENERIC = "(a + b)² on (a + b)(a + b), ja siinä on myös keskimmäinen tulo 2ab. Kokeile lukuarvoilla, esim. a = 1, b = 1."


def pretty(e):
    return show(sp.expand(e)).replace(" · ", "").replace("^2", "²")


def make_items(run, date, count=5, start=1):
    items = []
    # 1: expression (x - 8)^2
    right, lin = sp.expand((X - 8) ** 2), X**2 + 64
    items.append(base_item(TID, CODE, start, ["MAA2.01"], ["G2"], "MAA", "P", "none", "Kerro auki ja sievennä (x − 8)².",
                           {"answer": {"kind": "expression", "variables": ["x"], "reference": str(right), "samples": [[0], [1], [2], [-3]]},
                            "wrong": [{"match": "x^2 + 64", "misconception": TID, "feedback": "Keskimmäinen tulo −2 · 8x = −16x puuttuu."}],
                            "input_hint": "esim. x^2 + 1"},
                           ["(x − 8)² = (x − 8)(x − 8).", f"= {pretty(right)}."], pretty(right), "Oikein.", TEMPLATE, {"e": "x - 8"}, date, run, generic_wrong=GENERIC))
    # 2: 47^2 by (50 - 3)^2
    right, lin = (50 - 3) ** 2, 50**2 + 3**2
    assert right == 47**2 == 2209 and lin == 2509
    items.append(base_item(TID, CODE, start + 1, ["MAA2.01"], ["G2"], "MAA", "T", "none",
                           "Laske 47² päässä kirjoittamalla 47 = 50 − 3 ja käyttämällä binomikaavaa.",
                           {"answer": {"kind": "number", "value": right},
                            "wrong": [{"match": lin, "misconception": TID, "feedback": "50² + 3² jättää pois keskimmäisen tulon −2 · 50 · 3 = −300."}]},
                           ["(50 − 3)² = 50² − 2 · 50 · 3 + 3².", "= 2500 − 300 + 9 = 2209."], str(right), "Oikein.", TEMPLATE, {"n": 47}, date, run, generic_wrong=GENERIC))
    # 3: area increase expression (MAB)
    right = sp.expand((X + 2) ** 2 - X**2)
    assert right == 4 * X + 4
    items.append(base_item(TID, CODE, start + 2, ["MAB2.07"], ["G2"], "MAB", "T", "none",
                           "Neliön muotoisen aukion sivu on x metriä. Aukiota levennetään 2 metriä sekä pituus- että leveyssuunnassa, jolloin siitä tulee neliö, jonka sivu on x + 2. Kirjoita lauseke pinta-alan lisäykselle (m²).",
                           {"answer": {"kind": "expression", "variables": ["x"], "reference": str(right), "samples": [[0], [1], [2], [5]]},
                            "wrong": [{"match": "4", "misconception": TID, "feedback": "(x + 2)² ei ole x² + 4; keskimmäinen tulo 4x puuttuu."}],
                            "input_hint": "esim. 3x + 1"},
                           ["Uusi pinta-ala (x + 2)² = x² + 4x + 4.", "Lisäys on x² + 4x + 4 − x² = 4x + 4."], pretty(right), "Oikein.", TEMPLATE, {"d": 2}, date, run, generic_wrong=GENERIC))
    # 4: a^2 + b^2 (MAB)
    s, p = 9, 20
    right = s**2 - 2 * p
    assert right == 41
    items.append(base_item(TID, CODE, start + 3, ["MAB2.07"], ["G2"], "MAB", "H", "none",
                           f"Kahden neliön sivujen pituuksien summa on {s} m ja tulo {p} m². Laske neliöiden yhteenlaskettu pinta-ala (m²).",
                           {"answer": {"kind": "number", "value": right, "unit": "m²"},
                            "wrong": [{"match": s**2, "misconception": TID, "feedback": "(a + b)² ei ole a² + b²; erotus on 2ab."}]},
                           [f"a² + b² = (a + b)² − 2ab = {s}² − 2 · {p}.", f"= {s**2} − {2 * p} = {right}."], f"{right} m²", "Oikein.",
                           TEMPLATE, {"s": s, "p": p}, date, run, generic_wrong=GENERIC))
    # 5: plausibility, difference (a+b)^2 - (a^2+b^2)
    a, b = 3, 4
    right = (a + b) ** 2 - (a**2 + b**2)
    assert right == 2 * a * b == 24
    items.append(base_item(TID, CODE, start + 4, ["MAA2.01"], ["G2"], "MAA", "H", "none",
                           f"Oppilas väittää, että (a + b)² = a² + b². Laske erotus (a + b)² − (a² + b²), kun a = {a} ja b = {b}, ja päättele, mitä erotus kertoo väitteestä.",
                           {"answer": {"kind": "number", "value": right},
                            "wrong": [{"match": 0, "misconception": TID, "feedback": f"({a} + {b})² = 49 ja {a}² + {b}² = 25, joten erotus ei ole 0."}]},
                           [f"({a} + {b})² = 49 ja {a}² + {b}² = 25.", "Erotus 24 = 2ab, joten väite on väärä."], str(right), "Oikein.", TEMPLATE, {"a": a, "b": b}, date, run, generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
