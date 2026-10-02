#!/usr/bin/env python3
"""LFUN-02 ME: which expressions equal the given one? Equivalence flags are computed with
sympy (numerically, on sample points); non-equivalent options are the linear misreading
f(a + b) = f(a) + f(b) and are tagged with the topic."""
import random

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

from gen_common import base_item, cli

TEMPLATE = "lfun02_me"
TID, CODE = "LFUN-02", "ME"
GENERIC = "Funktio ei yleensä jaa summaa: f(a + b) on eri asia kuin f(a) + f(b). Sijoita lukuja ja vertaa."
TR = standard_transformations + (implicit_multiplication_application,)
SYM = {c: sp.Symbol(c, positive=True) for c in "xy"}


def pyx(text):
    return text.replace("²", "**2").replace("√", "sqrt").replace("−", "-").replace("·", "*").replace("^", "**")


def item(rng, n, lops, syll, level, g, prompt, reference, variables, samples, opts, steps, final, mis, date, run):
    ref = parse_expr(pyx(reference), local_dict=dict(SYM), transformations=TR)
    options = []
    for text, mtag in opts:
        e = parse_expr(pyx(text), local_dict={**SYM, "ln": sp.log, "lg": lambda v: sp.log(v, 10)}, transformations=TR)
        eq = all(abs(complex(sp.N((e - ref).subs(dict(zip((SYM[v] for v in variables), s)))))) < 1e-9 for s in samples)
        options.append({"text": text, "equivalent": eq, "misconception": None if eq else mtag})
    # fixed shuffle
    rng.shuffle(options)
    for i, o in enumerate(options):
        o["id"] = "abcdefgh"[i]
    options = [{k: o[k] for k in ("id", "text", "equivalent", "misconception")} for o in options]
    ids = [o["id"] for o in options if o["equivalent"]]
    final_text = f"{' ja '.join(ids)}" if len(ids) < 3 else ", ".join(ids)
    return base_item(TID, CODE, n, lops, g, syll, level, "none", prompt,
                     {"reference": reference.replace("²", "^2").replace("−", "-").replace("√", "sqrt").replace("·", "*"),
                      "variables": variables, "samples": samples, "options": options},
                     steps, final_text, "Oikein: funktio ei jaa summaa, käytä sen omia laskusääntöjä.",
                     TEMPLATE, {"reference": reference}, date, run, misconceptions=mis, generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2203)
    items = [
        item(rng, start, ["MAB2.07"], "MAB", "P", ["G2"],
             "Neliön muotoisen laatan sivu on x + 4 metriä. Mitkä lausekkeista antavat laatan pinta-alan (m²)? Valitse kaikki.",
             "(x + 4)^2", ["x"], [[1], [2], [5]],
             [("x² + 8x + 16", None), ("(x + 4)(x + 4)", None), ("x² + 16", "LFUN-02"), ("x² + 4x + 16", "ALG-09")],
             ["Pinta-ala on sivun neliö: (x + 4)² = (x + 4)(x + 4).", "Kerrotaan auki: x² + 4x + 4x + 16 = x² + 8x + 16."],
             None, [TID, "ALG-09"], date, run),
        item(rng, start + 1, ["MAB2.07"], "MAB", "T", ["G3"],
             "Pellon sivu on 3x − 2 metriä. Mitkä lausekkeista ovat yhtä suuria kuin pellon pinta-ala? Perustele valintasi sijoittamalla x = 1.",
             "(3x - 2)^2", ["x"], [[1], [2], [3]],
             [("9x² − 12x + 4", None), ("(3x − 2)(3x − 2)", None), ("9x² + 4", "LFUN-02"), ("9x² − 4", "ALG-09")],
             ["Kun x = 1, sivu on 1 ja pinta-ala 1.", "9x² + 4 antaa 13 ja 9x² − 4 antaa 5, joten ne eivät kelpaa; 9x² − 12x + 4 antaa 1."],
             None, [TID, "ALG-09"], date, run),
        item(rng, start + 2, ["MAA2.01", "MAA5.03"], "MAA", "T", ["G2"],
             "Mitkä lausekkeista ovat yhtä suuria kuin sin(2x) kaikilla x:n arvoilla? Valitse kaikki.",
             "sin(2*x)", ["x"], [[1], [2], [3]],
             [("2 sin(x) cos(x)", None), ("sin(x)cos(x) + cos(x)sin(x)", None), ("2 sin(x)", "LFUN-02"), ("sin(x) + sin(x)cos(x)", "LTRI-02")],
             ["Kaksinkertaisen kulman kaava: sin(2x) = 2 sin x cos x.", "Sini ei ole lineaarinen: sin(2x) ≠ 2 sin x. Kokeile x = π/2."],
             None, [TID, "LTRI-02"], date, run),
        item(rng, start + 3, ["MAA2.01"], "MAA", "H", ["G2"],
             "Mitkä lausekkeista ovat yhtä suuria kuin √(x² + y²), kun x > 0 ja y > 0? Valitse kaikki.",
             "sqrt(x^2 + y^2)", ["x", "y"], [[3, 4], [1, 2], [2, 5]],
             [("√(y² + x²)", None), ("(x² + y²)^(1/2)", None), ("x + y", "LFUN-02"), ("√(x²) + √(y²)", "LFUN-02")],
             ["Juuri on potenssi 1/2, joten √(x² + y²) = (x² + y²)^(1/2) ja yhteenlaskun järjestys ei vaikuta.", "Kun x = 3 ja y = 4, arvo on 5, mutta x + y = 7."],
             None, [TID], date, run),
        item(rng, start + 4, ["MAA2.01", "MAA5.07"], "MAA", "H", ["G2"],
             "Mitkä lausekkeista ovat yhtä suuria kuin ln(xy²), kun x > 0 ja y > 0? Valitse kaikki.",
             "ln(x*y^2)", ["x", "y"], [[2, 3], [1, 5], [4, 2]],
             [("ln(x) + 2 ln(y)", None), ("ln(x) + ln(y²)", None), ("ln(x + y²)", "LFUN-02"), ("ln(x) + ln(y)", "LEXP-01")],
             ["ln(xy²) = ln x + ln(y²) = ln x + 2 ln y.", "Summan logaritmi ei ole logaritmien summa, ja eksponentti y² tulee mukaan."],
             None, [TID, "LEXP-01"], date, run),
    ]
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
