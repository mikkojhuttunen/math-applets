#!/usr/bin/env python3
"""ALG-03 (value from alphabet position), type NE. The answer is computed from the equation; the tagged wrong
answer is the letter's position in the alphabet (or the position of the next letter in item 5)."""
import random

from gen_common import base_item, cli

TEMPLATE = "alg03_ne"
TID, CODE = "ALG-03", "NE"
BAD = ("Kirjaimen paikka aakkosissa ei vaikuta sen arvoon. Kirjain on tuntematon luku, jonka arvo ratkaistaan "
       "yhtälöstä.")
GOOD = "Oikein: kirjaimen arvo ratkaistaan yhtälöstä, ei aakkospaikasta."
LETTERS = "kmnptwyd"


def pos(ch):
    return ord(ch) - 96


def make_items(run, date, count=5, start=1):
    rng = random.Random(302)
    items, used = [], set()
    for k in range(count):
        while True:
            ch = rng.choice(LETTERS)
            if ch not in used:
                break
        used.add(ch)
        p = pos(ch)
        v = rng.choice([x for x in range(3, 13) if abs(x - p) > 1])
        M = chr(8722)
        if k == 0:
            c = rng.choice([4, 5, 7, 8])
            prompt, level = f"{ch} + {c} = {v + c}. Mikä on {ch}?", "T"
            ans, wrong = v, [p]
            steps = [f"{ch} = {v + c} {M} {c} = {v}"]
        elif k == 1:
            c = rng.choice([2, 3, 4])
            prompt, level = f"{c}{ch} = {c * v}. Mikä on {ch}?", "T"
            ans, wrong = v, [p]
            steps = [f"{ch} = {c * v} ÷ {c} = {v}"]
        elif k == 2:
            c = rng.choice([3, 4, 6])
            prompt, level = f"{ch} {M} {c} = {v - c}. Mikä on {ch}?", "T"
            ans, wrong = v, [p]
            steps = [f"{ch} = {v - c} + {c} = {v}"]
        elif k == 3:
            prompt, level = f"Luvun {ch} kaksinkertainen on {2 * v}. Mikä on luku {ch}?", "H"
            ans, wrong = v, [p]
            steps = [f"2{ch} = {2 * v}", f"{ch} = {v}"]
        else:
            ch2 = chr(ord(ch) + 1)
            prompt = (f"Tiedetään, että {ch} + 2 = {v + 2} ja {ch2} = {ch} + 1. Mikä on {ch2}?")
            level = "H"
            ans, wrong = v + 1, [pos(ch2), p]
            steps = [f"{ch} = {v + 2} {M} 2 = {v}", f"{ch2} = {v} + 1 = {v + 1}"]
        wrong = [w for w in dict.fromkeys(wrong) if w != ans]
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": w, "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T14", "T15"], 7, level, prompt, payload, steps,
                               str(ans), GOOD, TEMPLATE, {"letter": ch, "position": p, "value": v, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
