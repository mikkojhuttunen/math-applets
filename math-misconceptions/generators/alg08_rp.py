#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type RP (write an equation with a given solution).
Valid and invalid equations are built from the same numbers; verify.py checks their solution sets.
The invalid equations multiply only the first term of the bracket."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg08_rp"
TID, CODE = "ALG-08", "RP"


def make_items(run, date, count=5, start=1):
    rng = random.Random(8305)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, x = rng.randint(2, 6), rng.randint(2, 7), rng.randint(2, 9)
            cc = rng.randint(2, 5)
            if (a, b, x) not in seen and x > b:
                break
        seen.add((a, b, x))
        level = "T"
        if k == 0:
            c = a * (x + b)
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {a}(x + {b}) ja jonka ratkaisu on x = {x}."
            valid = [f"{a}(x + {b}) = {c}", f"{a}x + {a * b} = {c}"]
            invalid = [f"{a}(x + {b}) = {c + a * b - b}", f"{a}x + {b} = {c}", f"{a}x + {b} = {a * x + a * b}"]
            steps = [f"Sijoitetaan x = {x}: {a}({x} + {b}) = {c}", f"{a}(x + {b}) = {c}"]
        elif k == 1:
            c = a * (x - b)
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {a}(x {MINUS} {b}) ja jonka ratkaisu on x = {x}."
            valid = [f"{a}(x {MINUS} {b}) = {c}", f"{a}x {MINUS} {a * b} = {c}"]
            invalid = [f"{a}(x {MINUS} {b}) = {c + a * b - b}", f"{a}x {MINUS} {b} = {c}", f"{a}x {MINUS} {b} = {a * x - a * b}"]
            steps = [f"Sijoitetaan x = {x}: {a}({x} {MINUS} {b}) = {c}", f"{a}(x {MINUS} {b}) = {c}"]
        elif k == 2:
            c = a * (x + b) + cc * x
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {a}(x + {b}) + {cc}x ja jonka ratkaisu on x = {x}."
            valid = [f"{a}(x + {b}) + {cc}x = {c}", f"{a + cc}x + {a * b} = {c}"]
            invalid = [f"{a}x + {b} + {cc}x = {c}", f"{a + cc}x + {b} = {c}", f"{a}(x + {b}) + {cc}x = {c + 3 * a}"]
            steps = [f"Sijoitetaan x = {x}: {a}({x} + {b}) + {cc} · {x} = {c}", f"{a}(x + {b}) + {cc}x = {c}"]
        elif k == 3:
            level = "H"
            m = rng.randint(2, 4)
            c = a * (m * x + b)
            prompt = f"Kirjoita yhtälö, jonka vasen puoli on {a}({m}x + {b}) ja jonka ratkaisu on x = {x}. Kirjoita yhtälön oikea puoli lukuna."
            valid = [f"{a}({m}x + {b}) = {c}", f"{a * m}x + {a * b} = {c}"]
            invalid = [f"{a * m}x + {b} = {c}", f"{a}({m}x + {b}) = {c + a * b - b}", f"{a * m}x + {b} = {a * m * x + a * b}"]
            cc = m
            steps = [f"Sijoitetaan x = {x}: {a}({m} · {x} + {b}) = {c}", f"{a}({m}x + {b}) = {c}"]
        else:
            level = "H"
            c = a * (x + b)
            prompt = (f"Siivooja veloittaa {a} euroa tunnilta. Työ kestää x + {b} tuntia, ja koko työn hinta on {c} euroa. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {x} on tuntimäärä ilman {b} tunnin lisäosaa.")
            valid = [f"{a}(x + {b}) = {c}", f"{a}x + {a * b} = {c}"]
            invalid = [f"{a}x + {b} = {c}", f"{a}(x + {b}) = {a * x}", f"{a}x + {b} = {a * x + a * b}"]
            steps = [f"Hinta = tuntihinta · tunnit = {a}(x + {b})", f"{a}(x + {b}) = {c}"]
        invalid = list(dict.fromkeys(invalid))
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": x},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, f"x = {x}",
                               "Oikein: kun x:n paikalle sijoitetaan pyydetty luku, yhtälön molemmat puolet ovat yhtä suuret.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": cc, "x": x}, date, run,
                               generic_wrong="Sijoita x:n paikalle pyydetty luku ja laske molemmat puolet: ovatko ne yhtä suuret? Muista, että kerroin kertoo koko sulun."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
