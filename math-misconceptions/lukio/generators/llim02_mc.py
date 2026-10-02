#!/usr/bin/env python3
"""LLIM-02 MC: 0,999... is less than 1. Values are computed with exact sympy rationals;
distractors are the "infinitely little less" readings."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, frac, show

TEMPLATE = "llim02_mc"
TID, CODE = "LLIM-02", "MC"
GENERIC = "Desimaaliesitys 0,999… tarkoittaa päättymätöntä summaa, jonka arvo on tasan 1. Se ei ole luku, joka vain lähestyy ykköstä."


def repeating(d, k=None):
    """Value of 0,ddd... (digit d repeating) as an exact fraction."""
    n = sp.Symbol("n", integer=True, positive=True)
    return sp.summation(sp.Integer(d) * sp.Rational(1, 10) ** n, (n, 1, sp.oo))


def eq_nine(rng, n, date, run):
    v = repeating(9)
    assert v == 1
    opts, cid = mc_options(
        rng, ("0,999… = 1", "Oikein: 0,999… = 9/10 + 9/100 + … on geometrinen sarja, jonka summa on 1."),
        [("0,999… < 1, koska luvusta puuttuu aina vähän", "LLIM-02", "Mikään äärellinen määrä ysejä ei ole 1, mutta päättymätön desimaaliesitys on määritelmän mukaan raja-arvo, joka on 1."),
         ("0,999… on lähes 1 mutta ei sama luku", "LLIM-02", "Reaaliluvuilla ei ole 'ääretöntä pientä väliä' lukujen 0,999… ja 1 välillä.")])
    return base_item(TID, CODE, n, ["MAA6.01", "MAY1.01"], ["G3"], "MAA", "P", "none",
                     "Mikä seuraavista väitteistä on oikein?", {"options": opts, "correct": [cid]},
                     ["0,999… = 9/10 + 9/100 + 9/1000 + …", "Geometrinen sarja a₁/(1 − q) = (9/10)/(1 − 1/10) = 1."], "0,999… = 1",
                     "Oikein.", TEMPLATE, {"d": 9}, date, run, generic_wrong=GENERIC)


def third_times_three(rng, n, date, run):
    third = repeating(3)
    assert third == sp.Rational(1, 3) and 3 * third == 1
    opts, cid = mc_options(
        rng, ("Kyllä: 3 · 1/3 = 1, ja 1/3 = 0,333…, joten 0,999… = 1", "Oikein. Sama luku voidaan kirjoittaa kahdella tavalla."),
        [("Ei: 0,333… on vain likiarvo luvusta 1/3, joten tulos on 0,999…", "LLIM-02", "Päättymätön esitys 0,333… on täsmälleen 1/3, ei likiarvo."),
         ("Ei: kertolasku ei toimi päättymättömillä desimaaliluvuilla", "LLIM-02", "Kertolasku toimii, kun desimaaliluku ymmärretään sarjan summana.")])
    return base_item(TID, CODE, n, ["MAY1.01"], ["G3"], "MAB", "P", "none",
                     "Koska 1/3 = 0,333…, saadaan 3 · 1/3 = 3 · 0,333… = 0,999…. Toisaalta 3 · 1/3 = 1. Onko tämä päättely kelvollinen osoittamaan, että 0,999… = 1?",
                     {"options": opts, "correct": [cid]},
                     ["1/3 = 0,333… täsmälleen.", "3 · 0,333… = 0,999… ja 3 · 1/3 = 1."], "Kyllä, 0,999… = 1",
                     "Oikein.", TEMPLATE, {"digit": 3}, date, run, generic_wrong=GENERIC)


def x_trick(rng, n, date, run):
    x = sp.Symbol("x")
    sol = sp.solve(sp.Eq(10 * x - x, 9), x)[0]
    assert sol == 1
    opts, cid = mc_options(
        rng, ("10x − x = 9, joten x = 1", "Oikein: 10x = 9,999… ja x = 0,999…, joten vähennys antaa 9x = 9."),
        [("10x − x = 8,999…, joten x on hiukan alle 1", "LLIM-02", "10x = 9,999… ja x = 0,999…: päättymättömät ysit kumoavat toisensa täsmälleen."),
         ("10x = 9,99…0, joten x = 0,9", "LLIM-02", "Päättymättömässä esityksessä ei ole viimeistä numeroa.")])
    return base_item(TID, CODE, n, ["MAY1.01"], ["G3"], "MAB", "T", "none",
                     "Olkoon x = 0,999…. Silloin 10x = 9,999…. Mitä saadaan, kun lasketaan 10x − x, ja mikä on x?",
                     {"options": opts, "correct": [cid]},
                     ["10x − x = 9,999… − 0,999… = 9.", "9x = 9, joten x = 1."], "x = 1", "Oikein.", TEMPLATE, {"x": "0.999..."},
                     date, run, generic_wrong=GENERIC)


def ratio_form(rng, n, d, date, run):
    v = repeating(d)
    assert v == sp.Rational(d, 9)
    right = frac(v)
    opts, cid = mc_options(
        rng, (right, f"Oikein: 0,{d}{d}{d}… = {d}/10 + {d}/100 + … = {right}."),
        [(f"{d}/10", "LLIM-02", "Tämä on vain ensimmäinen termi; sarjassa on päättymätön määrä lisättäviä termejä."),
         (f"{d}/10 + {d}/100 = {frac(sp.Rational(d, 10) + sp.Rational(d, 100))}", "LLIM-02", "Äärellinen summa ei ole päättymätön desimaaliesitys.")])
    return base_item(TID, CODE, n, ["MAA6.01"], ["G3"], "MAA", "H", "none",
                     f"Kirjoita jaksollinen desimaaliluku 0,{d}{d}{d}… murtolukuna. Mikä on sen arvo?",
                     {"options": opts, "correct": [cid]},
                     [f"Geometrinen sarja a₁ = {d}/10, q = 1/10.", f"S = (a₁)/(1 − q) = {right}."], right, "Oikein.", TEMPLATE, {"d": d},
                     date, run, generic_wrong=GENERIC)


def plausibility(rng, n, date, run):
    assert (repeating(9) + 1) / 2 == 1  # the midpoint of the two numbers is 1 itself
    opts, cid = mc_options(
        rng, ("Ei: jos vielä 0,999… < 1, niin lukujen väliin mahtuisi toinen luku, mutta sitä ei ole", "Oikein: kahden eri reaaliluvun välissä on aina toinen luku, mutta 0,999… ja 1 välissä ei ole mitään."),
        [("Kyllä: esimerkiksi luku 0,999…5 mahtuu väliin", "LLIM-02", "Päättymättömässä desimaaliesityksessä ei ole viimeistä numeroa, joten tällaista lukua ei ole."),
         ("Kyllä: lukujen välissä on ääretön pieni väli", "LLIM-02", "Reaaliluvuissa ei ole äärettömän pieniä väliä.")])
    return base_item(TID, CODE, n, ["MAY1.01"], ["G3"], "MAB", "K", "none",
                     "Väite: 0,999… ja 1 ovat eri luvut, koska 0,999… < 1. Tarkista väite: onko lukujen 0,999… ja 1 väliin mahdollista löytää jokin toinen luku?",
                     {"options": opts, "correct": [cid]},
                     ["Kahden eri reaaliluvun keskiarvo on aina niiden välissä.", "Lukujen 0,999… ja 1 väliin ei voi sijoittaa mitään lukua.",
                      "Siis luvut ovat sama luku."], "Ei; luvut ovat sama", "Oikein.", TEMPLATE, {}, date, run,
                     generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(4102)
    items = [eq_nine(rng, start, date, run), third_times_three(rng, start + 1, date, run), x_trick(rng, start + 2, date, run),
             ratio_form(rng, start + 3, 7, date, run), plausibility(rng, start + 4, date, run)]
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
