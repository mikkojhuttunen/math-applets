#!/usr/bin/env python3
"""ALG-09 (square of a sum), type ES (error spotting). Lines before the error line are equivalent to line 1
and the error line breaks equivalence (checked by verify.py); the injected error is (a + b)² = a² + b²
or the dropped cross term."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg09_es"
TID, CODE = "ALG-09", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = "Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Kokeile vaikka x = 1. Muista, että (a + b)² = (a + b)(a + b)."
INTRO = "Oppilas sieventää lausekkeen rivi riviltä. "


def make_items(run, date, count=5, start=1):
    rng = random.Random(9302)
    items = []
    for k in range(count):
        b, c, a = rng.randint(2, 9), rng.randint(2, 6), rng.randint(2, 4)
        ctx = INTRO
        if k == 0:
            level, err, etype = "T", 2, "power_over_sum"
            lines = [f"(x + {b})² + {c}", f"x² + {b * b} + {c}", f"x² + {b * b + c}"]
            fix = f"(x + {b})² = (x + {b})(x + {b}) = x² + {2 * b}x + {b * b}. Oikea tulos on x² + {2 * b}x + {b * b + c}."
        elif k == 1:
            level, err, etype = "T", 2, "power_over_sum"
            lines = [f"(x {MINUS} {b})² + {c}x", f"x² {MINUS} {b * b} + {c}x", f"x² + {c}x {MINUS} {b * b}"]
            fix = (f"(x {MINUS} {b})² = (x {MINUS} {b})(x {MINUS} {b}) = x² {MINUS} {2 * b}x + {b * b}. "
                   f"Oikea tulos on x² {'+' if c >= 2 * b else MINUS} {abs(c - 2 * b)}x + {b * b}.")
        elif k == 2:
            level, err, etype = "T", 4, "drops_cross_term"
            lines = [f"(x + {b})²", f"(x + {b})(x + {b})", f"x² + {b}x + {b}x + {b * b}", f"x² + {b * b}"]
            fix = f"Rivi 3 on oikein. Keskimmäiset termit {b}x + {b}x = {2 * b}x eivät katoa: oikea tulos on x² + {2 * b}x + {b * b}."
        elif k == 3:
            level, err, etype = "H", 2, "power_over_sum"
            lines = [f"({a}x + {b})²", f"({a}x)² + {b}²", f"{a * a}x² + {b * b}"]
            fix = (f"({a}x + {b})² = ({a}x + {b})({a}x + {b}) = {a * a}x² + {2 * a * b}x + {b * b}. "
                   f"Oikea tulos on {a * a}x² + {2 * a * b}x + {b * b}.")
        else:
            level, err, etype = "H", 2, "power_over_sum"
            ctx = (f"Neliönmuotoisen puutarhan sivun pituus on x + {b} metriä. Siitä erotetaan neliönmuotoinen "
                   f"kukkapenkki, jonka sivu on {b} metriä. Oppilas laskee jäljelle jäävän pinta-alan lausekkeen rivi riviltä. ")
            lines = [f"(x + {b})² {MINUS} {b * b}", f"x² + {b * b} {MINUS} {b * b}", "x²"]
            fix = f"(x + {b})² = x² + {2 * b}x + {b * b}. Oikea tulos on x² + {2 * b}x."
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, ctx + ASK, payload,
                               [fix], f"Virhe on rivillä {err}",
                               "Oikein: (a + b)² on tulo (a + b)(a + b), ja siinä on myös kaksinkertainen tulo 2ab.",
                               TEMPLATE, {"a": a, "b": b, "c": c}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
