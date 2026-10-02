#!/usr/bin/env python3
"""EXT-02 ME (lukio level): which expressions equal the given power expression? Equivalence flags are
computed numerically with sympy; non-equivalent options are the misreadings a^0 = 0, a^-n negative or a
product, and tagged with the topic."""
import random

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

from gen_common import base_item, cli

TEMPLATE = "ext02_me"
TID, CODE = "EXT-02", "ME"
GENERIC = "a⁰ = 1 ja a⁻ⁿ = 1/aⁿ. Sijoita lukuarvo ja vertaa, esim. x = 2."
TR = standard_transformations + (implicit_multiplication_application,)
X = sp.Symbol("x", positive=True)


def pyx(t):
    return t.replace("²", "**2").replace("−", "-").replace("·", "*").replace("^", "**")


def item(rng, n, lops, syll, level, prompt, reference, samples, opts, steps, date, run):
    ref = parse_expr(pyx(reference), local_dict={"x": X}, transformations=TR)
    options = []
    for text, mtag in opts:
        e = parse_expr(pyx(text), local_dict={"x": X}, transformations=TR)
        eq = all(abs(complex(sp.N((e - ref).subs(X, s[0])))) < 1e-9 for s in samples)
        options.append({"text": text, "equivalent": eq, "misconception": None if eq else mtag})
    rng.shuffle(options)
    for i, o in enumerate(options):
        o["id"] = "abcdefgh"[i]
    options = [{k: o[k] for k in ("id", "text", "equivalent", "misconception")} for o in options]
    ids = [o["id"] for o in options if o["equivalent"]]
    final = " ja ".join(ids)
    return base_item(TID, CODE, n, lops, ["G2"], syll, level, "none", prompt,
                     {"reference": reference.replace("−", "-").replace("·", "*"), "variables": ["x"],
                      "samples": samples, "options": options},
                     steps, final, "Oikein: käytä a⁰ = 1 ja a⁻ⁿ = 1/aⁿ.", TEMPLATE,
                     {"reference": reference}, date, run, generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(4417)
    S = [[2], [3], [5]]
    items = [
        item(rng, start, ["MAY1.04", "MAA5.05"], "MAA", "P",
             "Mitkä lausekkeista ovat yhtä suuria kuin x⁻² kaikilla x ≠ 0? Valitse kaikki.",
             "x^(-2)", S,
             [("1/x^2", None), ("(1/x)^2", None), ("−2x", "EXT-02"), ("−x^2", "EXT-02")],
             ["x⁻² = 1/x² = (1/x)².", "Kun x = 2, x⁻² = 1/4, mutta −2x = −4 ja −x² = −4."], date, run),
        item(rng, start + 1, ["MAY1.04", "MAA5.05"], "MAA", "T",
             "Mitkä lausekkeista ovat yhtä suuria kuin x⁰ + x⁻¹ kaikilla x ≠ 0? Valitse kaikki.",
             "x^0 + x^(-1)", S,
             [("1 + 1/x", None), ("(x + 1)/x", None), ("1/x", "EXT-02"), ("1 − x", "EXT-02")],
             ["x⁰ = 1 ja x⁻¹ = 1/x, joten summa on 1 + 1/x = (x + 1)/x.", "Lauseke 1/x unohtaa, että x⁰ = 1, ei 0."], date, run),
        item(rng, start + 2, ["MAY1.04"], "MAB", "T",
             "Hiukkasen massa on 2 · 10⁻ˣ grammaa, kun x on positiivinen kokonaisluku. Mitkä lausekkeista ovat yhtä suuria kuin 2 · 10⁻ˣ? Valitse kaikki.",
             "2 · 10^(-x)", S,
             [("2/10^x", None), ("2 · (1/10)^x", None), ("−20x", "EXT-02"), ("2 · 10^x", "EXT-02")],
             ["10⁻ˣ = 1/10ˣ = (1/10)ˣ.", "Kun x = 2, massa on 2/100 = 0,02 g, mutta 2 · 10² = 200 ja −20x = −40 eivät sovi."], date, run),
        item(rng, start + 3, ["MAY1.04", "MAA5.05"], "MAA", "H",
             "Mitkä lausekkeista ovat yhtä suuria kuin (x⁻¹)⁻² kaikilla x ≠ 0? Valitse kaikki.",
             "(x^(-1))^(-2)", S,
             [("x^2", None), ("x^2 · x^0", None), ("x^(-3)", "EXT-02"), ("1/x^2", "EXT-02")],
             ["Potenssin potenssissa eksponentit kerrotaan: (−1) · (−2) = 2, joten tulos on x².", "x⁻³ syntyy, jos eksponentit lasketaan yhteen."], date, run),
        item(rng, start + 4, ["MAY1.04"], "MAB", "H",
             "Bakteerien määrä on aluksi 500 ja se kaksinkertaistuu joka tunti, joten N(x) = 500 · 2ˣ. Mitkä lausekkeista ovat yhtä suuria kuin 500 · 2⁻ˣ eli määrä x tuntia ennen alkuhetkeä? Valitse kaikki.",
             "500 · 2^(-x)", S,
             [("500/2^x", None), ("500 · (1/2)^x", None), ("−500 · 2^x", "EXT-02"), ("500 · 2^x", "EXT-02")],
             ["2⁻ˣ = 1/2ˣ, joten määrä pienenee, kun mennään ajassa taaksepäin.", "Kun x = 2, määrä on 500/4 = 125. Lauseke −500 · 2ˣ antaisi negatiivisen määrän."], date, run),
    ]
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
