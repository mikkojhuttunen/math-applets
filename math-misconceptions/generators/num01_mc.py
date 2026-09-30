#!/usr/bin/env python3
"""NUM-01 (longer decimal is larger), type MC. Options come from the same Decimal values; answer by comparison."""
import random

from decimal import Decimal

from gen_common import base_item, cli, mc_options
from gen_decimal import CTX, CTX4, dec, digits, fmt, hundredths, tenths

TEMPLATE = "num01_mc"
TID, CODE = "NUM-01", "MC"
BAD = ("Desimaaliluvun numeroita ei lueta kokonaislukuna. Vertaa samoja paikka-arvoja: "
       "muuta luvut esimerkiksi sadasosiksi (0,6 = 0,60).")
SAME = "Luvuilla on eri arvot. Kirjoita lyhyempi luku samalla desimaalimäärällä (0,6 = 0,60) ja vertaa."
UNSURE = "Luvut voi aina vertailla, esimerkiksi muuttamalla ne samoiksi paikka-arvoiksi."


def pair(rng, whole):
    """(short, long) with the longer decimal numerically SMALLER."""
    while True:
        d = rng.randint(3, 9)
        n = rng.randint(11, 10 * d - 1)
        if n % 10:
            return tenths(whole, d), hundredths(whole, n)


def make_items(run, date, count=5, start=1):
    rng = random.Random(401)
    items, seen = [], set()
    for k in range(count):
        if k < 3:
            level, whole = "T", (0 if k == 0 else rng.randint(1, 4))
            short, long_ = pair(rng, whole)
            a, b = (short, long_) if rng.random() < 0.5 else (long_, short)
            if k == 0:
                prompt = f"Kumpi luvuista on suurempi: {fmt(a)} vai {fmt(b)}?"
                unit = ""
            else:
                intro, q, unit = CTX[rng.randrange(len(CTX))]
                prompt = f"{intro.format(a=fmt(a), b=fmt(b))} {q}"
                unit = " " + unit
            assert long_ < short and digits(long_) > digits(short)
            correct = (f"{fmt(short)}{unit}", f"Oikein: {fmt(short)} = {fmt(short)}0 ja sadasosina {fmt(short)}0 > {fmt(long_)}.")
            wrongs = [(f"{fmt(long_)}{unit}", "NUM-01", BAD), ("Luvut ovat yhtä suuret" if not unit else "Ne ovat yhtä suuret", None, SAME),
                      ("Sitä ei voi päätellä", None, UNSURE)]
            options, cid = mc_options(rng, correct, wrongs)
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{fmt(short)}0 > {fmt(long_)}"]
            params = {"short": fmt(short), "long": fmt(long_), "context": k}
            final = fmt(short)
            key = (short, long_)
        elif k == 3:
            level = "H"
            whole = rng.randint(1, 3)
            short, long_ = pair(rng, whole)
            while True:
                other = hundredths(whole, rng.randint(11, 99))
                t2 = tenths(whole, rng.randint(1, 9))
                if other % Decimal("0.1") and len({short, long_, other, t2}) == 4:
                    break
            vals = [short, long_, other, t2]
            big = max(vals)
            two = [x for x in vals if digits(x) == 2]
            trap = max(two, key=lambda x: int(x * 100) % 100)  # longest digit string after the comma
            assert trap != big
            intro, q, unit = CTX4[1]
            ordered = vals[:]
            rng.shuffle(ordered)
            prompt = intro.format(a=fmt(ordered[0]), b=fmt(ordered[1]), c=fmt(ordered[2]), d=fmt(ordered[3])) + " " + q
            rest = [x for x in vals if x not in (big, trap)]
            correct = (f"{fmt(big)} {unit}", f"Oikein: {fmt(big)} on suurin, kun luvut vertaillaan samoilla paikka-arvoilla.")
            wrongs = [(f"{fmt(trap)} {unit}", "NUM-01", BAD)] + [
                (f"{fmt(x)} {unit}", None, "Vertaa ensin kokonaisosia ja sitten desimaaleja.") for x in rest]
            options, cid = mc_options(rng, correct, wrongs)
            steps = [", ".join(fmt(x) for x in sorted(vals)) + " (pienimmästä suurimpaan)"]
            params = {"values": [fmt(x) for x in vals], "context": 1}
            final = fmt(big)
            key = tuple(sorted(vals))
        else:
            level = "H"
            whole = 0
            short, long_ = pair(rng, whole)
            while (short, long_) in seen:
                short, long_ = pair(rng, whole)
            prompt = (f"Kumpi luku on suurempi, {fmt(short)} vai {fmt(long_)}? Valitse oikea perustelu.")
            correct = (f"{fmt(short)} = {fmt(short)}0 eli {int(short * 100)} sadasosaa, ja {int(short * 100)} > {int(long_ * 100)}",
                       "Oikein: luvut vertaillaan samoissa paikka-arvoissa.")
            wrongs = [(f"{fmt(long_)} on suurempi, koska {int(long_ * 100)} > {int(short * 10)}", "NUM-01", BAD),
                      (f"{fmt(short)} on suurempi, koska siinä on vähemmän numeroita", "NUM-02",
                       "Tulos on oikea, mutta perustelu ei ole: numeroiden määrä ei ratkaise. Muuta luvut samoiksi paikka-arvoiksi."),
                      (f"Luvut ovat yhtä suuret, koska molemmissa on nolla ja pilkku", None, SAME)]
            options, cid = mc_options(rng, correct, wrongs)
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{int(short * 100)} sadasosaa > {int(long_ * 100)} sadasosaa"]
            params = {"short": fmt(short), "long": fmt(long_), "justify": True}
            final = f"{fmt(short)} > {fmt(long_)}"
            key = (short, long_)
        assert key not in seen, "duplicate numbers"
        seen.add(key)
        tt = ["T11", "T12"]
        mis = ["NUM-01"] + (["NUM-02"] if k == 4 else [])
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S2.06", "S2.08"], tt, 7, level, prompt, payload, steps, final,
                               "Oikein: desimaaliluvut vertaillaan paikka-arvoittain.", TEMPLATE, params, date, run,
                               misconceptions=mis))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
