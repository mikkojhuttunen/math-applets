#!/usr/bin/env python3
"""EXT-02 (integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2), type FS. All lines are numeric expressions (^ for the
exponent) equivalent to line 1; the blanked line is computed by code and verify.py checks the chain for
equivalence (the variable x is only a schema placeholder)."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext02_fs"
TID, CODE = "EXT-02", "FS"
SAMPLES = [[1], [2], [3]]
GOOD = "Oikein: potenssi on toistettu kertolasku, a^0 = 1 ja a^(−n) = 1/a^n."
GENERIC = "Muista, että a^0 = 1 ja a^(−n) = 1/a^n. Tarkista välivaihe laskemalla."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1206)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, b = rng.choice([(2, 5), (3, 4), (5, 6)])
            lines = [f"{a}^3 + {b}", f"{a} · {a} · {a} + {b}", f"{num(a ** 3 + b)}"]
            blank, level, params = 2, "T", {"a": a, "b": b}
            hint = "Kirjoita välivaihe, jossa potenssi on avattu tuloksi"
        elif k == 1:
            a, b, c = rng.choice([(7, 3, 4), (5, 2, 6), (9, 4, 1)])
            lines = [f"{b} · {a}^0 + {c}", f"{b} · 1 + {c}", f"{num(b + c)}"]
            blank, level, params = 2, "T", {"a": a, "b": b, "c": c}
            hint = "Kirjoita välivaihe, jossa nollas potenssi on laskettu"
        elif k == 2:
            a = rng.choice([2, 3, 5])
            lines = [f"{a}^({MINUS}2) · {a}^3", f"1/{a * a} · {a ** 3}", f"{a}"]
            blank, level, params = 2, "T", {"a": a}
            hint = "Kirjoita välivaihe, jossa negatiivinen eksponentti on muutettu murtoluvuksi"
        elif k == 3:
            a = rng.choice([2, 4, 5])
            lines = [f"{a}^0 + {a}^({MINUS}1) + {a}^2", f"1 + 1/{a} + {a * a}", f"{a * a + 1} + 1/{a}"]
            blank, level, params = 2, "H", {"a": a}
            hint = "Kirjoita välivaihe, jossa jokainen potenssi on laskettu"
        else:
            a, b, c = rng.choice([(2, 7, 4), (3, 9, 6), (5, 7, 8)])
            lines = [f"{b}^0 · {a}^({MINUS}1) · {a * c}", f"1 · 1/{a} · {a * c}", f"{c}"]
            blank, level, params = 2, "H", {"a": a, "b": b, "c": c}
            hint = "Kirjoita välivaihe, jossa potenssit on laskettu"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        ref = lines[blank - 1]
        prompt = f"Täydennä puuttuva rivi. {hint}: {lines[0]} = □ = {lines[2]}"
        answer = {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}
        steps = [f"{lines[i]} = {lines[i + 1]}" for i in range(len(lines) - 1)]
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S2.11"], ["T10", "T11"], 8, level, prompt, payload, steps,
                               ref, GOOD, TEMPLATE, {**params, "blank": blank}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
