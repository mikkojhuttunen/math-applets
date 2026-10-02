#!/usr/bin/env python3
"""EXT-02 NE (lukio level): integer exponents. Values computed with Fraction; wrong answers read a power
as a product, a^0 as 0 and a^-n as negative."""
from fractions import Fraction

from gen_common import base_item, cli, frac

TEMPLATE = "ext02_ne"
TID, CODE = "EXT-02", "NE"
GENERIC = "Potenssi on toistettu kertolasku, a⁰ = 1 ja negatiivinen eksponentti tarkoittaa käänteislukua: a⁻ⁿ = 1/aⁿ."


def rat(v):
    return {"kind": "rational", "value": f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)}


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, answer, wrong, steps, final, hint, params):
        items.append(base_item(TID, CODE, n, lops, ["G2"], syll, level, "none", prompt,
                               {"answer": answer, "wrong": wrong, "input_hint": hint}, steps, final, "Oikein.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    def w(m, fb):
        return {"match": m, "misconception": TID, "feedback": fb}

    v = Fraction(2) ** -3
    add(start, ["MAY1.04", "MAA5.05"], "MAA", "P", "Laske 2⁻³. Anna vastaus murtolukuna.", rat(v),
        [w("-6", "2⁻³ ei ole −3 · 2."), w("-8", "Negatiivinen eksponentti tarkoittaa käänteislukua, ei negatiivista lukua.")],
        ["2⁻³ = 1/2³.", "= 1/8."], frac(v), "esim. 1/4", {"a": 2, "n": -3})
    v = Fraction(5) ** 0 + Fraction(3) ** -2
    assert v == Fraction(10, 9)
    add(start + 1, ["MAY1.04", "MAA5.05"], "MAA", "T", "Laske 5⁰ + 3⁻². Anna vastaus murtolukuna.", rat(v),
        [w("-9", "5⁰ = 1, ei 0, ja 3⁻² = 1/9, ei −9."), w("1/9", "5⁰ = 1, ei 0.")],
        ["5⁰ = 1 ja 3⁻² = 1/3² = 1/9.", "1 + 1/9 = 10/9."], frac(v), "esim. 3/2", {"expr": "5^0+3^-2"})
    v = Fraction(4) * Fraction(10) ** -2
    assert v == Fraction(1, 25)
    add(start + 2, ["MAY1.04"], "MAB", "T", "Laske 4 · 10⁻² desimaalilukuna.",
        {"kind": "number", "value": 0.04},
        [w("-400", "10⁻² on 1/100, ei −100."), w("-0.04", "Negatiivinen eksponentti ei tee luvusta negatiivista.")],
        ["10⁻² = 1/100 = 0,01.", "4 · 0,01 = 0,04."], "0,04", "Kirjoita desimaaliluku", {"c": 4, "n": -2})
    v = Fraction(2, 3) ** -2
    assert v == Fraction(9, 4)
    add(start + 3, ["MAY1.04", "MAA5.05"], "MAA", "H", "Laske (2/3)⁻². Anna vastaus supistettuna murtolukuna.", rat(v),
        [w("-4/9", "Negatiivinen eksponentti ei tee tuloksesta negatiivista."), w("4/9", "Negatiivinen eksponentti kääntää murtoluvun: (2/3)⁻² = (3/2)².")],
        ["(2/3)⁻² = (3/2)².", "= 9/4."], frac(v), "esim. 5/2", {"base": "2/3", "n": -2})
    v = Fraction(500) * Fraction(2) ** -3
    assert v == Fraction(125, 2)
    add(start + 4, ["MAY1.04"], "MAB", "H",
        "Bakteerien määrä on N(t) = 500 · 2^t, missä t on aika tunteina. Montako bakteeria oli 3 tuntia ennen hetkeä t = 0? Laske N(−3).",
        {"kind": "number", "value": 62.5},
        [w("-4000", "2⁻³ on 1/8, ei −8."), w("-62.5", "Määrä ei voi olla negatiivinen: 2⁻³ = 1/8.")],
        ["N(−3) = 500 · 2⁻³.", "= 500 · 1/8 = 62,5."], "62,5", "Kirjoita luku", {"n0": 500, "t": -3})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
