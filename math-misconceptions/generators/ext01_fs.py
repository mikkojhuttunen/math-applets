#!/usr/bin/env python3
"""EXT-01 (negative base and square: -3² read as 9), type FS. All lines are numeric expressions equivalent to
line 1; the blanked line is computed by code and verify.py checks the chain for equivalence (the variable x is
only a schema placeholder)."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext01_fs"
TID, CODE = "EXT-01", "FS"
SAMPLES = [[1], [2], [3]]
GOOD = "Oikein: potenssi lasketaan ennen miinusmerkkiä, ja sulkeissa miinus kuuluu kantalukuun."
GENERIC = "Muista, että −a² = −(a · a), mutta (−a)² = (−a) · (−a) = a². Tarkista välivaihe laskemalla."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1202)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, b = rng.choice([4, 5, 6]), rng.choice([10, 20, 30])
            lines = [f"{MINUS}{a}² + {b}", f"{MINUS}({a} · {a}) + {b}", f"{num(b - a * a)}"]
            blank, level, params = 2, "T", {"a": a, "b": b}
            prompt = f"Täydennä puuttuva rivi. Kirjoita välivaihe, jossa potenssi on avattu tuloksi: {lines[0]} = □ = {lines[2]}"
        elif k == 1:
            a, c = rng.choice([3, 7, 8]), rng.choice([4, 6, 9])
            lines = [f"{MINUS}{a}² {MINUS} {c}", f"{MINUS}({a} · {a}) {MINUS} {c}", f"{MINUS}{a * a} {MINUS} {c}", f"{num(-a * a - c)}"]
            blank, level, params = 3, "T", {"a": a, "c": c}
            prompt = f"Täydennä puuttuva rivi. Laske potenssin arvo: {lines[0]} = {lines[1]} = □ = {lines[3]}"
        elif k == 2:
            d, c = rng.choice([2, 3, 4]), rng.choice([20, 30, 40])
            lines = [f"({MINUS}{d})² {MINUS} {d}²", f"({MINUS}{d}) · ({MINUS}{d}) {MINUS} {d} · {d}", f"{d * d} {MINUS} {d * d}", "0"]
            blank, level, params = 3, "T", {"d": d, "variant": "equal-squares"}
            prompt = f"Täydennä puuttuva rivi. Laske tulot: {lines[0]} = {lines[1]} = □ = 0"
        elif k == 3:
            a, b = rng.choice([(3, 4), (2, 5), (6, 3)])
            lines = [f"{MINUS}{a}² + ({MINUS}{b})²", f"{MINUS}{a * a} + {b * b}", f"{num(b * b - a * a)}"]
            blank, level, params = 2, "H", {"a": a, "b": b}
            prompt = (f"Täydennä puuttuva rivi. Kirjoita välivaihe, jossa molemmat potenssit on laskettu: "
                      f"{lines[0]} = □ = {lines[2]}")
        else:
            a, b, c = rng.choice([(2, 3, 20), (3, 2, 30), (4, 3, 50)])
            lines = [f"{c} {MINUS} {a}² {MINUS} ({MINUS}{b})²", f"{c} {MINUS} {a * a} {MINUS} {b * b}", f"{num(c - a * a - b * b)}"]
            blank, level, params = 2, "H", {"a": a, "b": b, "c": c}
            prompt = (f"Täydennä puuttuva rivi. Kirjoita välivaihe, jossa molemmat potenssit on laskettu: "
                      f"{lines[0]} = □ = {lines[2]}")
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        ref = lines[blank - 1]
        answer = {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}
        steps = [f"{lines[i]} = {lines[i + 1]}" for i in range(len(lines) - 1)]
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S2.01", "S2.11"], ["T10", "T11"], 7, level, prompt, payload, steps,
                               ref, GOOD, TEMPLATE, {**params, "blank": blank}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
