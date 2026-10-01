#!/usr/bin/env python3
"""EXT-01 (negative base and square: -3² read as 9), type ES (error spotting). Lines are numeric expressions;
lines before the error line are equivalent to line 1 and the error line breaks equivalence (both checked by
verify.py). The injected error reads -a² as (-a)², i.e. drops the minus sign of the power."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext01_es"
TID, CODE = "EXT-01", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = "Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Muista, että −a² = −(a · a)."
INTRO = "Oppilas laskee rivi riviltä. "


def make_items(run, date, count=5, start=1):
    rng = random.Random(1201)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, b = rng.choice([4, 5, 6]), rng.choice([10, 20, 30])
            lines = [f"{MINUS}{a}² + {b}", f"{a}² + {b}", f"{a * a + b}"]
            err, level = 2, "T"
            fix = (f"Potenssi lasketaan ennen miinusmerkkiä: {MINUS}{a}² = {MINUS}({a} · {a}) = {num(-a * a)}. "
                   f"Oikea tulos on {num(b - a * a)}.")
            params = {"a": a, "b": b}
        elif k == 1:
            a, c = rng.choice([3, 5, 7]), rng.choice([4, 6, 8])
            lines = [f"{MINUS}{a}² {MINUS} {c}", f"{MINUS}({a} · {a}) {MINUS} {c}", f"{a} · {a} {MINUS} {c}", f"{a * a - c}"]
            err, level = 3, "T"
            fix = (f"Rivi 2 on oikein. Miinus kuuluu potenssin eteen, joten {MINUS}({a} · {a}) = {num(-a * a)} eikä {a * a}. "
                   f"Oikea tulos on {num(-a * a - c)}.")
            params = {"a": a, "c": c}
        elif k == 2:
            d, c = rng.choice([2, 3, 4]), rng.choice([20, 30, 40])
            lines = [f"{MINUS}({MINUS}{d})² + {c}", f"{d}² + {c}", f"{d * d + c}"]
            err, level = 2, "T"
            fix = (f"Sulkeissa (−{d})² = {d * d}, ja sen eteen jää miinus: {MINUS}({MINUS}{d})² = {num(-d * d)}. "
                   f"Oikea tulos on {c - d * d}.")
            params = {"d": d, "c": c}
        elif k == 3:
            a = rng.choice([5, 6, 7])
            lines = [f"{MINUS}{a}² + ({MINUS}{a})²", f"{a}² + {a}²", f"{2 * a * a}"]
            err, level = 2, "H"
            fix = (f"{MINUS}{a}² = {num(-a * a)} ja ({MINUS}{a})² = {a * a}. "
                   f"Oikea tulos on {num(-a * a)} + {a * a} = 0.")
            params = {"a": a}
        else:
            a, c = rng.choice([2, 3, 4]), rng.choice([2, 3, 5])
            lines = [f"{MINUS}{a}² {MINUS} ({MINUS}{a})²", f"{MINUS}({a} · {a}) {MINUS} {a} · {a}",
                     f"{a} · {a} {MINUS} {a} · {a}", "0"]
            err, level = 3, "H"
            fix = (f"Rivi 2 on oikein: {MINUS}{a}² = {num(-a * a)} ja ({MINUS}{a})² = {a * a}. "
                   f"Oikea tulos on {num(-a * a)} {MINUS} {a * a} = {num(-2 * a * a)}.")
            params = {"a": a}
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"lines": lines, "error_line": err, "error_type": "negative_base_square"}
        items.append(base_item(TID, CODE, start + k, ["S2.01", "S2.11"], ["T10", "T11"], 7, level, INTRO + ASK, payload,
                               [fix], f"Virhe on rivillä {err}",
                               "Oikein: potenssi lasketaan ennen etumerkkiä, ja sulkeet määräävät, kuuluuko miinus kantalukuun.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
