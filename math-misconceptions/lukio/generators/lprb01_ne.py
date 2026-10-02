#!/usr/bin/env python3
"""LPRB-01 NE: equiprobability bias. Probabilities are enumerated with itertools and reduced with Fraction;
the wrong answer counts the listed outcomes as equally likely."""
from fractions import Fraction
from itertools import product

from gen_common import base_item, cli, frac

TEMPLATE = "lprb01_ne"
TID, CODE = "LPRB-01", "NE"
GENERIC = "Laske alkeistulokset, jotka ovat yhtä todennäköisiä (esimerkiksi noppaparit tai kolikkojonot), ja jaa suotuisten määrä kaikkien määrällä."


def prob_dice(pred):
    hits = sum(1 for a, b in product(range(1, 7), repeat=2) if pred(a, b))
    return Fraction(hits, 36)


def prob_coins(n, ks):
    hits = sum(1 for r in product("KL", repeat=n) if r.count("K") in ks)
    return Fraction(hits, 2 ** n)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, p, wrong, wfb, steps, hint, params):
        items.append(base_item(TID, CODE, n, lops, ["G2", "G4"], syll, level, "none", prompt,
                               {"answer": {"kind": "rational", "value": f"{p.numerator}/{p.denominator}" if p.denominator != 1 else str(p.numerator)},
                                "wrong": [{"match": wrong, "misconception": TID, "feedback": wfb}],
                                "input_hint": hint},
                               steps, frac(p), "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    p = prob_dice(lambda a, b: a + b == 9)
    add(start, ["MAA8.04"], "MAA", "T",
        "Heitetään kahta noppaa. Mikä on todennäköisyys, että silmälukujen summa on 9? Anna vastaus supistettuna murtolukuna.",
        p, "1/11", "1/11 olettaa, että summat 2–12 ovat yhtä todennäköisiä. Laske noppaparit, joiden summa on 9.",
        ["Noppapareja on 36.", "Summa 9: (3, 6), (4, 5), (5, 4), (6, 3), eli 4 paria.", f"P = 4/36 = {frac(p)}."], "esim. 1/6", {"sum": 9})
    p = prob_coins(2, {1})
    add(start + 1, ["MAB5.06"], "MAB", "P",
        "Heitetään kahta kolikkoa. Mikä on todennäköisyys, että tulee täsmälleen yksi klaava?",
        p, "1/3", "1/3 olettaa, että tulokset 0, 1 ja 2 klaavaa ovat yhtä todennäköisiä. Luettele KK, KL, LK, LL.",
        ["Tulosparit KK, KL, LK, LL ovat yhtä todennäköisiä.", f"Täsmälleen yksi klaava: KL ja LK, P = 2/4 = {frac(p)}."], "esim. 1/2", {"coins": 2})
    p = prob_coins(3, {2})
    add(start + 2, ["MAA8.04"], "MAA", "T",
        "Heitetään kolmea kolikkoa. Mikä on todennäköisyys, että täsmälleen kaksi on klaavaa?",
        p, "1/4", "1/4 olettaa, että tulokset 0, 1, 2 ja 3 klaavaa ovat yhtä todennäköisiä. Luettele kaikki 8 jonoa.",
        ["Jonoja on 2³ = 8.", f"Kaksi klaavaa: KKL, KLK, LKK, P = 3/8 = {frac(p)}."], "esim. 3/8", {"coins": 3})
    p = prob_dice(lambda a, b: a + b <= 4)
    add(start + 3, ["MAB5.06"], "MAB", "T",
        "Heitetään kahta noppaa. Mikä on todennäköisyys, että silmälukujen summa on enintään 4? Anna supistettuna murtolukuna.",
        p, "3/11", "3/11 laskee summat 2, 3 ja 4 yhtä todennäköisiksi. Laske noppaparit: summa 2 yksi, summa 3 kaksi, summa 4 kolme.",
        ["Summa 2: (1, 1), summa 3: (1, 2), (2, 1), summa 4: (1, 3), (2, 2), (3, 1).", f"Yhteensä 6 paria, P = 6/36 = {frac(p)}."], "esim. 1/6", {"max_sum": 4})
    p = prob_dice(lambda a, b: a == 6 or b == 6)
    add(start + 4, ["MAA8.04"], "MAA", "H",
        "Heitetään kahta noppaa. Mikä on todennäköisyys, että ainakin toisen nopan silmäluku on 6? Tarkista, että tulos on järkevä: se on suurempi kuin yhden nopan todennäköisyys 1/6.",
        p, "1/2", "1/2 olettaa, että ”kuutonen tulee tai ei tule” on tasajakauma. Laske noppaparit: 36 − 25 = 11.",
        ["Parit, joissa ei kuutosta: 5 · 5 = 25.", f"Ainakin yksi kuutonen: 36 − 25 = 11, P = 11/36 = {frac(p)}."], "esim. 11/36", {"event": "at least one six"})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
