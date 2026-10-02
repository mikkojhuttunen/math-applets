#!/usr/bin/env python3
"""LPRB-06 ES: order handled wrongly in counting. Each item shows a worked count where one line
drops the division by the number of orders, or divides although order matters. The count in
every line is computed with math.comb / math.perm and checked against the displayed lines."""
from math import comb, factorial, perm

from gen_common import base_item, cli, num

TEMPLATE = "lprb06_es"
TID, CODE = "LPRB-06", "ES"
GENERIC = "Kysy ensin, onko järjestyksellä merkitystä. Jos ei ole, jaa järjestettyjen valintojen määrä järjestysten määrällä k!."


def prod_text(n, k):
    return "·".join(str(n - i) for i in range(k))


def fact_text(k):
    return "·".join(str(k - i) for i in range(k))


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, prompt, lines, etype, steps, final, fb, params):
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, "none", prompt,
                               {"lines": lines, "error_line": 3, "error_type": etype},
                               steps, final, fb, TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: 3 of 8, division forgotten
    n_, k = 8, 3
    add(start, ["MAA8.03"], "MAA", "P",
        f"Luokasta, jossa on {n_} oppilasta, valitaan {k} edustajaa. Oppilas laski edustajaryhmien määrän näin. Napauta rivi, jossa on virhe.",
        [f"{prod_text(n_, k)}/({fact_text(k)})", f"{perm(n_, k)}/{factorial(k)}", f"{perm(n_, k)}"], "order_not_divided_out",
        [f"Rivillä 3 jako {factorial(k)}:lla on unohdettu: {perm(n_, k)} laskee valinnat järjestyksineen.",
         f"Oikein: {perm(n_, k)}/{factorial(k)} = {comb(n_, k)}."], f"{comb(n_, k)} ryhmää",
        "Oikein: sama ryhmä eri järjestyksessä on yksi ryhmä, joten järjestysten määrä jaetaan pois.", {"n": n_, "k": k})
    # 2: medals, order matters, but divided
    n_, k = 8, 3
    add(start + 1, ["MAA8.03"], "MAA", "P",
        f"Kisassa on {n_} osallistujaa. Kulta, hopea ja pronssi jaetaan kolmelle parhaalle. Oppilas laski palkintojärjestysten määrän näin. Napauta rivi, jossa on virhe.",
        [prod_text(n_, k), f"{perm(n_, k)}", f"{perm(n_, k)}/{factorial(k)}"], "divided_although_order_matters",
        [f"Rivillä 3 on jaettu {factorial(k)}:lla, vaikka kulta, hopea ja pronssi ovat eri palkintoja.",
         f"Oikein: järjestyksellä on väliä, joten {prod_text(n_, k)} = {perm(n_, k)}."], f"{perm(n_, k)} järjestystä",
        "Oikein: kun järjestyksellä on väliä, järjestyksiä ei jaeta pois.", {"n": n_, "k": k})
    # 3: 2 boys of 6 and 1 girl of 5, division forgotten in one factor
    b, g = 6, 5
    add(start + 2, ["MAA8.03"], "MAA", "H",
        f"Ryhmässä on {b} poikaa ja {g} tyttöä. Työryhmään valitaan kaksi poikaa ja yksi tyttö. Oppilas laski työryhmien määrän näin. Napauta rivi, jossa on virhe.",
        [f"{prod_text(b, 2)}/({fact_text(2)})·{g}", f"{comb(b, 2)}·{g}", f"{perm(b, 2)}·{g}"], "order_not_divided_out",
        [f"Rivillä 3 poikaparin valinta on laskettu järjestyksineen: {perm(b, 2)} eikä {comb(b, 2)}.",
         f"Oikein: {comb(b, 2)}·{g} = {comb(b, 2) * g}."], f"{comb(b, 2) * g} työryhmää",
        "Oikein: poikaparin järjestyksellä ei ole väliä, joten pareja on C(6, 2) = 15.", {"boys": b, "girls": g})
    # 4: 3 toppings of 7, divided by k instead of k!
    n_, k = 7, 3
    add(start + 3, ["MAB5.07"], "MAB", "T",
        f"Pizzaan valitaan {k} eri täytettä {n_}:stä. Oppilas laski erilaisten täytevalintojen määrän näin. Napauta rivi, jossa on virhe.",
        [f"{prod_text(n_, k)}/({fact_text(k)})", f"{perm(n_, k)}/{factorial(k)}", f"{perm(n_, k)}/{k}"], "divided_by_k_not_k_factorial",
        [f"Rivillä 3 on jaettu luvulla {k} eikä {k}! = {factorial(k)}: {k} täytettä voidaan järjestää {factorial(k)} tavalla.",
         f"Oikein: {perm(n_, k)}/{factorial(k)} = {comb(n_, k)}."], f"{comb(n_, k)} valintaa",
        f"Oikein: {k} täytteen järjestysten määrä on {k}! = {factorial(k)}.", {"n": n_, "k": k})
    # 5: handshakes of 6, plausibility hint
    n_ = 6
    add(start + 4, ["MAB5.07"], "MAB", "T",
        f"Juhlissa on {n_} vierasta, ja jokainen kättelee jokaisen kanssa kerran. Oppilas laski kättelyjen määrän näin. Napauta rivi, jossa on virhe. Vihje: jokainen kättely kuuluu kahdelle vieraalle.",
        [f"{n_}·{n_ - 1}/(2·1)", f"{perm(n_, 2)}/2", f"{perm(n_, 2)}"], "order_not_divided_out",
        [f"Rivillä 3 jako 2:lla on unohdettu: {perm(n_, 2)} laskee jokaisen kättelyn kahdesti, A–B ja B–A.",
         f"Oikein: {perm(n_, 2)}/2 = {comb(n_, 2)}."], f"{comb(n_, 2)} kättelyä",
        f"Oikein: kättely A–B on sama kuin B–A. Tulos {perm(n_, 2)} olisi myös suurempi kuin vierasparien määrä.", {"n": n_})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
