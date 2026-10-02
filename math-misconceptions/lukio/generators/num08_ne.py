#!/usr/bin/env python3
"""NUM-08 NE (lukio level): successive percentage changes. Growth factors multiplied with Fraction."""
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "num08_ne"
TID, CODE = "NUM-08", "NE"
GENERIC = "Peräkkäiset prosenttimuutokset kerrotaan keskenään: jokainen lasketaan edellisen muutoksen jälkeisestä arvosta, ei alkuarvosta."


def f(p):
    return Fraction(100 + p, 100)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, g, syll, level, prompt, answer, wrong_match, wfb, steps, final, params):
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt,
                               {"answer": answer, "wrong": [{"match": wrong_match, "misconception": TID, "feedback": wfb}],
                                "input_hint": "Kirjoita luku"}, steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    v = 80 * f(15) * f(-15)
    assert float(v) == 78.2
    add(start, ["MAY1.03", "MAA9.03"], ["G4"], "MAA", "T", "Takin hinta on 80 €. Hinta nousee 15 % ja laskee sen jälkeen 15 %. Laske lopullinen hinta euroina.",
        {"kind": "number", "value": 78.2, "tolerance": 0.01, "unit": "€"}, 80, "Lasku lasketaan korotetusta hinnasta 92 €, joten hinta ei palaa alkuarvoon.",
        ["80 · 1,15 = 92.", "92 · 0,85 = 78,20."], "78,20 €", {"price": 80, "p": [15, -15]})
    k = f(10) * f(10) - 1
    assert k == Fraction(21, 100)
    add(start + 1, ["MAY1.03", "MAB6.01"], ["G4", "G8"], "MAB", "P", "Vuokra nousee kaksi vuotta peräkkäin 10 % vuodessa. Kuinka monta prosenttia vuokra on noussut yhteensä?",
        {"kind": "number", "value": 21, "tolerance": 0.01, "unit": "%"}, 20, "Toinen korotus koskee jo korotettua vuokraa, joten kokonaisnousu on enemmän kuin 20 %.",
        ["1,10 · 1,10 = 1,21.", "Nousu on 21 %."], "21 %", {"p": [10, 10]})
    k = 1 - f(-20) * f(-20)
    assert k == Fraction(36, 100)
    add(start + 2, ["MAY1.03", "MAB6.01"], ["G4", "G8"], "MAB", "T", "Tuotteen hintaa alennetaan 20 % ja sitten vielä 20 %. Kuinka monta prosenttia hinta on laskenut yhteensä?",
        {"kind": "number", "value": 36, "tolerance": 0.01, "unit": "%"}, 40, "Toinen alennus lasketaan jo alennetusta hinnasta, joten kokonaislasku on pienempi kuin 40 %.",
        ["0,80 · 0,80 = 0,64.", "Lasku on 100 % − 64 % = 36 %."], "36 %", {"p": [-20, -20]})
    k = f(3) ** 3 - 1
    assert round(float(k) * 100, 2) == 9.27
    add(start + 3, ["MAY1.03", "MAA9.03"], ["G4", "G8"], "MAA", "H", "Palkka nousee 3 % vuodessa kolmen vuoden ajan. Kuinka monta prosenttia palkka on noussut yhteensä? Anna vastaus kahden desimaalin tarkkuudella.",
        {"kind": "number", "value": 9.27, "tolerance": 0.01, "unit": "%"}, 9, "Kolme 3 %:n korotusta ei ole 9 %, koska korotukset kertautuvat.",
        ["Vuosikerroin on 1,03.", "1,03³ ≈ 1,0927, joten nousu on noin 9,27 %."], "9,27 %", {"p": 3, "years": 3})
    undo = 1 - 1 / f(20)
    assert round(float(undo) * 100, 2) == 16.67
    add(start + 4, ["MAY1.03", "MAB6.01"], ["G4"], "MAB", "H", "Hinta nousee 20 %. Kuinka monta prosenttia sen on sen jälkeen laskettava, jotta hinta palaa alkuperäiseksi? Anna vastaus kahden desimaalin tarkkuudella.",
        {"kind": "number", "value": 16.67, "tolerance": 0.01, "unit": "%"}, 20, "Lasku lasketaan korotetusta hinnasta, joka on suurempi kuin alkuhinta, joten 20 % veisi liikaa.",
        ["Haetaan k, jolle 1,20 · k = 1.", "k = 1/1,2 ≈ 0,8333, joten lasku on noin 16,67 %."], "16,67 %", {"p": 20})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
