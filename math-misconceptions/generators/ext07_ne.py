#!/usr/bin/env python3
"""EXT-07 (area unit conversion: 1 m² = 100 cm²), type NE. Conversions use the exact area factors (1 m² = 10 000 cm²,
1 km² = 1 000 000 m²) with Decimal arithmetic; the tagged wrong answer uses the length factor (100 or 1 000)."""
import random
from decimal import Decimal

from gen_common import base_item, cli, num

TEMPLATE = "ext07_ne"
TID, CODE = "EXT-07", "NE"
BAD = ("Pinta-alayksiköiden muuntokerroin on pituusyksikön kerroin toiseen potenssiin: "
       "1 m² = 1 m · 1 m = 100 cm · 100 cm = 10 000 cm².")
GOOD = "Oikein: pinta-alan muuntokerroin on pituuden kertoimen neliö."
M2_CM2, KM2_M2 = 10_000, 1_000_000


def big(n):
    return f"{int(n):,}".replace(",", " ")


def d(x):
    s = format(Decimal(x).normalize(), "f")
    return s.replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1807)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            n = rng.choice([2, 3, 4, 6, 7])
            ans, wrong, level = n * M2_CM2, n * 100, "T"
            prompt = f"Muunna {n} m² neliösenttimetreiksi. Kirjoita vastaus ilman yksikköä."
            steps = [f"1 m² = 10 000 cm²", f"{n} · 10 000 = {big(ans)}"]
            params = {"n": n}
        elif k == 1:
            n = Decimal(rng.choice(["1.5", "2.5", "0.5", "3.5"]))
            ans, wrong, level = int(n * M2_CM2), int(n * 100), "T"
            prompt = f"Muunna {d(n)} m² neliösenttimetreiksi. Kirjoita vastaus ilman yksikköä."
            steps = ["1 m² = 10 000 cm²", f"{d(n)} · 10 000 = {big(ans)}"]
            params = {"n": str(n)}
        elif k == 2:
            n = rng.choice([2, 3, 5, 8])
            ans, wrong, level = n, n * 100, "T"
            prompt = f"Muunna {big(n * M2_CM2)} cm² neliömetreiksi. Kirjoita vastaus ilman yksikköä."
            steps = ["10 000 cm² = 1 m²", f"{big(n * M2_CM2)} ÷ 10 000 = {n}"]
            params = {"cm2": n * M2_CM2}
        elif k == 3:
            w, l, t = rng.choice([(4, 5, 20), (3, 5, 25), (4, 6, 30)])
            area_cm2 = w * l * M2_CM2
            tile = t * t
            ans, level = area_cm2 // tile, "H"
            assert area_cm2 % tile == 0
            wrong = w * l * 100 // tile
            assert w * l * 100 % tile == 0 and wrong != ans
            prompt = (f"Lattian mitat ovat {w} m ja {l} m. Laatat ovat neliön muotoisia, ja niiden sivu on {t} cm. "
                      f"Montako laattaa tarvitaan lattian peittämiseen?")
            steps = [f"Lattia: {w} · {l} = {w * l} m² = {big(area_cm2)} cm²", f"Laatta: {t} · {t} = {tile} cm²",
                     f"{big(area_cm2)} ÷ {tile} = {ans}"]
            params = {"floor": [w, l], "tile": t}
        else:
            n = rng.choice([2, 3, 5])
            ans, wrong, level = n * KM2_M2, n * 1000, "H"
            prompt = f"Järven pinta-ala on {n} km². Kuinka monta neliömetriä se on? Kirjoita vastaus ilman yksikköä."
            steps = ["1 km = 1 000 m, joten 1 km² = 1 000 · 1 000 m² = 1 000 000 m²", f"{n} · 1 000 000 = {big(ans)}"]
            params = {"km2": n}
        assert wrong != ans
        assert (k, str(params)) not in seen
        seen.add((k, str(params)))
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": wrong, "misconception": TID, "feedback": BAD}],
                   "input_hint": "Kirjoita luku ilman välilyöntejä"}
        items.append(base_item(TID, CODE, start + k, ["S5.14"], ["T18"], 7, level, prompt, payload, steps,
                               big(ans), GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
