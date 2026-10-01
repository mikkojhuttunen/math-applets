#!/usr/bin/env python3
"""ALG-09 (square of a sum), type FS (fill in the missing step). Every line is equivalent to line 1
(checked by verify.py); the blanked line is accepted by equivalence to the reference expression."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg09_fs"
TID, CODE = "ALG-09", "FS"
SAMPLES = [[1], [2], [3]]
GENERIC = ("Muista, että (a + b)² = (a + b)(a + b). Kerro jokainen termi jokaisella termillä, "
           "niin saat myös keskimmäiset termit. Tarkista sijoittamalla x = 1.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(9304)
    items = []
    for k in range(count):
        b, c, d = rng.randint(2, 9), rng.randint(2, 4), rng.randint(2, 9)
        level, ctx = "T", ""
        if k == 0:
            lines = [f"(x + {b})²", f"(x + {b})(x + {b})", f"x² + {b}x + {b}x + {b * b}", f"x² + {2 * b}x + {b * b}"]
            blank, how = 2, "Kirjoita neliö tulona."
        elif k == 1:
            lines = [f"(x {MINUS} {b})²", f"(x {MINUS} {b})(x {MINUS} {b})", f"x² {MINUS} {b}x {MINUS} {b}x + {b * b}",
                     f"x² {MINUS} {2 * b}x + {b * b}"]
            blank, how = 3, "Kerro sulut keskenään ja kirjoita kaikki neljä termiä."
        elif k == 2:
            lines = [f"({c}x + {b})²", f"({c}x + {b})({c}x + {b})", f"{c * c}x² + {c * b}x + {c * b}x + {b * b}",
                     f"{c * c}x² + {2 * c * b}x + {b * b}"]
            blank, how = 4, "Kirjoita sievennetty lauseke."
        elif k == 3:
            level = "H"
            lines = [f"(x + {b})² + {d}", f"x² + {2 * b}x + {b * b} + {d}", f"x² + {2 * b}x + {b * b + d}"]
            blank, how = 2, "Avaa neliö."
        else:
            level = "H"
            ctx = (f"Neliönmuotoisen terassin sivu on x + {b} metriä, ja siitä jää x metrin sivuinen neliö kukkapenkiksi. "
                   "Terassin jäljelle jäävä pinta-ala lasketaan rivi riviltä. ")
            lines = [f"(x + {b})² {MINUS} x²", f"x² + {2 * b}x + {b * b} {MINUS} x²", f"{2 * b}x + {b * b}"]
            blank, how = 2, "Avaa neliö."
        shown = [lines[i] if i != blank - 1 else "□" for i in range(len(lines))]
        prompt = f"{ctx}Täydennä puuttuva rivi: {', '.join(shown)}. {how}"
        ref = lines[blank - 1]
        payload = {"lines": lines, "blank_index": blank,
                   "answer": {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}}
        items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, prompt, payload,
                               [f"Rivi {blank}: {ref}", f"Lopputulos: {lines[-1]}"], ref,
                               "Oikein: (a + b)² on tulo (a + b)(a + b), ja siinä on myös keskimmäiset termit 2ab.",
                               TEMPLATE, {"b": b, "c": c, "d": d}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
