#!/usr/bin/env python3
"""FUN-05 MC (lukio level): every linear function is proportional (f(2x) = 2 f(x) for f(x) = ax + b).
Function values computed with Fraction; the distractor is the proportional extrapolation."""
import random
from fractions import Fraction

from gen_common import base_item, cli, frac, mc_options, num

TEMPLATE = "fun05_mc"
TID, CODE = "FUN-05", "MC"
GENERIC = "Funktio f(x) = ax + b on verrannollinen vain, kun b = 0. Jos b ≠ 0, x:n kaksinkertaistuminen ei kaksinkertaista f(x):ää."


def lin(a, b):
    return lambda x: Fraction(a) * x + Fraction(b)


def make_items(run, date, count=5, start=1):
    rng = random.Random(2605)
    items = []

    def add(n, lops, syll, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, ["G5"], syll, level, "none", prompt, {"options": opts, "correct": [cid]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    f = lin(2, 4)
    assert f(5) == 14 and f(10) == 24 and 2 * f(5) == 28
    add(start, ["MAY1.06"], "MAA", "P", "Taksin hinta on 4 € + 2 € jokaiselta kilometriltä. Viiden kilometrin matka maksaa 14 €. Mitä kymmenen kilometrin matka maksaa?",
        (f"{num(f(10))} €", "Oikein: 4 + 2 · 10 = 24. Perusmaksu 4 € maksetaan vain kerran."),
        [(f"{num(2 * f(5))} €", TID, "Hinta ei kaksinkertaistu, koska perusmaksu 4 € ei kasva matkan mukana."),
         (f"{num(2 * 10)} €", None, "Perusmaksu 4 € puuttuu: hinta on 4 € + 2 € · 10."),
         (f"{num(f(5) + 2 * 10)} €", None, "Lisäkilometrejä on 5, ei 10: 14 € on jo viiden kilometrin hinta.")],
        ["f(x) = 4 + 2x.", "f(10) = 4 + 20 = 24."], f"{num(f(10))} €", {"a": 2, "b": 4, "x": 10})
    f = lin(8, 30)
    assert f(2) == 46 and f(6) == 78 and 3 * f(2) == 138
    add(start + 1, ["MAY1.06", "MAB4.01"], "MAB", "T", "Polkupyörän vuokra on 30 € + 8 € tunnilta. Kahden tunnin vuokra on 46 €. Mitä kuuden tunnin vuokra maksaa?",
        (f"{num(f(6))} €", "Oikein: 30 + 8 · 6 = 78."),
        [(f"{num(3 * f(2))} €", TID, "Kolminkertainen aika ei kolminkertaista hintaa, koska 30 € on kiinteä maksu."),
         (f"{num(f(2) + 6 * 8)} €", None, "Kahden tunnin hinta sisältää jo kaksi tuntia, joten lisätunteja on neljä, ei kuutta."),
         (f"{num(6 * 8)} €", None, "Kiinteä maksu 30 € puuttuu.")],
        ["f(t) = 30 + 8t.", "f(6) = 30 + 48 = 78."], f"{num(f(6))} €", {"a": 8, "b": 30, "t": 6})
    add(start + 2, ["MAY1.06"], "MAA", "T", "Mikä funktioista kuvaa suoraa verrannollisuutta (y on verrannollinen x:ään)?",
        ("f(x) = 0,5x", "Oikein: f(x) = ax ja f(0) = 0, joten kaksinkertainen x antaa kaksinkertaisen f(x):n."),
        [("f(x) = 0,5x + 2", TID, "Funktio on lineaarinen mutta f(0) = 2 ≠ 0, joten se ei ole verrannollinen."),
         ("f(x) = 2 − 0,5x", TID, "Suora laskee mutta ei kulje origon kautta, joten kyseessä ei ole suora verrannollisuus."),
         ("f(x) = 0,5x²", None, "x:n kaksinkertaistuminen nelinkertaistaa f(x):n, joten tämä ei ole suora verrannollisuus.")],
        ["Verrannollisessa funktiossa f(x) = ax.", "Vain f(x) = 0,5x on tätä muotoa."], "f(x) = 0,5x", {"a": 0.5})
    vals = [(1, 7), (2, 10), (3, 13)]
    assert [Fraction(y, x) for x, y in vals] == [7, 5, Fraction(13, 3)]
    add(start + 3, ["MAY1.06", "MAB4.01"], "MAB", "H", "Taulukossa on x = 1, 2, 3 ja y = 7, 10, 13. Mikä väite on tosi?",
        ("y ei ole verrannollinen x:ään, koska suhde y/x ei ole vakio (7, 5, 13/3).", "Oikein: verrannollisuudessa y/x olisi vakio."),
        [("y on verrannollinen x:ään, koska y kasvaa, kun x kasvaa.", TID, "Kasvaminen ei riitä. Verrannollisessa y/x on vakio ja x = 0 antaa y = 0."),
         ("y on verrannollinen x:ään, koska y kasvaa tasaisesti 3 kerrallaan.", TID, "Tasainen kasvu tarkoittaa lineaarista funktiota y = 3x + 4, mutta verrannollisuus vaatisi y = 3x."),
         ("y on verrannollinen x:ään, koska 7 + 10 = 17.", None, "Summalla ei voi perustella verrannollisuutta.")],
        ["y/x = 7, 5 ja 13/3.", "Suhde ei ole vakio, joten verrannollisuutta ei ole; y = 3x + 4."], "ei verrannollinen", {"table": vals})
    f = lin(2, 3)
    assert f(1) == 5 and f(2) == 7 and 2 * f(1) == 10
    add(start + 4, ["MAY1.06"], "MAA", "H", "Pekka väittää, että jokaiselle lineaariselle funktiolle pätee f(2x) = 2f(x). Mikä on perusteltu vastaus funktion f(x) = 2x + 3 kohdalla?",
        ("Väite on väärä: f(2 · 1) = 7, mutta 2 · f(1) = 10. Yhtälö pätisi vain, jos vakiotermi olisi 0.", "Oikein: yksi vastaesimerkki riittää kumoamaan yleisen väitteen."),
        [("Väite on tosi, koska funktion kuvaaja on suora.", TID, "Suoran kuvaaja ei riitä. Suoran täytyy kulkea origon kautta, jotta f(2x) = 2f(x)."),
         ("Väite on tosi, koska f(2) = 7 ja f(1) = 5 kasvavat molemmat.", TID, "Kasvaminen ei riitä; tarkista, onko f(2) kaksi kertaa f(1)."),
         ("Väite on väärä, koska funktio on lineaarinen.", None, "Lineaarisuus ei riitä perusteeksi. Perustele laskemalla vastaesimerkki.")],
        ["f(1) = 5, f(2) = 7.", "2 · f(1) = 10 ≠ 7, joten väite ei päde."], "väite on väärä", {"a": 2, "b": 3})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
