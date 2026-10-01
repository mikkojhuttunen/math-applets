#!/usr/bin/env python3
"""EXT-01 (negative base and square: -3² read as 9), type MC. Values are computed with Python integers."""
import random

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "ext01_mc"
TID, CODE = "EXT-01", "MC"
BAD = ("Potenssimerkintä koskee vain sitä lukua, jonka vieressä se on. Lausekkeessa −3² potenssi lasketaan ensin: "
       "−3² = −(3 · 3) = −9. Vasta sulkeissa (−3)² = 9.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(905)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a = rng.choice([4, 5, 6, 7])
            v = -(a ** 2)
            prompt = f"Mikä on lausekkeen −{a}² arvo?"
            correct = (num(v), f"Oikein: −{a}² = −({a} · {a}) = {num(v)}.")
            wrongs = [(num(a ** 2), "EXT-01", BAD), (num(-2 * a), None, f"Tämä on −{a} · 2. Potenssi {a}² tarkoittaa {a} · {a}."),
                      (num(2 * a), None, f"Tämä on {a} · 2. Potenssi {a}² tarkoittaa {a} · {a}.")]
            steps = [f"−{a}² = −({a} · {a})", f"= {num(v)}"]
            final, params, level = num(v), {"a": a}, "T"
        elif k == 1:
            a = rng.choice([2, 3, 8, 9])
            prompt = "Mikä seuraavista väitteistä on oikein?"
            correct = (f"(−{a})² = {a ** 2} ja −{a}² = {num(-a ** 2)}", f"Oikein: sulkeet määräävät, kuuluuko miinus potenssin kantalukuun.")
            wrongs = [(f"(−{a})² = −{a ** 2} ja −{a}² = {a ** 2}", None, f"Tämä on päinvastoin. Sulkeissa (−{a})² = (−{a}) · (−{a}) = {a ** 2}."),
                      (f"(−{a})² = {a ** 2} ja −{a}² = {a ** 2}", "EXT-01", BAD),
                      (f"(−{a})² = −{a ** 2} ja −{a}² = −{a ** 2}", None, f"Kun {a}² kerrotaan luvulla −{a}, miinus kertaa miinus on plus: (−{a})² = {a ** 2}.")]
            steps = [f"(−{a})² = (−{a}) · (−{a}) = {a ** 2}", f"−{a}² = −({a} · {a}) = {num(-a ** 2)}"]
            final, params, level = f"(−{a})² = {a ** 2}, −{a}² = {num(-a ** 2)}", {"a": a}, "T"
        elif k == 2:
            a = rng.choice([3, 6, 7, 9])
            prompt = f"Laskin näyttää, että −{a}² = {num(-a ** 2)}. Onko tulos oikein?"
            correct = (f"On: potenssi lasketaan ensin, joten −{a}² = −({a} · {a}) = {num(-a ** 2)}", "Oikein.")
            wrongs = [(f"Ei ole: miinus kertaa miinus on plus, joten tuloksen pitäisi olla {a ** 2}", "EXT-01", BAD),
                      (f"Ei ole: tuloksen pitäisi olla {num(-2 * a)}", None, f"Potenssi {a}² tarkoittaa {a} · {a}, ei {a} · 2."),
                      ("Ei ole: laskimen tulos riippuu laskimesta", None, "Laskujärjestys on sovittu: potenssi lasketaan ennen etumerkkiä.")]
            steps = [f"−{a}² = −({a} · {a})", f"= {num(-a ** 2)}"]
            final, params, level = "On oikein", {"a": a}, "T"
        elif k == 3:
            a = rng.choice([3, 4, 5, 6])
            prompt = f"Mikä seuraavista lausekkeista on arvoltaan {a ** 2}?"
            correct = (f"(−{a})²", f"Oikein: (−{a})² = (−{a}) · (−{a}) = {a ** 2}.")
            wrongs = [(f"−{a}²", "EXT-01", BAD), (f"−({a}²)", None, f"Tämä on {num(-a ** 2)}: potenssi {a}² on {a ** 2} ja sen eteen tulee miinus."),
                      (f"−{a} · {a}", None, f"Tämä on {num(-a ** 2)}: erimerkkisten lukujen tulo on negatiivinen.")]
            steps = [f"(−{a})² = {a ** 2}", f"−{a}² = {num(-a ** 2)}"]
            final, params, level = f"(−{a})²", {"a": a}, "H"
        else:
            prompt = "Mikä perustelu on oikea sille, että −3² = −9 eikä 9?"
            correct = ("Potenssi koskee vain lukua 3, joten −3² = −(3 · 3) = −9", "Oikein: potenssi lasketaan ennen miinusmerkkiä.")
            wrongs = [("Potenssi koskee koko lukua −3, joten −3² = (−3) · (−3) = 9", "EXT-01", BAD),
                      ("Miinus ja potenssi kumoavat toisensa, joten tulos on −3 + 3 = 0", None, "Miinusmerkki ja potenssi eivät kumoa toisiaan."),
                      ("Tulos on −9, koska 3 · 3 = 9 ja luku on aina negatiivinen", None, "Etumerkki ei ole \"aina\" negatiivinen: (−3)² = 9.")]
            steps = ["Potenssi lasketaan ensin: 3² = 9", "Miinusmerkki tulee sen eteen: −9"]
            final, params, level = "Potenssi koskee vain lukua 3", {"a": 3, "justify": True}, "H"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S2.01", "S2.11"], ["T10", "T11"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: potenssi lasketaan ennen etumerkkiä.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
