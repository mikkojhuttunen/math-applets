#!/usr/bin/env python3
"""LTRI-03 NE (lukio level): the radian is not seen as a measure of angle; pi is read as 180.
All answers are numbers computed with sympy; the wrong answers are typical readings of the radian
as a degree (or the calculator left in degree mode)."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "ltri03_ne"
TID, CODE = "LTRI-03", "NE"
GENERIC = "π rad vastaa kulmaa 180°. Radiaani on kulman mitta, ja 1 rad ≈ 57,3°."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, value, tol, wrongs, steps, final, params, hint="Kirjoita luku"):
        for w, _ in wrongs:
            assert abs(float(w) - value) > tol
        items.append(base_item(TID, CODE, n, ["MAA5.01"], ["G2"], "MAA", level, "none", prompt,
                               {"answer": {"kind": "number", "value": value, "tolerance": tol},
                                "wrong": [{"match": w, "misconception": TID, "feedback": f} for w, f in wrongs],
                                "input_hint": hint},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    v = round(float(sp.rad(180)), 3)
    add(start, "P", "Kuinka monta radiaania kulma 180° on? Pyöristä kolmeen desimaaliin.", v, 0.0006,
        [(180, "Luku 180 on kulma asteina. Puolikas kierros on radiaaneina π ≈ 3,142.")],
        ["180° = π rad.", "π ≈ 3,142."], show(v), {"deg": 180})
    v = round(float(sp.deg(1)), 1)
    add(start + 1, "P", "Kuinka monta astetta kulma 1 rad on? Pyöristä kymmenesosiin.", v, 0.06,
        [(1, "Radiaani ja aste ovat eri yksiköt. 1 rad on noin 57,3°, ei 1°.")],
        ["1 rad = 180°/π.", "180°/π ≈ 57,3°."], show(v), {"rad": 1})
    v = round(float(sp.sin(2)), 3)
    d = round(float(sp.sin(sp.rad(2))), 3)
    assert v == 0.909 and d == 0.035
    add(start + 2, "T", "Laske sin 2, kun kulma 2 on radiaaneina. Pyöristä kolmeen desimaaliin.", v, 0.0006,
        [(d, "Arvo 0,035 on sin 2°, eli laskin oli astetilassa. Radiaaneina 2 rad ≈ 114,6°.")],
        ["2 rad ≈ 114,6°.", "sin 2 ≈ 0,909."], show(v), {"x": 2})
    v = round(float(sp.rad(270)), 3)
    assert v == 4.712
    add(start + 3, "T", "Kuinka monta radiaania kulma 270° on? Pyöristä kolmeen desimaaliin.", v, 0.0006,
        [(270, "Luku 270 on kulma asteina. Kulma 270° on 3π/2 rad."),
         (3.142, "Tämä on π, eli 180°. Kulma 270° on 3π/2 rad.")],
        ["270° = 3/4 kierrosta = 3/4 · 2π rad.", "3π/2 ≈ 4,712."], show(v), {"deg": 270})
    r_, th = 5, 2
    v = r_ * th
    d = round(float(2 * sp.pi * r_ * th / 360), 2)
    add(start + 4, "H", "Sektorin säde on 5 cm ja keskuskulma 2 rad. Laske kaaren pituus (cm). Vihje: kaari on lyhyempi kuin koko ympyrän kehä 2π · 5 ≈ 31,4 cm.", v, 0.01,
        [(d, "Arvo 0,17 syntyy, kun 2 luetaan asteiksi. Kulma 2 rad on noin 114,6°, ja kaaren pituus on rθ.")],
        ["b = rθ = 5 · 2.", "b = 10 cm."], show(v), {"r": 5, "theta": 2})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
