#!/usr/bin/env python3
"""LVEC-03 NE (lukio level): the dot product gives a vector. All answers are numbers computed
with sympy; the wrong answers are the component products a typical pupil would read off from
a1*b1, a2*b2 instead of their sum."""
import sympy as sp

from gen_common import base_item, cli, show

TEMPLATE = "lvec03_ne"
TID, CODE = "LVEC-03", "NE"
GENERIC = "Pistetulo a · b = a₁b₁ + a₂b₂ on luku, ei vektori. Komponenttien tulot lasketaan yhteen."


def pt(p):
    return f"({show(p[0])}, {show(p[1])})"


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, level, prompt, value, wrongs, steps, params, lops=None):
        for w, _ in wrongs:
            assert float(w) != float(value)
        items.append(base_item(TID, CODE, n, lops or ["MAA4.08"], ["G2"], "MAA", level, "none", prompt,
                               {"answer": {"kind": "number", "value": int(value)},
                                "wrong": [{"match": int(w), "misconception": TID, "feedback": f} for w, f in wrongs],
                                "input_hint": "Kirjoita luku"},
                               steps, show(value), "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    a, b = sp.Matrix([2, 3]), sp.Matrix([4, 1])
    add(start, "P", f"Laske pistetulo a · b, kun a = {pt(a)} ja b = {pt(b)}.", a.dot(b),
        [(a[0] * b[0], "8 on vain x-komponenttien tulo. Pistetulo on kummankin komponenttiparin tulojen summa, ja tulos on yksi luku.")],
        [f"a · b = {a[0]} · {b[0]} + {a[1]} · {b[1]}.", f"= {a[0] * b[0]} + {a[1] * b[1]} = {a.dot(b)}."], {"a": [2, 3], "b": [4, 1]})
    a, b = sp.Matrix([3, 5]), sp.Matrix([2, -1])
    add(start + 1, "P", f"Pistetulo a · b lasketaan vektoreille a = {pt(a)} ja b = {pt(b)}. Kuinka monesta luvusta tulos koostuu?", 1,
        [(2, "Pistetulon tulos on yksi luku, ei kaksikomponenttinen vektori. Tulot a₁b₁ ja a₂b₂ lasketaan yhteen.")],
        ["Pistetulo a · b = a₁b₁ + a₂b₂.", "Tulos on yksi luku (skalaari)."], {"a": [3, 5], "b": [2, -1]})
    a, b = sp.Matrix([4, -2]), sp.Matrix([1, 2])
    add(start + 2, "T", f"Laske a · b, kun a = {pt(a)} ja b = {pt(b)}.", a.dot(b),
        [(a[0] * b[0], "4 on vain x-komponenttien tulo. Lisää y-komponenttien tulo (−2) · 2 = −4."),
         (a[1] * b[1], "−4 on vain y-komponenttien tulo. Lisää x-komponenttien tulo 4 · 1 = 4.")],
        [f"a · b = {a[0]} · {b[0]} + ({show(a[1])}) · {b[1]} = {a[0] * b[0]} − {-a[1] * b[1]} = {a.dot(b)}.", "Vektorit ovat kohtisuorassa."], {"a": [4, -2], "b": [1, 2]})
    k = sp.Symbol("k")
    a, b = sp.Matrix([k, 3]), sp.Matrix([6, -2])
    sol = sp.solve(sp.Eq(a.dot(b), 0), k)
    assert sol == [1]
    add(start + 3, "T", f"Vektorit a = (k, 3) ja b = {pt(b)} ovat kohtisuorassa. Mikä on k?", sol[0],
        [(0, "k = 0 seuraa vain, jos pistetulo ajatellaan vektoriksi (6k, −6). Pistetulo on luku 6k − 6, ja se asetetaan nollaksi.")],
        ["Kohtisuorilla vektoreilla a · b = 0.", "a · b = 6k + 3 · (−2) = 6k − 6 = 0.", "Siis k = 1."], {"b": [6, -2]})
    a, b = sp.Matrix([-3, 5]), sp.Matrix([2, 1])
    d = a.dot(b)
    add(start + 4, "H", f"Oppilas laski vektoreille a = {pt(a)} ja b = {pt(b)} tuloksen a · b = {pt((a[0] * b[0], a[1] * b[1]))}. Mikä on a · b oikeasti?", d,
        [(a[0] * b[0], "−6 on vain x-komponenttien tulo, ja pistetulo on yksi luku."),
         (a[1] * b[1], "5 on vain y-komponenttien tulo. Pistetulo on tulojen summa.")],
        [f"a · b = ({show(a[0])}) · {b[0]} + {a[1]} · {b[1]} = {a[0] * b[0]} + {a[1] * b[1]} = {d}.", "Oppilaan vastaus oli vektori, mutta pistetulo on luku."], {"a": [-3, 5], "b": [2, 1]})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
