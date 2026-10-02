#!/usr/bin/env python3
"""LPRB-04 MC: representativeness (an irregular sequence is more likely). Probabilities are computed
by enumeration; the distractor ranks the irregular-looking sequence higher."""
import random
from fractions import Fraction
from itertools import product
from math import comb

from gen_common import base_item, cli, frac, mc_options

TEMPLATE = "lprb04_mc"
TID, CODE = "LPRB-04", "MC"
GENERIC = "Jokainen tietty tulosjono on yhtä todennäköinen, jos jokainen heitto on riippumaton ja tulokset yhtä todennäköisiä. Satunnaisen näköinen jono ei ole todennäköisempi kuin säännöllinen."


def make_items(run, date, count=5, start=1):
    rng = random.Random(8104)
    items = []

    def add(n, lops, syll, level, g, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, g, syll, level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: coin sequences 5
    seq_a, seq_b = "KLKKL", "KKKKK"
    p = Fraction(1, 2 ** 5)
    assert sum(1 for r in product("KL", repeat=5) if "".join(r) == seq_a) == 1
    add(start, ["MAA8.04"], "MAA", "P", ["G3"],
        "Kolikkoa heitetään viisi kertaa. Kumpi tulosjono on todennäköisempi: K L K K L vai K K K K K?",
        (f"Yhtä todennäköisiä, kummankin todennäköisyys on {frac(p)}", "Oikein: kolikkojonoja on 32, ja ne ovat kaikki yhtä todennäköisiä."),
        [("K L K K L, koska se näyttää satunnaisemmalta", TID, "Näyttö ei ratkaise. Jokainen tietty viiden heiton jono on yhtä todennäköinen, 1/32."),
         ("K K K K K, koska kolikko on oikeudenmukainen", None, "Myös K L K K L on tarkalleen yksi jono 32:sta.")],
        ["Jonoja on 2⁵ = 32, ja ne ovat yhtä todennäköisiä.", "Kumpikin tietty jono on yksi 32:sta."], f"Yhtä todennäköisiä, {frac(p)}", {"a": seq_a, "b": seq_b})

    # 2: lotto row 1-7 vs mixed row (MAB)
    n_, k = 40, 7
    add(start + 1, ["MAB5.06"], "MAB", "T", ["G3"],
        "Lotossa arvotaan 7 numeroa 40:stä. Matti pelaa rivin 1, 2, 3, 4, 5, 6, 7 ja Maija rivin 4, 11, 19, 23, 28, 35, 38. Kumman rivin todennäköisyys on suurempi?",
        (f"Yhtä suuri, kummankin 1/{comb(n_, k)}", f"Oikein: kaikki {comb(n_, k)} eri riviä ovat yhtä todennäköisiä."),
        [("Maijan, koska rivi näyttää satunnaisemmalta", TID, "Arvonta ei ”tiedä” rivin kuviota. Jokainen tietty rivi on yksi mahdollisuus kaikista."),
         ("Matin, koska numerot ovat peräkkäin", None, "Peräkkäisyys ei lisää todennäköisyyttä: rivi on yhtä todennäköinen kuin muutkin.")],
        [f"Eri rivejä on C({n_}, {k}) = {comb(n_, k)}.", "Jokainen niistä on yhtä todennäköinen."], f"Yhtä suuri, 1/{comb(n_, k)}", {"n": n_, "k": k})

    # 3: dice sequence of six
    add(start + 2, ["MAA8.04"], "MAA", "T", ["G3"],
        "Noppaa heitetään kuusi kertaa. Kumpi tulosjono on todennäköisempi: 1, 2, 3, 4, 5, 6 vai 3, 1, 6, 2, 6, 4?",
        ("Yhtä todennäköisiä, kummankin todennäköisyys on (1/6)⁶", "Oikein: jokainen tietty kuuden heiton jono syntyy todennäköisyydellä (1/6)⁶."),
        [("Jono 3, 1, 6, 2, 6, 4, koska se näyttää satunnaiselta", TID, "Satunnaisen näköisiä jonoja on paljon, mutta tietty jono on silti yksi 6⁶:sta."),
         ("Jono 1, 2, 3, 4, 5, 6, koska sen luvut ovat kaikki eri", None, "Jokainen tietty jono on yhtä todennäköinen.")],
        ["Jonoja on 6⁶, ja ne ovat yhtä todennäköisiä.", "Kummankin todennäköisyys on 1/6⁶."], "Yhtä todennäköisiä", {"sequences": 2})

    # 4: sequence vs event: exactly three heads in six vs six heads (MAB)
    ways = comb(6, 3)
    assert ways == 20
    add(start + 3, ["MAB5.06"], "MAB", "H", ["G3"],
        "Kolikkoa heitetään kuusi kertaa. Kumpi on todennäköisempää: KKKKKK vai että kuudesta heitosta täsmälleen kolme on klaavaa (missä järjestyksessä tahansa)?",
        (f"Kolme klaavaa on todennäköisempää: {ways}/64 vs 1/64", f"Oikein: kolmen klaavan tapahtumaan kuuluu {ways} jonoa, kuutosjonoon vain yksi."),
        [("Yhtä todennäköisiä, koska kaikki jonot ovat yhtä todennäköisiä", TID, "Tietyt jonot ovat yhtä todennäköisiä, mutta toinen kohta on tapahtuma, johon kuuluu useita jonoja."),
         ("KKKKKK, koska siinä kaikki heitot ovat samanlaisia", None, "KKKKKK on vain yksi jono 64:stä, kolmen klaavan tapahtuma 20 jonoa.")],
        ["Jonoja on 2⁶ = 64, ja ne ovat yhtä todennäköisiä.", f"KKKKKK on 1 jono; täsmälleen 3 klaavaa C(6, 3) = {ways} jonoa."], f"{ways}/64 > 1/64", {"n": 6, "k": 3})

    # 5: justification, children in family (MAB)
    add(start + 4, ["MAB5.06"], "MAB", "H", ["G3"],
        "Perheeseen syntyy kuusi lasta. Anna sanoo: ”Syntymäjärjestys T P T T P T on todennäköisempi kuin T T T T T T, koska jälkimmäinen on niin epätavallinen.” Mikä on oikea perustelu?",
        ("Kumpikin tietty syntymäjärjestys on yhtä todennäköinen, 1/64, jos tytön ja pojan todennäköisyydet ovat yhtä suuret.", "Oikein: tietty jono on aina yksi 64 yhtä todennäköisestä jonosta."),
        [("Anna on oikeassa, koska sekalaiset jonot ovat yleisempiä.", TID, "Sekalaisia jonoja on paljon, mutta tietty sekalainen jono on yhtä harvinainen kuin tietty tasajono."),
         ("Jono T T T T T T on todennäköisempi, koska se on helppo muistaa.", None, "Muistettavuus ei vaikuta todennäköisyyteen.")],
        ["Jonoja on 2⁶ = 64.", "Jokainen tietty jono on yksi niistä, joten todennäköisyys on 1/64."], "Yhtä todennäköisiä, 1/64", {"n": 6})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
