#!/usr/bin/env python3
"""ALG-09 (square of a sum), type ME (multi-select equivalence). Equivalence flags are checked by verify.py
with sympy; distractors distribute the power over the sum or lose the cross term."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg09_me"
TID, CODE = "ALG-09", "ME"


def make_items(run, date, count=5, start=1):
    rng = random.Random(9305)
    items = []
    for k in range(count):
        b, c, d = rng.randint(2, 9), rng.randint(2, 4), rng.randint(2, 9)
        ctx = ""
        if k == 0:
            level, ref = "T", f"(x + {b})²"
            eq = [f"x² + {2 * b}x + {b * b}", f"(x + {b})(x + {b})", f"x² + {b}x + {b}x + {b * b}"]
            bad = [(f"x² + {b * b}", TID), (f"x² + {b}x + {b * b}", TID), (f"2x + {2 * b}", None)]
            steps = [f"(x + {b})² = (x + {b})(x + {b})", f"x² + {2 * b}x + {b * b}"]
        elif k == 1:
            level, ref = "T", f"(x {MINUS} {b})²"
            eq = [f"x² {MINUS} {2 * b}x + {b * b}", f"(x {MINUS} {b})(x {MINUS} {b})", f"{b * b} {MINUS} {2 * b}x + x²"]
            bad = [(f"x² {MINUS} {b * b}", TID), (f"x² {MINUS} {2 * b}x {MINUS} {b * b}", TID), (f"x² + {2 * b}x + {b * b}", None)]
            steps = [f"(x {MINUS} {b})² = (x {MINUS} {b})(x {MINUS} {b})", f"x² {MINUS} {2 * b}x + {b * b}"]
        elif k == 2:
            level, ref = "T", f"({c}x + {b})²"
            eq = [f"{c * c}x² + {2 * c * b}x + {b * b}", f"({c}x + {b})({c}x + {b})", f"{b * b} + {2 * c * b}x + {c * c}x²"]
            bad = [(f"{c * c}x² + {b * b}", TID), (f"{c * c}x² + {c * b}x + {b * b}", TID), (f"{c}x² + {2 * c * b}x + {b * b}", None)]
            steps = [f"({c}x + {b})² = ({c}x + {b})({c}x + {b})", f"{c * c}x² + {2 * c * b}x + {b * b}"]
        elif k == 3:
            level, ref = "H", f"(x + {b})² {MINUS} x²"
            eq = [f"{2 * b}x + {b * b}", f"{b * b} + {2 * b}x", f"x² + {2 * b}x + {b * b} {MINUS} x²"]
            bad = [(f"{b * b}", TID), (f"{2 * b}x", TID), (f"{b}x + {b * b}", TID)]
            steps = [f"(x + {b})² = x² + {2 * b}x + {b * b}", f"{2 * b}x + {b * b}"]
        else:
            level, ref = "H", f"(x + {b})² + {d}"
            ctx = (f"Neliönmuotoisen terassin sivu on x + {b} metriä, ja viereen tulee {d} m² kukkapenkki. "
                   "Valitse kaikki lausekkeet, jotka kuvaavat yhteenlaskettua pinta-alaa neliömetreinä. ")
            eq = [f"x² + {2 * b}x + {b * b} + {d}", f"x² + {2 * b}x + {b * b + d}", f"(x + {b})(x + {b}) + {d}"]
            bad = [(f"x² + {b * b} + {d}", TID), (f"x² + {b}x + {b * b + d}", TID), (f"(x + {b + d})²", None)]
            steps = [f"(x + {b})² = x² + {2 * b}x + {b * b}", f"x² + {2 * b}x + {b * b + d}"]
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref} kaikilla x:n arvoilla."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[-2], [1], [3]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S3.04", "S3.03"], ["T14"], 8, level, prompt, payload, steps,
                               steps[-1], "Oikein: (a + b)² = a² + 2ab + b².", TEMPLATE,
                               {"b": b, "c": c, "d": d}, date, run,
                               generic_wrong="Kokeile sijoittaa x:n paikalle luku, esimerkiksi x = 1, ja vertaa lausekkeiden arvoja."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
