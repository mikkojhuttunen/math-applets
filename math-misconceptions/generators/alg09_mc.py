#!/usr/bin/env python3
"""ALG-09 (square of a sum), type MC. Options are computed with sympy; the typical wrong answer
distributes the power over the sum, (a + b)² = a² + b²."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options

TEMPLATE = "alg09_mc"
TID, CODE = "ALG-09", "MC"
x = sp.Symbol("x")
POW = "Potenssi ei jakaudu summan yli: (a + b)² = (a + b)(a + b), ja tulossa on myös kaksinkertainen tulo 2ab."


def fmt(expr):
    return str(sp.expand(expr)).replace("**2", "²").replace("*", "").replace("-", "−")


def make_items(run, date, count=5, start=1):
    rng = random.Random(9301)
    items = []
    for k in range(count):
        b = rng.randint(2, 9)
        c = rng.randint(2, 4)
        if k == 0:
            level, prompt = "T", f"Avaa sulut: (x + {b})²"
            good, base, s = (x + b) ** 2, x, b
            wrongs = [(x**2 + b**2, POW), (x**2 + b * x + b**2, POW), (x**2 + 2 * b, POW)]
            steps = [f"(x + {b})(x + {b})", fmt(good)]
        elif k == 1:
            level, prompt = "T", f"Avaa sulut: (x {chr(0x2212)} {b})²"
            good = (x - b) ** 2
            wrongs = [(x**2 - b**2, POW), (x**2 - 2 * b * x - b**2, "Viimeinen termi on (" + chr(0x2212) + f"{b})² = {b**2}, ei {chr(0x2212)}{b**2}."),
                      (x**2 + 2 * b * x + b**2, "Keskimmäisen termin merkki on miinus, koska termit ovat x ja " + chr(0x2212) + str(b) + ".")]
            steps = [f"(x {chr(0x2212)} {b})(x {chr(0x2212)} {b})", fmt(good)]
        elif k == 2:
            level, prompt = "T", f"Laske ilman laskinta: ({b} + {c})². Mikä on tulos?"
            good = (b + c) ** 2
            wrongs = [(b**2 + c**2, POW), (b**2 + b * c + c**2, POW), (b + c**2 if False else 2 * (b + c), "Potenssi tarkoittaa kertomista itsellään, ei kahdella kertomista.")]
            steps = [f"{b} + {c} = {b + c}", f"{b + c}² = {(b + c) ** 2}"]
        elif k == 3:
            level = "H"
            prompt = (f"Neliönmuotoisen pihan sivun pituus on (x + {b}) metriä. Mikä lauseke antaa pihan pinta-alan avattuna?")
            good = (x + b) ** 2
            wrongs = [(x**2 + b**2, "Neliö jakautuu osiin x², kaksi suorakulmiota x · " + str(b) + " ja " + str(b) + "²."),
                      (x**2 + b * x + b**2, "Suorakulmioita x · " + f"{b} on kaksi, ei yksi."),
                      (x**2 + 2 * b * x, "Pienen neliön " + f"{b}² = {b**2} puuttuu.")]
            steps = [f"Pinta-ala = (x + {b})²", f"x² + 2 · {b}x + {b}² = {fmt(good)}"]
        else:
            level = "H"
            n = rng.randint(1, 3)
            wrong_expr = x**2 + b**2
            prompt = (f"Oppilas väittää, että (x + {b})² = {fmt(wrong_expr)}. Miten väitteen voi tarkistaa sijoittamalla x = {n}?")
            lhs, rhs = (n + b) ** 2, n**2 + b**2
            assert lhs != rhs
            options, cid = mc_options(rng, (f"Vasen puoli on ({n} + {b})² = {lhs} ja oikea puoli {rhs}, joten väite on väärä",
                                            "Oikein: jos lausekkeet olisivat yhtä suuret, niiden arvot olisivat samat."), [
                (f"Molemmat puolet ovat {rhs}, joten väite on oikein", TID, POW),
                (f"Vasen puoli on {lhs} ja oikea {rhs}, mutta väite on silti oikein, koska potenssi jakautuu", TID, POW),
                ("Sijoittamalla ei voi tarkistaa lausekkeiden yhtäsuuruutta", TID, "Sijoittamalla voi tarkistaa, ovatko lausekkeet yhtä suuret.")])
            payload = {"options": options, "correct": [cid]}
            items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, prompt, payload,
                                   [f"x = {n}: ({n} + {b})² = {lhs}", f"{n}² + {b}² = {rhs}"], f"Arvot {lhs} ja {rhs} eroavat",
                                   "Oikein: väärä väite paljastuu, kun arvot eivät ole yhtä suuret.", TEMPLATE,
                                   {"b": b, "x": n}, date, run))
            continue
        seen, wl = {fmt(good)}, []
        for w, fb in wrongs:
            if fmt(w) not in seen:
                seen.add(fmt(w))
                wl.append((fmt(w), TID, fb))
        options, cid = mc_options(rng, (fmt(good), "Oikein: (a + b)² = a² + 2ab + b²."), wl)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, prompt, payload, steps, fmt(good),
                               "Oikein: (a + b)² = a² + 2ab + b².", TEMPLATE, {"b": b, "c": c}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
