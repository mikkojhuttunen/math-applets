#!/usr/bin/env python3
"""ALG-09 ME (lukio level): which expressions equal the given square of a sum or difference? Equivalence
flags are computed numerically with sympy; non-equivalent options drop the middle term or confuse the
square with a difference of squares, and are tagged with the topic."""
import random

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

from gen_common import base_item, cli

TEMPLATE = "alg09_me"
TID, CODE = "ALG-09", "ME"
GENERIC = "(a + b)² on (a + b)(a + b), ja siinä on myös keskimmäinen tulo 2ab. Sijoita lukuarvot ja vertaa."
TR = standard_transformations + (implicit_multiplication_application,)
SYM = {c: sp.Symbol(c, positive=True) for c in "abxy"}


def pyx(t):
    return t.replace("²", "**2").replace("−", "-").replace("·", "*").replace("^", "**")


def item(rng, n, lops, syll, level, prompt, reference, variables, samples, opts, steps, date, run):
    ref = parse_expr(pyx(reference), local_dict=dict(SYM), transformations=TR)
    options = []
    for text, mtag in opts:
        e = parse_expr(pyx(text), local_dict=dict(SYM), transformations=TR)
        eq = all(abs(complex(sp.N((e - ref).subs({SYM[v]: val for v, val in zip(variables, s)})))) < 1e-9 for s in samples)
        options.append({"text": text, "equivalent": eq, "misconception": None if eq else mtag})
    rng.shuffle(options)
    for i, o in enumerate(options):
        o["id"] = "abcdefgh"[i]
    options = [{k: o[k] for k in ("id", "text", "equivalent", "misconception")} for o in options]
    ids = [o["id"] for o in options if o["equivalent"]]
    return base_item(TID, "ME", n, lops, ["G2"], syll, level, "none", prompt,
                     {"reference": reference.replace("−", "-").replace("·", "*"), "variables": variables,
                      "samples": samples, "options": options},
                     steps, " ja ".join(ids), "Oikein: binomin neliössä on aina keskimmäinen tulo.", TEMPLATE,
                     {"reference": reference}, date, run, generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(5521)
    items = [
        item(rng, start, ["MAA2.01"], "MAA", "P",
             "Mitkä lausekkeista ovat yhtä suuria kuin (x + 5)² kaikilla x:n arvoilla? Valitse kaikki.",
             "(x + 5)^2", ["x"], [[1], [2], [4]],
             [("x^2 + 10x + 25", None), ("(x + 5)(x + 5)", None), ("x^2 + 25", "ALG-09"), ("x^2 + 5x + 25", "ALG-09")],
             ["(x + 5)² = x² + 2 · x · 5 + 5² = x² + 10x + 25.", "Kun x = 1, (x + 5)² = 36, mutta x² + 25 = 26."], date, run),
        item(rng, start + 1, ["MAB2.07"], "MAB", "T",
             "Neliön muotoisen tontin sivu on 2x − 3 metriä. Mitkä lausekkeista ovat yhtä suuria kuin tontin pinta-ala (m²) kaikilla sallituilla x:n arvoilla? Valitse kaikki.",
             "(2*x - 3)^2", ["x"], [[2], [3], [5]],
             [("4x^2 − 12x + 9", None), ("(3 − 2x)^2", None), ("4x^2 − 9", "ALG-09"), ("4x^2 + 9", "ALG-09")],
             ["(2x − 3)² = 4x² − 12x + 9; myös (3 − 2x)² on sama, koska vastaluvun neliö on sama.", "Kun x = 3, pinta-ala on 9. Lauseke 4x² − 9 antaisi 27 ja 4x² + 9 antaisi 45."], date, run),
        item(rng, start + 2, ["MAA2.01"], "MAA", "T",
             "Mitkä lausekkeista ovat yhtä suuria kuin (x + y)² − (x − y)², kun x > 0 ja y > 0? Valitse kaikki.",
             "(x + y)^2 - (x - y)^2", ["x", "y"], [[1, 2], [3, 1], [2, 5]],
             [("4xy", None), ("2xy + 2xy", None), ("0", "ALG-09"), ("2x^2 + 2y^2", "ALG-09")],
             ["(x + y)² = x² + 2xy + y² ja (x − y)² = x² − 2xy + y², joten erotus on 4xy.", "Kun x = 1 ja y = 2, erotus on 9 − 1 = 8, mutta 0 ja 2x² + 2y² = 10 eivät täsmää."], date, run),
        item(rng, start + 3, ["MAA2.01"], "MAA", "H",
             "Mitkä lausekkeista ovat yhtä suuria kuin (x + 1/x)², kun x > 0? Valitse kaikki.",
             "(x + 1/x)^2", ["x"], [[1], [2], [3]],
             [("x^2 + 2 + 1/x^2", None), ("(x^2 + 1)^2/x^2", None), ("x^2 + 1/x^2", "ALG-09"), ("x^2 + 1/x^2 + 1", "ALG-09")],
             ["(x + 1/x)² = x² + 2 · x · (1/x) + 1/x² = x² + 2 + 1/x².", "Kun x = 1, arvo on 4, mutta x² + 1/x² = 2 ja x² + 1/x² + 1 = 3."], date, run),
        item(rng, start + 4, ["MAB2.07"], "MAB", "H",
             "Neliön muotoisen alueen sivu on a metriä ja sitä laajennetaan b metriä joka suuntaan sivulla. Mitkä lausekkeista ovat yhtä suuria kuin pinta-alan lisäys (a + b)² − a²? Oletetaan a > 0 ja b > 0. Valitse kaikki.",
             "(a + b)^2 - a^2", ["a", "b"], [[1, 2], [3, 1], [2, 5]],
             [("2ab + b^2", None), ("b(2a + b)", None), ("b^2", "ALG-09"), ("2ab", "ALG-09")],
             ["(a + b)² − a² = a² + 2ab + b² − a² = 2ab + b² = b(2a + b).", "Kun a = 1 ja b = 2, lisäys on 9 − 1 = 8. Lauseke b² antaa 4 ja 2ab antaa 4: kulmaneliö b² tai kaksi suorakaidetta 2ab eivät yksin riitä."], date, run),
    ]
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, "ME")
