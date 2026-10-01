#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type ME (multi-select equivalence). Equivalence flags are
checked by verify.py with sympy; distractors multiply only one term of the bracket."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg08_me"
TID, CODE = "ALG-08", "ME"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8305)
    items = []
    for k in range(count):
        a, b, c = rng.randint(2, 7), rng.randint(2, 8), rng.randint(2, 6)
        ctx = ""
        if k == 0:
            level, ref = "T", f"{a}(x + {b})"
            eq = [f"{a}x + {a * b}", f"{a * b} + {a}x", f"{a} · x + {a} · {b}"]
            bad = [(f"{a}x + {b}", TID), (f"x + {a * b}", TID), (f"{a + b}x", None)]
            steps = [f"{a}(x + {b}) = {a} · x + {a} · {b}", f"{a}x + {a * b}"]
        elif k == 1:
            level, ref = "T", f"{a}(x {MINUS} {b})"
            eq = [f"{a}x {MINUS} {a * b}", f"{MINUS}{a * b} + {a}x", f"{a} · x {MINUS} {a} · {b}"]
            bad = [(f"{a}x {MINUS} {b}", TID), (f"x {MINUS} {a * b}", TID), (f"{a}x + {a * b}", "ALG-11")]
            steps = [f"{a}(x {MINUS} {b}) = {a} · x {MINUS} {a} · {b}", f"{a}x {MINUS} {a * b}"]
        elif k == 2:
            level, ref = "T", f"{a}({b} + {c}x)"
            eq = [f"{a * b} + {a * c}x", f"{a * c}x + {a * b}", f"{a} · {b} + {a} · {c}x"]
            bad = [(f"{a * b} + {c}x", TID), (f"{b} + {a * c}x", TID), (f"{a * b * c}x", None)]
            steps = [f"{a}({b} + {c}x) = {a} · {b} + {a} · {c}x", f"{a * b} + {a * c}x"]
        elif k == 3:
            level, ref = "H", f"{a}(x + {b}) + {c}"
            eq = [f"{a}x + {a * b} + {c}", f"{a}x + {a * b + c}", f"{c} + {a * b} + {a}x"]
            bad = [(f"{a}x + {b} + {c}", TID), (f"x + {a * b} + {c}", TID), (f"{a}(x + {b + c})", None)]
            steps = [f"{a}(x + {b}) + {c} = {a}x + {a * b} + {c}", f"{a}x + {a * b + c}"]
        else:
            level, ref = "H", f"{a}({c}x + {b})"
            ctx = (f"Kauppias pakkaa {a} pussia. Jokaiseen pussiin tulee {c}x grammaa karkkia ja {b} grammaa suklaata. "
                   "Valitse kaikki lausekkeet, jotka kuvaavat pussien kokonaispainoa grammoina. ")
            eq = [f"{a * c}x + {a * b}", f"{a * b} + {a * c}x", f"{a} · {c}x + {a} · {b}"]
            bad = [(f"{a * c}x + {b}", TID), (f"{c}x + {a * b}", TID), (f"{a + c}x + {a + b}", None)]
            steps = [f"{a}({c}x + {b}) = {a} · {c}x + {a} · {b}", f"{a * c}x + {a * b}"]
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref} kaikilla x:n arvoilla."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[-2], [1], [3]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, steps[-1],
                               "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin.", TEMPLATE,
                               {"a": a, "b": b, "c": c}, date, run,
                               misconceptions=[TID] + (["ALG-11"] if k == 1 else []),
                               generic_wrong="Kokeile sijoittaa x:n paikalle luku, esimerkiksi x = 1, ja vertaa lausekkeiden arvoja."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
