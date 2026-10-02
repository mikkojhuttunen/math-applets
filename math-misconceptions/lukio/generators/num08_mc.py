#!/usr/bin/env python3
"""NUM-08 MC (lukio level): successive percentage changes. Growth factors multiplied with Fraction."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "num08_mc"
TID, CODE = "NUM-08", "MC"
GENERIC = "Peräkkäiset prosenttimuutokset kerrotaan keskenään: jokainen lasketaan edellisen muutoksen jälkeisestä arvosta, ei alkuarvosta."


def f(p):
    return Fraction(100 + p, 100)


def make_items(run, date, count=5, start=1):
    rng = random.Random(1308)
    items = []

    def add(n, lops, g, syll, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt, {"options": opts, "correct": [cid]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    k = f(20) * f(-20)
    assert k == Fraction(24, 25)
    add(start, ["MAY1.03", "MAA9.03"], ["G4"], "MAA", "T", "Hinta nousee 20 % ja laskee sen jälkeen 20 %. Mikä on kokonaismuutos alkuperäiseen hintaan verrattuna?",
        ("−4 %", "Oikein: 1,2 · 0,8 = 0,96, joten hinta on 4 % alkuhintaa pienempi."),
        [("0 %", TID, "Nousu ja lasku eivät kumoa toisiaan, koska lasku lasketaan jo korotetusta hinnasta."),
         ("+4 %", None, "Kerroin 0,96 on pienempi kuin 1, joten hinta on laskenut."),
         ("−2 %", None, "Muutokset kerrotaan keskenään, niitä ei jaeta tai keskiarvoteta.")],
        ["Kertoimet: 1,20 ja 0,80.", f"1,20 · 0,80 = {num(float(k))}."], "−4 %", {"p": [20, -20]})
    price = 50 * f(30) * f(-30)
    assert price == Fraction(91, 2)
    add(start + 1, ["MAY1.03", "MAB6.01"], ["G4", "G8"], "MAB", "P", "Takin hinta on 50 €. Hinta nousee 30 % ja alennetaan sitten 30 %. Mikä on lopullinen hinta?",
        ("45,50 €", "Oikein: 50 · 1,3 · 0,7 = 45,50."),
        [("50,00 €", TID, "Alennus lasketaan korotetusta hinnasta 65 €, joten lasku on 19,50 €, ei 15 €."),
         ("35,00 €", None, "Tässä molemmat muutokset on laskettu alkuhinnasta: 50 − 15 − 15. Jälkimmäinen lasketaan korotetusta hinnasta."),
         ("47,50 €", None, "Tarkista kertoimet: 1,3 · 0,7 = 0,91.")],
        ["50 · 1,30 = 65.", "65 · 0,70 = 45,50."], "45,50 €", {"price": 50, "p": [30, -30]})
    k = f(10) * f(20)
    assert k == Fraction(33, 25) and k - 1 == Fraction(32, 100)
    add(start + 2, ["MAY1.03", "MAB6.01"], ["G4", "G8"], "MAB", "T", "Palkka nousee ensin 10 % ja sitten 20 %. Kuinka monta prosenttia palkka on noussut yhteensä?",
        ("32 %", "Oikein: 1,10 · 1,20 = 1,32."),
        [("30 %", TID, "Prosentit eivät yhdisty laskemalla yhteen: toinen korotus koskee jo korotettua palkkaa."),
         ("22 %", None, "Prosentteja ei lasketa yhteen eikä kerrota keskenään; kerro kertoimet 1,10 ja 1,20."),
         ("12 %", None, "Kokonaismuutos lasketaan kertoimista 1,10 · 1,20.")],
        ["1,10 · 1,20 = 1,32.", "Nousu on 32 %."], "32 %", {"p": [10, 20]})
    k = 1 - f(-10) ** 3
    assert k == Fraction(271, 1000)
    add(start + 3, ["MAY1.03", "MAA9.03"], ["G4", "G8"], "MAA", "H", "Asukasluku pienenee 10 % vuodessa kolmen vuoden ajan. Kuinka monta prosenttia asukasluku on pienentynyt yhteensä?",
        ("27,1 %", "Oikein: 0,9³ = 0,729, joten väheneminen on 27,1 %."),
        [("30 %", TID, "Kolme 10 %:n vähennystä ei ole 30 %, koska jokainen lasketaan edellisen vuoden pienemmästä arvosta."),
         ("33,1 %", None, "33,1 % olisi kolmen 10 %:n korotuksen kokonaismuutos (1,1³ − 1)."),
         ("9,0 %", None, "Kolmen vuoden muutos on 1 − 0,9³.")],
        ["Vuosikerroin on 0,90.", "0,9³ = 0,729, joten muutos on −27,1 %."], "27,1 %", {"p": -10, "years": 3})
    undo = 1 - 1 / f(25)
    assert undo == Fraction(1, 5)
    add(start + 4, ["MAY1.03", "MAB6.01"], ["G4"], "MAB", "H",
        "Arvioi ensin: hinta nousi 25 %. Kuinka monta prosenttia sen on laskettava, jotta se palaa alkuperäiseksi?",
        ("20 %", "Oikein: 1,25 · 0,80 = 1, joten lasku on 20 % korotetusta hinnasta."),
        [("25 %", TID, "Lasku lasketaan korotetusta hinnasta, joka on suurempi kuin alkuhinta, joten 25 % veisi liikaa."),
         ("30 %", None, "Tarkista: 1,25 · 0,70 = 0,875, eli hinta jäisi alle alkuhinnan."),
         ("15 %", None, "Tarkista: 1,25 · 0,85 ≈ 1,06, eli hinta jäisi yli alkuhinnan.")],
        ["Haetaan kerroin k, jolle 1,25 · k = 1.", "k = 0,80, joten lasku on 20 %."], "20 %", {"p": 25})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
