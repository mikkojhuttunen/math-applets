#!/usr/bin/env python3
"""NUM-03 (whole-number bias in fraction addition), type NE. The answer is an integer numerator or denominator computed with Fraction."""
import random
from fractions import Fraction
from math import lcm

from gen_common import base_item, cli

TEMPLATE = "num03_ne"
TID, CODE = "NUM-03", "NE"
BAD = "Osoittajat ja nimittäjät eivät lasku erikseen yhteen. Muuta murtoluvut samannimisiksi ja laske vain osoittajat yhteen."
DENS = [(2, 3), (3, 4), (2, 5), (3, 5), (4, 6), (3, 6), (2, 4)]


def unlike(rng, n=2):
    while True:
        ds = rng.sample([2, 3, 4, 5, 6, 8, 12], n)
        ns = [rng.randint(1, d - 1) for d in ds]
        L = lcm(*ds)
        naive = sum(ns)
        correct = sum(x * (L // d) for x, d in zip(ns, ds))
        if correct != naive and all(L % d == 0 for d in ds) and L <= 24 and all(x < d for x, d in zip(ns, ds)):
            return ds, ns, L, correct, naive


def make_items(run, date, count=5, start=1):
    rng = random.Random(502)
    items, seen = [], set()
    for k in range(count):
        level = "T" if k < 3 else "H"
        if k == 0:
            d = rng.choice([8, 10, 12])
            a, c = rng.sample(range(1, d // 2), 2)
            prompt = f"Laske {a}/{d} + {c}/{d}. Kirjoita summan nimittäjä."
            ans, wrong, key = d, [2 * d], (a, c, d)
            steps = [f"{a}/{d} + {c}/{d} = {a + c}/{d}", f"Nimittäjä on {d}"]
            params = {"a": a, "c": c, "d": d}
        elif k in (1, 2):
            ds, ns, L, ans, naive = unlike(rng)
            wrong = [naive]
            if k == 1:
                prompt = f"{ns[0]}/{ds[0]} + {ns[1]}/{ds[1]} = ?/{L}. Kirjoita puuttuva osoittaja."
            else:
                prompt = (f"Maljakkoon kaadetaan {ns[0]}/{ds[0]} l ja sen jälkeen {ns[1]}/{ds[1]} l vettä. "
                          f"Vettä on yhteensä ?/{L} litraa. Kirjoita puuttuva osoittaja.")
            steps = [f"{ns[0]}/{ds[0]} = {ns[0] * (L // ds[0])}/{L}, {ns[1]}/{ds[1]} = {ns[1] * (L // ds[1])}/{L}",
                     f"{ns[0] * (L // ds[0])} + {ns[1] * (L // ds[1])} = {ans}"]
            key, params = (tuple(ds), tuple(ns)), {"denominators": ds, "numerators": ns, "common": L}
        elif k == 3:
            while True:
                ds, ns, L, ans, naive = unlike(rng, 3)
                if L <= 24 and ans == L:
                    break
            prompt = (f"Laske {ns[0]}/{ds[0]} + {ns[1]}/{ds[1]} + {ns[2]}/{ds[2]}. "
                      f"Kuinka monta kokonaista summa on? Kirjoita luku.")
            ans, wrong = 1, [0]
            key = (tuple(ds), tuple(ns), "w")
            steps = [", ".join(f"{n}/{d} = {n * (L // d)}/{L}" for n, d in zip(ns, ds)),
                     f"Yhteensä {L}/{L} = 1"]
            params = {"denominators": ds, "numerators": ns, "common": L}
        else:
            ds, ns, L, ans, naive = unlike(rng, 3)
            prompt = (f"{ns[0]}/{ds[0]} + {ns[1]}/{ds[1]} + {ns[2]}/{ds[2]} = ?/{L}. Kirjoita puuttuva osoittaja.")
            wrong = [naive]
            key = (tuple(ds), tuple(ns), "t")
            steps = [", ".join(f"{n}/{d} = {n * (L // d)}/{L}" for n, d in zip(ns, ds)),
                     " + ".join(str(n * (L // d)) for n, d in zip(ns, ds)) + f" = {ans}"]
            params = {"denominators": ds, "numerators": ns, "common": L}
        assert key not in seen and all(w != ans for w in wrong)
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": ans},
                   "wrong": [{"match": w, "misconception": "NUM-03", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + k, ["S2.02"], ["T11"], 7, "T" if k < 3 else "H", prompt, payload,
                               steps, str(ans), "Oikein: samannimisillä murtoluvuilla lasketaan vain osoittajat yhteen.",
                               TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
