#!/usr/bin/env python3
"""LVEC-01 MC: length of a sum is not the sum of lengths. Lengths computed with sympy."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lvec01_mc"
TID, CODE = "LVEC-01", "MC"
GENERIC = "Summavektorin pituus on yleensä pienempi kuin pituuksien summa. Piirrä vektorit peräkkäin tai laske koordinaateilla."


def vlen(v):
    return sp.sqrt(sum(c**2 for c in v))


def vtxt(v):
    return f"({show(v[0])}, {show(v[1])})"


def item(n, prompt, correct, wrongs, steps, final, level, g, params, date, run, rng, lops=("MAA4.07",)):
    opts, cid = mc_options(rng, correct, wrongs)
    return base_item(TID, CODE, n, list(lops), g, "MAA", level, "none", prompt,
                     {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                     generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(4701)
    items = []
    # 1: perpendicular, coordinates
    a, b = (3, 0), (0, 4)
    s = (a[0] + b[0], a[1] + b[1])
    assert vlen(s) == 5
    items.append(item(start, f"Vektorit ovat a = {vtxt(a)} ja b = {vtxt(b)}. Mikä on summavektorin a + b pituus?",
                      ("5", "Oikein: a + b = (3, 4) ja |a + b| = √(9 + 16) = 5."),
                      [("7", TID, "7 on pituuksien summa |a| + |b|. Summavektorin pituus lasketaan summavektorin koordinaateista."),
                       ("1", None, "1 on pituuksien erotus. Laske vektorin (3, 4) pituus.")],
                      [f"a + b = {vtxt(s)}.", f"|a + b| = √({s[0]}² + {s[1]}²) = {vlen(s)}."], "5", "P", ["G2"],
                      {"a": a, "b": b}, date, run, rng))
    # 2: perpendicular forces
    f1, f2 = 6, 8
    res = vlen((f1, f2))
    assert res == 10
    items.append(item(start + 1, f"Kappaleeseen vaikuttaa {f1} N:n voima itään ja {f2} N:n voima pohjoiseen. Kuinka suuri on kokonaisvoima?",
                      ("10 N", "Oikein: voimat ovat kohtisuorassa, joten pituus on √(6² + 8²) = 10."),
                      [("14 N", TID, "Voimien suuruudet eivät summaudu, kun suunnat ovat eri. Käytä Pythagoraan lausetta."),
                       ("2 N", None, "2 N olisi voimien erotus, kun ne vetävät vastakkain.")],
                      [f"Voimat ovat kohtisuorassa: F = √({f1}² + {f2}²) = {res}."], "10 N", "P", ["G2"],
                      {"f1": f1, "f2": f2}, date, run, rng))
    # 3: non-trivial, integer sum length
    a, b = (1, 2), (3, -2)
    s = (a[0] + b[0], a[1] + b[1])
    assert vlen(s) == 4
    wrong = f"√5 + √13 ≈ {show(round(float(vlen(a) + vlen(b)), 1))}"
    items.append(item(start + 2, f"Vektorit ovat a = {vtxt(a)} ja b = {vtxt(b)}. Mikä on |a + b|?",
                      ("4", "Oikein: a + b = (4, 0), joten |a + b| = 4."),
                      [(wrong, TID, "Tämä on |a| + |b|. Summavektorin pituus lasketaan summavektorin koordinaateista."),
                       ("√18 ≈ 4,2", None, "√(5 + 13) toimii vain, kun vektorit ovat kohtisuorassa. Laske ensin a + b.")],
                      [f"a + b = {vtxt(s)}.", f"|a + b| = {vlen(s)}."], "4", "T", ["G2"],
                      {"a": a, "b": b}, date, run, rng))
    # 4: when does equality hold (justification)
    items.append(item(start + 3, "Millä ehdolla |a + b| = |a| + |b|?",
                      ("Kun vektorit ovat samansuuntaiset", "Oikein: vain silloin vektorit asettuvat peräkkäin samaa suuntaa, ja pituudet lasketaan yhteen."),
                      [("Aina", TID, "Kokeile kohtisuoria vektoreita (3, 0) ja (0, 4): |a + b| = 5, mutta |a| + |b| = 7."),
                       ("Kun vektorit ovat kohtisuorassa", None, "Silloin |a + b| = √(|a|² + |b|²), mikä on pienempi kuin |a| + |b|."),
                       ("Ei koskaan", None, "Samansuuntaisille vektoreille yhtälö pätee, esim. (2, 0) ja (3, 0).")],
                      ["Piirrä vektorit peräkkäin. Summavektori on yhtä pitkä kuin pituuksien summa vain, jos reitti on suora.",
                       "Muuten kolmioepäyhtälö |a + b| < |a| + |b| pätee."],
                      "Vain samansuuntaisille vektoreille", "T", ["G4"], {"case": "equality"}, date, run, rng))
    # 5: plausibility, possible lengths
    la, lb = 5, 2
    lo, hi = abs(la - lb), la + lb
    cands = [3, 5, 7, 8]
    impossible = [c for c in cands if not lo <= c <= hi]
    assert impossible == [8]
    items.append(item(start + 4, f"Vektorien pituudet ovat |a| = {la} ja |b| = {lb}. Mikä seuraavista ei voi olla |a + b|?",
                      ("8", f"Oikein: |a + b| on enintään {la} + {lb} = 7."),
                      [("3", TID, "3 on mahdollinen: vektorit vastakkaissuuntaiset, 5 − 2 = 3. Summavektorin pituus ei ole aina 7."),
                       ("5", TID, "5 on mahdollinen, esimerkiksi kun vektorit ovat sopivassa kulmassa. Summavektorin pituus ei ole aina 7."),
                       ("7", None, "7 on mahdollinen: vektorit samansuuntaiset.")],
                      [f"Kolmioepäyhtälö: {lo} ≤ |a + b| ≤ {hi}.", "Luku 8 on suurempi kuin 7."], "8", "H", ["G4"],
                      {"la": la, "lb": lb}, date, run, rng))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
