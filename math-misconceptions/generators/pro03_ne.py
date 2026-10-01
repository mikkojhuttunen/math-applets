#!/usr/bin/env python3
"""PRO-03 (same perimeter means same area), type NE. The answer is computed from the side lengths; the typical wrong
entry repeats the area of the other shape with the same perimeter."""
import random

from gen_common import base_item, cli

TEMPLATE = "pro03_ne"
TID, CODE = "PRO-03", "NE"
BAD = "Sama piiri ei tarkoita samaa alaa. Laske pinta-ala kuvion omista sivuista: ala = pituus · leveys."


def make_items(run, date, count=5, start=1):
    rng = random.Random(832)
    items = []
    for k in range(count):
        unit = None
        if k == 0:
            level = "T"
            while True:
                a, b = rng.randint(2, 9), rng.randint(3, 13)
                if a != b and (a + b) % 2 == 0:
                    break
            s = (a + b) // 2
            prompt = f"Suorakulmion sivut ovat {a} cm ja {b} cm. Neliön piiri on yhtä suuri. Kuinka monta neliösenttimetriä neliön ala on?"
            ans, wrong = s * s, [a * b]
            steps = [f"Piiri 2 · ({a} + {b}) = {2 * (a + b)} cm", f"Neliön sivu {s} cm", f"Ala {s}² = {s * s} cm²"]
            params, unit = {"a": a, "b": b}, "cm²"
        elif k == 1:
            level = "T"
            half = rng.choice([8, 10, 12, 14])
            s = half // 2
            a = rng.randint(1, s - 1)
            b = half - a
            prompt = (f"Neliön piiri on {2 * half} cm ja ala {s * s} cm². Suorakulmion piiri on myös {2 * half} cm ja sen toinen sivu on {a} cm. "
                      "Kuinka monta neliösenttimetriä suorakulmion ala on?")
            ans, wrong = a * b, [s * s]
            steps = [f"Toinen sivu {half} {chr(8722)} {a} = {b} cm", f"Ala {a} · {b} = {a * b} cm²"]
            params, unit = {"half": half, "a": a}, "cm²"
        elif k == 2:
            level = "T"
            half = rng.choice([10, 12, 14, 16])
            a = rng.randint(2, half // 2 - 2)
            b = half - a
            s = half // 2
            prompt = (f"Neliön muotoisen kangaspalan reunanauha on {2 * half} cm pitkä. Suorakulmion muotoinen kangas rajataan yhtä pitkällä nauhalla, "
                      f"ja sen toinen sivu on {a} cm. Kuinka monta neliösenttimetriä suorakulmion ala on?")
            ans, wrong = a * b, [s * s]
            steps = [f"Toinen sivu {half} {chr(8722)} {a} = {b} cm", f"Ala {a} · {b} = {a * b} cm²"]
            params, unit = {"half": half, "a": a}, "cm²"
        elif k == 3:
            level = "H"
            half = rng.choice([14, 16, 18, 20])
            s = half // 2
            a = rng.randint(2, s - 2)
            b = half - a
            prompt = (f"Aita on {2 * half} m pitkä. Siitä tehdään joko neliön muotoinen aitaus tai suorakulmio, jonka toinen sivu on {a} m. "
                      "Kuinka monta neliömetriä suurempi neliön ala on kuin suorakulmion ala?")
            ans, wrong = s * s - a * b, [0]
            steps = [f"Neliön ala {s}² = {s * s} m²", f"Suorakulmion ala {a} · {b} = {a * b} m²", f"{s * s} {chr(8722)} {a * b} = {s * s - a * b}"]
            params, unit = {"half": half, "a": a}, "m²"
        else:
            level = "H"
            half = rng.choice([13, 15, 17])
            a, c = rng.sample(range(1, half // 2 + 1), 2)
            b, d = half - a, half - c
            prompt = (f"Suorakulmioilla on sama piiri {2 * half} cm. Toisen sivut ovat {a} cm ja {b} cm, toisen {c} cm ja {d} cm. "
                      "Kuinka monta neliösenttimetriä alat eroavat toisistaan?")
            ans, wrong = abs(a * b - c * d), [0]
            steps = [f"Alat {a} · {b} = {a * b} cm² ja {c} · {d} = {c * d} cm²", f"Erotus {abs(a * b - c * d)} cm²"]
            params, unit = {"a": a, "c": c, "half": half}, "cm²"
        assert all(w != ans for w in wrong)
        answer = {"kind": "number", "value": ans}
        if unit:
            answer["unit"] = unit
        payload = {"answer": answer,
                   "wrong": [{"match": w, "misconception": TID, "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt, payload, steps, str(ans).replace(".", ","),
                               "Oikein: ala lasketaan kuvion omista sivuista, ei piiristä.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
