#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type MC. Correct option and distractors are computed (sympy)
from the same numbers; the typical wrong answer multiplies only the first term."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options

TEMPLATE = "alg08_mc"
TID, CODE = "ALG-08", "MC"
x = sp.Symbol("x")
FIRST = "Kerroin kertoo kaikki sulun sisällä olevat termit, ei vain ensimmäistä."


def fmt(expr):
    return str(sp.expand(expr)).replace("*", "").replace("-", "−")


def inner(c, b, sign):
    return f"{'' if c == 1 else c}x {'+' if sign > 0 else '−'} {b}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8301)
    items = []
    for k in range(count):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        c = 1 if k < 2 else rng.randint(2, 5)
        sign = 1 if k in (0, 2) else -1
        if k < 3:
            level = "T"
            prompt = f"Avaa sulut: {a}({inner(c, b, sign)})"
            good = a * (c * x + sign * b)
            first_only = a * c * x + sign * b
            second_only = c * x + sign * a * b
            wrongs = [(first_only, TID, FIRST),
                      (second_only, TID, "Kerroin kertoo myös ensimmäisen termin."),
                      (a * c * x - sign * a * b, "ALG-11" if sign < 0 else None,
                       "Tarkista termin merkki kertolaskun jälkeen.")]
            steps = [f"{a} · {'' if c == 1 else c}x + {a} · ({sign * b})", fmt(good)]
        elif k == 3:
            level = "H"
            prompt = (f"Yhden lipun hinta on x euroa ja jokaiseen lippuun lisätään {b} euron palvelumaksu. "
                      f"Perhe ostaa {a} lippua. Mikä lauseke antaa kokonaishinnan avattuna?")
            good = a * (x + b)
            wrongs = [(a * x + b, TID, "Palvelumaksu maksetaan jokaisesta lipusta, joten sekin kerrotaan luvulla " + str(a) + "."),
                      (x + a * b, TID, "Myös lipun hinta x kerrotaan lippujen määrällä."),
                      (a * x + a + b, TID, "Luvulla " + str(a) + " kerrotaan palvelumaksu, ei lisätä sitä.")]
            steps = [f"{a}(x + {b}) = {a}x + {a} · {b}", fmt(good)]
        else:
            level = "H"
            a, b = rng.randint(3, 6), rng.randint(2, 5)
            expr = a * (x + b)
            wrong_expr = a * x + b
            at = 1
            prompt = (f"Oppilas kirjoittaa {a}(x + {b}) = {fmt(wrong_expr)}. Miten virheen voi todeta sijoittamalla x = {at}?")
            lhs, rhs = expr.subs(x, at), wrong_expr.subs(x, at)
            assert lhs != rhs
            options, cid = mc_options(rng, (f"Vasen puoli on {a}({at} + {b}) = {lhs} ja oikea puoli {rhs}, joten väite on väärä",
                                            "Oikein: jos lausekkeet ovat yhtä suuret, niiden arvot ovat samat jokaisella x:n arvolla."), [
                (f"Molemmat puolet saavat arvon {lhs}, joten väite on oikein", TID, FIRST),
                (f"Sijoittamalla ei voi tarkistaa sulkulausekkeen avaamista", TID, "Sijoittamalla voi tarkistaa, ovatko lausekkeet yhtä suuret."),
                (f"Vasen puoli on {lhs} ja oikea {rhs}, mutta väite on silti oikein, koska kerroin {a} on molemmissa", TID,
                 "Yhtä suurilla lausekkeilla on täsmälleen sama arvo.")])
            payload = {"options": options, "correct": [cid]}
            items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload,
                                   [f"x = {at}: {a}({at} + {b}) = {lhs}", f"{fmt(wrong_expr)} = {rhs}"],
                                   f"Arvot {lhs} ja {rhs} eroavat", "Oikein: väärä sulkujen avaus näkyy arvojen eroavuutena.",
                                   TEMPLATE, {"a": a, "b": b, "x": at}, date, run))
            continue
        cands = [(w, m, fb) for w, m, fb in wrongs if sp.expand(w - good) != 0]
        seen, wl = set(), []
        for w, m, fb in cands:
            if fmt(w) not in seen:
                seen.add(fmt(w))
                wl.append((fmt(w), m, fb))
        options, cid = mc_options(rng, (fmt(good), "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin."), wl)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, fmt(good),
                               "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin.", TEMPLATE,
                               {"a": a, "b": b, "c": c, "sign": sign}, date, run,
                               misconceptions=[TID] + (["ALG-11"] if any(o["misconception"] == "ALG-11" for o in options) else [])))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
