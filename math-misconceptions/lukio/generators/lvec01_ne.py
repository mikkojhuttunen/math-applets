#!/usr/bin/env python3
"""LVEC-01 NE: length of a sum is not the sum of lengths. Numeric answers computed with sympy."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lvec01_ne"
TID, CODE = "LVEC-01", "NE"
GENERIC = "Summavektorin pituus on yleensä pienempi kuin pituuksien summa. Piirrä vektorit peräkkäin tai laske koordinaateilla."


def vlen(v):
    return sp.sqrt(sum(c**2 for c in v))


def vtxt(v):
    return f"({show(v[0])}, {show(v[1])})"


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, prompt, value, wrong_val, wfb, steps, level, g, params, unit=None):
        ans = {"kind": "number", "value": value}
        if unit:
            ans["unit"] = unit
        items.append(base_item(TID, CODE, n, ["MAA4.07"], g, "MAA", level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": wrong_val, "misconception": TID, "feedback": wfb}]},
                               steps, f"{show(value)}" + (f" {unit}" if unit else ""), "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1 perpendicular, coordinates
    a, b = (8, 0), (0, 15)
    r = vlen((a[0] + b[0], a[1] + b[1]))
    assert r == 17
    add(start, f"Vektorit ovat a = {vtxt(a)} ja b = {vtxt(b)}. Laske |a + b|.", int(r), 23,
        "23 on pituuksien summa |a| + |b|. Laske summavektorin (8, 15) pituus.",
        ["a + b = (8, 15).", f"|a + b| = √(8² + 15²) = {r}."], "P", ["G2"], {"a": a, "b": b})
    # 2 boat and current
    v1, v2 = 4, 3
    r = vlen((v1, v2))
    assert r == 5
    add(start + 1, f"Vene kulkee tyynessä vedessä {v1} m/s itään. Virta kuljettaa sitä {v2} m/s pohjoiseen. Kuinka nopeasti vene liikkuu rantaan nähden (m/s)?",
        int(r), v1 + v2, "7 m/s on nopeuksien summa. Nopeudet ovat kohtisuorassa, joten käytä Pythagoraan lausetta.",
        [f"v = √({v1}² + {v2}²) = {r} m/s."], "P", ["G2"], {"v1": v1, "v2": v2}, unit="m/s")
    # 3 opposite vectors
    m = 7
    add(start + 2, f"Vektorien pituudet ovat |a| = {m} ja |b| = {m}, ja b = −a. Laske |a + b|.", 0, 2 * m,
        "14 on pituuksien summa. Kun b = −a, vektorit kumoavat toisensa.", ["a + b = a − a = 0.", "Nollavektorin pituus on 0."],
        "T", ["G2"], {"m": m})
    # 4 minimum length (plausibility)
    la, lb = 9, 4
    add(start + 3, f"Vektorien pituudet ovat |a| = {la} ja |b| = {lb}. Mikä on pienin mahdollinen |a + b|?", la - lb, la + lb,
        "13 on suurin mahdollinen arvo, ei pienin. Pienin saadaan vastakkaissuuntaisilla vektoreilla.",
        ["Pienin arvo saadaan, kun vektorit ovat vastakkaissuuntaiset.", f"|a + b| = {la} − {lb} = {la - lb}."],
        "H", ["G4"], {"la": la, "lb": lb})
    # 5 non-trivial coordinates, integer sum length
    a, b = (7, 1), (-4, 3)
    s = (a[0] + b[0], a[1] + b[1])
    r = vlen(s)
    assert r == 5
    add(start + 4, f"Vektorit ovat a = {vtxt(a)} ja b = {vtxt(b)}. Laske |a + b|.", int(r),
        round(float(vlen(a) + vlen(b)), 2),
        "Tämä on |a| + |b|. Summavektorin pituus lasketaan summavektorin koordinaateista.",
        [f"a + b = {vtxt(s)}.", f"|a + b| = √({s[0]}² + {s[1]}²) = {r}."], "H", ["G2"], {"a": a, "b": b})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
