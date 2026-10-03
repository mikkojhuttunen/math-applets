#!/usr/bin/env python3
"""LTRI-03 MC (lukio level): the radian is not seen as a measure of angle; pi is read as 180.
Values are computed with sympy; distractors carry the topic tag when they treat the radian as a degree."""
import math
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "ltri03_mc"
TID, CODE = "LTRI-03", "MC"
GENERIC = "π rad vastaa kulmaa 180°. Radiaani on kulman mitta, ja 1 rad ≈ 57,3°."


def make_items(run, date, count=5, start=1):
    rng = random.Random(3011)
    items = []

    def add(n, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, ["MAA5.01"], ["G2"], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: 180 degrees in radians
    assert sp.rad(180) == sp.pi
    add(start, "P", "Mikä on kulma 180° radiaaneina?",
        ("π", "Oikein: puolikas kierros on π rad."),
        [("180", TID, "Luku 180 on kulma asteina. Radiaaneina puolikas kierros on π ≈ 3,14."),
         ("π/180", None, "Tämä on yhden asteen suuruus radiaaneina."),
         ("2π", None, "2π rad on koko kierros, 360°.")],
        ["Koko kierros on 360° = 2π rad.", "Puolikas kierros on 180° = π rad."], "π", {"deg": 180})
    # 2: pi rad in degrees
    assert sp.deg(sp.pi) == 180
    add(start + 1, "P", "Kulma on π radiaania. Kuinka monta astetta se on?",
        ("180°", "Oikein: π rad = 180°."),
        [("3,14°", TID, "Luku π ≈ 3,14 on radiaanien määrä. Asteina π rad on 180°, ei 3,14°."),
         ("90°", None, "90° on π/2 rad."),
         ("360°", None, "360° on 2π rad.")],
        ["π rad on puolikas kierros.", "Puolikas kierros on 180°."], "180°", {"rad": "pi"})
    # 3: calculator mode
    r = float(sp.sin(2))
    d = float(sp.sin(sp.rad(2)))
    assert abs(r - 0.909) < 0.001 and abs(d - 0.035) < 0.001
    add(start + 2, "T", "Laskin antaa tulokseksi sin 2 ≈ 0,035, vaikka kulma 2 on annettu radiaaneina. Mikä on todennäköisin syy?",
        ("Laskin oli astetilassa ja luki kulman 2°. Radiaaneina sin 2 ≈ 0,909.", "Oikein: asetus ratkaisee, tulkitaanko luku asteiksi vai radiaaneiksi."),
        [("Laskin oli radiaanitilassa, ja sin 2 on todella 0,035.", TID, "Radiaaneina kulma 2 rad ≈ 114,6°, ja sen sini on lähes 1. Arvo 0,035 on sin 2°."),
         ("Sinifunktio antaa pieniä arvoja, kun kulma on kokonaisluku.", None, "Sini vaihtelee välillä −1 ja 1 kokonaislukukulmilla aivan kuten muillakin."),
         ("Luku 2 on pyöristetty nollaksi.", None, "Pyöristys ei selitä arvoa: sin 0 = 0, ei 0,035.")],
        ["2 rad = 2 · 180°/π ≈ 114,6°.", "sin 114,6° ≈ 0,909, kun taas sin 2° ≈ 0,035."], "Laskin oli astetilassa", {"x": 2})
    # 4: size of one radian
    deg1 = float(sp.deg(1))
    assert abs(deg1 - 57.2958) < 1e-3
    add(start + 3, "T", "Kuinka suuri kulma 1 radiaani on asteina?",
        ("noin 57,3°", "Oikein: 1 rad = 180°/π ≈ 57,3°."),
        [("1°", TID, "Radiaani ja aste ovat eri yksiköt. Yksi radiaani on paljon suurempi kuin yksi aste."),
         ("noin 3,14°", None, "Luku 3,14 on π eikä kulma asteina."),
         ("noin 0,017°", None, "Tämä on 1° radiaaneina (≈ 0,017 rad), ei 1 rad asteina.")],
        ["π rad = 180°, joten 1 rad = 180°/π.", "180°/π ≈ 57,3°."], "noin 57,3°", {"rad": 1})
    # 5: arc length with the angle in radians
    r_, th = 5, 2
    arc = r_ * th
    deg_arc = float(2 * sp.pi * r_ * th / 360)
    assert arc == 10 and abs(deg_arc - 0.1745) < 1e-3
    add(start + 4, "K", "Ympyrän sektorin säde on 5 cm ja keskuskulma 2 rad. Mikä on sektorin kaaren pituus?",
        ("10 cm", "Oikein: kaaren pituus b = rθ = 5 · 2 = 10 cm, kun θ on radiaaneina."),
        [("noin 0,17 cm", TID, "Tässä keskuskulma 2 luetaan asteiksi. Se on kuitenkin 2 rad ≈ 114,6°."),
         ("25 cm", None, "Tämä on sektorin pinta-ala (r²θ/2 = 25 cm²) lukuna, ei kaaren pituus."),
         ("5π cm", None, "Tämä on puoliympyrän kaari. Kulma 2 rad ei ole π.")],
        ["Kaaren pituus b = rθ, kun θ on radiaaneina.", "b = 5 cm · 2 = 10 cm."], "10 cm", {"r": 5, "theta": 2})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
