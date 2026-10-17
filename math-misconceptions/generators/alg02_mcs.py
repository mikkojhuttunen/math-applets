#!/usr/bin/env python3
"""ALG-02 (different letters must differ in value), type MC select-all (a reverse problem).
The second letter is described in words; the pupil ticks every equation for x whose solution is the value shared
by both letters. Correct and wrong equations come from the same numbers; wrong ones give x a value different
from the other letter."""
import random

from gen_common import MINUS, base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "alg02_mcs"
TID, CODE = "ALG-02", "MC"


def make_items(run, date, count=5, start=1):
    rng = random.Random(302)
    items = []
    used = set()
    for k in range(count):
        while True:
            p = rng.randint(3, 9)
            c = rng.randint(2, 6)
            if p not in used:
                used.add(p)
                break
        if k == 0:
            level = "T"
            prompt = (f"Kaksoset ovat yhtä vanhoja. Toisen ikä on {p} vuotta, ja toisen ikää merkitään x:llä. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {p}.")
            valid = [f"x = {p}", f"x + {c} = {p} + {c}", f"2x = {2 * p}"]
            invalid = [(f"x = {p + 1}", TID), (f"x + 1 = {p}", TID), (f"x {MINUS} 1 = {p}", TID)]
            steps = [f"x = y = {p}", f"x + {c} = {p} + {c}"]
        elif k == 1:
            level = "T"
            prompt = (f"Kolikoilla x ja y on sama arvo. Kolikon y arvo on {p} senttiä. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {p}.")
            valid = [f"x + {c} = {p + c}", f"{p} = x", f"3x = {3 * p}"]
            invalid = [(f"x + {c} = {p}", TID), (f"x = {p + c}", TID), (f"2x = {p}", None)]
            steps = [f"x = y = {p}", f"x + {c} = {p} + {c} = {p + c}"]
        elif k == 2:
            level = "T"
            prompt = f"Luvut x ja y ovat yhtä suuret, ja y = {p}. Valitse kaikki yhtälöt, joiden ratkaisu on x = {p}."
            valid = [f"x + {p} = {2 * p}", f"{2 * p} = x + {p}"]
            invalid = [(f"x + {p + 1} = {2 * p}", TID), (f"x + {p - 1} = {2 * p}", TID), (f"x + {2 * p} = {2 * p}", None)]
            steps = [f"x = y = {p}", f"Sijoita x = {p}: {p} + {p} = {2 * p}, joten x + {p} = {2 * p} kelpaa"]
        elif k == 3:
            level = "H"
            prompt = (f"Luvuille x ja y pätee x + y = {2 * p} ja x = y. Valitse kaikki yhtälöt, joissa on vain tuntematon x "
                      f"ja joiden ratkaisu on x = {p}.")
            valid = [f"2x = {2 * p}", f"x + x = {2 * p}", f"x = {2 * p} {MINUS} x"]
            invalid = [(f"x + 1 = {2 * p}", TID), (f"x = {2 * p}", TID), (f"3x = {2 * p}", None)]
            steps = [f"x + y = {2 * p}, y = x", f"x + x = {2 * p}", f"2x = {2 * p}, x = {p}"]
        else:
            level = "H"
            prompt = f"Luvut x ja y ovat yhtä suuret, ja y = {p}. Valitse kaikki yhtälöt, joiden ratkaisu on x = {p}."
            valid = [f"3x {MINUS} {p} = {2 * p}", f"{2 * p} = 3x {MINUS} {p}"]
            invalid = [(f"3x {MINUS} {p + 1} = {2 * p}", TID), (f"3x {MINUS} {2 * p} = {2 * p}", None),
                       (f"3x {MINUS} {c + p} = {2 * p}", TID)]
            steps = [f"x = y = {p}", f"Sijoita x = {p}: 3 · {p} {MINUS} {p} = {2 * p}, joten 3x {MINUS} {p} = {2 * p} kelpaa"]
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", p, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15"], 7, level, prompt, payload, steps,
                               "; ".join(pretty(v) for v in valid), "x ja y saavat olla sama luku, ja yhtälö toteutuu arvolla x = " + str(p) + ".",
                               TEMPLATE, {"p": p, "c": c, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
