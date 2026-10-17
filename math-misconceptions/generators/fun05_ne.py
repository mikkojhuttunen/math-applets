#!/usr/bin/env python3
"""FUN-05 (every linear function is proportional), type NE. Answers come from y = a x + b; the tagged wrong answer
assumes proportionality (y scales with x)."""
import random

from gen_common import base_item, cli

TEMPLATE = "fun05_ne"
TID, CODE = "FUN-05", "NE"
BAD = ("Lineaarinen funktio ei ole aina suoraan verrannollinen: vakiotermi ei kasva x:n mukana. "
       "Laske arvo sijoittamalla x lausekkeeseen tai käytä muutosta.")
GOOD = "Oikein: arvo lasketaan sijoittamalla lausekkeeseen; x:n kaksin- tai kolminkertaistaminen ei kerro y:tä samoin."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1271)
    items = []
    for k in range(count):
        if k == 0:
            a, b = rng.choice([(2, 3), (3, 4), (5, 2)])
            x0 = rng.choice([4, 5, 6])
            ans, wrong = a * 2 * x0 + b, 2 * (a * x0 + b)
            prompt = f"Funktio on y = {a}x + {b}. Kun x = {x0}, y = {a * x0 + b}. Mikä on y, kun x = {2 * x0}?"
            steps = [f"y = {a} · {2 * x0} + {b} = {ans}", f"Ei {wrong}, sillä funktio ei ole suoraan verrannollinen"]
            level, params = "T", {"a": a, "b": b, "x0": x0, "form": k}
        elif k == 1:
            a, b = rng.choice([(2, 4), (3, 5), (4, 6)])
            ans, wrong = a * 10 + b, 2 * (a * 5 + b)
            prompt = (f"Pizzan kuljetuksen hinta on {b} € + {a} € jokaiselta kilometriltä. 5 km:n kuljetus maksaa {a * 5 + b} €. "
                      "Mitä 10 km:n kuljetus maksaa euroina?")
            steps = [f"{b} + {a} · 10 = {ans}"]
            level, params = "T", {"a": a, "b": b, "form": k}
        elif k == 2:
            a, b = rng.choice([(3, 2), (4, 5), (2, 6)])
            x0 = rng.choice([2, 3])
            ans, wrong = a * 3 * x0 + b, 3 * (a * x0 + b)
            prompt = f"Funktio on y = {a}x + {b}. Kun x = {x0}, y = {a * x0 + b}. Mikä on y, kun x = {3 * x0}?"
            steps = [f"y = {a} · {3 * x0} + {b} = {ans}"]
            level, params = "T", {"a": a, "b": b, "x0": x0, "form": k}
        elif k == 3:
            a, b = rng.choice([(3, 4), (2, 5), (5, 3)])
            x0 = rng.choice([3, 4, 6])
            ans, wrong = a * x0, a * x0 + b
            prompt = f"Funktio on y = {a}x + {b}. Kuinka paljon y:n arvo kasvaa, kun x kasvaa arvosta {x0} arvoon {2 * x0}?"
            steps = [f"y({x0}) = {a * x0 + b}, y({2 * x0}) = {a * 2 * x0 + b}", f"Kasvu = {a * 2 * x0 + b} − {a * x0 + b} = {ans}"]
            level, params = "H", {"a": a, "b": b, "x0": x0, "form": k}
        else:
            p, q = rng.choice([(5, 7), (4, 7), (3, 8)])
            ans, wrong = p + 3 * (q - p), 4 * p
            prompt = f"Suoralla on piste (1, {p}) ja piste (2, {q}). Mikä on y, kun x = 4?"
            steps = [f"Kulmakerroin = ({q} − {p}) / (2 − 1) = {q - p}", f"y = {p} + 3 · {q - p} = {ans}"]
            level, params = "H", {"p": p, "q": q, "form": k}
        assert ans != wrong
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": wrong, "misconception": TID, "feedback": BAD}],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S4.03"], ["T14", "T15"], 8, level, prompt, payload, steps,
                               str(ans), GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
