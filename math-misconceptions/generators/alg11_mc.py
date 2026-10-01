#!/usr/bin/env python3
"""ALG-11 (minus sign not distributed), type MC. Linear expressions are kept as (p, q) = px + q, so the correct
option and every distractor are computed from the same numbers; the typical wrong answer applies the minus
sign before a bracket to the first term only."""
import random

from gen_common import MINUS, base_item, cli, lin, mc_options

TEMPLATE = "alg11_mc"
TID, CODE = "ALG-11", "MC"
FIRST = "Miinusmerkki sulun edessä koskee kaikkia sulun sisällä olevia termejä, ei vain ensimmäistä."
GOOD = "Oikein: sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin."


def build(rng, good, wrongs):
    """wrongs = [((p, q), misconception, feedback)]; drops duplicates of the correct answer."""
    seen, out = {lin(*good)}, []
    for e, m, fb in wrongs:
        if lin(*e) not in seen:
            seen.add(lin(*e))
            out.append((lin(*e), m, fb))
    return mc_options(rng, (lin(*good), GOOD), out)


def make_items(run, date, count=5, start=1):
    rng = random.Random(1101)
    items = []
    for k in range(count):
        a, b, c = rng.randint(2, 7), rng.randint(2, 9), rng.randint(2, 9)
        steps = []
        if k == 0:
            level, prompt = "T", f"Sievennä: {MINUS}(x {MINUS} {b})"
            good = (-1, b)
            wr = [((-1, -b), TID, FIRST), ((1, -b), None, "Sulun edessä oleva miinus ei jää pois, vaan muuttaa merkit."),
                  ((1, b), None, "Ensimmäisen termin merkki muuttuu myös.")]
            steps = [f"{MINUS}(x {MINUS} {b}) = {MINUS}x + {b}"]
        elif k == 1:
            level, prompt = "T", f"Sievennä: {MINUS}({a}x + {b})"
            good = (-a, -b)
            wr = [((-a, b), TID, FIRST), ((a, -b), None, "Ensimmäisen termin merkki muuttuu myös."),
                  ((a, b), None, "Sulun edessä oleva miinus muuttaa merkit.")]
            steps = [f"{MINUS}({a}x + {b}) = {MINUS}{a}x {MINUS} {b}"]
        elif k == 2:
            level, prompt = "T", f"Sievennä: {c} {MINUS} ({a}x {MINUS} {b})"
            good = (-a, c + b)
            wr = [((-a, c - b), TID, FIRST), ((a, c + b), None, "Miinus muuttaa myös termin " + f"{a}x merkin."),
                  ((a, c - b), None, "Sulun sisällä olevien termien merkit muuttuvat molemmat.")]
            steps = [f"{c} {MINUS} ({a}x {MINUS} {b}) = {c} {MINUS} {a}x + {b}", lin(*good)]
        elif k == 3:
            level = "H"
            prompt = (f"Tilillä on {c + b} euroa. Siitä maksetaan lasku, jonka hinta on x euroa, mutta laskusta saa {b} euron "
                      f"alennuksen. Mikä lauseke antaa jäljelle jäävän rahamäärän sievennettynä?")
            good = (-1, c + 2 * b)
            wr = [((-1, c), TID, FIRST), ((1, c), None, "Lasku pienentää tilin saldoa, joten x on miinusmerkkinen."),
                  ((-1, c + b), None, "Alennus pienentää laskua, joten se kasvattaa jäljelle jäävää rahaa."),
                  ((1, c + 2 * b), None, "Lasku pienentää tilin saldoa, joten x on miinusmerkkinen.")]
            steps = [f"{c + b} {MINUS} (x {MINUS} {b}) = {c + b} {MINUS} x + {b}", lin(*good)]
        else:
            level = "H"
            at = rng.randint(2, 5)
            prompt = (f"Oppilas kirjoittaa {MINUS}(x {MINUS} {b}) = {MINUS}x {MINUS} {b}. "
                      f"Miten virheen voi todeta sijoittamalla x = {at}?")
            lhs, rhs = -(at - b), -at - b
            assert lhs != rhs
            options, cid = mc_options(rng, (f"Vasen puoli on {MINUS}({at} {MINUS} {b}) = {lhs}, oikea puoli on {rhs}, joten väite on väärä".replace("-", MINUS),
                                            "Oikein: jos lausekkeet ovat yhtä suuret, niiden arvot ovat samat jokaisella x:n arvolla."), [
                (f"Molemmat puolet saavat arvon {lhs}, joten väite on oikein".replace("-", MINUS), TID, FIRST),
                ("Sijoittamalla ei voi tarkistaa merkkien muuttumista", TID, "Sijoittamalla voi tarkistaa, ovatko lausekkeet yhtä suuret."),
                (f"Arvot {lhs} ja {rhs} eroavat, mutta väite on silti oikein, koska miinus on molemmissa".replace("-", MINUS), TID,
                 "Yhtä suurilla lausekkeilla on täsmälleen sama arvo.")])
            payload = {"options": options, "correct": [cid]}
            items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, prompt, payload,
                                   [f"x = {at}: {MINUS}({at} {MINUS} {b}) = {lhs}".replace("-", MINUS), f"{MINUS}{at} {MINUS} {b} = {rhs}"],
                                   f"Arvot {lhs} ja {rhs} eroavat".replace("-", MINUS),
                                   "Oikein: väärä merkkien muutos näkyy arvojen eroavuutena.",
                                   TEMPLATE, {"b": b, "x": at}, date, run))
            continue
        options, cid = build(rng, good, wr)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, prompt, payload, steps,
                               lin(*good), GOOD, TEMPLATE, {"a": a, "b": b, "c": c}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
