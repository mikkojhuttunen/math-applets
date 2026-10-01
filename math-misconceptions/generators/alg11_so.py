#!/usr/bin/env python3
"""ALG-11 (minus sign not distributed), type SO (step ordering). Every line is an expression equivalent to
line 1 (checked by verify.py); lines are listed in the correct order and shuffled by the app."""
import random

from gen_common import MINUS, base_item, cli, lin

TEMPLATE = "alg11_so"
TID, CODE = "ALG-11", "SO"
ASK = "Järjestä rivit oikeaan järjestykseen niin, että lauseke sievenee vaihe vaiheelta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1104)
    items = []
    for k in range(count):
        a, b, c, d = rng.randint(3, 7), rng.randint(2, 6), rng.randint(8, 15), rng.randint(1, 2)
        ctx = ""
        if k == 0:
            level = "T"
            lines = [f"{c} {MINUS} (x + {b})", f"{c} {MINUS} x {MINUS} {b}", f"{c - b} {MINUS} x"]
            expl = f"Miinus muuttaa sulun molempien termien merkit: {MINUS}x {MINUS} {b}. Lopuksi {c} {MINUS} {b} = {c - b}."
        elif k == 1:
            level = "T"
            lines = [f"{c} {MINUS} ({a}x {MINUS} {b})", f"{c} {MINUS} {a}x + {b}", f"{c + b} {MINUS} {a}x"]
            expl = f"Miinus muuttaa myös luvun {MINUS}{b} merkin plussaksi. Lopuksi {c} + {b} = {c + b}."
        elif k == 2:
            level = "T"
            a = rng.randint(a + 1, 9)
            e = rng.randint(2, a - 1)
            lines = [f"({a}x + {c}) {MINUS} ({e}x + {b})", f"{a}x + {c} {MINUS} ({e}x + {b})",
                     f"{a}x + {c} {MINUS} {e}x {MINUS} {b}", f"{a}x {MINUS} {e}x + {c} {MINUS} {b}", lin(a - e, c - b)]
            expl = f"Poistetaan ensin ensimmäisen sulun merkit, sitten toisen sulun termien merkit vaihtuvat, ja lopuksi lasketaan samanmuotoiset termit."
            b = e
        elif k == 3:
            level = "H"
            lines = [f"{MINUS}({a}x {MINUS} {b}) {MINUS} (x + {c})", f"{MINUS}{a}x + {b} {MINUS} (x + {c})",
                     f"{MINUS}{a}x + {b} {MINUS} x {MINUS} {c}", f"{MINUS}{a}x {MINUS} x + {b} {MINUS} {c}", lin(-(a + 1), b - c)]
            expl = f"Kummankin sulun edessä oleva miinus vaihtaa sulun sisällä olevien termien merkit; sen jälkeen lasketaan samanmuotoiset termit."
        else:
            level = "H"
            ctx = f"Ostoksen hinta on {c} euroa. Siitä vähennetään alennus, jonka suuruus on x {MINUS} {b} euroa. "
            lines = [f"{c} {MINUS} (x {MINUS} {b})", f"{c} {MINUS} x + {b}", f"{c + b} {MINUS} x"]
            expl = f"Alennus x {MINUS} {b} vähennetään kokonaan: miinus vaihtaa molempien termien merkit."
        assert len(set(lines)) == len(lines)
        payload = {"lines": lines, "accept": "exact"}
        items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, ctx + ASK, payload,
                               [expl, f"Sievin muoto: {lines[-1]}"], lines[-1],
                               "Oikein: sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
