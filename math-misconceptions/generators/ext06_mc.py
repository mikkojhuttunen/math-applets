#!/usr/bin/env python3
"""EXT-06 (sine read as a length; adjacent and opposite leg mixed up), type MC. Ratios are computed with exact
fractions from Pythagorean triples; the tagged distractors give a side length as the sine or use the adjacent leg."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options

TEMPLATE = "ext06_mc"
TID, CODE = "EXT-06", "MC"
BAD = ("Sini on suhdeluku: vastainen kateetti jaettuna hypotenuusalla. Se ei ole pituus eikä siinä ole yksikköä, "
       "ja viereinen kateetti kuuluu kosinille.")
GOOD = "Oikein: sin α = vastainen kateetti / hypotenuusa."
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15)]


def fr(f):
    return f"{f.numerator}/{f.denominator}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1706)
    items, seen = [], set()
    for k in range(count):
        a, b, c = rng.choice([t for t in TRIPLES if t not in seen])
        seen.add((a, b, c))
        assert a * a + b * b == c * c
        sin, cos, tan = Fraction(a, c), Fraction(b, c), Fraction(a, b)
        assert len({sin, cos, tan}) == 3
        if k == 0:
            level = "T"
            prompt = (f"Suorakulmaisen kolmion kateetit ovat {a} cm ja {b} cm ja hypotenuusa {c} cm. "
                      f"Kulman α vastainen kateetti on {a} cm. Mikä on sin α?")
            correct = (fr(sin), GOOD)
            wrongs = [(f"{a} cm", TID, BAD), (fr(cos), TID, "Tämä on viereinen kateetti jaettuna hypotenuusalla, eli cos α."),
                      (fr(tan), None, "Tämä on vastainen jaettuna viereisellä kateetilla, eli tan α.")]
            steps = [f"sin α = vastainen / hypotenuusa = {a}/{c}"]
        elif k == 1:
            level = "T"
            names = rng.choice([("A", "B", "C"), ("P", "Q", "R"), ("K", "L", "M")])
            x, y, z = names
            prompt = (f"Kolmiossa {x}{y}{z} kulma {z} on suora ja α on kulma {x}. Mikä sivu on kulman α vastainen kateetti?")
            correct = (f"{y}{z}", "Oikein: vastainen kateetti on kulmaa vastapäätä oleva sivu, ja kulma α on kärjessä " + x + ".")
            wrongs = [(f"{x}{z}", TID, "Sivu " + x + z + " on kulman α viereinen kateetti. Vastainen kateetti on kulmaa vastapäätä."),
                      (f"{x}{y}", None, f"Sivu {x}{y} on suoran kulman vastapäinen sivu eli hypotenuusa, ei kateetti."),
                      (f"{x}{y}{z}", None, "Tämä on koko kolmio, ei sivu.")]
            steps = [f"Kulma α on kärjessä {x}", f"Sen vastapäinen sivu on {y}{z}"]
            sin = None
        elif k == 2:
            level = "T"
            prompt = (f"Oppilas kirjoittaa: \"sin α = {a} cm\", kun suorakulmaisen kolmion vastainen kateetti on {a} cm "
                      f"ja hypotenuusa {c} cm. Mikä on virhe?")
            correct = (f"Sini on suhdeluku: oikea arvo on {fr(sin)}, eikä siinä ole yksikköä", GOOD)
            wrongs = [(f"Ei virhettä, sini on vastaisen kateetin pituus", TID, BAD),
                      (f"Pitäisi jakaa viereisellä kateetilla {b} cm, jolloin saadaan {fr(tan)}", None,
                       "Vastainen jaettuna viereisellä kateetilla on tan α, ei sin α."),
                      (f"Pitäisi jakaa hypotenuusalla, mutta käyttää viereistä kateettia {b} cm", TID,
                       "Sinin osoittaja on vastainen kateetti, ei viereinen.")]
            steps = [f"sin α = {a}/{c}"]
        elif k == 3:
            level = "H"
            prompt = "Voiko suorakulmaisen kolmion kulman sini olla suurempi kuin 1?"
            correct = ("Ei, koska kateetti on aina lyhyempi kuin hypotenuusa, joten suhde on pienempi kuin 1", GOOD)
            wrongs = [("Kyllä, jos kolmio on tarpeeksi suuri, koska sini on sivun pituus", TID, BAD),
                      ("Kyllä, jos kulma on tarpeeksi suuri", None, "Teräväkulmaisen kulman sini on aina välillä 0 ja 1."),
                      ("Kyllä, jos viereinen kateetti on pidempi kuin vastainen", TID,
                       "Sini ei riipu viereisestä kateetista: se on vastainen / hypotenuusa, ja hypotenuusa on pisin sivu.")]
            steps = ["sin α = vastainen / hypotenuusa", "Hypotenuusa on pisin sivu, joten suhde < 1"]
            sin = None
        else:
            level = "H"
            m = rng.choice([2, 3])
            prompt = (f"Kolmion kateetit ovat {a} cm ja {b} cm ja hypotenuusa {c} cm. Toisen samanmuotoisen kolmion "
                      f"sivut ovat {m} kertaa pidemmät. Mitä tapahtuu sinille sin α?")
            correct = (f"Se ei muutu: sin α = {fr(sin)}", "Oikein: suhde pysyy samana, kun kolmiota suurennetaan.")
            wrongs = [(f"Se muuttuu {m}-kertaiseksi, koska vastainen kateetti pitenee {m}-kertaiseksi", TID, BAD),
                      (f"Se muuttuu {m} kertaa pienemmäksi", None, "Hypotenuusa ja kateetti kasvavat yhtä paljon, joten suhde ei muutu."),
                      (f"Se on {fr(cos)}, koska viereinen kateetti ei muutu", TID, "Sinin osoittaja on vastainen kateetti, ja kaikki sivut muuttuvat.")]
            steps = [f"Uudet sivut {m * a}, {m * b}, {m * c}", f"sin α = {m * a}/{m * c} = {fr(sin)}"]
        options, cid = mc_options(rng, correct, wrongs)
        final = correct[0]
        items.append(base_item(TID, CODE, start + k, ["S5.10"], ["T17"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE,
                               {"triple": [a, b, c]}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
