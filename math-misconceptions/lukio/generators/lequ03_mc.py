#!/usr/bin/env python3
"""LEQU-03 MC (lukio level): an inequality is multiplied by an expression of unknown sign.
Correct options are computed with sympy; distractors carry misconception tags."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options

TEMPLATE = "lequ03_mc"
TID, CODE = "LEQU-03", "MC"
X = sp.Symbol("x", real=True)
GENERIC = "Epäyhtälön saa kertoa puolittain vain lausekkeella, jonka merkki tiedetään. Siirrä kaikki vasemmalle ja tutki merkit."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1103)
    items = []

    def add(n, g, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, ["MAA2.06", "MAA2.07"], [g], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: 5/x > 2  -> 0 < x < 5/2
    s = sp.solve_univariate_inequality(5 / X > 2, X, relational=False)
    assert s == sp.Interval.open(0, sp.Rational(5, 2))
    add(start, "G4", "T", "Ratkaise epäyhtälö 5/x > 2.",
        ("0 < x < 5/2", "Oikein: murtoluku on positiivinen vain, kun x > 0."),
        [("x < 5/2", TID, "Kertoessasi x:llä oletit x > 0. Kokeile x = −1: 5/(−1) = −5, ei suurempi kuin 2."),
         ("x > 5/2", None, "Epäyhtälön suunta kääntyi väärin. Kokeile x = 3: 5/3 < 2."),
         ("x < 0 tai x > 5/2", None, "Kokeile x = −1: 5/(−1) = −5, ei suurempi kuin 2.")],
        ["Siirrä 2 vasemmalle: (5 − 2x)/x > 0.", "Samanmerkkiset osoittaja ja nimittäjä: 0 < x < 5/2."], "0 < x < 5/2", {"a": 5, "b": 2})
    # 2: -6/x < 3  -> x < -2 or x > 0
    s = sp.solve_univariate_inequality(-6 / X < 3, X, relational=False)
    assert s == sp.Union(sp.Interval.open(-sp.oo, -2), sp.Interval.open(0, sp.oo))
    add(start + 1, "G4", "T", "Ratkaise epäyhtälö −6/x < 3.",
        ("x < −2 tai x > 0", "Oikein: kun x > 0, vasen puoli on negatiivinen ja siis pienempi kuin 3; kun x < 0, tarvitaan x < −2."),
        [("x > −2", TID, "Kertoessasi x:llä oletit x > 0, mutta silloin pätee −6 < 3x vain x > −2 ja x > 0. Kokeile x = −1: −6/(−1) = 6, ei pienempi kuin 3."),
         ("−2 < x < 0", None, "Kokeile x = −1: −6/(−1) = 6, ei pienempi kuin 3."),
         ("x < −2", None, "Tapaus x > 0 puuttuu: x = 1 antaa −6 < 3.")],
        ["Siirrä 3 vasemmalle: (−6 − 3x)/x < 0, eli (x + 2)/x > 0.", "Samanmerkkiset: x < −2 tai x > 0."], "x < −2 tai x > 0", {"a": -6, "b": 3})
    # 3: justification
    add(start + 2, "G3", "T", "Oppilas ratkaisi epäyhtälön 1/x < 2 kertomalla molemmat puolet x:llä ja sai 1 < 2x. Mikä on tämän vaiheen ongelma?",
        ("Kun x < 0, epäyhtälön suunta kääntyy, joten tapaukset x > 0 ja x < 0 on käsiteltävä erikseen.", "Oikein."),
        [("Vaihe on aina oikein, koska molemmille puolille tehdään sama kertolasku.", TID, "Kertominen negatiivisella luvulla kääntää epäyhtälön suunnan."),
         ("Epäyhtälöä ei saa kertoa millään lausekkeella.", None, "Kertominen on sallittu, kun lausekkeen merkki tiedetään."),
         ("Kertominen x:llä onnistuu vain, jos x on kokonaisluku.", None, "Kokonaisuudella ei ole tässä merkitystä, vaan merkillä.")],
        ["x:n merkkiä ei tiedetä.", "Jos x < 0, epäyhtälö kääntyy: 1 > 2x."], "Tapaukset x > 0 ja x < 0 erikseen", {"a": 1, "b": 2})
    # 4: plausibility check of 4/x > 1 with answer x < 4
    s = sp.solve_univariate_inequality(4 / X > 1, X, relational=False)
    assert s == sp.Interval.open(0, 4)
    add(start + 3, "G4", "H", "Oppilas ratkaisi epäyhtälön 4/x > 1 ja sai x < 4. Mikä päätelmä on oikea?",
        ("Ratkaisu on väärä: x = −1 toteuttaa epäyhtälön x < 4, mutta 4/(−1) = −4 ei ole suurempi kuin 1.", "Oikein."),
        [("Ratkaisu on oikea, koska x = 2 antaa 4/2 = 2 > 1.", TID, "Yksi toimiva testiluku ei riitä. Kokeile myös negatiivista lukua."),
         ("Ratkaisu on väärä, koska oikea ratkaisu on x > 4.", None, "x = 8 antaa 4/8 < 1. Oikea ratkaisu on 0 < x < 4."),
         ("Ratkaisu on oikea, koska x = 0 antaa 4/0 > 1.", None, "Nollalla ei voi jakaa.")],
        ["x = −1: 4/(−1) = −4, ei > 1.", "Oikea ratkaisu: (4 − x)/x > 0, eli 0 < x < 4."], "Ratkaisu on väärä; oikea on 0 < x < 4", {"a": 4, "b": 1})
    # 5: positive denominator allows direct multiplication
    s = sp.solve_univariate_inequality(6 / (X ** 2 + 1) > 1, X, relational=False)
    assert s == sp.Interval.open(-sp.sqrt(5), sp.sqrt(5))
    add(start + 4, "G3", "H", "Ratkaise epäyhtälö 6/(x² + 1) > 1.",
        ("−√5 < x < √5", "Oikein: x² + 1 > 0 aina, joten kertominen ei muuta suuntaa: 6 > x² + 1."),
        [("x < √5", "LEQU-04", "x² < 5 tarkoittaa |x| < √5, ei vain x < √5."),
         ("x < −√5 tai x > √5", TID, "Kerroit suunnan kääntäen, vaikka x² + 1 on aina positiivinen."),
         ("−5 < x < 5", None, "Epäyhtälöstä saadaan x² < 5, ei x² < 25.")],
        ["x² + 1 > 0, joten saa kertoa: 6 > x² + 1.", "x² < 5, joten −√5 < x < √5."], "−√5 < x < √5", {"a": 6})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
