#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type ES (error spotting). Lines before the error line are equations with the
same solutions as line 1; the error line keeps only the positive root, which changes the solution set (checked by
verify.py)."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext04_es"
TID, CODE = "EXT-04", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
INTRO = "Oppilas ratkaisee yhtälön rivi riviltä. "
GENERIC = ("Tarkista rivi kerrallaan, onko uudella rivillä samat ratkaisut kuin edellisellä. "
           "Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0: positiivinen ja negatiivinen juuri.")
GOOD = "Oikein: neliö ei erota lukua ja sen vastalukua, joten ratkaisuja on kaksi."


def roots(p, q):
    return [x for x in range(-60, 61) if p * x * x + q == 0]


def make_items(run, date, count=5, start=1):
    rng = random.Random(1403)
    items, seen = [], set()
    for k in range(count):
        ctx = ""
        if k == 0:
            a = rng.choice([6, 7, 9])
            lines = [f"x² {MINUS} {a * a} = 0", f"x² = {a * a}", f"x = {a}"]
            err, level, params = 3, "T", {"a": a}
            r = roots(1, -a * a)
        elif k == 1:
            a, p = rng.choice([(4, 3), (5, 2)])
            lines = [f"{p}x² = {p * a * a}", f"x² = {a * a}", f"x = {a}"]
            err, level, params = 3, "T", {"a": a, "p": p}
            r = roots(p, -p * a * a)
        elif k == 2:
            a, c = rng.choice([(8, 5), (6, 4)])
            lines = [f"x² + {c} = {a * a + c}", f"x² = {a * a}", f"x = {a}"]
            err, level, params = 3, "T", {"a": a, "c": c}
            r = roots(1, -a * a)
        elif k == 3:
            a = 5
            ctx = "Ajattelen lukua. Kun sen neliöstä vähennetään 25, tulos on nolla. "
            lines = [f"x² {MINUS} 25 = 0", "x² = 25", "x = 5"]
            err, level, params = 3, "H", {"a": a, "context": "number-puzzle"}
            r = roots(1, -25)
        else:
            a, p, c = 4, 3, 7
            lines = [f"{p}x² + {c} = {p * a * a + c}", f"{p}x² = {p * a * a}", f"x² = {a * a}", f"x = {a}"]
            err, level, params = 4, "H", {"a": a, "p": p, "c": c}
            r = roots(p, -p * a * a)
        assert r == [-a, a]
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        fix = (f"Rivi {err} ottaa huomioon vain positiivisen juuren. "
               f"Oikein: x = {a} tai x = {num(-a)}, koska ({num(-a)})² = {a * a}.")
        payload = {"lines": lines, "error_line": err, "error_type": "negative_root_lost"}
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, INTRO + ctx + ASK, payload,
                               [fix], f"Virhe on rivillä {err}", GOOD, TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
