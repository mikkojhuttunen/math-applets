#!/usr/bin/env python3
"""LVEC-03 MC (lukio level): the dot product gives a vector. The dot product is a number,
a1*b1 + a2*b2; the typical wrong answer multiplies the components separately. Values are computed
with sympy; distractors carry the misconception tag."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lvec03_mc"
TID, CODE = "LVEC-03", "MC"
GENERIC = "Pistetulo a · b = a₁b₁ + a₂b₂ on luku, ei vektori. Komponenttien tulot lasketaan yhteen."


def pt(p):
    return f"({show(p[0])}, {show(p[1])})"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1403)
    items = []

    def add(n, level, prompt, correct, wrongs, steps, final, params, lops=None):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops or ["MAA4.08"], ["G2"], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: a = (2, 3), b = (4, 1)
    a, b = sp.Matrix([2, 3]), sp.Matrix([4, 1])
    d = a.dot(b)
    comp = (a[0] * b[0], a[1] * b[1])
    add(start, "P", f"Vektorit ovat a = {pt(a)} ja b = {pt(b)}. Mikä on pistetulo a · b?",
        (show(d), f"Oikein: {a[0]} · {b[0]} + {a[1]} · {b[1]} = {d}."),
        [(pt(comp), TID, "Pistetulo on luku, ei vektori. Komponenttien tulot lasketaan yhteen."),
         (show(a[0] + b[0] + a[1] + b[1]), None, "Komponentit kerrotaan keskenään, ei lasketa yhteen."),
         (pt(a + b), None, "Tämä on summavektori a + b, ei pistetulo.")],
        [f"a · b = {a[0]} · {b[0]} + {a[1]} · {b[1]}.", f"a · b = {comp[0]} + {comp[1]} = {d}."], show(d), {"a": [2, 3], "b": [4, 1]})
    # 2: what kind of object
    add(start + 1, "P", "Vektorien a ja b pistetulo a · b on...",
        ("luku, jolla ei ole suuntaa.", "Oikein: pistetulo on skalaari."),
        [("vektori, jonka komponentit ovat vektorien vastinkomponenttien tulot.", TID, "Vektorien komponenttien tulot lasketaan yhteen, ja tulos on luku."),
         ("vektori, joka on kohtisuorassa vektoreihin a ja b nähden.", None, "Näin toimii ristitulo avaruudessa, ei pistetulo."),
         ("aina positiivinen luku.", None, "Pistetulo voi olla negatiivinen, esimerkiksi (1, 0) · (−1, 0) = −1.")],
        ["Pistetulo a · b = a₁b₁ + a₂b₂ on yksi luku.", "Luvulla ei ole suuntaa, joten se ei ole vektori."], "Luku", {})
    # 3: perpendicular
    a, b = sp.Matrix([3, -2]), sp.Matrix([2, 3])
    d = a.dot(b)
    assert d == 0
    comp = (a[0] * b[0], a[1] * b[1])
    add(start + 2, "T", f"Vektorit ovat a = {pt(a)} ja b = {pt(b)}. Mitä pistetulo kertoo niiden asennosta?",
        (f"a · b = {d}, joten vektorit ovat kohtisuorassa.", f"Oikein: {a[0]} · {b[0]} + ({show(a[1])}) · {b[1]} = 0."),
        [(f"a · b = {pt(comp)}, joka ei ole nollavektori, joten vektorit eivät ole kohtisuorassa.", TID, "Pistetulo ei ole vektori. Laske komponenttien tulojen summa: se on 0."),
         (f"a · b = {d}, joten vektorit ovat yhdensuuntaiset.", None, "Pistetulo 0 tarkoittaa kohtisuoruutta. Yhdensuuntaisilla vektoreilla pistetulo on pituuksien tulo tai sen vastaluku."),
         (f"a · b = {a[0] + b[0] + a[1] + b[1]}, joten ne eivät ole kohtisuorassa.", None, "Komponentit kerrotaan keskenään ja tulot lasketaan yhteen.")],
        [f"a · b = {a[0]} · {b[0]} + ({show(a[1])}) · {b[1]} = {6} − {6} = 0.", "Pistetulo 0 tarkoittaa, että vektorit ovat kohtisuorassa."], "Kohtisuorassa", {"a": [3, -2], "b": [2, 3]})
    # 4: from lengths and angle
    la, lb, ang = 3, 4, 60
    d = sp.nsimplify(la * lb * sp.cos(sp.rad(ang)))
    assert d == 6
    add(start + 3, "H", f"Vektorien pituudet ovat |a| = {la} ja |b| = {lb}, ja niiden välinen kulma on {ang}°. Mikä on a · b?",
        (show(d), f"Oikein: {la} · {lb} · cos {ang}° = {d}."),
        [(f"vektori, jonka pituus on {la * lb}", TID, "Pistetulo on luku |a||b|cos α, ei vektori."),
         (show(la * lb), None, "Tämä unohtaa tekijän cos 60° = 1/2."),
         (show(sp.nsimplify(la * lb * sp.sin(sp.rad(ang)))), None, "Pistetulossa käytetään kosinia, ei sinia.")],
        [f"a · b = |a||b|cos α = {la} · {lb} · cos {ang}°.", f"cos {ang}° = 1/2, joten a · b = {d}."], show(d), {"la": la, "lb": lb, "angle": ang},
        lops=["MAA4.08", "MAA10.02"])
    # 5: plausibility of a student's result
    a, b = sp.Matrix([2, -1]), sp.Matrix([3, 6])
    d = a.dot(b)
    comp = (a[0] * b[0], a[1] * b[1])
    add(start + 4, "H", f"Oppilas laski vektoreille a = {pt(a)} ja b = {pt(b)} tuloksen a · b = {pt(comp)}. Mikä väite osoittaa tuloksen virheelliseksi?",
        ("Pistetulo on luku, joten vastauksen täytyy olla yksi luku. Oikea tulos on 0.", f"Oikein: {a[0]} · {b[0]} + ({show(a[1])}) · {b[1]} = {d}."),
        [("Tulos on virheellinen vain siksi, että komponentit on pitänyt laskea yhteen ennen kertomista.", TID, "Komponentit kerrotaan, ja tulot lasketaan yhteen: 2 · 3 + (−1) · 6. Oleellista on, että tulos on luku."),
         ("Tulos on oikein, koska pistetulo kertoo vektorit komponenteittain.", TID, "Pistetulo ei kerro komponentteja erikseen vaan laskee tulot yhteen: a · b on luku."),
         ("Tulos on virheellinen, koska pistetulon täytyy olla positiivinen.", None, "Pistetulo voi olla negatiivinen tai nolla.")],
        [f"a · b = {a[0]} · {b[0]} + ({show(a[1])}) · {b[1]} = {a[0] * b[0]} − {-a[1] * b[1]} = {d}.", "Tulos on luku 0, joten vektorit ovat kohtisuorassa."],
        "Pistetulo on luku, 0", {"a": [2, -1], "b": [3, 6]})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
