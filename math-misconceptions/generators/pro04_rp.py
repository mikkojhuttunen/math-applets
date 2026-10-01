#!/usr/bin/env python3
"""PRO-04 (larger perimeter means larger area), type RP. The wanted side x makes two shapes equal in area although
the second has the larger perimeter; the invalid equations equate the perimeters. verify.py checks solution sets."""
import random

from gen_common import base_item, cli

TEMPLATE = "pro04_rp"
TID, CODE = "PRO-04", "RP"
GENERIC = "Pidempi piiri ei tarkoita suurempaa alaa. Ala on pituus · leveys; sijoita x ja laske molempien alat."
GOOD = "Oikein: alat ovat yhtä suuret, kun pituus · leveys on sama, vaikka piirit eroavat."
MINUS = chr(8722)


def pick(rng, seen):
    """a x b rectangle and a divisor c of its area with c > max(a, b), so the second rectangle has the larger perimeter."""
    while True:
        a, b = rng.randint(3, 9), rng.randint(3, 9)
        if a == b:
            continue
        area = a * b
        cs = [c for c in range(max(a, b) + 1, area) if area % c == 0]
        if cs and (a, b) not in seen:
            seen.add((a, b))
            c = rng.choice(cs)
            return a, b, c, area // c


def make_items(run, date, count=5, start=1):
    rng = random.Random(8441)
    items, seen = [], set()
    for k in range(count):
        level = "T"
        if k < 4:
            a, b, c, x = pick(rng, seen)
            if k == 0:
                prompt = (f"Suorakulmion A sivut ovat {a} cm ja {b} cm. Suorakulmion B yksi sivu on {c} cm. "
                          f"Kirjoita yhtälö, jonka ratkaisu x = {x} on B:n toinen sivu (cm), kun suorakulmioiden alat ovat yhtä suuret.")
            elif k == 1:
                prompt = (f"Matto on {a} m pitkä ja {b} m leveä. Toinen matto on {c} m pitkä. Kirjoita yhtälö, "
                          f"jonka ratkaisu x = {x} on toisen maton leveys (m), kun matoilla on sama pinta-ala.")
            elif k == 2:
                prompt = (f"Pelto on {a} m · {b} m. Toisen pellon yksi sivu on {c} m, ja pellot ovat yhtä suuret. "
                          f"Kirjoita yhtälö, jonka ratkaisu x = {x} on toisen pellon toinen sivu (m).")
            else:
                level = "H"
                prompt = (f"Suorakulmion A sivut ovat {a} cm ja {b} cm. Suorakulmion B sivu on {c} cm, ja B:n piiri on suurempi kuin A:n piiri. "
                          f"Silti suorakulmioiden alat ovat yhtä suuret. Kirjoita yhtälö, jonka ratkaisu x = {x} on B:n toinen sivu (cm).")
            valid = [f"{c} * x = {a} * {b}", f"x = {a * b} / {c}"]
            invalid = [f"{c} + x = {a} + {b}", f"x = {b}", f"2 * ({c} + x) = 2 * ({a} + {b})"]
            steps = [f"A:n ala {a} · {b} = {a * b} cm²", f"B:n ala {c} · x = {a * b}", f"x = {a * b} / {c} = {x}"]
            params = {"a": a, "b": b, "c": c}
            ordering = f"B:n piiri {2 * (c + x)} on suurempi kuin A:n piiri {2 * (a + b)}, mutta alat ovat samat"
            steps.append(ordering)
        else:
            level = "H"
            while True:
                s = rng.randint(4, 9)
                divs = [d for d in range(2, s) if (s * s) % d == 0 and (s * s) // d != s]
                if divs:
                    break
            a = rng.choice(divs)
            x = s * s // a
            prompt = (f"Neliön sivu on {s} cm. Suorakulmion yksi sivu on {a} cm, ja sen ala on yhtä suuri kuin neliön ala. "
                      f"Kirjoita yhtälö, jonka ratkaisu x = {x} on suorakulmion toinen sivu (cm).")
            valid = [f"{a} * x = {s} * {s}", f"x = {s * s} / {a}"]
            invalid = [f"2 * ({a} + x) = {4 * s}", f"x = {s}", f"{a} + x = {2 * s}"]
            steps = [f"Neliön ala {s}² = {s * s} cm²", f"{a} · x = {s * s}", f"x = {x}",
                     f"Suorakulmion piiri {2 * (a + x)} cm on suurempi kuin neliön piiri {4 * s} cm, mutta alat ovat samat"]
            params = {"s": s, "a": a}
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": x},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt, payload, steps, f"x = {x}",
                               GOOD, TEMPLATE, dict(params, form=k), date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
