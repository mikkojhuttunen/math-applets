#!/usr/bin/env python3
"""EXT-02 MC (lukio level): integer exponents (2^3 = 6, a^0 = 0, 2^-1 = -2). Values computed with Fraction."""
import random
from fractions import Fraction

from gen_common import base_item, cli, frac, mc_options, num

TEMPLATE = "ext02_mc"
TID, CODE = "EXT-02", "MC"
GENERIC = "Potenssi on toistettu kertolasku, a⁰ = 1 ja negatiivinen eksponentti tarkoittaa käänteislukua: a⁻ⁿ = 1/aⁿ."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1402)
    items = []

    def add(n, lops, syll, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, ["G2"], syll, level, "none", prompt, {"options": opts, "correct": [cid]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    v = Fraction(2) ** -3
    assert v == Fraction(1, 8)
    add(start, ["MAY1.04", "MAA5.05"], "MAA", "P", "Mikä on 2⁻³?",
        (frac(v), "Oikein: 2⁻³ = 1/2³ = 1/8."),
        [(num(-6), TID, "Eksponentti ei kerro lukua: 2⁻³ ei ole −3 · 2."),
         (num(-8), TID, "Negatiivinen eksponentti ei tee tuloksesta negatiivista, vaan tarkoittaa käänteislukua."),
         ("1/6", None, "Nimittäjässä on potenssi 2³ = 8, ei tulo 2 · 3.")],
        ["a⁻ⁿ = 1/aⁿ.", "2⁻³ = 1/2³ = 1/8."], frac(v), {"a": 2, "n": -3})
    v = Fraction(3) ** 0 + Fraction(2) ** -2
    assert v == Fraction(5, 4)
    add(start + 1, ["MAY1.04", "MAA5.05"], "MAA", "T", "Laske 3⁰ + 2⁻².",
        (frac(v), "Oikein: 3⁰ = 1 ja 2⁻² = 1/4, summa on 5/4."),
        [(num(-4), TID, "3⁰ ei ole 0 vaan 1, ja 2⁻² ei ole −4 vaan 1/4."),
         (frac(Fraction(1, 4)), TID, "3⁰ = 1, ei 0."),
         ("2", None, "2⁻² = 1/4, ei 1.")],
        ["3⁰ = 1 ja 2⁻² = 1/2² = 1/4.", "1 + 1/4 = 5/4."], frac(v), {"expr": "3^0+2^-2"})
    cm = Fraction(10) ** -2 * 100
    assert cm == 1
    add(start + 2, ["MAY1.04"], "MAB", "P", "Mikä on 10⁻² metriä senttimetreinä?",
        ("1 cm", "Oikein: 10⁻² m = 1/100 m = 0,01 m = 1 cm."),
        [("−100 cm", TID, "Negatiivinen eksponentti ei tarkoita negatiivista lukua vaan käänteislukua: 10⁻² = 1/100."),
         ("100 cm", None, "10⁻² on 1/100, ei 100."),
         ("0,1 cm", None, "10⁻² = 0,01 m, ja 0,01 m = 1 cm.")],
        ["10⁻² = 1/10² = 0,01.", "0,01 m = 1 cm."], "1 cm", {"base": 10, "n": -2})
    v = Fraction(4) * Fraction(10) ** -3
    assert v == Fraction(4, 1000)
    add(start + 3, ["MAY1.04"], "MAB", "T", "Mikä luku on 4 · 10⁻³ desimaalilukuna?",
        ("0,004", "Oikein: 10⁻³ = 0,001, joten 4 · 10⁻³ = 0,004."),
        [("−4000", TID, "Negatiivinen eksponentti ei tee luvusta negatiivista. 10⁻³ on 1/1000."),
         ("0,0004", None, "10⁻³ = 0,001: pilkku siirtyy kolme paikkaa vasemmalle, ei neljää."),
         ("0,04", None, "Pilkku siirtyy kolme paikkaa vasemmalle, ei kahta.")],
        ["10⁻³ = 1/10³ = 0,001.", "4 · 0,001 = 0,004."], "0,004", {"c": 4, "n": -3})
    assert Fraction(2) ** 3 / Fraction(2) ** 3 == 1 and Fraction(2) ** (3 - 3) == 1
    add(start + 4, ["MAY1.04", "MAA5.05"], "MAA", "H", "Mikä perustelu osoittaa oikein, että a⁰ = 1 (a ≠ 0)?",
        ("a³/a³ = 1, ja potenssien jakosäännön mukaan a³/a³ = a³⁻³ = a⁰.", "Oikein: jakosääntö ja jakolasku a/a = 1 antavat yhdessä a⁰ = 1."),
        [("Nollakertainen kertominen on 0, joten a⁰ = 0.", TID, "a⁰ ei ole ”a kerrottuna nollalla”. Potenssi aⁿ on n tekijää a, ja tyhjä tulo on 1."),
         ("a⁰ = a, koska eksponentti 0 ei muuta lukua.", None, "Eksponentti 1 jättää luvun ennalleen: a¹ = a. Eksponentti 0 antaa 1."),
         ("Se on pelkkä sopimus, eikä sille ole perustelua.", None, "Sopimukselle on perustelu: se pitää potenssisäännöt voimassa.")],
        ["a³/a³ = 1.", "Jakosäännöllä a³/a³ = a⁰, joten a⁰ = 1."], "a⁰ = 1", {"a": "a", "n": 3})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
