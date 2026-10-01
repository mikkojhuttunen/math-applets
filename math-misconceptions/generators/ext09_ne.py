#!/usr/bin/env python3
"""EXT-09 (slope and intercept confused; steeper line means larger y), type NE. Answers are computed from the line
y = m x + b; the tagged wrong answers give the intercept where the slope is asked (and the reverse)."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext09_ne"
TID, CODE = "EXT-09", "NE"
BAD = ("Kulmakerroin ja vakiotermi menevät sekaisin. Suoralla y = mx + b luku m on x:n kerroin eli kulmakerroin "
       "ja b on y:n arvo kohdassa x = 0.")
GOOD = "Oikein: kulmakerroin on x:n kerroin, vakiotermi on y:n arvo kohdassa x = 0."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1902)
    items = []
    for k in range(count):
        m, b = rng.choice([2, 3, 4, 5]), rng.choice([1, 2, 6, 7, 8, 9])
        if k == 1:
            m = -rng.choice([2, 3, 4])
        if k == 0:
            prompt = f"Suoran yhtälö on y = {m}x + {b}. Mikä on suoran kulmakerroin?"
            ans, wrong, level = m, [(b, TID), (m + b, None)], "T"
            steps = [f"Muoto y = mx + b, joten m = {m}"]
        elif k == 1:
            prompt = f"Suoran yhtälö on y = {b} {MINUS} {abs(m)}x. Mikä on suoran kulmakerroin?"
            ans, wrong, level = m, [(b, TID), (abs(m), None)], "T"
            steps = [f"Kirjoitetaan y = {num(m)}x + {b}", f"Kulmakerroin on {num(m)}"]
        elif k == 2:
            prompt = f"Suora y = {m}x + {b} leikkaa y-akselin pisteessä (0, y). Mikä on y?"
            ans, wrong, level = b, [(m, TID), (m + b, None)], "T"
            steps = [f"Sijoitetaan x = 0: y = {m} · 0 + {b} = {b}"]
        elif k == 3:
            prompt = (f"Suoran pisteiden taulukossa x = 0, 1, 2 ja y = {b}, {b + m}, {b + 2 * m}. "
                      f"Mikä on suoran kulmakerroin?")
            ans, wrong, level = m, [(b, TID), (b + m, None), (b + 2 * m, TID)], "H"
            steps = [f"Kun x kasvaa yhdellä, y muuttuu {b + m} {MINUS} {b} = {m}", f"Kulmakerroin on {m}"]
        else:
            prompt = (f"Suoran y = {m}x + {b} pisteessä x = 0 on y = {b}. Kuinka paljon y kasvaa, kun x kasvaa 4 "
                      f"yksikköä?")
            ans, wrong, level = 4 * m, [(m, None), (4 * b, TID)], "H"
            steps = [f"Kulmakerroin on {m}, joten 4 yksikön muutoksella y muuttuu 4 · {m} = {4 * m}"]
        wrong = [(w, t) for w, t in dict(wrong).items() if w != ans]
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": w, "misconception": t, "feedback": BAD if t else
                              "Tarkista, mitä lukua kysytään: kulmakerroin on x:n kerroin."} for w, t in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S4.05"], ["T15"], 8, level, prompt, payload, steps,
                               num(ans), GOOD, TEMPLATE, {"m": m, "b": b, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
