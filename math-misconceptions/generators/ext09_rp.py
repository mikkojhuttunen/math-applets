#!/usr/bin/env python3
"""EXT-09 (slope and intercept confused; steeper line means larger y), type RP. The solution x is computed from the
line y = m x + b; valid equations use the slope as the coefficient of x and the intercept as the constant term,
invalid ones swap the two. verify.py checks the solution sets."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "ext09_rp"
TID, CODE = "EXT-09", "RP"
GOOD = "Oikein: kulmakerroin on x:n kerroin ja vakiotermi on y:n arvo kohdassa x = 0."
GENERIC = ("Sijoita x:n paikalle pyydetty luku ja tarkista tulos. Suoralla y = mx + b luku m on x:n kerroin "
           "(kulmakerroin) ja b on vakiotermi (y:n arvo kohdassa x = 0).")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1903)
    items = []
    for k in range(count):
        level = "T"
        while True:  # slope and intercept must differ, otherwise the swapped equation is also valid
            m, b, v = rng.choice([2, 3, 4, 5]), rng.choice([1, 2, 3, 6, 7, 8]), rng.randint(2, 9)
            if m != b:
                break
        y0 = m * v + b
        if k == 0:
            prompt = (f"Suoran yhtälö on y = {m}x + {b}. Kirjoita yhtälö, jonka ratkaisu on x = {v}, "
                      f"kun suoran piste on korkeudella y = {y0}.")
            valid = [f"{m} * x + {b} = {y0}", f"{m} * x = {y0 - b}"]
            invalid = [f"{b} * x + {m} = {y0}", f"{m} + {b} * x = {y0}", f"{b} * x = {y0}"]
            steps = [f"Sijoitetaan y = {y0}: {m}x + {b} = {y0}", f"{m}x = {y0 - b}", f"x = {v}"]
            params = {"m": m, "b": b, "v": v}
        elif k == 1:
            m = -rng.choice([2, 3, 4])
            b = rng.choice([30, 40, 50])
            v = rng.randint(2, 9)
            y0 = b + m * v
            prompt = (f"Suoran yhtälö on y = {b} {MINUS} {-m}x. Kirjoita yhtälö, jonka ratkaisu on x = {v}, "
                      f"kun y = {y0}.")
            valid = [f"{b} - {-m} * x = {y0}", f"{b} - {y0} = {-m} * x"]
            invalid = [f"{-m} - {b} * x = {y0}", f"{b} + {-m} * x = {y0}", f"{-m} * x = {y0}"]
            steps = [f"Sijoitetaan y = {y0}: {b} {MINUS} {-m}x = {y0}", f"{-m}x = {b - y0}", f"x = {v}"]
            params = {"m": m, "b": b, "v": v}
        elif k == 2:
            b = m * rng.randint(1, 4)
            v = -b // m
            prompt = (f"Suoran yhtälö on y = {m}x + {b}. Kirjoita yhtälö, jonka ratkaisu on x = {MINUS}{-v}, "
                      f"kun suora leikkaa x-akselin (y = 0).")
            valid = [f"{m} * x + {b} = 0", f"{m} * x = {-b}"]
            invalid = [f"{b} * x + {m} = 0", f"{m} * x = {b}", f"{b} * x = {m}"]
            steps = [f"Sijoitetaan y = 0: {m}x + {b} = 0", f"{m}x = {MINUS}{b}", f"x = {MINUS}{-v}"]
            params = {"m": m, "b": b, "v": v}
        elif k == 3:
            level = "H"
            while True:
                m1, m2 = rng.sample([1, 2, 3, 4, 5, 6], 2)
                b1, b2 = rng.randint(1, 12), rng.randint(1, 12)
                if (b2 - b1) % (m1 - m2) == 0 and (b2 - b1) // (m1 - m2) > 0 and b1 != b2:
                    break
            v = (b2 - b1) // (m1 - m2)
            prompt = (f"Suorat y = {m1}x + {b1} ja y = {m2}x + {b2} leikkaavat. Kirjoita yhtälö, jonka ratkaisu on "
                      f"x = {v} eli leikkauspisteen x-koordinaatti.")
            valid = [f"{m1} * x + {b1} = {m2} * x + {b2}", f"{m1} * x - {m2} * x = {b2} - {b1}"]
            invalid = [f"{b1} * x + {m1} = {b2} * x + {m2}", f"{m1} * x + {b1} = {b2} * x + {m2}",
                       f"{m1} * x + {m2} = {b1} * x + {b2}"]
            steps = ["Leikkauspisteessä y-arvot ovat yhtä suuret", f"{m1}x + {b1} = {m2}x + {b2}", f"x = {v}"]
            params = {"m1": m1, "b1": b1, "m2": m2, "b2": b2}
        else:
            level = "H"
            y0 = b + m * v
            prompt = (f"Suoran pisteiden taulukossa x = 0, 1, 2 ja y = {b}, {b + m}, {b + 2 * m}. Kirjoita yhtälö, "
                      f"jonka ratkaisu on x = {v}, kun y = {y0}.")
            valid = [f"{b} + {m} * x = {y0}", f"{m} * x = {y0 - b}"]
            invalid = [f"{m} + {b} * x = {y0}", f"{b + m} * x = {y0}", f"{b} * x = {y0}"]
            steps = [f"Kun x = 0, y = {b}, ja x:n kasvaessa yhdellä y kasvaa {m}", f"y = {b} + {m}x",
                     f"{b} + {m}x = {y0}, joten x = {v}"]
            params = {"m": m, "b": b, "v": v}
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": v},
                   "checks": {"valid": valid, "invalid": invalid}}
        final = f"x = {str(v).replace('-', MINUS)}"
        items.append(base_item(TID, CODE, start + k, ["S4.05"], ["T15"], 8, level, prompt, payload, steps, final,
                               GOOD, TEMPLATE, params | {"form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
