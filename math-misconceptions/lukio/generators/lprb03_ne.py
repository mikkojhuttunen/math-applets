#!/usr/bin/env python3
"""LPRB-03 NE: conjunction fallacy. P(A and B) is computed by enumeration or the multiplication
rule with Fraction; the wrong answers are P(A), P(B) or the sum (the larger or more detailed event)."""
from fractions import Fraction
from itertools import product

from gen_common import base_item, cli, frac

TEMPLATE = "lprb03_ne"
TID, CODE = "LPRB-03", "NE"
GENERIC = "P(A ja B) on enintään yhtä suuri kuin P(A) ja P(B). Laske tapahtuman ”A ja B” suotuisat tulokset tai käytä kertosääntöä."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, g, prompt, p, wrongs, steps, hint, params):
        for m, _ in wrongs:
            assert Fraction(m) != p
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt,
                               {"answer": {"kind": "rational", "value": f"{p.numerator}/{p.denominator}" if p.denominator != 1 else str(p.numerator)},
                                "wrong": [{"match": m, "misconception": TID, "feedback": f} for m, f in wrongs],
                                "input_hint": hint},
                               steps, frac(p), "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: die, even and greater than 3
    p = Fraction(sum(1 for x in range(1, 7) if x % 2 == 0 and x > 3), 6)
    add(start, ["MAA8.05"], "MAA", "T", ["G3"],
        "Noppaa heitetään kerran. Mikä on todennäköisyys, että tulos on parillinen ja suurempi kuin 3? Anna vastaus supistettuna murtolukuna.",
        p, [("1/2", "1/2 on pelkän parillisen tuloksen todennäköisyys. Molempien ehtojen pitää täyttyä, joten tuloksia on vähemmän.")],
        ["Parillinen ja suurempi kuin 3: tulokset 4 ja 6.", f"P = 2/6 = {frac(p)}."], "esim. 1/3", {"events": ["even", ">3"]})
    # 2: card, red ace
    p = Fraction(2, 52)
    add(start + 1, ["MAB5.06"], "MAB", "T", ["G3"],
        "Korttipakasta (52 korttia) nostetaan yksi kortti. Mikä on todennäköisyys, että se on punainen ässä? Anna vastaus supistettuna murtolukuna.",
        p, [("1/2", "1/2 on punaisen kortin todennäköisyys. Punainen ässä on vain osa punaisista korteista."),
            ("1/13", "1/13 on ässän todennäköisyys. Punainen ässä on vain osa ässistä.")],
        ["Punaisia ässiä on 2 (hertta ja ruutu).", f"P = 2/52 = {frac(p)}."], "esim. 1/26", {"cards": "red ace"})
    # 3: three coins, first and third heads
    hits = sum(1 for r in product("KL", repeat=3) if r[0] == "K" and r[2] == "K")
    p = Fraction(hits, 8)
    add(start + 2, ["MAB5.06"], "MAB", "T", ["G3"],
        "Heitetään kolmea kolikkoa peräkkäin. Mikä on todennäköisyys, että ensimmäinen ja kolmas heitto ovat molemmat klaavoja?",
        p, [("1/2", "1/2 on yhden heiton todennäköisyys. Kummankin heiton pitää onnistua.")],
        ["Jonoja on 8; sopivia ovat KKK ja KLK.", f"P = 2/8 = {frac(p)}."], "esim. 1/4", {"coins": 3})
    # 4: independent multiplication
    p = Fraction(2, 5) * Fraction(1, 2)
    add(start + 3, ["MAA8.05"], "MAA", "H", ["G3"],
        "Tapahtumat A ja B ovat riippumattomia, P(A) = 2/5 ja P(B) = 1/2. Mikä on P(A ja B)? Anna vastaus supistettuna murtolukuna.",
        p, [("9/10", "9/10 = 2/5 + 1/2 on summa. Riippumattomien tapahtumien yhteinen todennäköisyys lasketaan kertomalla."),
            ("1/2", "P(B) on suurempi kuin P(A ja B). Tapahtuma ”A ja B” on osa tapahtumaa B.")],
        ["Riippumattomille tapahtumille P(A ja B) = P(A) · P(B).", f"P = 2/5 · 1/2 = {frac(p)}."], "esim. 1/5", {"p_a": "2/5", "p_b": "1/2"})
    # 5: plausibility, two dice: sum 7 and first die 3
    hits = sum(1 for a, b in product(range(1, 7), repeat=2) if a + b == 7 and a == 3)
    p = Fraction(hits, 36)
    pa = Fraction(sum(1 for a, b in product(range(1, 7), repeat=2) if a + b == 7), 36)
    add(start + 4, ["MAA8.05"], "MAA", "H", ["G3"],
        "Heitetään kahta noppaa. Eero arvioi, että todennäköisyys sille, että summa on 7 ja ensimmäinen noppa näyttää kolmosta, on vähintään 1/6. Laske todennäköisyys ja tarkista Eeron arvio.",
        p, [(frac(pa), f"{frac(pa)} on pelkän summan 7 todennäköisyys. Lisäehto ”ensimmäinen noppa on 3” pienentää sitä.")],
        ["Noppapareja on 36.", "Summa 7 ja ensimmäinen 3: vain pari (3, 4).", f"P = 1/36. Eeron arvio 1/6 on summan 7 todennäköisyys, ei yhdistetyn tapahtuman."], "esim. 1/36", {"dice": 2})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
