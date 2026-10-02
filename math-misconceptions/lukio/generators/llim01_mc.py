#!/usr/bin/env python3
"""LLIM-01 MC: a limit cannot be reached (limit read as a bound the function never attains).
Limits are computed with sympy; distractors are the "never reached" readings."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "llim01_mc"
TID, CODE = "LLIM-01", "MC"
X = sp.Symbol("x")
GENERIC = "Raja-arvo on luku, jota funktion arvot lähestyvät. Funktio voi saada raja-arvonsa arvona, eikä se ole este."


def limit_const(rng, n, c, a, date, run):
    lim = sp.limit(sp.Integer(c) + 0 * X, X, a)
    assert lim == c
    opts, cid = mc_options(
        rng, (f"Raja-arvo on {show(c)}.", f"Oikein: vakiofunktion arvo on koko ajan {show(c)}, joten myös raja-arvo on {show(c)}."),
        [("Raja-arvoa ei ole, koska funktio ei koskaan lähesty lukua, vaan on jo perillä.", "LLIM-01",
          "Raja-arvon olemassaolo ei vaadi, että arvo on eri kuin raja-arvo. Vakiofunktion arvot ovat täsmälleen raja-arvo."),
         (f"Raja-arvo on hieman alle {show(c)}, koska raja-arvoa ei voi saavuttaa.", "LLIM-01",
          "Raja-arvoa ei tarvitse olla 'ylittämätön raja'. Tässä arvo on joka kohdassa sama.")])
    return base_item(TID, CODE, n, ["MAA6.01"], ["G2"], "MAA", "P", "none",
                     f"Funktio on f(x) = {show(c)} kaikilla x. Mitä voit sanoa raja-arvosta lim f(x), kun x → {show(a)}?",
                     {"options": opts, "correct": [cid]},
                     [f"f(x) = {show(c)} jokaisella x.", f"Arvot lähestyvät lukua {show(c)} ja ovat sitä jo."], f"{show(c)}",
                     "Oikein.", TEMPLATE, {"c": c, "a": a}, date, run, generic_wrong=GENERIC)


def limit_removable(rng, n, a, date, run):
    f = (X**2 - a**2) / (X - a)
    lim = sp.limit(f, X, a)
    assert lim == 2 * a
    opts, cid = mc_options(
        rng, (show(lim), f"Oikein: f(x) = x + {show(a)} kun x ≠ {show(a)}, joten raja-arvo on {show(lim)}, vaikka f({show(a)}) ei ole määritelty."),
        [(f"Raja-arvoa ei ole, koska funktiota ei ole määritelty kohdassa x = {show(a)}.", "LLIM-03",
          "Raja-arvo kuvaa käyttäytymistä lähellä kohtaa, ei arvoa itse kohdassa."),
         (f"Raja-arvo on pienempi kuin {show(lim)}, koska funktio ei koskaan ehdi arvoon {show(lim)}.", "LLIM-01",
          "Se, ettei arvoa saavuteta tässä pisteessä, ei tarkoita että raja-arvo olisi pienempi.")])
    return base_item(TID, CODE, n, ["MAA6.01"], ["G2", "G3"], "MAA", "T", "none",
                     f"Mikä on lim (x² − {show(a**2)})/(x − {show(a)}), kun x → {show(a)}?",
                     {"options": opts, "correct": [cid]},
                     [f"x² − {show(a**2)} = (x − {show(a)})(x + {show(a)}).", f"Supistetaan: x + {show(a)}, kun x ≠ {show(a)}.",
                      f"Kun x → {show(a)}, arvo → {show(lim)}."], show(lim), "Oikein.", TEMPLATE, {"a": a}, date, run,
                     generic_wrong=GENERIC)


def limit_attained(rng, n, a, b, date, run):
    f = a * X + b
    lim = sp.limit(f, X, 2)
    assert lim == 2 * a + b
    opts, cid = mc_options(
        rng, (show(lim), f"Oikein: f(2) = {show(lim)} ja raja-arvo on sama. Funktio saa raja-arvonsa arvona."),
        [(f"Raja-arvoa ei ole, koska f(2) = {show(lim)} ja raja-arvo on aina vain lähestyttävä arvo.", "LLIM-01",
          "Raja-arvo voi olla funktion arvo. Jatkuvalla funktiolla näin on aina."),
         (f"Raja-arvo on {show(lim - 1)} eli arvoa alempi, koska siihen ei päästä.", "LLIM-01",
          "Raja-arvo ei ole lähestyttävää arvoa alempi 'turvaväli'.")])
    return base_item(TID, CODE, n, ["MAA6.01"], ["G2"], "MAA", "T", "none",
                     f"Funktio on f(x) = {show(f).replace(' · ', '')}. Mikä on lim f(x), kun x → 2?",
                     {"options": opts, "correct": [cid]},
                     [f"f on polynomi, joten raja-arvo saadaan sijoittamalla x = 2.", f"f(2) = {show(lim)}."], show(lim),
                     "Oikein.", TEMPLATE, {"a": a, "b": b}, date, run, generic_wrong=GENERIC)


def limit_oneover(rng, n, k, date, run):
    seq = [sp.Rational(1, 10**i) for i in range(1, 4)]
    lim = sp.limit(k / X, X, sp.oo)
    assert lim == 0
    opts, cid = mc_options(
        rng, ("0", "Oikein: arvot lähestyvät nollaa mielivaltaisen tarkasti, joten raja-arvo on 0. Se, ettei jono saa arvoa 0, ei muuta tätä."),
        [("Raja-arvoa ei ole, koska funktio ei koskaan saa arvoa 0.", "LLIM-01",
          "Raja-arvo ei ole funktion arvo. Se on luku, jota arvot lähestyvät kuinka tarkasti tahansa."),
         (f"Raja-arvo on hyvin pieni positiivinen luku, esim. {show(float(seq[-1]))}.".replace(".", ","), "LLIM-01",
          "Raja-arvo on yksi tarkka luku, ei 'riittävän lähellä oleva' luku.")])
    return base_item(TID, CODE, n, ["MAA6.01"], ["G2", "G3"], "MAA", "H", "none",
                     f"Funktio on f(x) = {show(k)}/x, kun x > 0. Mikä on raja-arvo, kun x kasvaa rajatta, vaikka f(x) ei koskaan ole 0?",
                     {"options": opts, "correct": [cid]},
                     [f"Kun x = 10, 100, 1000, ..., arvot ovat {show(k)}/10, {show(k)}/100, ...", "Arvot lähestyvät nollaa kuinka tarkasti tahansa.",
                      "Raja-arvo on 0 vaikka arvoa 0 ei saavuteta."], "0", "Oikein.", TEMPLATE, {"k": k}, date, run,
                     generic_wrong=GENERIC)


def limit_justify(rng, n, date, run):
    lim = sp.limit((sp.sin(X) / X), X, 0)
    assert lim == 1
    opts, cid = mc_options(
        rng, ("Raja-arvo 1 ei ole ristiriidassa sen kanssa, ettei funktio ole määritelty kohdassa 0: raja-arvo kuvaa arvoja kohdan lähellä.",
              "Oikein. Raja-arvo on määritelty kohdan ympäristön avulla, ei pelkän kohdan arvon avulla."),
        [("Väite on virheellinen: raja-arvo 1 tarkoittaisi, että funktio saa arvon 1 kohdassa 0, mutta f(0) ei ole määritelty.", "LLIM-03",
          "Raja-arvo ja funktion arvo ovat eri asioita."),
         ("Väite on virheellinen: funktio ei koskaan saavuta arvoa 1, joten raja-arvo ei voi olla 1.", "LLIM-01",
          "Se, ettei arvoa saavuteta, ei estä sitä olemasta raja-arvo.")])
    return base_item(TID, CODE, n, ["MAA6.01"], ["G3"], "MAA", "K", "none",
                     "Taulukko: f(x) = sin x / x, kun x = 0,1; 0,01; 0,001, arvot ovat noin 0,9983; 0,99998; 0,9999998. Funktiota ei ole määritelty kohdassa 0. Perustele, voiko raja-arvo kohdassa 0 silti olla 1.",
                     {"options": opts, "correct": [cid]},
                     ["Arvot lähestyvät lukua 1 mielivaltaisen tarkasti.", "Raja-arvo ei riipu arvosta kohdassa 0."], "1",
                     "Oikein.", TEMPLATE, {}, date, run, generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(4101)
    items = [limit_const(rng, start, 3, 5, date, run), limit_removable(rng, start + 1, 3, date, run),
             limit_attained(rng, start + 2, 3, -1, date, run), limit_oneover(rng, start + 3, 4, date, run),
             limit_justify(rng, start + 4, date, run)]
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
