#!/usr/bin/env python3
"""PRO-01 (illusion of linearity: area), type NE. The answer is computed from the scale factor k; the wrong entry is the linear guess."""
import random

from gen_common import base_item, cli

TEMPLATE = "pro01_ne"
TID, CODE = "PRO-01", "NE"
BAD = "Pinta-ala ei kasva samassa suhteessa kuin pituudet. Jos pituudet ovat k-kertaiset, pinta-ala on k²-kertainen."


def make_items(run, date, count=5, start=1):
    rng = random.Random(622)
    items = []
    for n in range(count):
        k = rng.choice([2, 3, 4, 5]) if n != 0 else rng.choice([2, 3])
        unit = None
        if n == 0:
            level, s = "T", rng.randint(2, 5)
            prompt = f"Neliön sivu on {s} cm. Sivu kasvatetaan {k}-kertaiseksi. Kuinka monta neliösenttimetriä uuden neliön ala on?"
            ans, wrong = (k * s) ** 2, [k * s * s, k * s]
            steps = [f"Uusi sivu {k * s} cm", f"Ala {k * s}² = {ans} cm²"]
            params, unit = {"k": k, "side": s}, "cm²"
        elif n == 1:
            level, a, b = "T", rng.randint(3, 6), rng.randint(7, 12)
            prompt = f"Valokuvan mitat ovat {a} cm ja {b} cm. Kuva suurennetaan niin, että jokainen mitta on {k}-kertainen. Mikä on suurennoksen pinta-ala neliösenttimetreinä?"
            ans, wrong = k * k * a * b, [k * a * b]
            steps = [f"Uudet mitat {k * a} cm ja {k * b} cm", f"Ala {k * a} · {k * b} = {ans} cm²"]
            params, unit = {"k": k, "a": a, "b": b}, "cm²"
        elif n == 2:
            level, area = "T", rng.choice([12, 15, 20, 25])
            prompt = f"Puutarhan pohjapiirroksen ala on {area} m². Kaikki pituudet kasvatetaan {k}-kertaisiksi. Mikä on uuden piirroksen ala neliömetreinä?"
            ans, wrong = k * k * area, [k * area]
            steps = [f"Pinta-alan kerroin {k}² = {k * k}", f"{area} · {k * k} = {ans}"]
            params, unit = {"k": k, "area": area}, "m²"
        elif n == 3:
            level, cans = "H", rng.choice([3, 4, 5])
            prompt = (f"Yksi lattia maalataan {cans} purkillisella. Toisen lattian jokainen mitta on {k}-kertainen ensimmäiseen verrattuna ja muoto on sama. "
                      "Montako purkillista maalia toiseen lattiaan tarvitaan?")
            ans, wrong = cans * k * k, [cans * k]
            steps = [f"Pinta-alan kerroin {k}² = {k * k}", f"{cans} · {k * k} = {ans}"]
            params = {"k": k, "cans": cans}
        else:
            level = "H"
            f = rng.choice([4, 9, 16])
            ans, wrong = int(f ** 0.5), [f]
            prompt = f"Kuvion pinta-ala on {f}-kertainen alkuperäiseen verrattuna. Kuinka moninkertaisia kuvion pituudet ovat alkuperäiseen verrattuna?"
            steps = [f"k² = {f}", f"k = {ans}"]
            params = {"area_factor": f}
        assert all(w != ans for w in wrong)
        answer = {"kind": "number", "value": ans}
        if unit:
            answer["unit"] = unit
        payload = {"answer": answer,
                   "wrong": [{"match": w, "misconception": "PRO-01", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + n, ["S5.05"], ["T16", "T18"], 8, level, prompt, payload, steps, str(ans),
                               "Oikein: pinta-ala muuttuu kertoimella k².", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
