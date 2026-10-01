#!/usr/bin/env python3
"""ALG-06 (operational reading of '='), type NE (number entry). Fixed seed, answers computed."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg06_ne"
TID, CODE = "ALG-06", "NE"
HINT = "Yhtäsuuruusmerkki kertoo, että molemmat puolet ovat yhtä suuret. Laske ensin se puoli, jossa ei ole laatikkoa."


def make_items(run, date, count=5, start=1):
    rng = random.Random(202)
    items = []
    for k in range(count):
        while True:
            a, b, c, d = (rng.randint(3, 9) for _ in range(4))
            if len({a, b, c}) == 3 and a + b > c + 1 and a > b > 0 and a - b > d:
                break
        s = a + b
        if k == 0:
            level, form = "T", "sum_left"
            prompt, ans = f"Täydennä luku: {a} + {b} = □ + {c}", s - c
            wrong = [(s, "ALG-06"), (s + c, "ALG-06")]
            steps = [f"{a} + {b} = {s}", f"□ + {c} = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
        elif k == 1:
            level, form = "T", "box_left"
            prompt, ans = f"Täydennä luku: □ + {c} = {a} + {b}", s - c
            wrong = [(s, "ALG-06"), (s + c, "ALG-06")]
            steps = [f"{a} + {b} = {s}", f"□ + {c} = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
        elif k == 2:
            level, form = "T", "box_last"
            prompt, ans = f"Täydennä luku: {a} + {b} = {c} + □", s - c
            wrong = [(s, "ALG-06"), (s + c, "ALG-06")]
            steps = [f"{a} + {b} = {s}", f"{c} + □ = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
        elif k == 3:
            level, form = "H", "minus"
            prompt, ans = f"Täydennä luku: {a} {MINUS} {b} = □ + {d}", a - b - d
            wrong = [(a - b, "ALG-06"), (a - b + d, "ALG-06")]
            steps = [f"{a} {MINUS} {b} = {a - b}", f"□ + {d} = {a - b}", f"□ = {a - b} {MINUS} {d} = {ans}"]
        else:
            level, form = "H", "balance"
            prompt = (f"Vaa'an vasemmassa kupissa on {a} kg:n ja {b} kg:n painot, oikeassa kupissa {c} kg:n paino. "
                      f"Montako kilogrammaa oikeaan kuppiin on lisättävä, jotta vaaka on tasapainossa?")
            ans = s - c
            wrong = [(s, "ALG-06"), (s + c, "ALG-06")]
            steps = [f"Vasen kuppi: {a} + {b} = {s} kg", f"Oikea kuppi: {c} + □ = {s}", f"□ = {s} {MINUS} {c} = {ans}"]
        assert ans > 0 and all(w != ans for w, _ in wrong) and len({w for w, _ in wrong}) == 2
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": w, "misconception": m, "feedback": HINT} for w, m in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps, str(ans),
                               "Oikein: puolten arvojen on oltava yhtä suuret.", TEMPLATE,
                               {"a": a, "b": b, "c": c, "d": d, "form": form}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
