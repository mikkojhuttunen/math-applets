#!/usr/bin/env python3
"""ALG-10 (reversal error), type MC. Every option equation is built from the same numbers."""
import random

from gen_common import LETTER_ADESSIVE, base_item, cli, mc_options

TEMPLATE = "alg10_mc"
TID, CODE = "ALG-10", "MC"
REV = "Kirjaimet on kirjoitettu sanojen järjestyksessä. Kerroin kuuluu sen suureen eteen, jota on vähemmän."
# (many description, few description, letter many, letter few, many genitive plural, few genitive plural)
CTX = [
    ("oppilaita", "opettajia", "o", "t", "oppilaiden", "opettajien"),
    ("kahvikuppeja", "teekuppeja", "k", "t", "kahvikuppien", "teekuppien"),
    ("pelaajia", "valmentajia", "p", "v", "pelaajien", "valmentajien"),
    ("kirjoja", "lehtiä", "k", "l", "kirjojen", "lehtien"),
    ("kyyhkysiä", "harakoita", "k", "h", "kyyhkysten", "harakoiden"),
]


def make_items(run, date, count=5, start=1):
    rng = random.Random(301)
    items = []
    for k in range(count):
        many, few, m, f, many_gen, few_gen = CTX[k]
        letters = (f"Merkitään {many_gen} määrää {LETTER_ADESSIVE[m]} ja {few_gen} määrää {LETTER_ADESSIVE[f]}. ")
        n = rng.randint(3, 9)
        if k < 3:
            level = "T"
            prompt = letters + (f"Koululla on {n} kertaa enemmän {many} kuin {few}." if k == 0 else
                                f"Tapahtumassa on {n} kertaa enemmän {many} kuin {few}.")
            correct = f"{m} = {n}{f}"
            good = f"{many.capitalize()} on {n} kertaa niin paljon kuin {few}, joten {correct}."
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
            prompt = letters + (f"{many.capitalize()} on {d} enemmän kuin {({2: 'kaksi', 3: 'kolme', 4: 'neljä'}[c])} kertaa {few_gen} määrä."
                      + " Mikä yhtälö kuvaa tilannetta?")
            correct = f"{m} = {c}{f} + {d}"
            good = f"{many.capitalize()} on {c} kertaa niin paljon kuin {few} ja lisäksi {d}, joten {correct}."
            wrongs = [(f"{c}{m} + {d} = {f}", "ALG-10", REV), (f"{m} = {c}({f} + {d})", None, f"Nyt {d} lisätään myös kerrottavaan, mutta vain kertolaskun tulokseen lisätään {d}."),
                      (f"{m} = {c}{f} {chr(0x2212)} {d}", None, "'Enemmän' tarkoittaa lisäämistä, ei vähentämistä.")]
            steps = [f"Kerrotaan ensin: {c} · {f}", f"Lisätään {d}: {m} = {c}{f} + {d}"]
            final = correct
            ops, tt = ["S1.04", "S3.05"], ["T14", "T7"]
        options, cid = mc_options(rng, (correct.replace("*", ""), good), wrongs)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ops, tt, 7 if k < 3 else 8, level, prompt, payload, steps, final,
                               "Suuremman määrän kirjain on yhtälön yksin puolella.", TEMPLATE,
                               {"n": n} if k < 3 else {"c": c, "d": d}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
