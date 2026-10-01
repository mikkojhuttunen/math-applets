#!/usr/bin/env python3
"""ALG-06 (operational reading of '='), type RP (write an equation with a given solution).
Valid and invalid equations are built from the same numbers; verify.py checks their solution sets."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg06_rp"
TID, CODE = "ALG-06", "RP"


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
            prompt = f"Täydennä yhtälö {a} + {b} = x + □ siten, että sen ratkaisu on x = {v}. Kirjoita koko yhtälö."
            valid = [f"{a} + {b} = x + {c}", f"x + {c} = {a} + {b}"]
            invalid = [f"{a} + {b} = x", f"{a} + {b} = x + {c + 1}", f"{a} + {b} = x {MINUS} {c}"]
            value = v
            steps = [f"{a} + {b} = {s}", f"x = {v}, joten □ = {s} {MINUS} {v} = {c}", f"{a} + {b} = x + {c}"]
        elif k == 1:
            level = "T"
            prompt = f"Täydennä yhtälö x + □ = {a} + {b} siten, että sen ratkaisu on x = {v}. Kirjoita koko yhtälö."
            valid = [f"x + {c} = {a} + {b}", f"{a} + {b} = x + {c}"]
            invalid = [f"x = {a} + {b}", f"x + {c + 1} = {a} + {b}", f"x + {a} = {b} + {c}"]
            value = v
            steps = [f"{a} + {b} = {s}", f"□ = {s} {MINUS} {v} = {c}", f"x + {c} = {a} + {b}"]
        elif k == 2:
            level = "T"
            prompt = f"Täydennä yhtälö {a} + {b} = □ + x siten, että sen ratkaisu on x = {v}. Kirjoita koko yhtälö."
            valid = [f"{a} + {b} = {c} + x", f"{c} + x = {a} + {b}"]
            invalid = [f"{a} + {b} = x", f"{a} + {b} = {c + 1} + x", f"{a} + {b} + {c} = x"]
            value = v
            steps = [f"{a} + {b} = {s}", f"□ = {s} {MINUS} {v} = {c}", f"{a} + {b} = {c} + x"]
        elif k == 3:
            level = "H"
            v3 = a - b - d
            prompt = f"Täydennä yhtälö {a} {MINUS} {b} = x + □ siten, että sen ratkaisu on x = {v3}. Kirjoita koko yhtälö."
            valid = [f"{a} {MINUS} {b} = x + {d}", f"x + {d} = {a} {MINUS} {b}"]
            invalid = [f"{a} {MINUS} {b} = x", f"{a} {MINUS} {b} = x + {d + 1}", f"{a} {MINUS} {b} = x {MINUS} {d}"]
            value = v3
            steps = [f"{a} {MINUS} {b} = {a - b}", f"□ = {a - b} {MINUS} {v3} = {d}", f"{a} {MINUS} {b} = x + {d}"]
        else:
            level = "H"
            prompt = (f"Vaa'an vasemmassa kupissa on {a} kg:n ja {b} kg:n painot, oikeassa kupissa {c} kg:n paino ja paino x kg. "
                      f"Kirjoita yhtälö, joka kuvaa tasapainoa ja jonka ratkaisu on x = {v}.")
            valid = [f"{a} + {b} = {c} + x", f"{c} + x = {a} + {b}", f"x = {a} + {b} {MINUS} {c}"]
            invalid = [f"{a} + {b} = x", f"{a} + {b} + {c} = x", f"{a} + {b} = {c} {MINUS} x"]
            value = v
            steps = [f"Vasen kuppi: {a} + {b} = {s} kg", f"Oikea kuppi: {c} + x", f"{a} + {b} = {c} + x"]
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps,
                               f"x = {value}", "Oikein: yhtälön molemmat puolet ovat yhtä suuret, kun x on pyydetty luku.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
