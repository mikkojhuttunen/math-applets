#!/usr/bin/env python3
"""ALG-12 (subtraction of a negative number), type ES (error spotting). Lines are numeric expressions; lines before
the error line are equivalent to line 1 and the error line breaks equivalence (both checked by verify.py). The
injected error subtracts the absolute value instead of adding it: a - (-b) is written as a - b."""
import random

from gen_common import MINUS, base_item, cli, num

TEMPLATE = "alg12_es"
TID, CODE = "ALG-12", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = ("Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Muista, että "
           "negatiivisen luvun vähentäminen on vastaluvun lisäämistä: a − (−b) = a + b.")
INTRO = "Oppilas laskee rivi riviltä. "


def make_items(run, date, count=5, start=1):
    rng = random.Random(1211)
    items, seen = [], set()
    for k in range(count):
        a, b, c = rng.sample(range(2, 10), 3)
        if k == 0:
            lines = [f"{a} {MINUS} ({MINUS}{b}) + {c}", f"{a} {MINUS} {b} + {c}", f"{num(a - b + c)}"]
            err, level = 2, "T"
            fix = (f"{a} {MINUS} ({MINUS}{b}) = {a} + {b}, sillä negatiivisen luvun vähentäminen on vastaluvun lisäämistä. "
                   f"Oikea tulos on {a + b + c}.")
        elif k == 1:
            lines = [f"{MINUS}{a} {MINUS} ({MINUS}{b})", f"{MINUS}{a} {MINUS} {b}", f"{num(-a - b)}"]
            err, level = 2, "T"
            fix = (f"{MINUS}{a} {MINUS} ({MINUS}{b}) = {MINUS}{a} + {b}. Oikea tulos on {num(b - a)}.")
        elif k == 2:
            lines = [f"{a} {MINUS} ({MINUS}{b}) {MINUS} ({MINUS}{c})", f"{a} + {b} {MINUS} ({MINUS}{c})",
                     f"{a} + {b} {MINUS} {c}", f"{num(a + b - c)}"]
            err, level = 3, "T"
            fix = (f"Rivi 2 on oikein. Viimeinen vähennys {MINUS} ({MINUS}{c}) on lisäämistä: {a + b} + {c} = {a + b + c}, "
                   f"ei {a + b} {MINUS} {c}.")
        elif k == 3:
            lines = [f"{a} {MINUS} ({MINUS}{b})", f"{a} {MINUS} {b}", f"{num(a - b)}"]
            err, level = 2, "H"
            fix = (f"Ylin lämpötila on {a} °C ja alin {MINUS}{b} °C, joten erotus on {a} {MINUS} ({MINUS}{b}) = {a} + {b} = {a + b} astetta.")
        else:
            lines = [f"{MINUS}{a} {MINUS} ({MINUS}{a}) + {b}", f"{MINUS}{a} {MINUS} {a} + {b}", f"{num(-2 * a + b)}"]
            err, level = 2, "H"
            fix = (f"{MINUS}{a} {MINUS} ({MINUS}{a}) = {MINUS}{a} + {a} = 0, joten oikea tulos on {b}.")
        if k == 3:
            intro = (f"Päivän ylin lämpötila on {a} °C ja alin {MINUS}{b} °C. Oppilas laskee ylimmän ja alimman lämpötilan "
                     "erotuksen rivi riviltä. ")
        else:
            intro = INTRO
        params = {"a": a, "b": b, "c": c, "form": k}
        key = (k, a, b, c)
        assert key not in seen
        seen.add(key)
        payload = {"lines": lines, "error_line": err, "error_type": "subtract_abs_value"}
        final = f"Virhe on rivillä {err}"
        items.append(base_item(TID, CODE, start + k, ["S2.01"], ["T10", "T11"], 7, level, intro + ASK, payload,
                               [fix], final,
                               "Oikein: negatiivisen luvun vähentäminen on sen vastaluvun lisäämistä.",
                               TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
