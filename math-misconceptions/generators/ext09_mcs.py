#!/usr/bin/env python3
"""EXT-09 (slope and intercept confused; steeper line means larger y), type MC select-all (a reverse problem).
The solution x is computed from the line y = m x + b; the pupil ticks every equation whose solution is that x.
Correct equations use the slope as the coefficient of x and the intercept as the constant term; wrong ones swap the
two, or drop or change a term. verify.py checks the solution sets."""
import random

from gen_common import MINUS, base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "ext09_mcs"
TID, CODE = "EXT-09", "MC"
GOOD = "Kulmakerroin on x:n kerroin ja vakiotermi on y:n arvo kohdassa x = 0."
GENERIC = ("Sijoita x:n paikalle pyydetty luku ja tarkista tulos. Suoralla y = mx + b luku m on x:n kerroin "
           "eli kulmakerroin, ja b on vakiotermi eli y:n arvo kohdassa x = 0.")


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
            prompt = (f"Suoran yhtälö on y = {m}x + {b}, ja suoran piste on korkeudella y = {y0}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on pisteen x-koordinaatti x = {v}.")
            valid = [f"{m}x + {b} = {y0}", f"{m}x = {y0 - b}"]
            invalid = [(f"{b}x + {m} = {y0}", TID), (f"{m} + {b}x = {y0}", TID), (f"{b}x = {y0}", None)]
            steps = [f"Sijoitetaan y = {y0}: {m}x + {b} = {y0}", f"{m}x = {y0 - b}", f"x = {v}"]
            params = {"m": m, "b": b, "v": v}
        elif k == 1:
            m = -rng.choice([2, 3, 4])
            b = rng.choice([30, 40, 50])
            v = rng.randint(2, 9)
            y0 = b + m * v
            prompt = (f"Suoran yhtälö on y = {b} {MINUS} {-m}x, ja suoran piste on korkeudella y = {y0}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on pisteen x-koordinaatti x = {v}.")
            valid = [f"{b} - {-m}x = {y0}", f"{b} - {y0} = {-m}x"]
            invalid = [(f"{-m} - {b}x = {y0}", TID), (f"{b} + {-m}x = {y0}", None), (f"{-m}x = {y0}", None)]
            steps = [f"Sijoitetaan y = {y0}: {b} {MINUS} {-m}x = {y0}", f"{-m}x = {b - y0}", f"x = {v}"]
            params = {"m": m, "b": b, "v": v}
        elif k == 2:
            b = m * rng.randint(1, 4)
            v = -b // m
            prompt = (f"Suoran yhtälö on y = {m}x + {b}. Suora leikkaa x-akselin kohdassa, jossa y = 0. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on leikkauskohta x = {MINUS}{-v}.")
            valid = [f"{m}x + {b} = 0", f"{m}x = {-b}"]
            invalid = [(f"{b}x + {m} = 0", TID), (f"{m}x = {b}", None), (f"{b}x = {m}", None)]
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
            prompt = (f"Suorat y = {m1}x + {b1} ja y = {m2}x + {b2} leikkaavat. Valitse kaikki yhtälöt, joiden "
                      f"ratkaisu on leikkauspisteen x-koordinaatti x = {v}.")
            valid = [f"{m1}x + {b1} = {m2}x + {b2}", f"{m1}x - {m2}x = {b2} - {b1}"]
            invalid = [(f"{b1}x + {m1} = {b2}x + {m2}", TID), (f"{m1}x + {b1} = {b2}x + {m2}", TID),
                       (f"{m1}x + {m2} = {b1}x + {b2}", None)]
            steps = ["Leikkauspisteessä y-arvot ovat yhtä suuret", f"{m1}x + {b1} = {m2}x + {b2}", f"x = {v}"]
            params = {"m1": m1, "b1": b1, "m2": m2, "b2": b2}
        else:
            level = "H"
            y0 = b + m * v
            prompt = (f"Suoran pisteiden taulukossa x = 0, 1, 2 ja y = {b}, {b + m}, {b + 2 * m}. Suoran piste on "
                      f"korkeudella y = {y0}. Valitse kaikki yhtälöt, joiden ratkaisu on pisteen x-koordinaatti x = {v}.")
            valid = [f"{b} + {m}x = {y0}", f"{m}x = {y0 - b}"]
            invalid = [(f"{m} + {b}x = {y0}", TID), (f"{b + m}x = {y0}", None), (f"{b}x = {y0}", None)]
            steps = [f"Kun x = 0, y = {b}, ja x:n kasvaessa yhdellä y kasvaa {m}", f"y = {b} + {m}x",
                     f"{b} + {m}x = {y0}, joten x = {v}"]
            params = {"m": m, "b": b, "v": v}
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", v, valid, invalid)
        final = "; ".join(pretty(e) for e in valid)
        items.append(base_item(TID, CODE, start + k, ["S4.05"], ["T15"], 8, level, prompt, payload, steps, final,
                               GOOD, TEMPLATE, params | {"form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
