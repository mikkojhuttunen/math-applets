#!/usr/bin/env python3
"""EXT-01 (negative base and square: -3² read as 9), type NE. Answers are computed with Python integers;
the typical wrong answer reads -a² as (-a)²."""
import random

from gen_common import base_item, cli, num

TEMPLATE = "ext01_ne"
TID, CODE = "EXT-01", "NE"
BAD = ("Potenssi koskee vain sitä lukua, jonka vieressä se on: −a² = −(a · a). Vasta sulkeissa (−a)² = a².")


def make_items(run, date, count=5, start=1):
    rng = random.Random(906)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a = rng.choice([3, 4, 5, 6])
            ans, wrong = -a ** 2, [a ** 2]
            prompt = f"Laske −{a}²."
            steps = [f"−{a}² = −({a} · {a})", f"= {num(ans)}"]
            params = {"a": a}
        elif k == 1:
            a, b = rng.choice([2, 3, 4]), rng.choice([10, 15, 20])
            ans, wrong = b - a ** 2, [b + a ** 2]
            prompt = f"Laske −{a}² + {b}."
            steps = [f"−{a}² = {num(-a ** 2)}", f"{num(-a ** 2)} + {b} = {num(ans)}"]
            params = {"a": a, "b": b}
        elif k == 2:
            a = rng.choice([5, 6, 7])
            ans, wrong = -2 * a ** 2, [0]
            prompt = f"Laske −{a}² − (−{a})²."
            steps = [f"−{a}² = {num(-a ** 2)}", f"(−{a})² = {a ** 2}", f"{num(-a ** 2)} − {a ** 2} = {num(ans)}"]
            params = {"a": a}
        elif k == 3:
            x = -rng.choice([3, 4, 5])
            ans, wrong = -(x ** 2), [x ** 2]
            prompt = f"Laske lausekkeen −x² arvo, kun x = {num(x)}."
            steps = [f"x² = ({num(x)})² = {x ** 2}", f"−x² = {num(ans)}"]
            params = {"x": x}
        else:
            a = rng.choice([2, 3])
            ans, wrong = -a ** 3, [a ** 2 + a ** 2 - a ** 3]
            prompt = f"Laske −{a}² + (−{a})² + (−{a})³."
            steps = [f"−{a}² = {num(-a ** 2)}", f"(−{a})² = {a ** 2}", f"(−{a})³ = {num(-a ** 3)}", f"summa = {num(ans)}"]
            params = {"a": a}
        assert all(w != ans for w in wrong)
        key = str(params) + str(k)
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "EXT-01", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S2.01", "S2.11"], ["T10", "T11"], 7, "T" if k < 3 else "H", prompt,
                               payload, steps, num(ans), "Oikein: potenssi lasketaan ennen etumerkkiä.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
