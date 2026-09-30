#!/usr/bin/env python3
"""ALG-05 (juxtaposition read as place value), type NE (number entry). Fixed seed, answers computed."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg05_ne"
TID, CODE = "ALG-05", "NE"
OP = "Luku ja kirjain vierekkäin tarkoittavat kertolaskua, eivät kymmeniä ja ykkösiä."


def make_items(run, date, count=5, start=1):
    rng = random.Random(322)
    items = []
    for k in range(count):
        c, v = rng.randint(2, 8), rng.randint(2, 9)
        while v == c:
            v = rng.randint(2, 9)
        letter = "nkmpt"[k]
        glued = 10 * c + v
        if k < 2:
            level = "T"
            prompt = f"Laske lausekkeen {c}{letter} arvo, kun {letter} = {v}."
            answer = c * v
            wrong = [(glued, "ALG-05", OP), (c + v, None, "Luku ja kirjain vierekkäin tarkoittavat kertolaskua, ei yhteenlaskua.")]
            steps = [f"{c}{letter} = {c} · {letter}", f"= {c} · {v}", f"= {answer}"]
        elif k == 2:
            level = "T"
            e = rng.randint(2, 6)
            prompt = f"Laske lausekkeen {c}{letter} {MINUS} {e} arvo, kun {letter} = {v}."
            answer = c * v - e
            wrong = [(glued - e, "ALG-05", OP), (c + v - e, None, "Luku ja kirjain vierekkäin tarkoittavat kertolaskua.")]
            steps = [f"{c}{letter} {MINUS} {e} = {c} · {v} {MINUS} {e}", f"= {c * v} {MINUS} {e}", f"= {answer}"]
        elif k == 3:
            level = "H"
            u, w = "ab"
            e = rng.randint(2, 6)
            prompt = f"Laske lausekkeen {u}{w} + {e} arvo, kun {u} = {c} ja {w} = {v}."
            answer = c * v + e
            wrong = [(glued + e, "ALG-05", OP), (c + v + e, None, "Kirjainten välissä ei ole plusmerkkiä: vierekkäin tarkoittaa kertolaskua.")]
            steps = [f"{u}{w} = {u} · {w} = {c} · {v} = {c * v}", f"{c * v} + {e} = {answer}"]
        else:
            level = "H"
            price = rng.randint(2, 6)
            qty = rng.randint(3, 8)
            pay = 100
            prompt = (f"Yksi kirja maksaa p euroa. Ostetaan {qty} kirjaa, jolloin hinta euroina on {qty}p. "
                      f"Kun p = {price}, maksetaan {pay} euron setelillä. Paljonko vaihtorahaa saadaan euroina?")
            answer = pay - qty * price
            wrong = [(pay - (10 * qty + price), "ALG-05", OP), (pay - (qty + price), None, "Hinta on kertolasku: " + f"{qty} · {price}.")]
            steps = [f"Hinta: {qty}p = {qty} · {price} = {qty * price}", f"Vaihtoraha: {pay} {MINUS} {qty * price} = {answer}"]
        assert all(w[0] != answer for w in wrong) and len({w[0] for w in wrong}) == len(wrong)
        payload = {"answer": {"kind": "number", "value": answer},
                   "wrong": [{"match": m, "misconception": t, "feedback": f} for m, t, f in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15"], 7, level, prompt, payload, steps, str(answer),
                               "Oikein: luku ja kirjain vierekkäin tarkoittavat kertolaskua.", TEMPLATE,
                               {"c": c, "v": v}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
