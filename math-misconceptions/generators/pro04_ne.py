#!/usr/bin/env python3
"""PRO-04 (larger perimeter means larger area), type NE. The answer is computed from the side lengths; the typical
wrong entry is the area (or perimeter) of the shape with the larger perimeter."""
import random

from gen_common import base_item, cli

TEMPLATE = "pro04_ne"
TID, CODE = "PRO-04", "NE"
BAD = "Suurempi piiri ei tarkoita suurempaa alaa. Laske kummankin kuvion ala sivujen tulona ja vertaa."


def thin_and_square(rng):
    while True:
        h = rng.randint(1, 3)
        w = rng.randint(8, 16)
        s = rng.randint(4, 8)
        if 2 * (w + h) > 4 * s and w * h < s * s:
            return w, h, s


def make_items(run, date, count=5, start=1):
    rng = random.Random(842)
    items = []
    for k in range(count):
        w, h, s = thin_and_square(rng)
        pr, ps, ar, as_ = 2 * (w + h), 4 * s, w * h, s * s
        if k == 0:
            level = "T"
            prompt = (f"Suorakulmion sivut ovat {w} cm ja {h} cm. Neliön sivu on {s} cm. "
                      "Kuinka monta neliösenttimetriä on suuremman alan arvo?")
            ans, wrong, unit = as_, [ar], "cm²"
            steps = [f"Suorakulmion ala {ar} cm², neliön ala {as_} cm²", f"Suurempi on {as_} cm²"]
        elif k == 1:
            level = "T"
            prompt = (f"Huone A on {w} m × {h} m ja huone B on {s} m × {s} m. "
                      "Kuinka monta neliömetriä on sen huoneen lattian ala, jonka ala on suurempi?")
            ans, wrong, unit = as_, [ar], "m²"
            steps = [f"A: {ar} m², B: {as_} m²", f"Suurempi ala on {as_} m²"]
        elif k == 2:
            level = "T"
            c, d = rng.choice([(7, 6), (8, 5), (9, 5), (8, 6), (7, 7)])
            w2 = rng.randint(14, 20)
            h2 = 2
            while 2 * (w2 + h2) <= 2 * (c + d) or w2 * h2 >= c * d:
                w2 += 1
            prompt = (f"Pelto A on {w2} m × {h2} m ja pelto B on {c} m × {d} m. "
                      "Kuinka monta neliömetriä on suuremman pellon ala?")
            ans, wrong, unit = c * d, [w2 * h2], "m²"
            steps = [f"A: {w2} · {h2} = {w2 * h2} m², B: {c} · {d} = {c * d} m²", f"Suurempi ala on {c * d} m²"]
            w, h, s = w2, h2, (c, d)
        elif k == 3:
            level = "H"
            prompt = (f"Kaksi aitausta: suorakulmio {w} m × {h} m ja neliö {s} m × {s} m. "
                      "Kuinka monta metriä aitaa kuluu sen aitauksen ympärille, jonka pinta-ala on suurempi?")
            ans, wrong, unit = ps, [pr], "m"
            steps = [f"Alat: {ar} m² ja {as_} m², suurempi on neliö", f"Neliön piiri 4 · {s} = {ps} m"]
        else:
            level = "H"
            prompt = (f"Suorakulmion leveys on {h} cm ja piiri {pr} cm. Neliön piiri on {ps} cm. "
                      "Kuinka monta neliösenttimetriä on suuremman alan arvo?")
            ans, wrong, unit = as_, [ar], "cm²"
            steps = [f"Suorakulmion pituus {pr // 2} {chr(8722)} {h} = {w} cm, ala {ar} cm²", f"Neliön sivu {s} cm, ala {as_} cm²"]
        assert all(x != ans for x in wrong)
        payload = {"answer": {"kind": "number", "value": ans, "unit": unit},
                   "wrong": [{"match": x, "misconception": TID, "feedback": BAD} for x in wrong],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt, payload, steps, str(ans),
                               "Oikein: ala lasketaan sivujen tulona; piirin suuruus ei kerro alasta.", TEMPLATE,
                               {"w": w, "h": h, "s": s}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
