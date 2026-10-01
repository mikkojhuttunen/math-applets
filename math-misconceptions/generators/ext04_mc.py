#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type MC. The solutions of every equation are found by brute force over an
integer window; the tagged distractor lists only the positive root."""
import random

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "ext04_mc"
TID, CODE = "EXT-04", "MC"
BAD = ("Yhtälöllä x² = a on kaksi ratkaisua, kun a > 0, koska myös vastaluvun neliö on a. "
       "Tarkista sijoittamalla: negatiivinen luku toteuttaa yhtälön.")
GOOD = "Oikein: neliö ei erota lukua ja sen vastalukua, joten ratkaisuja on kaksi: positiivinen ja negatiivinen juuri."


def roots(p, q):
    """Integer solutions of p x² + q = 0 by brute force."""
    return [x for x in range(-60, 61) if p * x * x + q == 0]


def both(a):
    return f"x = {a} tai x = {num(-a)}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1401)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a = rng.choice([4, 6, 7, 9])
            p, q, level = 1, -a * a, "T"
            prompt = f"Ratkaise yhtälö x² = {a * a}."
        elif k == 1:
            a = rng.choice([5, 8, 11, 12])
            p, q, level = 1, -a * a, "T"
            prompt = f"Ratkaise yhtälö x² − {a * a} = 0."
        elif k == 2:
            a, p = rng.choice([(5, 2), (4, 3), (3, 4)])
            q, level = -p * a * a, "T"
            prompt = f"Ratkaise yhtälö {p}x² = {p * a * a}."
        elif k == 3:
            a, p = rng.choice([(4, 3), (3, 5), (2, 7)])
            q, level = -p * a * a, "H"
            prompt = f"Ratkaise yhtälö {p}x² − {p * a * a} = 0."
        else:
            a = rng.choice([5, 6, 8])
            p, q, level = 1, -a * a, "H"
        r = roots(p, q)
        assert r == [-a, a]
        sol = both(a)
        if k == 4:
            prompt = (f"Oppilas ratkaisi yhtälön x² = {a * a} ja sai vastaukseksi x = {a}. "
                      "Mikä perustelu osoittaa, että ratkaisu on puutteellinen?")
            correct = (f"Myös x = {num(-a)} toteuttaa yhtälön, koska ({num(-a)})² = {a * a}", GOOD)
            wrongs = [(f"Ratkaisu on täydellinen, koska luvun {a * a} neliöjuuri on {a}", TID, BAD),
                      (f"Ratkaisu on väärä, koska x = {a * a}", None, f"Luku {a * a} on x², ei x. Tarkista sijoittamalla."),
                      (f"Ratkaisu on väärä, koska {a}² ei ole {a * a}", None, f"{a}² = {a * a}, joten x = {a} on ratkaisu. Puuttuu vain toinen ratkaisu.")]
            steps = [f"({num(-a)})² = {a * a}", f"Ratkaisut: {sol}"]
        else:
            correct = (sol, GOOD)
            wrongs = [(f"x = {a}", TID, BAD),
                      (f"x = {a * a}" if p == 1 else f"x = {p * a * a}", None,
                       "Tämä on luku x², ei x. Ota neliöjuuri."),
                      (f"x = {num(-a)}", None, "Myös positiivinen luku toteuttaa yhtälön.")]
            steps = ([f"{p}x² = {p * a * a}", f"x² = {a * a}"] if p != 1 else [f"x² = {a * a}"]) + \
                    [f"x = {a} tai x = {num(-a)}, koska {a}² = ({num(-a)})² = {a * a}"]
        key = (k, a, p)
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, sol, GOOD, TEMPLATE,
                               {"a": a, "p": p, "q": q}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
