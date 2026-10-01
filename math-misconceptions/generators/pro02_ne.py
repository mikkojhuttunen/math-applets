#!/usr/bin/env python3
"""PRO-02 (illusion of linearity: volume), type NE. The answer is computed from the scale factor k; wrong entries are the linear and squared guesses."""
import random

from gen_common import base_item, cli

TEMPLATE = "pro02_ne"
TID, CODE = "PRO-02", "NE"
BAD = "Tilavuus ei kasva samassa suhteessa kuin pituudet. Jos pituudet ovat k-kertaiset, tilavuus on k³-kertainen."


def make_items(run, date, count=5, start=1):
    rng = random.Random(632)
    items = []
    for n in range(count):
        k = rng.choice([2, 3, 4, 5]) if n != 0 else rng.choice([2, 3])
        unit = None
        if n == 0:
            level, s = "T", rng.randint(2, 4)
            prompt = f"Kuution särmä on {s} cm. Särmä kasvatetaan {k}-kertaiseksi. Kuinka monta kuutiosenttimetriä uuden kuution tilavuus on?"
            ans, wrong = (k * s) ** 3, [k * s ** 3, k * s]
            steps = [f"Uusi särmä {k * s} cm", f"Tilavuus {k * s}³ = {ans} cm³"]
            params, unit = {"k": k, "edge": s}, "cm³"
        elif n == 1:
            level, a, b, c = "T", rng.randint(2, 4), rng.randint(3, 5), rng.randint(2, 4)
            prompt = f"Laatikon mitat ovat {a} cm, {b} cm ja {c} cm. Jokainen mitta kasvatetaan {k}-kertaiseksi. Mikä on uuden laatikon tilavuus kuutiosenttimetreinä?"
            ans, wrong = k ** 3 * a * b * c, [k * a * b * c]
            steps = [f"Uudet mitat {k * a}, {k * b} ja {k * c} cm", f"Tilavuus {k * a} · {k * b} · {k * c} = {ans} cm³"]
            params, unit = {"k": k, "a": a, "b": b, "c": c}, "cm³"
        elif n == 2:
            level, vol = "T", rng.choice([6, 8, 12, 15])
            prompt = f"Pienoismallin tilavuus on {vol} cm³. Oikean esineen jokainen mitta on {k}-kertainen pienoismalliin verrattuna. Mikä on esineen tilavuus kuutiosenttimetreinä?"
            ans, wrong = k ** 3 * vol, [k * vol, k * k * vol]
            steps = [f"Tilavuuden kerroin {k}³ = {k ** 3}", f"{vol} · {k ** 3} = {ans}"]
            params, unit = {"k": k, "volume": vol}, "cm³"
        elif n == 3:
            level, l = "H", rng.choice([2, 3, 5])
            prompt = (f"Pieneen akvaarioon mahtuu {l} l vettä. Suuremman akvaarion muoto on sama ja jokainen mitta on {k}-kertainen. "
                      "Montako litraa vettä suureen akvaarioon mahtuu?")
            ans, wrong = l * k ** 3, [l * k, l * k * k]
            steps = [f"Tilavuuden kerroin {k}³ = {k ** 3}", f"{l} · {k ** 3} = {ans}"]
            params, unit = {"k": k, "litres": l}, "l"
        else:
            level = "H"
            f = rng.choice([8, 27, 64])
            ans, wrong = round(f ** (1 / 3)), [f]
            prompt = f"Kappaleen tilavuus on {f}-kertainen alkuperäiseen verrattuna, ja kappaleen muoto on sama. Kuinka moninkertaisia kappaleen pituudet ovat alkuperäiseen verrattuna?"
            assert ans ** 3 == f
            steps = [f"k³ = {f}", f"k = {ans}"]
            params = {"volume_factor": f}
        assert all(w != ans for w in wrong)
        answer = {"kind": "number", "value": ans}
        if unit:
            answer["unit"] = unit
        payload = {"answer": answer,
                   "wrong": [{"match": w, "misconception": "PRO-02", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + n, ["S5.05"], ["T16", "T18"], 8, level, prompt, payload, steps, str(ans),
                               "Oikein: tilavuus muuttuu kertoimella k³.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
