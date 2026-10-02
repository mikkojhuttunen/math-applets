#!/usr/bin/env python3
"""LPRB-06 RP: order handled wrongly in counting. The pupil writes an equation whose only
solution is the correct number of choices k. The value is computed with math.comb / math.perm;
the invalid examples are the count with the wrong treatment of order."""
from math import comb, factorial, perm

from gen_common import base_item, cli

TEMPLATE = "lprb06_rp"
TID, CODE = "LPRB-06", "RP"
GENERIC = "Kysy ensin, onko järjestyksellä merkitystä. Jos ei ole, jaa järjestettyjen valintojen määrä järjestysten määrällä k!."


def pt(n, k):
    return "·".join(str(n - i) for i in range(k))


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, value, valid, invalid, steps, final, fb, params):
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, "none", prompt,
                               {"constraint": {"type": "solution_equals", "variable": "k", "value": value},
                                "checks": {"valid": valid, "invalid": invalid}},
                               steps, final, fb, TEMPLATE, params, date, run, generic_wrong=GENERIC))

    n_, k = 8, 3
    add(start, ["MAA8.03"], "MAA", "T",
        f"Luokasta, jossa on {n_} oppilasta, valitaan {k} edustajaa. Merkitään k = erilaisten edustajaryhmien määrä. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo.",
        comb(n_, k), [f"k = {pt(n_, k)}/(3·2·1)", f"6k = {pt(n_, k)}"], [f"k = {pt(n_, k)}", f"k = {pt(n_, k)}/3"],
        [f"Järjestyksellä ei ole väliä: {pt(n_, k)} laskee valinnat järjestyksineen, ja jokainen ryhmä tulee 3! = 6 kertaa.", f"k = {perm(n_, k)}/6 = {comb(n_, k)}."],
        f"esim. k = {pt(n_, k)}/(3·2·1) (k = {comb(n_, k)})", "Oikein: järjestettyjen valintojen määrä jaetaan järjestysten määrällä.", {"n": n_, "k": k})
    n_, k = 6, 2
    add(start + 1, ["MAB5.07"], "MAB", "P",
        f"Pizzaan valitaan {k} eri täytettä {n_}:sta. Merkitään k = erilaisten täytevalintojen määrä. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo.",
        comb(n_, k), [f"k = {pt(n_, k)}/2", f"2k = {pt(n_, k)}"], [f"k = {pt(n_, k)}", f"k = {n_}·2"],
        [f"Täytteet ovat joukko: {pt(n_, k)} = {perm(n_, k)} laskee jokaisen parin kahdesti.", f"k = {perm(n_, k)}/2 = {comb(n_, k)}."],
        f"esim. k = {pt(n_, k)}/2 (k = {comb(n_, k)})", "Oikein: täytteiden järjestyksellä ei ole väliä.", {"n": n_, "k": k})
    n_, k = 7, 3
    add(start + 2, ["MAA8.03"], "MAA", "T",
        f"Kilpailussa on {n_} osallistujaa. Kulta, hopea ja pronssi jaetaan kolmelle parhaalle. Merkitään k = erilaisten palkintojärjestysten määrä. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo.",
        perm(n_, k), [f"k = {pt(n_, k)}", f"k = {perm(n_, k)}"], [f"k = {pt(n_, k)}/(3·2·1)", f"k = {pt(n_, k)}/3"],
        [f"Järjestyksellä on väliä, koska mitalit ovat eri arvoisia: {pt(n_, k)} = {perm(n_, k)}."],
        f"esim. k = {pt(n_, k)} (k = {perm(n_, k)})", "Oikein: kun järjestyksellä on väliä, ei jaeta.", {"n": n_, "k": k})
    n_, k = 9, 4
    add(start + 3, ["MAA8.03"], "MAA", "H",
        f"Kerhossa on {n_} jäsentä, ja heistä valitaan {k} hengen joukkue. Merkitään k = erilaisten joukkueiden määrä. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo.",
        comb(n_, k), [f"k = {pt(n_, k)}/(4·3·2·1)", f"24k = {pt(n_, k)}"], [f"k = {pt(n_, k)}", f"k = {pt(n_, k)}/4"],
        [f"{perm(n_, k)} laskee valinnat järjestyksineen; jokainen joukkue tulee 4! = {factorial(k)} kertaa.", f"k = {perm(n_, k)}/{factorial(k)} = {comb(n_, k)}."],
        f"esim. k = {pt(n_, k)}/(4·3·2·1) (k = {comb(n_, k)})", "Oikein: jaetaan 4!:lla, ei 4:llä.", {"n": n_, "k": k})
    n_ = 7
    add(start + 4, ["MAB5.07"], "MAB", "H",
        f"Juhlissa on {n_} vierasta, ja jokainen kättelee jokaisen kanssa kerran. Merkitään k = kättelyjen määrä. Kirjoita yhtälö, jonka ainoa ratkaisu on k:n oikea arvo, ja tarkista, että k on pienempi kuin {perm(n_, 2)}.",
        comb(n_, 2), [f"k = {n_}·{n_ - 1}/2", f"2k = {n_}·{n_ - 1}"], [f"k = {n_}·{n_ - 1}", f"k = {n_}·{n_ - 2}"],
        [f"Jokainen kättely A–B on sama kuin B–A, joten {perm(n_, 2)} jaetaan 2:lla.", f"k = {perm(n_, 2)}/2 = {comb(n_, 2)}, mikä on pienempi kuin {perm(n_, 2)}."],
        f"esim. k = {n_}·{n_ - 1}/2 (k = {comb(n_, 2)})", "Oikein: kättelyt ovat pareja, ei järjestettyjä pareja.", {"n": n_})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
