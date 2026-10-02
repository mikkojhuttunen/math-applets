#!/usr/bin/env python3
"""FUN-05 NE (lukio level): every linear function is proportional. Values computed with Fraction;
the wrong answer is the proportional extrapolation k * f(x0)."""
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "fun05_ne"
TID, CODE = "FUN-05", "NE"
GENERIC = "Funktio f(x) = ax + b on verrannollinen vain, kun b = 0. Jos b ≠ 0, x:n kaksinkertaistuminen ei kaksinkertaista f(x):ää."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, value, unit, wrong, wfb, steps, final, params):
        assert float(value) != float(wrong)
        ans = {"kind": "number", "value": float(value), "tolerance": 0.01}
        if unit:
            ans["unit"] = unit
        items.append(base_item(TID, CODE, n, lops, ["G5"], syll, level, "none", prompt,
                               {"answer": ans, "wrong": [{"match": float(wrong), "misconception": TID, "feedback": wfb}],
                                "input_hint": "Kirjoita luku"}, steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    f = lambda x: 3 * x + 4
    add(start, ["MAY1.06"], "MAA", "T", "Funktio on f(x) = 3x + 4, ja f(5) = 19. Laske f(10).",
        f(10), None, 2 * f(5), "f(10) ei ole 2 · f(5), koska vakiotermi 4 ei kaksinkertaistu.",
        ["f(10) = 3 · 10 + 4 = 34."], "34", {"a": 3, "b": 4, "x": 10})
    g = lambda t: 5 + Fraction(1, 10) * t
    add(start + 1, ["MAY1.06", "MAB4.01"], "MAB", "P", "Puhelinliittymä maksaa 5 € kuukaudessa ja lisäksi 0,10 € minuutilta. Sadan minuutin puhelut maksavat 15 €. Mitä kolmensadan minuutin puhelut maksavat euroina?",
        g(300), "€", 3 * g(100), "Hinta ei kolminkertaistu, koska kuukausimaksu 5 € maksetaan vain kerran.",
        ["Hinta = 5 + 0,10 · 300 = 35."], "35 €", {"fixed": 5, "per_min": 0.1, "minutes": 300})
    h = lambda k: 40 + 25 * k
    add(start + 2, ["MAY1.06", "MAB4.01"], "MAB", "T", "Kuntosalin liittymismaksu on 40 € ja kuukausimaksu 25 €. Neljän kuukauden kokonaiskustannus on 140 €. Mikä on kahdentoista kuukauden kokonaiskustannus euroina?",
        h(12), "€", 3 * h(4), "Kustannus ei kolminkertaistu, koska liittymismaksu 40 € maksetaan vain kerran.",
        ["Kustannus = 40 + 25 · 12 = 340."], "340 €", {"fixed": 40, "per_month": 25, "months": 12})
    a = Fraction(13 - 7, 3 - 1)
    b = 7 - a
    ff = lambda x: a * x + b
    assert (a, b) == (3, 4)
    add(start + 3, ["MAY1.06"], "MAA", "H", "Lineaarisen funktion arvot ovat f(1) = 7 ja f(3) = 13. Laske f(6).",
        ff(6), None, 2 * ff(3), "f(6) ei ole 2 · f(3). Selvitä ensin kulmakerroin ja vakiotermi.",
        ["Kulmakerroin a = (13 − 7)/(3 − 1) = 3.", "b = 7 − 3 = 4, joten f(x) = 3x + 4.", "f(6) = 22."], "22", {"points": [[1, 7], [3, 13]], "x": 6})
    w = lambda t: 6 + 3 * t
    est = Fraction(w(4) * 10, 4)
    assert w(4) == 18 and est == Fraction(45)
    add(start + 4, ["MAY1.06"], "MAA", "H", "Altaassa on aluksi 6 litraa vettä, ja siihen lasketaan vettä 3 litraa minuutissa. Neljän minuutin jälkeen vettä on 18 litraa. Eeva arvioi, että kymmenen minuutin jälkeen vettä on 45 litraa. Laske vesimäärä litroina ja tarkista Eevan arvio.",
        w(10), "l", est, "45 l saadaan kertomalla 18 l luvulla 10/4, mutta alkuvesi 6 l ei kasva ajan mukana.",
        ["Vesimäärä = 6 + 3 · 10 = 36 l.", "Eevan arvio 45 l on liian suuri: se olettaa, että määrä on verrannollinen aikaan."], "36 l", {"initial": 6, "rate": 3, "minutes": 10})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
