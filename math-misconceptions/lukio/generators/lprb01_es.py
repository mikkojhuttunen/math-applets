#!/usr/bin/env python3
"""LPRB-01 ES: equiprobability bias. Each item shows a worked probability where the last line
counts outcomes (sums, numbers of heads) as equally likely. The correct probability is
enumerated with itertools and compared with the displayed lines."""
from fractions import Fraction
from itertools import product

from gen_common import base_item, cli

TEMPLATE = "lprb01_es"
TID, CODE = "LPRB-01", "ES"
GENERIC = "Luettele alkeistulokset, jotka ovat yhtä todennäköisiä (noppaparit, kolikkojonot), ja jaa suotuisten määrä kaikkien määrällä."


def dice(pred):
    return Fraction(sum(1 for a, b in product(range(1, 7), repeat=2) if pred(a, b)), 36)


def coins(n, pred):
    return Fraction(sum(1 for r in product("KL", repeat=n) if pred(r.count("K"))), 2 ** n)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, lines, truth, wrong, etype, steps, fb, params):
        assert Fraction(lines[1].split("/")[0]) / Fraction(lines[1].split("/")[1]) == truth
        assert wrong != truth
        items.append(base_item(TID, CODE, n, lops, ["G2", "G4"], syll, level, "none", prompt,
                               {"lines": lines, "error_line": 3, "error_type": etype},
                               steps, f"{truth.numerator}/{truth.denominator}", fb, TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    p = dice(lambda a, b: a + b in (9, 10))
    add(start, ["MAA8.04"], "MAA", "T",
        "Heitetään kahta noppaa. Oppilas laski todennäköisyyden, että silmälukujen summa on 9 tai 10. Napauta rivi, jossa on virhe.",
        ["4/36 + 3/36", "7/36", "2/11"], p, Fraction(2, 11), "sums_as_equally_likely",
        ["Rivillä 3 summia 2–12 on pidetty yhtä todennäköisinä: kahdesta 11 summasta.", f"Oikein: summa 9 syntyy 4 tavalla ja summa 10 kolmella, yhteensä 7 noppaparia 36:sta, P = 7/36."],
        "Oikein: summat eivät ole yhtä todennäköisiä, noppaparit ovat.", {"sums": [9, 10]})
    p = coins(2, lambda k: k >= 1)
    add(start + 1, ["MAB5.06"], "MAB", "P",
        "Heitetään kahta kolikkoa. Oppilas laski todennäköisyyden, että ainakin yksi on klaava. Napauta rivi, jossa on virhe.",
        ["1/4 + 1/4 + 1/4", "3/4", "2/3"], p, Fraction(2, 3), "outcome_counts_as_equally_likely",
        ["Rivillä 3 tulokset 0, 1 ja 2 klaavaa on pidetty yhtä todennäköisinä, ja suotuisia on 2 niistä 3:sta.", "Oikein: tulokset KK, KL, LK, LL ovat yhtä todennäköisiä; ainakin yksi klaava on kolmessa 4:stä."],
        "Oikein: klaavojen lukumäärät eivät ole yhtä todennäköisiä, vain jonot ovat.", {"coins": 2})
    p = coins(3, lambda k: k == 2)
    add(start + 2, ["MAA8.04"], "MAA", "T",
        "Heitetään kolmea kolikkoa. Oppilas laski todennäköisyyden, että täsmälleen kaksi on klaavaa. Napauta rivi, jossa on virhe.",
        ["1/8 + 1/8 + 1/8", "3/8", "1/4"], p, Fraction(1, 4), "outcome_counts_as_equally_likely",
        ["Rivillä 3 tulokset 0, 1, 2 ja 3 klaavaa on pidetty yhtä todennäköisinä: yksi neljästä.", "Oikein: jonoja on 8, ja kaksi klaavaa on jonoissa KKL, KLK, LKK, eli P = 3/8."],
        "Oikein: jonoja on 8, ja kolme niistä sisältää kaksi klaavaa.", {"coins": 3})
    p = dice(lambda a, b: a + b <= 3)
    add(start + 3, ["MAB5.06"], "MAB", "T",
        "Heitetään kahta noppaa. Oppilas laski todennäköisyyden, että summa on enintään 3. Napauta rivi, jossa on virhe.",
        ["1/36 + 2/36", "3/36", "2/11"], p, Fraction(2, 11), "sums_as_equally_likely",
        ["Rivillä 3 summia 2–12 on pidetty yhtä todennäköisinä: kaksi summaa (2 ja 3) 11:stä.", "Oikein: summa 2 syntyy yhdellä noppaparilla ja summa 3 kahdella, P = 3/36 = 1/12."],
        "Oikein: summa 3 on kaksi kertaa todennäköisempi kuin summa 2.", {"max_sum": 3})
    p = dice(lambda a, b: {a, b} == {5, 6})
    add(start + 4, ["MAA8.04"], "MAA", "H",
        "Heitetään kahta noppaa. Oppilas laski todennäköisyyden, että tulokset ovat viitonen ja kuutonen (jossakin järjestyksessä). Napauta rivi, jossa on virhe. Vihje: onko tämä todennäköisempää kuin kaksi kuutosta?",
        ["1/36 + 1/36", "2/36", "1/36"], p, Fraction(1, 36), "unordered_pair_as_single_outcome",
        ["Rivillä 3 viitonen–kuutonen on laskettu yhdeksi noppapariksi, vaikka paria (5, 6) ja paria (6, 5) on kaksi.", "Oikein: 2/36 = 1/18, kaksi kertaa todennäköisempi kuin kaksi kuutosta (1/36)."],
        "Oikein: eri tulokset (5, 6) ja (6, 5) ovat kaksi erillistä noppaparia.", {"pair": [5, 6]})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
