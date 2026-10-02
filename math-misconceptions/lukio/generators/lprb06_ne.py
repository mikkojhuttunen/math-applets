#!/usr/bin/env python3
"""LPRB-06 NE: order handled wrongly in counting. Answers computed with math.comb / math.perm;
the wrong answer is the count with the wrong treatment of order."""
from math import comb, perm

from gen_common import base_item, cli, num

TEMPLATE = "lprb06_ne"
TID, CODE = "LPRB-06", "NE"
GENERIC = "Kysy ensin, onko järjestyksellä merkitystä. Jos ei ole, jaa järjestettyjen valintojen määrä järjestysten määrällä."


def make_items(run, date, count=5, start=1):
    items = []

    def add(n, lops, syll, level, tools, prompt, value, wrong, wfb, steps, params):
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, tools, prompt,
                               {"answer": {"kind": "number", "value": value},
                                "wrong": [{"match": wrong, "misconception": TID, "feedback": wfb}]},
                               steps, num(value), "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: 3 of 10, set
    n_, k = 10, 3
    add(start, ["MAA8.03"], "MAA", "T", "none",
        f"Luokasta, jossa on {n_} oppilasta, valitaan {k} edustajaa. Montako erilaista edustajaryhmää voidaan valita?",
        comb(n_, k), perm(n_, k), f"{num(perm(n_, k))} on järjestettyjen valintojen määrä. Samat {k} oppilasta eri järjestyksessä ovat sama ryhmä, joten jaa luvulla {k}! = {perm(k, k)}.",
        [f"Järjestyksellä ei ole väliä: C({n_}, {k}).", f"{perm(n_, k)} / {perm(k, k)} = {comb(n_, k)}."], {"n": n_, "k": k})
    # 2: lottery-like 4 of 12, MAB
    n_, k = 12, 4
    add(start + 1, ["MAB5.07"], "MAB", "T", "none",
        f"Arvonnassa {n_} osallistujan joukosta nostetaan {k} voittajaa, jotka saavat saman palkinnon. Montako erilaista voittajajoukkoa on mahdollista?",
        comb(n_, k), perm(n_, k), f"{num(perm(n_, k))} laskee voittajat nostojärjestyksessä. Palkinto on sama, joten jaa luvulla {k}! = {perm(k, k)}.",
        [f"Nostojärjestyksellä ei ole väliä: C({n_}, {k}).", f"{perm(n_, k)} / {perm(k, k)} = {comb(n_, k)}."], {"n": n_, "k": k})
    # 3: medals, order matters
    n_, k = 8, 3
    add(start + 2, ["MAA8.03"], "MAA", "P", "none",
        f"Kisassa on {n_} osallistujaa. Kulta, hopea ja pronssi jaetaan kolmelle parhaalle. Montako erilaista palkintojärjestystä on mahdollista?",
        perm(n_, k), comb(n_, k), f"{comb(n_, k)} laskee vain kolmen hengen joukon. Tässä on väliä, kuka saa minkäkin mitalin, joten järjestystä ei jaeta pois.",
        [f"Järjestyksellä on väliä: {n_}·{n_ - 1}·{n_ - 2}.", f"{n_}·{n_ - 1}·{n_ - 2} = {perm(n_, k)}."], {"n": n_, "k": k})
    # 4: mixed: 2 boys of 6 and 1 girl of 5, MAA
    b, g = 6, 5
    value = comb(b, 2) * g
    wrong = perm(b, 2) * g
    add(start + 3, ["MAA8.03"], "MAA", "H", "none",
        f"Ryhmässä on {b} poikaa ja {g} tyttöä. Ryhmästä valitaan kaksi poikaa ja yksi tyttö työryhmään. Montako erilaista työryhmää voidaan valita?",
        value, wrong, f"{num(wrong)} laskee poikaparin järjestyksineen. Poikapari valitaan C({b}, 2) = {comb(b, 2)} tavalla.",
        [f"Pojat: C({b}, 2) = {comb(b, 2)}.", f"Tytöt: {g} tapaa.", f"Tuloperiaate: {comb(b, 2)} · {g} = {value}."], {"boys": b, "girls": g})
    # 5: plausibility, 5 of 15, cas, MAA
    n_, k = 15, 5
    add(start + 4, ["MAA8.03"], "MAA", "H", "cas",
        f"Kerhosta, jossa on {n_} jäsentä, valitaan {k} hengen joukkue. Kaisa arvioi, että vaihtoehtoja on yli 360 000. Laske joukkueiden määrä ja tarkista arvio.",
        comb(n_, k), perm(n_, k), f"{num(perm(n_, k))} sisältää jokaisen joukkueen {perm(k, k)} järjestyksessä. Jaa luvulla {k}! = {perm(k, k)}.",
        [f"{n_}·{n_ - 1}·{n_ - 2}·{n_ - 3}·{n_ - 4} = {perm(n_, k)}.", f"Jaetaan {k}! = {perm(k, k)}: {comb(n_, k)}.", "Arvio 360 000 on yli satakertainen."], {"n": n_, "k": k})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
