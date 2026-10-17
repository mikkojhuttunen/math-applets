#!/usr/bin/env python3
"""PRO-04 (larger perimeter means larger area), type MC select-all (a reverse problem).
The wanted side x makes two shapes equal in area although the second has the larger perimeter. The pupil ticks every
equation whose solution is that x: correct equations equate the areas; wrong ones equate the perimeters or
half-perimeters (the misconception: equal areas would need equal perimeters) or reuse a given side."""
import random

from gen_common import base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "pro04_mcs"
TID, CODE = "PRO-04", "MC"
GENERIC = "Pidempi piiri ei tarkoita suurempaa alaa. Ala on pituus · leveys; sijoita x ja laske molempien alat."
GOOD = "Alat ovat yhtä suuret, kun pituus · leveys on sama, vaikka piirit eroavat."
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
                prompt = (f"Suorakulmion A sivut ovat {a} cm ja {b} cm. Suorakulmion B sivut ovat {c} cm ja x cm, "
                          f"ja suorakulmioiden alat ovat yhtä suuret. Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            elif k == 1:
                prompt = (f"Matto on {a} m pitkä ja {b} m leveä. Toinen matto on {c} m pitkä ja x m leveä, ja matoilla on sama pinta-ala. "
                          f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            elif k == 2:
                prompt = (f"Pelto on {a} m · {b} m. Toisen pellon sivut ovat {c} m ja x m, ja pellot ovat yhtä suuret. "
                          f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            else:
                level = "H"
                prompt = (f"Suorakulmion A sivut ovat {a} cm ja {b} cm. Suorakulmion B sivut ovat {c} cm ja x cm, ja B:n piiri on suurempi kuin A:n piiri. "
                          f"Silti suorakulmioiden alat ovat yhtä suuret. Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            valid = [f"{c} * x = {a} * {b}", f"x = {a * b} / {c}"]
            invalid = [(f"{c} + x = {a} + {b}", TID), (f"x = {b}", None), (f"2 * ({c} + x) = 2 * ({a} + {b})", TID)]
            unit = "cm" if k in (0, 3) else "m"
            first, second, other = {1: ("Ensimmäisen maton", "Toisen maton", "ensimmäisen maton"),
                                    2: ("Ensimmäisen pellon", "Toisen pellon", "ensimmäisen pellon")}.get(k, ("A:n", "B:n", "A:n"))
            steps = [f"{first} ala {a} · {b} = {a * b} {unit}²", f"{second} ala {c} · x = {a * b}", f"x = {a * b} / {c} = {x}"]
            params = {"a": a, "b": b, "c": c}
            ordering = (f"{second} piiri {2 * (c + x)} {unit} on suurempi kuin {other} piiri {2 * (a + b)} {unit}, "
                        f"mutta alat ovat samat")
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
            prompt = (f"Neliön sivu on {s} cm. Suorakulmion sivut ovat {a} cm ja x cm, ja sen ala on yhtä suuri kuin neliön ala. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            valid = [f"{a} * x = {s} * {s}", f"x = {s * s} / {a}"]
            invalid = [(f"2 * ({a} + x) = {4 * s}", TID), (f"x = {s}", None), (f"{a} + x = {2 * s}", TID)]
            steps = [f"Neliön ala {s}² = {s * s} cm²", f"{a} · x = {s * s}", f"x = {x}",
                     f"Suorakulmion piiri {2 * (a + x)} cm on suurempi kuin neliön piiri {4 * s} cm, mutta alat ovat samat"]
            params = {"s": s, "a": a}
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", x, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S5.07"], ["T18"], 7, level, prompt, payload, steps,
                               "; ".join(pretty(v) for v in valid),
                               GOOD, TEMPLATE, dict(params, form=k), date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
