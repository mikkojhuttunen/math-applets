#!/usr/bin/env python3
"""LPRB-06 MC: order handled wrongly in counting. Counts are computed with math.comb / math.perm;
distractors are the ordered count for an unordered question (and the reverse)."""
import random
from math import comb, perm

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "lprb06_mc"
TID, CODE = "LPRB-06", "MC"
GENERIC = "Kysy ensin, onko järjestyksellä merkitystä. Jos ei ole, jokainen joukko lasketaan vain kerran: jaa järjestettyjen valintojen määrä järjestysten määrällä."


def make_items(run, date, count=5, start=1):
    rng = random.Random(8603)
    items = []

    def add(n, lops, syll, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, lops, ["G4"], syll, level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))

    # 1: committee 3 of 8
    n_, k = 8, 3
    c, p = comb(n_, k), perm(n_, k)
    add(start, ["MAA8.03"], "MAA", "T",
        f"Oppilaskunnan hallitukseen valitaan {n_} ehdokkaasta {k} jäsentä. Kaikilla jäsenillä on samat tehtävät. Montako erilaista hallitusta voidaan valita?",
        (num(c), f"Oikein: järjestyksellä ei ole väliä, joten C({n_}, {k}) = {num(c)}."),
        [(num(p), TID, f"{n_} · {n_ - 1} · {n_ - 2} = {num(p)} laskee myös eri järjestykset. Sama kolmen hengen joukko tulee silloin laskettua {num(perm(k, k))} kertaa."),
         (num(n_ * k), None, "Tulo 8 · 3 ei vastaa valintojen määrää."),
         (num(2 ** n_), None, "2^8 laskee kaikki mahdolliset osajoukot, ei vain kolmen hengen joukkoja.")],
        [f"Järjestyksellä ei ole väliä.", f"C({n_}, {k}) = {n_}·{n_ - 1}·{n_ - 2} / {k}! = {num(p)} / {num(perm(k, k))} = {num(c)}."],
        num(c), {"n": n_, "k": k})

    # 2: pizza toppings 2 of 6, MAB
    n_, k = 6, 2
    c, p = comb(n_, k), perm(n_, k)
    add(start + 1, ["MAB5.07"], "MAB", "P",
        f"Pizzaan valitaan {n_} täytteen joukosta {k} eri täytettä. Täytteiden järjestyksellä ei ole väliä. Montako erilaista pizzaa voi tehdä?",
        (num(c), f"Oikein: {n_} · {n_ - 1} = {num(p)} jaetaan kahdella, koska järjestys ei ole väliä. Tulos on {num(c)}."),
        [(num(p), TID, "Laskit pareja järjestyksineen: juusto + sieni ja sieni + juusto ovat sama pizza."),
         (num(n_ + k), None, f"Summa {n_} + {k} ei kuvaa valintojen määrää."),
         (num(n_ ** k), None, "6 · 6 sallisi saman täytteen kahdesti.")],
        [f"Ensimmäinen täyte {n_} tavalla, toinen {n_ - 1} tavalla: {num(p)} järjestettyä paria.", f"Jokainen pari on laskettu kahdesti, joten {num(p)} / 2 = {num(c)}."],
        num(c), {"n": n_, "k": k})

    # 3: medals, order matters (reverse direction)
    n_, k = 9, 3
    c, p = comb(n_, k), perm(n_, k)
    add(start + 2, ["MAA8.03"], "MAA", "T",
        f"Juoksukilpailussa on {n_} juoksijaa. Kulta-, hopea- ja pronssimitali jaetaan kolmelle nopeimmalle. Montako erilaista mitalijakoa on mahdollista?",
        (num(p), f"Oikein: järjestyksellä on väliä, koska mitalit ovat erilaisia. {n_}·{n_ - 1}·{n_ - 2} = {num(p)}."),
        [(num(c), TID, "C(9, 3) laskee vain kolmen juoksijan joukon. Tässä on väliä sillä, kuka saa kullan, kuka hopean ja kuka pronssin."),
         (num(n_ * k), None, "9 · 3 ei vastaa mitalijakojen määrää."),
         (num(n_ ** k), None, "9³ sallisi saman juoksijan usealle mitalille.")],
        ["Kullan saa yksi 9:stä, hopean yksi jäljellä olevista 8:sta ja pronssin yksi 7:stä.", f"{n_}·{n_ - 1}·{n_ - 2} = {num(p)}."],
        num(p), {"n": n_, "k": k})

    # 4: handshakes 12 people, MAB, H
    n_ = 12
    c, p = comb(n_, 2), perm(n_, 2)
    add(start + 3, ["MAB5.07"], "MAB", "T",
        f"Juhlissa on {n_} vierasta, ja jokainen kättelee jokaista toista vierasta tasan kerran. Montako kättelyä juhlissa on yhteensä?",
        (num(c), f"Oikein: kättely on parin kesken, joten järjestyksellä ei ole väliä. C({n_}, 2) = {num(c)}."),
        [(num(p), TID, "Jokainen kättely tulee tällä laskulla kahdesti: A kättelee B:tä ja B kättelee A:ta on sama kättely."),
         (num(n_ * 2), None, "12 · 2 olettaa, että jokainen kättelee vain kahta."),
         (num(n_ ** 2), None, "12² laskisi myös kättelyt itsensä kanssa.")],
        [f"Jokainen {n_} vieraasta kättelee {n_ - 1} muuta: {num(p)}.", f"Jokainen kättely on laskettu kahdesti, joten {num(c)}."],
        num(c), {"n": n_})

    # 5: justification H
    n_, k = 10, 3
    c, p = comb(n_, k), perm(n_, k)
    add(start + 4, ["MAA8.03"], "MAA", "H",
        f"Koululla on {n_} ehdokasta kolmen hengen toimikuntaan, jossa kaikki ovat samanarvoisia. Aino laskee {n_}·{n_ - 1}·{n_ - 2} = {num(p)} ja sanoo, että toimikuntia on {num(p)}. Mikä on virhe?",
        (f"Hän laskee jokaisen kolmen hengen joukon {num(perm(k, k))} kertaa, joten tulos on jaettava luvulla {num(perm(k, k))}.",
         f"Oikein: {num(p)} laskee jokaisen toimikunnan kaikissa {num(perm(k, k))} järjestyksessä. Oikea määrä on {num(p)} / {num(perm(k, k))} = {num(c)}."),
        [("Hänen pitäisi laskea 10 · 3 = 30, koska jokaiselle paikalle on 3 vaihtoehtoa.", None, "Paikkoja ei ole nimetty, ja ehdokkaita on 10, ei 3."),
         (f"Laskussa ei ole virhettä, koska ensimmäinen jäsen voidaan valita {n_} tavalla.", TID, "Valintajärjestys ei kuulu tulokseen: samat kolme henkilöä eri järjestyksessä on sama toimikunta."),
         (f"Hänen pitäisi vähentää tuloksesta {n_}.", None, "Vähennyslaskulla ei korjata kertaluvun laskemista monta kertaa.")],
        [f"Tulo {n_}·{n_ - 1}·{n_ - 2} laskee henkilöt valintajärjestyksessä.", f"Samat kolme henkilöä voidaan valita {num(perm(k, k))} järjestyksessä, joten {num(c)} erilaista toimikuntaa."],
        num(c), {"n": n_, "k": k})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
