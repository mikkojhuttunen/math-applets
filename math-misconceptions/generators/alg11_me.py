#!/usr/bin/env python3
"""ALG-11 (minus sign not distributed), type ME (multi-select equivalence). Equivalence flags are checked by
verify.py with sympy; the tagged distractors leave some bracket term's sign unchanged."""
import random

from gen_common import MINUS, base_item, cli, lin

TEMPLATE = "alg11_me"
TID, CODE = "ALG-11", "ME"
GENERIC = "Kokeile sijoittaa x:n paikalle luku, esimerkiksi x = 1, ja vertaa lausekkeiden arvoja."
GOOD = "Oikein: sulun edessä oleva miinus muuttaa jokaisen sulun sisällä olevan termin merkin."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1107)
    items = []
    for k in range(count):
        a, b, c, e = rng.randint(3, 7), rng.randint(2, 6), rng.randint(8, 15), rng.randint(2, 4)
        ctx = ""
        if k == 0:
            level, ref = "T", f"{c} {MINUS} (x + {b})"
            eq = [f"{c} {MINUS} x {MINUS} {b}", f"{c - b} {MINUS} x", f"{MINUS}x + {c - b}"]
            bad = [(f"{c} {MINUS} x + {b}", TID), (f"{c + b} {MINUS} x", TID), (f"{c - b} + x", None)]
            steps = [f"{ref} = {c} {MINUS} x {MINUS} {b}", f"{c - b} {MINUS} x"]
        elif k == 1:
            level, ref = "T", f"{c} {MINUS} ({a}x {MINUS} {b})"
            eq = [f"{c} {MINUS} {a}x + {b}", f"{c + b} {MINUS} {a}x", f"{MINUS}{a}x + {c + b}"]
            bad = [(f"{c} {MINUS} {a}x {MINUS} {b}", TID), (f"{c - b} {MINUS} {a}x", TID), (f"{c + b} + {a}x", None)]
            steps = [f"{ref} = {c} {MINUS} {a}x + {b}", f"{c + b} {MINUS} {a}x"]
        elif k == 2:
            level, ref = "T", f"({a + 3}x + {c}) {MINUS} ({e}x + {b})"
            p = a + 3 - e
            eq = [f"{a + 3}x + {c} {MINUS} {e}x {MINUS} {b}", lin(p, c - b), f"{c - b} + {p}x"]
            bad = [(f"{a + 3}x + {c} {MINUS} {e}x + {b}", TID), (lin(p, c + b), TID), (lin(a + 3 + e, c - b), None)]
            steps = [f"{ref} = {a + 3}x + {c} {MINUS} {e}x {MINUS} {b}", lin(p, c - b)]
        elif k == 3:
            level, ref = "H", f"{MINUS}({a}x {MINUS} {b}) {MINUS} (x + {c})"
            eq = [f"{MINUS}{a}x + {b} {MINUS} x {MINUS} {c}", lin(-(a + 1), b - c), f"{b - c} {MINUS} {a + 1}x"]
            bad = [(f"{MINUS}{a}x + {b} {MINUS} x + {c}", TID), (lin(-(a + 1), b + c), TID), (lin(a + 1, b - c), None)]
            steps = [f"{ref} = {MINUS}{a}x + {b} {MINUS} x {MINUS} {c}", lin(-(a + 1), b - c)]
        else:
            level, ref = "H", f"{c} {MINUS} (x {MINUS} {b})"
            ctx = (f"Tilillä on {c} euroa. Siitä vähennetään lasku, jonka suuruus on x {MINUS} {b} euroa. "
                   "Valitse kaikki lausekkeet, jotka kuvaavat jäljelle jäävää rahamäärää euroina. ")
            eq = [f"{c} {MINUS} x + {b}", f"{c + b} {MINUS} x", f"{MINUS}x + {c + b}"]
            bad = [(f"{c} {MINUS} x {MINUS} {b}", TID), (f"{c + b} + x", None), (f"x {MINUS} {c - b}", None)]
            steps = [f"{ref} = {c} {MINUS} x + {b}", f"{c + b} {MINUS} x"]
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref} kaikilla x:n arvoilla."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        assert len({t for t, _, _ in opts}) == len(opts)
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": q, "misconception": m}
                   for i, (t, q, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[-2], [1], [3]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S3.02", "S2.01"], ["T14"], 7, level, prompt, payload, steps,
                               steps[-1], GOOD, TEMPLATE, {"a": a, "b": b, "c": c, "e": e}, date, run,
                               generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
