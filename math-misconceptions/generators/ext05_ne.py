#!/usr/bin/env python3
"""EXT-05 (Pythagorean theorem assumed to hold for every triangle), type NE. The difference a² + b² − c² and the
number of right triangles in a list are computed by code; the tagged wrong answer is the value obtained when the
theorem is assumed to hold for every triangle (difference 0, or every triangle counted as right-angled)."""
import random

from gen_common import base_item, cli, num

TEMPLATE = "ext05_ne"
TID, CODE = "EXT-05", "NE"
BAD = ("Pythagoraan lause pätee vain suorakulmaisessa kolmiossa. Muissa kolmioissa erotus a² + b² − c² "
       "ei ole nolla. Laske neliöt erikseen.")
GOOD = "Oikein: neliöt lasketaan erikseen, ja vain suorakulmaisessa kolmiossa erotus on nolla."


def is_right(a, b, c):
    s = sorted([a, b, c])
    return s[0] ** 2 + s[1] ** 2 == s[2] ** 2


def make_items(run, date, count=5, start=1):
    rng = random.Random(1506)
    items, seen = [], set()
    for k in range(count):
        if k in (0, 1, 3):
            a, b, c = [(5, 6, 8), (4, 5, 6), None, (8, 11, 13)][k]
            assert not is_right(a, b, c)
            level = "T" if k < 3 else "H"
            if k == 3:
                prompt = (f"Tikkaat nojaavat seinää vasten. Kolmion sivut ovat {a} m, {b} m ja {c} m "
                          f"({c} m on pisin). Laske {c}² − ({a}² + {b}²).")
                ans = c * c - (a * a + b * b)
                steps = [f"{a}² + {b}² = {a * a + b * b}", f"{c}² = {c * c}", f"{c * c} − {a * a + b * b} = {ans}"]
            else:
                prompt = (f"Kolmion sivut ovat {a}, {b} ja {c}. Laske erotus {a}² + {b}² − {c}².")
                ans = a * a + b * b - c * c
                steps = [f"{a}² + {b}² = {a * a + b * b}", f"{c}² = {c * c}", f"{a * a + b * b} − {c * c} = {ans}"]
            wrong = 0
            params = {"a": a, "b": b, "c": c}
        elif k == 2:
            a, b, c = 7, 9, 12
            assert not is_right(a, b, c)
            level = "T"
            prompt = (f"Pellon sivut ovat {a} m, {b} m ja {c} m. Kuinka paljon luku {c}² on suurempi "
                      f"kuin summa {a}² + {b}²?")
            ans = c * c - (a * a + b * b)
            wrong = 0
            steps = [f"{a}² + {b}² = {a * a + b * b}", f"{c}² = {c * c}", f"{c * c} − {a * a + b * b} = {ans}"]
            params = {"a": a, "b": b, "c": c}
        else:
            level = "H"
            tris = [(5, 12, 13), (6, 7, 9), (8, 15, 17), (7, 9, 11), (9, 12, 15)] if k == 4 else None
            ans = sum(is_right(*t) for t in tris)
            names = ", ".join(f"({x}, {y}, {z})" for x, y, z in tris)
            prompt = f"Kolmioiden sivut ovat {names}. Kuinka moni kolmioista on suorakulmainen?"
            wrong = len(tris)
            steps = [f"{x}² + {y}² = {x * x + y * y}, {z}² = {z * z}: " + ("suorakulmainen" if is_right(x, y, z) else "ei suorakulmainen")
                     for x, y, z in tris] + [f"Suorakulmaisia on {ans}"]
            params = {"triangles": [list(t) for t in tris]}
        assert wrong != ans
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": wrong, "misconception": TID, "feedback": BAD}],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + k, ["S5.09"], ["T17"], 8, level, prompt, payload, steps,
                               num(ans), GOOD, TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
