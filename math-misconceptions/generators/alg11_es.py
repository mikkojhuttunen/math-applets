#!/usr/bin/env python3
"""ALG-11 (minus sign not distributed), type ES (error spotting). Lines before the error line are equivalent
to line 1 and the error line breaks equivalence (both checked by verify.py); the injected error leaves the
sign of every bracket term except the first unchanged."""
import random

from gen_common import MINUS, base_item, cli, lin

TEMPLATE = "alg11_es"
TID, CODE = "ALG-11", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = "Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen kaikilla x:n arvoilla? Kokeile vaikka x = 1."
INTRO = "Oppilas sieventää lausekkeen rivi riviltä. "


def make_items(run, date, count=5, start=1):
    rng = random.Random(1103)
    items = []
    for k in range(count):
        a, b, c, d = rng.randint(3, 7), rng.randint(2, 6), rng.randint(8, 15), rng.randint(1, 2)
        ctx = INTRO
        if k == 0:
            level, err = "T", 2
            lines = [f"{c} {MINUS} (x + {b})", f"{c} {MINUS} x + {b}", f"{c + b} {MINUS} x"]
            fix = f"Miinus koskee koko sulkua: {MINUS}(x + {b}) = {MINUS}x {MINUS} {b}. Oikea tulos on {c - b} {MINUS} x."
        elif k == 1:
            level, err = "T", 2
            lines = [f"{c} {MINUS} ({a}x {MINUS} {b})", f"{c} {MINUS} {a}x {MINUS} {b}", f"{c - b} {MINUS} {a}x"]
            fix = (f"Miinus muuttaa myös luvun {MINUS}{b} merkin: {MINUS}({a}x {MINUS} {b}) = {MINUS}{a}x + {b}. "
                   f"Oikea tulos on {c + b} {MINUS} {a}x.")
        elif k == 2:
            level, err = "T", 3
            a = rng.randint(a + 1, 9)
            e = rng.randint(2, a - 1)
            lines = [f"({a}x + {c}) {MINUS} ({e}x + {b})", f"{a}x + {c} {MINUS} ({e}x + {b})",
                     f"{a}x + {c} {MINUS} {e}x + {b}", f"{lin(a - e, c + b)}"]
            fix = (f"Rivi 2 on oikein. Miinus koskee koko jälkimmäistä sulkua: {MINUS}({e}x + {b}) = {MINUS}{e}x {MINUS} {b}. "
                   f"Oikea tulos on {lin(a - e, c - b)}.")
            b = e  # keep params readable
        elif k == 3:
            level, err = "H", 3
            lines = [f"{MINUS}({a}x {MINUS} {b}) {MINUS} (x + {c})", f"{MINUS}{a}x + {b} {MINUS} (x + {c})",
                     f"{MINUS}{a}x + {b} {MINUS} x + {c}", lin(-(a + 1), b + c)]
            fix = (f"Rivi 2 on oikein. Miinus koskee koko sulkua (x + {c}): {MINUS}(x + {c}) = {MINUS}x {MINUS} {c}. "
                   f"Oikea tulos on {lin(-(a + 1), b - c)}.")
        else:
            level, err = "H", 2
            ctx = (f"Kaupassa jokaisesta {c} euron ostoksesta saa alennuksen, joka on x euroa mutta enintään {b} euroa pienempi "
                   f"kuin tavallinen alennus. Oppilas kirjoittaa maksettavan summan lausekkeen ja sieventää sen rivi riviltä. ")
            ctx = (f"Ostoksen hinta on {c} euroa. Siitä vähennetään alennus, jonka suuruus on x {MINUS} {b} euroa. "
                   f"Oppilas kirjoittaa maksettavan summan lausekkeen ja sieventää sen rivi riviltä. ")
            lines = [f"{c} {MINUS} (x {MINUS} {b})", f"{c} {MINUS} x {MINUS} {b}", f"{c - b} {MINUS} x"]
            fix = (f"Alennus x {MINUS} {b} vähennetään kokonaan: {MINUS}(x {MINUS} {b}) = {MINUS}x + {b}. "
                   f"Oikea tulos on {c + b} {MINUS} x.")
        payload = {"lines": lines, "error_line": err, "error_type": "minus_not_distributed"}
        items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, ctx + ASK, payload,
                               [fix], f"Virhe on rivillä {err}",
                               "Oikein: sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
