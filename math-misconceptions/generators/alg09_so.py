#!/usr/bin/env python3
"""ALG-09 (square of a sum), type SO (step ordering). Every line is an expression equivalent to line 1
(checked by verify.py); lines are listed in the correct order and shuffled by the app."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg09_so"
TID, CODE = "ALG-09", "SO"
ASK = "Järjestä rivit oikeaan järjestykseen niin, että lauseke avautuu vaihe vaiheelta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(9303)
    items = []
    for k in range(count):
        b, c, a = rng.randint(2, 9), rng.randint(2, 6), rng.randint(2, 4)
        ctx = ""
        if k == 0:
            level = "T"
            lines = [f"(x + {b})²", f"(x + {b})(x + {b})", f"x² + {b}x + {b}x + {b * b}", f"x² + {2 * b}x + {b * b}"]
            expl = "Potenssi kirjoitetaan tulona, kerrotaan jokainen termi jokaisella ja lasketaan samanmuotoiset termit yhteen."
        elif k == 1:
            level = "T"
            lines = [f"(x {MINUS} {b})²", f"(x {MINUS} {b})(x {MINUS} {b})", f"x² {MINUS} {b}x {MINUS} {b}x + {b * b}",
                     f"x² {MINUS} {2 * b}x + {b * b}"]
            expl = f"Potenssi kirjoitetaan tulona. Termit ovat x ja {MINUS}{b}, joten tulo {MINUS}{b} · ({MINUS}{b}) = {b * b}."
        elif k == 2:
            level = "T"
            lines = [f"(x + {b})² + {c}x", f"(x + {b})(x + {b}) + {c}x", f"x² + {b}x + {b}x + {b * b} + {c}x",
                     f"x² + {2 * b}x + {b * b} + {c}x", f"x² + {2 * b + c}x + {b * b}"]
            expl = "Avataan potenssi tulona, lasketaan x-termit yhteen kahdessa vaiheessa."
        elif k == 3:
            level = "H"
            lines = [f"({a}x + {b})²", f"({a}x + {b})({a}x + {b})", f"{a * a}x² + {a * b}x + {a * b}x + {b * b}",
                     f"{a * a}x² + {2 * a * b}x + {b * b}"]
            expl = f"Potenssi kirjoitetaan tulona; {a}x · {a}x = {a * a}x² ja keskitermit ovat {a * b}x + {a * b}x."
        else:
            level = "H"
            ctx = (f"Neliönmuotoisen puutarhan sivun pituus on x + {b} metriä. Siitä erotetaan neliönmuotoinen "
                   f"kukkapenkki, jonka sivu on x metriä. Jäljelle jäävä pinta-ala sievennetään. ")
            lines = [f"(x + {b})² {MINUS} x²", f"(x + {b})(x + {b}) {MINUS} x²", f"x² + {b}x + {b}x + {b * b} {MINUS} x²",
                     f"x² + {2 * b}x + {b * b} {MINUS} x²", f"{2 * b}x + {b * b}"]
            expl = "Avataan potenssi tulona, lasketaan samanmuotoiset termit yhteen ja x²-termit kumoutuvat."
        payload = {"lines": lines, "accept": "exact"}
        items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, ctx + ASK, payload,
                               [expl, f"Sievin muoto: {lines[-1]}"], lines[-1],
                               "Oikein: (a + b)² avataan tulona (a + b)(a + b), ja siinä on myös kaksinkertainen tulo 2ab.",
                               TEMPLATE, {"a": a, "b": b, "c": c}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
