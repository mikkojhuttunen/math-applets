#!/usr/bin/env python3
"""LFUN-02 MC: linearity applied to every function (squares of sums, sin, lg).
Correct values are computed with sympy; each distractor is the linear misreading."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lfun02_mc"
TID, CODE = "LFUN-02", "MC"
X = sp.Symbol("x")
GENERIC = "Funktio ei yleensä jaa summaa: f(a + b) on eri asia kuin f(a) + f(b). Kokeile lukuarvoilla."


def disp(e):
    return show(e).replace(" · ", "")


def poly(e):
    return show(sp.expand(e)).replace(" · ", "").replace("^2", "²")


def square_item(rng, n, a_expr, lops, syll, level, stem, date, run):
    right = sp.expand(a_expr**2)
    a, b = sp.Poly(a_expr, X).all_coeffs()
    lin = sp.expand(a**2 * X**2 + b**2)
    other = sp.expand(a**2 * X**2 + a * b * X + b**2)
    assert len({right, lin, other}) == 3
    opts, cid = mc_options(
        rng, (poly(right), f"Oikein: ({disp(a_expr)})² = ({disp(a_expr)})({disp(a_expr)}), joten keskimmäinen tulo 2ab on mukana."),
        [(poly(lin), "LFUN-02", "Neliö ei jaa summaan: puuttuu keskimmäinen tulo 2ab. Kokeile x = 1."),
         (poly(other), None, "Keskimmäinen termi on 2ab, ei ab.")])
    steps = [f"({disp(a_expr)})² = ({disp(a_expr)})({disp(a_expr)})", f"= {poly(right)}"]
    return base_item(TID, CODE, n, [lops], ["G2"], syll, level, "none", stem.format(e=disp(a_expr)),
                     {"options": opts, "correct": [cid]}, steps, poly(right), "Oikein.", TEMPLATE,
                     {"expr": str(a_expr)}, date, run, misconceptions=[TID, "ALG-09"], generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2201)
    items = [
        square_item(rng, start, X + 5, "MAA2.01", "MAA", "P", "Mikä on lausekkeen ({e})² sievennetty muoto?", date, run),
        square_item(rng, start + 1, 2 * X + 3, "MAB2.07", "MAB", "P",
                    "Neliön muotoisen laatan sivun pituus on {e} metriä. Mikä lauseke antaa laatan pinta-alan (m²)?", date, run),
        square_item(rng, start + 2, X - 4, "MAB2.07", "MAB", "T",
                    "Neliön muotoisesta pellosta (sivu x metriä) otetaan pois 4 metrin kaista. Uuden neliön sivu on {e} metriä. Mikä on sen pinta-ala?", date, run),
    ]
    # sin(a + b)
    a, b = sp.pi / 6, sp.pi / 3
    right, lin = sp.simplify(sp.sin(a + b)), sp.simplify(sp.sin(a) + sp.sin(b))
    prod = sp.simplify(sp.sin(a) * sp.sin(b))
    assert right == 1 and lin != right
    opts, cid = mc_options(rng, (show(right), "Oikein: sin(π/6 + π/3) = sin(π/2) = 1."),
                           [(show(lin), "LFUN-02", "Sini ei jaa summaa. Lisäksi sini ei koskaan ylitä lukua 1, mutta tämä arvo on yli 1."),
                            (show(prod), None, "Tulo ei tule tästäkään säännöstä: laske ensin kulma π/6 + π/3.")])
    items.append(base_item(TID, CODE, start + 3, ["MAA2.01", "MAA5.03"], ["G3"], "MAA", "T", "none",
                           "Mikä on sin(π/6 + π/3) tarkka arvo? Tarkista vastauksesi järkevyys: sinin arvot ovat välillä −1…1.",
                           {"options": opts, "correct": [cid]},
                           ["π/6 + π/3 = π/2.", "sin(π/2) = 1."], "1", "Oikein.", TEMPLATE, {"a": "pi/6", "b": "pi/3"},
                           date, run, misconceptions=[TID, "LTRI-02"], generic_wrong=GENERIC))
    # lg 20 + lg 5
    p, q = 20, 5
    right = sp.log(p * q, 10)
    assert sp.simplify(right) == 2
    opts, cid = mc_options(rng, ("2", "Oikein: lg 20 + lg 5 = lg(20 · 5) = lg 100 = 2."),
                           [(f"lg {p + q} ≈ {show(round(float(sp.log(p + q, 10)), 1))}".replace(".", ","), "LFUN-02",
                             "Logaritmien summa on tulon logaritmi, ei summan logaritmi."),
                            (f"lg 20 · lg 5 ≈ {show(round(float(sp.log(p, 10) * sp.log(q, 10)), 2))}".replace(".", ","), "LEXP-01",
                             "Logaritmien summaa ei lasketa kertomalla logaritmeja keskenään.")])
    items.append(base_item(TID, CODE, start + 4, ["MAA2.01", "MAA5.07"], ["G2"], "MAA", "H", "none",
                           "Laske lg 20 + lg 5.", {"options": opts, "correct": [cid]},
                           ["lg a + lg b = lg(ab).", "lg 20 + lg 5 = lg 100 = 2."], "2", "Oikein.", TEMPLATE,
                           {"p": p, "q": q}, date, run, misconceptions=[TID, "LEXP-01"], generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
