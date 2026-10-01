#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type NE. The solutions of p x² + q = 0 are found by brute force over an
integer window; each question asks for a value that needs both roots, and the tagged wrong answer is the value
obtained from the positive root only."""
import random

from gen_common import base_item, cli, num

TEMPLATE = "ext04_ne"
TID, CODE = "EXT-04", "NE"
BAD = ("Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0: positiivinen ja negatiivinen juuri. "
       "Tarkista sijoittamalla: myös vastaluku toteuttaa yhtälön.")
GOOD = "Oikein: neliö ei erota lukua ja sen vastalukua, joten otetaan huomioon sekä positiivinen että negatiivinen juuri."


def roots(p, q):
    return [x for x in range(-60, 61) if p * x * x + q == 0]


def make_items(run, date, count=5, start=1):
    rng = random.Random(1402)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a = rng.choice([6, 8, 9])
            p, q, level = 1, -a * a, "T"
            prompt = f"Ratkaise yhtälö x² = {a * a}. Kirjoita negatiivinen ratkaisu."
            r = roots(p, q)
            ans, wrong = min(r), max(r)
            steps = [f"x² = {a * a}", f"x = {a} tai x = {num(-a)}", f"Negatiivinen ratkaisu on {num(-a)}"]
        elif k == 1:
            a, p = rng.choice([(5, 3), (4, 5), (3, 2)])
            q, level = -p * a * a, "T"
            prompt = f"Ratkaise yhtälö {p}x² = {p * a * a}. Kirjoita pienempi ratkaisu."
            r = roots(p, q)
            ans, wrong = min(r), max(r)
            steps = [f"x² = {a * a}", f"x = {a} tai x = {num(-a)}", f"Pienempi ratkaisu on {num(-a)}"]
        elif k == 2:
            a = rng.choice([7, 11, 12])
            p, q, level = 1, -a * a, "H"
            prompt = (f"Kaksi eri lukua toteuttavat yhtälön x² − {a * a} = 0. "
                      "Kuinka suuri on lukujen etäisyys toisistaan lukusuoralla?")
            r = roots(p, q)
            ans, wrong = max(r) - min(r), max(r)
            steps = [f"x² = {a * a}", f"x = {a} tai x = {num(-a)}", f"Etäisyys on {a} − ({num(-a)}) = {2 * a}"]
        elif k == 3:
            a, p = rng.choice([(4, 3), (6, 2), (5, 4)])
            q, level = -p * a * a, "T"
            prompt = f"Kuinka monta ratkaisua yhtälöllä {p}x² − {p * a * a} = 0 on?"
            r = roots(p, q)
            ans, wrong = len(r), 1
            steps = [f"{p}x² = {p * a * a}", f"x² = {a * a}", f"x = {a} tai x = {num(-a)}", f"Ratkaisuja on {len(r)}"]
        else:
            a, p = rng.choice([(5, 2), (3, 6), (4, 3)])
            q, level = -p * a * a, "H"
            prompt = (f"Ratkaise yhtälö {p}x² − {p * a * a} = 0 ja laske kaikkien ratkaisujen itseisarvojen summa.")
            r = roots(p, q)
            ans, wrong = sum(abs(x) for x in r), a
            steps = [f"x² = {a * a}", f"x = {a} tai x = {num(-a)}", f"|{a}| + |{num(-a)}| = {2 * a}"]
        assert wrong != ans and len(r) == 2
        key = (k, a, p)
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": wrong, "misconception": TID, "feedback": BAD}],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, prompt, payload, steps,
                               num(ans), GOOD, TEMPLATE, {"a": a, "p": p, "q": q}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
