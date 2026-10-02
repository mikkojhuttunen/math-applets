#!/usr/bin/env python3
"""LPRB-04 NE: representativeness. Counts and probabilities are computed by enumeration;
the wrong answer ranks the irregular-looking sequence higher."""
from fractions import Fraction
from itertools import product
from math import comb

from gen_common import base_item, cli, frac, num

TEMPLATE = "lprb04_ne"
TID, CODE = "LPRB-04", "NE"
GENERIC = "Jokainen tietty tulosjono on yhtä todennäköinen, jos heitot ovat riippumattomia ja tulokset yhtä todennäköisiä. Satunnaisen näköisyys ei lisää todennäköisyyttä."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, answer, wrong, wfb, steps, final, params):
        items.append(base_item(TID, CODE, n, lops, ["G3"], syll, level, "none", prompt,
                               {"answer": answer, "wrong": [{"match": wrong, "misconception": TID, "feedback": wfb}]},
                               steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: how many 5-toss sequences are more likely than KKKKK
    seqs = ["".join(r) for r in product("KL", repeat=5)]
    more = sum(1 for s in seqs if Fraction(1, 32) > Fraction(1, 32))
    assert more == 0
    add(start, ["MAA8.04"], "MAA", "P",
        "Kolikkoa heitetään viisi kertaa, ja jonoja on 32. Montako näistä jonoista on todennäköisempiä kuin KKKKK?",
        {"kind": "number", "value": more}, "31", "31 tarkoittaisi, että KKKKK on muita epätodennäköisempi. Jokainen tietty jono on yhtä todennäköinen, joten yksikään ei ole todennäköisempi.",
        ["Kaikki 32 jonoa ovat yhtä todennäköisiä.", "Yksikään jono ei ole todennäköisempi kuin KKKKK."], "0", {"n": 5})

    # 2: P of a specific sequence of 6 tosses (rational)
    p = Fraction(1, 2 ** 6)
    add(start + 1, ["MAB5.06"], "MAB", "T",
        "Kolikkoa heitetään kuusi kertaa. Mikä on todennäköisyys, että jono on täsmälleen K L L K L K? Anna murtolukuna.",
        {"kind": "rational", "value": "1/64"}, "1/20", "1/20 on tapahtuman ”kolme klaavaa kuudesta” todennäköisyyden suuruusluokkaa, mutta tietty jono on vain yksi 64 jonosta.",
        ["Jonoja on 2⁶ = 64, ja ne ovat yhtä todennäköisiä.", f"Tietyn jonon todennäköisyys on {frac(p)}."], frac(p), {"n": 6})

    # 3: probability ratio of sequences, number
    add(start + 2, ["MAA8.04"], "MAA", "T",
        "Noppaa heitetään neljä kertaa. Montako kertaa todennäköisempi on jono 3, 1, 4, 2 kuin jono 6, 6, 6, 6? Jos yhtä todennäköisiä, vastaa 1.",
        {"kind": "number", "value": 1}, "4", "Ensimmäinen jono ei ole todennäköisempi, vaikka se näyttää satunnaisemmalta. Kummankin todennäköisyys on 1/6⁴.",
        ["Kummankin jonon todennäköisyys on (1/6)⁴.", "Suhde on 1."], "1", {"n": 4})

    # 4: events vs sequences (MAB), number of sequences
    k = comb(6, 3)
    add(start + 3, ["MAB5.06"], "MAB", "H",
        "Kolikkoa heitetään kuusi kertaa. Montako kertaa todennäköisempää on, että täsmälleen kolme heitoista on klaavaa, kuin että jono on KKKKKK?",
        {"kind": "number", "value": k}, "1", "Vastaus 1 pätee kahdelle tietylle jonolle, mutta ”kolme klaavaa” sisältää kaikki jonot, joissa on kolme klaavaa.",
        ["Jokainen jono on yhtä todennäköinen, 1/64.", f"Kolme klaavaa: C(6, 3) = {k} jonoa, KKKKKK: 1 jono.", f"Suhde on {k}."], num(k), {"n": 6, "k": 3})

    # 5: lottery row, percent difference
    n_, k = 35, 7
    total = comb(n_, k)
    add(start + 4, ["MAA8.04"], "MAA", "H",
        f"Arvonnassa nostetaan 7 numeroa {n_}:stä. Mikä on todennäköisyys, että rivi on täsmälleen 1, 2, 3, 4, 5, 6, 7? Anna vastaus muodossa 1/n eli kirjoita luku n.",
        {"kind": "number", "value": total}, "0", "Todennäköisyys ei ole nolla: ”liian säännöllinen” rivi on yhtä mahdollinen kuin mikä tahansa muu.",
        [f"Eri rivejä on C({n_}, {k}) = {total}.", f"Jokaisen todennäköisyys on 1/{total}, myös rivin 1–7."], num(total), {"n": n_, "k": k})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
