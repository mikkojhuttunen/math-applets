#!/usr/bin/env python3
"""LPRB-01 RP: equiprobability bias. The pupil writes an equation whose only solution is the
probability p. The true value is enumerated with itertools; the invalid examples treat the
listed outcomes (numbers of heads, same or different) as equally likely."""
from fractions import Fraction
from itertools import product

from gen_common import base_item, cli

TEMPLATE = "lprb01_rp"
TID, CODE = "LPRB-01", "RP"
GENERIC = "Luettele yhtä todennäköiset alkeistulokset (kolikkojonot) ja jaa suotuisten määrä kaikkien määrällä."


def coins(n, pred):
    return Fraction(sum(1 for r in product("KL", repeat=n) if pred(r)), 2 ** n)


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, p, valid, invalid, steps, params):
        value = p.numerator / p.denominator
        assert Fraction(value) == p  # exact in binary, so the JSON number is exact
        items.append(base_item(TID, CODE, n, lops, ["G2", "G4"], syll, level, "none", prompt,
                               {"constraint": {"type": "solution_equals", "variable": "p", "value": value},
                                "checks": {"valid": valid, "invalid": invalid}},
                               steps, f"p = {p.numerator}/{p.denominator}",
                               "Oikein: lasketaan yhtä todennäköisten kolikkojonojen määrä.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    p = coins(2, lambda r: "K" in r)
    add(start, ["MAB5.06"], "MAB", "P",
        "Heitetään kahta kolikkoa. Merkitään p = todennäköisyys, että ainakin yksi on klaava. Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo.",
        p, ["p = 3/4", "4p = 3"], ["p = 2/3", "3p = 2"],
        ["Jonot KK, KL, LK, LL ovat yhtä todennäköisiä, ja kolmessa niistä on klaava.", "p = 3/4. Arvo 2/3 olettaisi, että tulokset 0, 1 ja 2 klaavaa ovat yhtä todennäköisiä."], {"coins": 2})
    p = coins(3, lambda r: r.count("K") == 2)
    add(start + 1, ["MAA8.04"], "MAA", "T",
        "Heitetään kolmea kolikkoa. Merkitään p = todennäköisyys, että täsmälleen kaksi on klaavaa. Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo.",
        p, ["p = 3/8", "8p = 3"], ["p = 1/4", "4p = 1"],
        ["Jonoja on 8; kaksi klaavaa on jonoissa KKL, KLK ja LKK.", "p = 3/8. Arvo 1/4 olettaisi, että tulokset 0–3 klaavaa ovat yhtä todennäköisiä."], {"coins": 3})
    p = coins(3, lambda r: "K" in r)
    add(start + 2, ["MAB5.06"], "MAB", "T",
        "Heitetään kolmea kolikkoa. Merkitään p = todennäköisyys, että ainakin yksi on klaava. Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo.",
        p, ["p = 1 − 1/8", "8p = 7"], ["p = 3/4", "4p = 3"],
        ["Ainoa jono ilman klaavaa on LLL, joten p = 1 − 1/8 = 7/8.", "Arvo 3/4 olettaisi, että tulokset 0–3 klaavaa ovat yhtä todennäköisiä."], {"coins": 3})
    p = coins(4, lambda r: r.count("K") == 1)
    add(start + 3, ["MAA8.04"], "MAA", "H",
        "Heitetään neljää kolikkoa. Merkitään p = todennäköisyys, että täsmälleen yksi on klaava. Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo.",
        p, ["p = 4/16", "4p = 1"], ["p = 1/5", "5p = 1"],
        ["Jonoja on 2⁴ = 16; yksi klaava on jonoissa, joissa klaavan paikka on 1., 2., 3. tai 4., eli 4 jonoa.", "p = 4/16 = 1/4. Arvo 1/5 olettaisi, että tulokset 0–4 klaavaa ovat yhtä todennäköisiä."], {"coins": 4})
    p = coins(3, lambda r: len(set(r)) == 1)
    add(start + 4, ["MAB5.06"], "MAB", "H",
        "Heitetään kolmea kolikkoa. Merkitään p = todennäköisyys, että kaikki kolme ovat samanlaisia (kaikki klaavoja tai kaikki kruunuja). Kirjoita yhtälö, jonka ainoa ratkaisu on p:n oikea arvo, ja perustele, miksi arvo 1/2 ei kelpaa.",
        p, ["p = 2/8", "4p = 1"], ["p = 1/2", "2p = 1"],
        ["Jonoja on 8; samanlaisia ovat vain KKK ja LLL, joten p = 2/8 = 1/4.", "Arvo 1/2 olettaisi, että ”kaikki samanlaisia” ja ”ei kaikki samanlaisia” ovat yhtä todennäköisiä, vaikka jälkimmäiseen kuuluu 6 jonoa."], {"coins": 3})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
