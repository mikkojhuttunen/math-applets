#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type RP (write an equation with a given solution).
Valid and invalid equations are built from the same numbers; verify.py checks their solution sets.
The invalid equations are the results of a sign slip or a one-sided operation."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg07_rp"
TID, CODE = "ALG-07", "RP"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8204)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
            if (a, b, x) not in seen:
                break
        seen.add((a, b, x))
        level, e = "T", 0
        if k == 0:
            c = a * x + b
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {a}x + {b} ja jonka ratkaisu on x = {x}."
            valid = [f"{a}x + {b} = {c}", f"{c} = {a}x + {b}"]
            invalid = [f"{a}x + {b} = {c + 2 * b}", f"{a}x + {b} = {a * x}", f"{a}x + {b} = {c - 2 * b}"]
            steps = [f"Sijoitetaan x = {x}: {a} · {x} + {b} = {c}", f"{a}x + {b} = {c}"]
        elif k == 1:
            c = a * x - b
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {a}x {MINUS} {b} ja jonka ratkaisu on x = {x}."
            valid = [f"{a}x {MINUS} {b} = {c}", f"{c} = {a}x {MINUS} {b}"]
            invalid = [f"{a}x {MINUS} {b} = {c + 2 * b}", f"{a}x {MINUS} {b} = {a * x}", f"{a}x {MINUS} {b} = {c - 2 * b}"]
            steps = [f"Sijoitetaan x = {x}: {a} · {x} {MINUS} {b} = {c}", f"{a}x {MINUS} {b} = {c}"]
        elif k == 2:
            c = b + a * x
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {b} + {a}x ja jonka ratkaisu on x = {x}."
            valid = [f"{b} + {a}x = {c}", f"{c} = {b} + {a}x"]
            invalid = [f"{b} + {a}x = {c + 2 * b}", f"{b} + {a}x = {a * x}", f"{b} + {a}x = {c - 2 * b}"]
            steps = [f"Sijoitetaan x = {x}: {b} + {a} · {x} = {c}", f"{b} + {a}x = {c}"]
        elif k == 3:
            level = "H"
            a = max(a, 5)
            e = rng.randint(2, a - 2)
            d = b + (a - e) * x
            prompt = f"Täydennä yhtälö {a}x + {b} = {e}x + □ siten, että sen ratkaisu on x = {x}. Kirjoita koko yhtälö."
            valid = [f"{a}x + {b} = {e}x + {d}", f"{e}x + {d} = {a}x + {b}"]
            invalid = [f"{a}x + {b} = {e}x + {d + 2 * b}", f"{a}x + {b} = {e}x + {d - 2 * b}", f"{a}x + {b} = {e}x + {d + b}"]
            c = d
            steps = [f"Molemmat puolet saavat saman arvon, kun x = {x}: {a} · {x} + {b} = {a * x + b}",
                     f"□ = {a * x + b} {MINUS} {e} · {x} = {d}", f"{a}x + {b} = {e}x + {d}"]
        else:
            level = "H"
            c = b + a * x
            prompt = (f"Taksin lähtömaksu on {b} euroa ja kilometrihinta {a} euroa. Matkan hinta oli {c} euroa. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {x} on ajettujen kilometrien määrä.")
            valid = [f"{b} + {a}x = {c}", f"{a}x + {b} = {c}", f"{a}x = {c} {MINUS} {b}"]
            invalid = [f"{a}x {MINUS} {b} = {c}", f"{a}x = {c} + {b}", f"{a}x + {b} = {a * x}"]
            steps = [f"Hinta = lähtömaksu + kilometrit · {a}", f"{b} + {a}x = {c}"]
            e = 0
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": x},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps, f"x = {x}",
                               "Oikein: kun x:n paikalle sijoitetaan pyydetty luku, yhtälön molemmat puolet ovat yhtä suuret.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "e": e, "x": x}, date, run,
                               generic_wrong="Sijoita x:n paikalle pyydetty luku ja laske molemmat puolet: ovatko ne yhtä suuret?"))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
