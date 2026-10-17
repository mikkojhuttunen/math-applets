#!/usr/bin/env python3
"""ALG-06 (operational reading of '='), type MC select-all (a reverse problem).
The pupil ticks every equation whose solution is the given value. Correct equations balance both sides
(e.g. 9 + 5 = x + 4, also with the sides swapped); wrong ones come from the same numbers, and the tagged ones
read '=' as "gives the answer" (9 + 5 = x, or adding every number: 9 + 5 + 7 = x)."""
import random

from gen_common import MINUS, base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "alg06_mcs"
TID, CODE = "ALG-06", "MC"


def make_items(run, date, count=5, start=1):
    rng = random.Random(204)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, c, d = (rng.randint(3, 9) for _ in range(4))
            if len({a, b, c}) == 3 and a > b and a + b > c + 1 and a - b > d and (a, b, c) not in seen:
                break
        seen.add((a, b, c))
        s, v = a + b, a + b - c
        if k == 0:
            level = "T"
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {v}."
            valid = [f"{a} + {b} = x + {c}", f"x + {c} = {a} + {b}"]
            invalid = [(f"{a} + {b} = x", TID), (f"{a} + {b} = x + {c + 1}", None), (f"{a} + {b} = x {MINUS} {c}", None)]
            value = v
            steps = [f"{a} + {b} = {s}", f"Sijoita x = {v}: {v} + {c} = {s}, joten {a} + {b} = x + {c} kelpaa"]
        elif k == 1:
            level = "T"
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {v}."
            valid = [f"x + {c} = {a} + {b}", f"{a} + {b} = x + {c}"]
            invalid = [(f"x = {a} + {b}", TID), (f"x + {c + 1} = {a} + {b}", None), (f"x + {a} = {b} + {c}", None)]
            value = v
            steps = [f"{a} + {b} = {s}", f"Sijoita x = {v}: {v} + {c} = {s}, joten x + {c} = {a} + {b} kelpaa"]
        elif k == 2:
            level = "T"
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {v}."
            valid = [f"{a} + {b} = {c} + x", f"{c} + x = {a} + {b}"]
            invalid = [(f"{a} + {b} = x", TID), (f"{a} + {b} = {c + 1} + x", None), (f"{a} + {b} + {c} = x", TID)]
            value = v
            steps = [f"{a} + {b} = {s}", f"Sijoita x = {v}: {c} + {v} = {s}, joten {a} + {b} = {c} + x kelpaa"]
        elif k == 3:
            level = "H"
            v3 = a - b - d
            prompt = f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {v3}."
            valid = [f"{a} {MINUS} {b} = x + {d}", f"x + {d} = {a} {MINUS} {b}"]
            invalid = [(f"{a} {MINUS} {b} = x", TID), (f"{a} {MINUS} {b} = x + {d + 1}", None), (f"{a} {MINUS} {b} = x {MINUS} {d}", None)]
            value = v3
            steps = [f"{a} {MINUS} {b} = {a - b}", f"Sijoita x = {v3}: {v3} + {d} = {a - b}, joten {a} {MINUS} {b} = x + {d} kelpaa"]
        else:
            level = "H"
            prompt = (f"Vaa'an vasemmassa kupissa on {a} kg:n ja {b} kg:n painot, oikeassa kupissa {c} kg:n paino ja paino x kg. "
                      f"Valitse kaikki yhtälöt, jotka kuvaavat tasapainoa ja joiden ratkaisu on x = {v}.")
            valid = [f"{a} + {b} = {c} + x", f"{c} + x = {a} + {b}", f"x = {a} + {b} {MINUS} {c}"]
            invalid = [(f"{a} + {b} = x", TID), (f"{a} + {b} + {c} = x", TID), (f"{a} + {b} = {c} {MINUS} x", None)]
            value = v
            steps = [f"Vasen kuppi: {a} + {b} = {s} kg", f"Oikea kuppi: {c} + x", f"{a} + {b} = {c} + x"]
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", value, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps,
                               "; ".join(pretty(e) for e in valid), "Yhtälön molemmat puolet ovat yhtä suuret, kun x on pyydetty luku.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
