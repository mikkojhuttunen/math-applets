#!/usr/bin/env python3
"""ALG-12 (subtraction of a negative number), type NE. Answers are computed from the integers; the tagged wrong
answer subtracts the absolute value of the negative number."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "alg12_ne"
TID, CODE = "ALG-12", "NE"
BAD = ("Negatiivisen luvun vähentäminen ei pienennä lukua. Vähentäminen on vastaluvun lisäämistä: "
       "a − (−b) = a + b.")
GOOD = "Oikein: negatiivisen luvun vähentäminen on sen vastaluvun lisäämistä, a − (−b) = a + b."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1202)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b = rng.randint(2, 12), rng.randint(2, 12)
            if a != b and (a, b) not in seen:
                break
        seen.add((a, b))
        if k == 0:
            prompt, level = f"Laske {a} {MINUS} ({MINUS}{b}).", "T"
            ans, wrong = a + b, [a - b]
            steps = [f"{a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b}"]
        elif k == 1:
            prompt, level = f"Laske {MINUS}{a} {MINUS} ({MINUS}{b}).", "T"
            ans, wrong = b - a, [-(a + b)]
            steps = [f"{MINUS}{a} {MINUS} ({MINUS}{b}) = {MINUS}{a} + {b} = {num(b - a)}"]
        elif k == 2:
            prompt, level = f"Laske {a} {MINUS} ({MINUS}{b}) {MINUS} ({MINUS}{b}).", "T"
            ans, wrong = a + 2 * b, [a - 2 * b]
            steps = [f"{a} + {b} + {b} = {a + 2 * b}"]
        elif k == 3:
            prompt = (f"Päivän ylin lämpötila on {a} °C ja alin {MINUS}{b} °C. Kuinka monta astetta ylin lämpötila "
                      f"on alinta korkeampi?")
            level = "H"
            ans, wrong = a + b, [a - b]
            steps = [f"Erotus on {a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b}"]
        else:
            prompt = (f"Sukeltaja on syvyydessä {MINUS}{a} m ja lokki korkeudella {b} m merenpinnasta. "
                      f"Mikä on lokin ja sukeltajan korkeusero metreinä?")
            level = "H"
            ans, wrong = a + b, [b - a]
            steps = [f"{b} {MINUS} ({MINUS}{a}) = {b} + {a} = {a + b}"]
        wrong = [w for w in dict.fromkeys(wrong) if w != ans]
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": w, "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S2.01"], ["T10", "T11"], 7, level, prompt, payload, steps,
                               num(ans), GOOD, TEMPLATE, {"a": a, "b": b, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
