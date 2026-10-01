#!/usr/bin/env python3
"""ALG-02 (different letters must differ in value), type RP.
The second letter is described in words; the equation is written for x and its solution must equal the
value shared by both letters. Valid and invalid equations come from the same numbers."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg02_rp"
TID, CODE = "ALG-02", "RP"


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
            prompt = (f"Kaksoset ovat yhtä vanhoja. Toisen ikä on y = {p} vuotta, ja toisen ikää merkitään kirjaimella x. "
                      f"Kirjoita yhtälö, jonka ratkaisu on x = {p}.")
            valid = [f"x = {p}", f"x + {c} = {p} + {c}", f"2x = {2 * p}"]
            invalid = [f"x = {p + 1}", f"x + 1 = {p}", f"x {MINUS} 1 = {p}"]
            steps = [f"x = y = {p}", f"x + {c} = {p} + {c}"]
        elif k == 1:
            level = "T"
            prompt = (f"Kolikoilla x ja y on sama arvo. Kolikon y arvo on {p} senttiä. "
                      f"Kirjoita yhtälö, jossa x on tuntematon ja jonka ratkaisu on x = {p}.")
            valid = [f"x + {c} = {p + c}", f"{p} = x", f"3x = {3 * p}"]
            invalid = [f"x + {c} = {p}", f"x = {p + c}", f"2x = {p}"]
            steps = [f"x = y = {p}", f"x + {c} = {p} + {c} = {p + c}"]
        elif k == 2:
            level = "T"
            prompt = (f"Luvut x ja y ovat yhtä suuret, ja y = {p}. Täydennä yhtälö x + □ = {2 * p} siten, "
                      f"että sen ratkaisu on x = {p}. Kirjoita koko yhtälö.")
            valid = [f"x + {p} = {2 * p}", f"{2 * p} = x + {p}"]
            invalid = [f"x + {p + 1} = {2 * p}", f"x + {p - 1} = {2 * p}", f"x + {2 * p} = {2 * p}"]
            steps = [f"x = {p}", f"□ = {2 * p} {MINUS} {p} = {p}", f"x + {p} = {2 * p}"]
        elif k == 3:
            level = "H"
            prompt = (f"Luvuille x ja y pätee x + y = {2 * p} ja x = y. Kirjoita yhtälö pelkästään tuntemattomalle x siten, "
                      f"että sen ratkaisu on x = {p}.")
            valid = [f"2x = {2 * p}", f"x + x = {2 * p}", f"x = {2 * p} {MINUS} x"]
            invalid = [f"x + 1 = {2 * p}", f"x = {2 * p}", f"3x = {2 * p}"]
            steps = [f"x + y = {2 * p}, y = x", f"x + x = {2 * p}", f"2x = {2 * p}, x = {p}"]
        else:
            level = "H"
            prompt = (f"Luvut x ja y ovat yhtä suuret, ja y = {p}. Kirjoita yhtälö muotoa 3x {MINUS} □ = {2 * p}, "
                      f"jonka ratkaisu on x = {p}. Kirjoita koko yhtälö.")
            valid = [f"3x {MINUS} {p} = {2 * p}", f"{2 * p} = 3x {MINUS} {p}"]
            invalid = [f"3x {MINUS} {p + 1} = {2 * p}", f"3x {MINUS} {2 * p} = {2 * p}", f"3x {MINUS} {c + p} = {2 * p}"]
            steps = [f"3 · {p} = {3 * p}", f"□ = {3 * p} {MINUS} {2 * p} = {p}", f"3x {MINUS} {p} = {2 * p}"]
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": p},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15"], 7, level, prompt, payload, steps,
                               f"x = {p}", "Oikein: x ja y saavat olla sama luku, ja yhtälö toteutuu arvolla x = " + str(p) + ".",
                               TEMPLATE, {"p": p, "c": c, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
