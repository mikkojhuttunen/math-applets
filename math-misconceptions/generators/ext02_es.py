#!/usr/bin/env python3
"""EXT-02 (integer exponents: 2³ = 6, a⁰ = 0, 2⁻¹ = -2), type ES (error spotting). Lines are numeric expressions
written with ^ for the exponent so that verify.py can parse them; lines before the error line are equivalent to
line 1 and the error line breaks equivalence. Injected errors: power read as a product, a⁰ read as 0, a negative
exponent read as a negative number."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "ext02_es"
TID, CODE = "EXT-02", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
INTRO = "Oppilas laskee rivi riviltä. "
GENERIC = "Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Potenssi on toistettu kertolasku, a^0 = 1 ja a^(−n) = 1/a^n."
GOOD = "Oikein: potenssi on toistettu kertolasku, a^0 = 1 ja negatiivinen eksponentti tarkoittaa käänteislukua."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1205)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, n, c = rng.choice([(2, 3, 5), (3, 3, 10), (5, 3, 20)])
            lines = [f"{a}^{n} {MINUS} {c}", f"{a} · {n} {MINUS} {c}", f"{num(a * n - c)}"]
            err, level = 2, "T"
            fix = (f"{a}^{n} = " + " · ".join([str(a)] * n) + f" = {a ** n}, ei {a} · {n}. Oikea tulos on {num(a ** n - c)}.")
            params = {"a": a, "n": n, "c": c}
        elif k == 1:
            a, b, c = rng.choice([(7, 3, 4), (5, 2, 6), (9, 4, 1)])
            lines = [f"{b} · {a}^0 + {c}", f"{b} · 0 + {c}", f"0 + {c}", f"{c}"]
            err, level = 2, "T"
            fix = f"{a}^0 = 1, ei 0. Oikea tulos on {b} · 1 + {c} = {b + c}."
            params = {"a": a, "b": b, "c": c}
        elif k == 2:
            a, b = rng.choice([(2, 10), (4, 12), (5, 20)])
            lines = [f"{a}^({MINUS}1) + {b}", f"{MINUS}{a} + {b}", f"{num(b - a)}"]
            err, level = 2, "T"
            fix = f"{a}^({MINUS}1) = 1/{a}, ei {MINUS}{a}. Oikea tulos on 1/{a} + {b}."
            params = {"a": a, "b": b}
        elif k == 3:
            a = rng.choice([2, 4, 5])
            lines = [f"{a}^0 + {a}^({MINUS}1)", f"1 + {a}^({MINUS}1)", f"1 {MINUS} {a}", f"{num(1 - a)}"]
            err, level = 3, "H"
            fix = (f"Rivi 2 on oikein, koska {a}^0 = 1. Mutta {a}^({MINUS}1) = 1/{a}, ei {MINUS}{a}. "
                   f"Oikea tulos on 1 + 1/{a}.")
            params = {"a": a}
        else:
            a = rng.choice([2, 3, 5])
            lines = [f"{a}^2 + {a}^({MINUS}2)", f"{a * a} + {a}^({MINUS}2)", f"{a * a} {MINUS} {a * a}", "0"]
            err, level = 3, "H"
            fix = (f"Rivi 2 on oikein. {a}^({MINUS}2) = 1/{a}^2 = 1/{a * a}, ei {MINUS}{a * a}. "
                   f"Oikea tulos on {a * a} + 1/{a * a}.")
            params = {"a": a}
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"lines": lines, "error_line": err, "error_type": "integer_exponent"}
        items.append(base_item(TID, CODE, start + k, ["S2.11"], ["T10", "T11"], 8, level, INTRO + ASK, payload,
                               [fix], f"Virhe on rivillä {err}", GOOD, TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
