#!/usr/bin/env python3
"""ALG-10 (reversal error), type MC. Every option equation is built from the same numbers."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "alg10_mc"
TID, CODE = "ALG-10", "MC"
REV = "Kirjaimet on kirjoitettu sanojen järjestyksessä. Kerroin kuuluu sen suureen eteen, jota on vähemmän."
# (many description, few description, letter many, letter few)
CTX = [
    ("oppilaita", "opettajia", "o", "t"),
    ("kahvikuppeja", "teekuppeja", "k", "t"),
    ("pelaajia", "valmentajia", "p", "v"),
    ("kirjoja", "lehtiä", "k", "l"),
    ("kyyhkysiä", "harakoita", "k", "h"),
]


def make_items(run, date, count=5, start=1):
    rng = random.Random(301)
    items = []
    for k in range(count):
        many, few, m, f = CTX[k]
        n = rng.randint(3, 9)
        if k < 3:
            level = "T"
            prompt = (f"Koululla on {n} kertaa enemmän {many} ({m}) kuin {few} ({f})." if k == 0 else
                      f"Tapahtumassa on {n} kertaa enemmän {many} ({m}) kuin {few} ({f}).")
            correct = f"{m} = {n}{f}"
            wrongs = [(f"{n}{m} = {f}", "ALG-10", REV), (f"{m} = {f} + {n}", None, "Tässä lisätään, mutta 'kertaa enemmän' tarkoittaa kertolaskua."),
                      (f"{m} = {f}/{n}", None, f"{m} on suurempi luku, joten {f}:ää pitää kertoa, ei jakaa.")]
            prompt += " Mikä yhtälö kuvaa tilannetta?"
            steps = [f"{m} on suurempi: {m} on {n} kertaa {f}", f"{m} = {n} · {f}"]
            final = correct
            ops, tt = ["S1.04"], ["T14", "T7"]
        else:
            level = "H"
            c = rng.randint(2, 4)
            d = rng.randint(2, 9)
            prompt = (f"{many.capitalize()} ({m}) on {d} enemmän kuin kolminkertainen määrä {few} ({f})." .replace("kolminkertainen", {2: "kaksinkertainen", 3: "kolminkertainen", 4: "nelinkertainen"}[c])
                      + " Mikä yhtälö kuvaa tilannetta?")
            correct = f"{m} = {c}{f} + {d}"
            wrongs = [(f"{c}{m} + {d} = {f}", "ALG-10", REV), (f"{m} = {c}({f} + {d})", None, f"Nyt {d} lisätään myös kerrottavaan, mutta vain kertolaskun tulokseen lisätään {d}."),
                      (f"{m} = {c}{f} {chr(0x2212)} {d}", None, "'Enemmän' tarkoittaa lisäämistä, ei vähentämistä.")]
            steps = [f"Kerrotaan ensin: {c} · {f}", f"Lisätään {d}: {m} = {c}{f} + {d}"]
            final = correct
            ops, tt = ["S1.04", "S3.05"], ["T14", "T7"]
        options, cid = mc_options(rng, (correct.replace("*", ""), "Oikein."), wrongs)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ops, tt, 7 if k < 3 else 8, level, prompt, payload, steps, final,
                               "Oikein: suuremman määrän kirjain on yhtälön yksin puolella.", TEMPLATE,
                               {"n": n} if k < 3 else {"c": c, "d": d}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
