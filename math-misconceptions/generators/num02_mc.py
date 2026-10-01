#!/usr/bin/env python3
"""NUM-02 (shorter decimal is larger), type MC. Options come from the same Decimal values."""
import random
from decimal import Decimal

from gen_common import base_item, cli, mc_options
from gen_decimal import CTX, CTX4, digits, fmt, hundredths, tenths

TEMPLATE = "num02_mc"
TID, CODE = "NUM-02", "MC"
BAD = ("Sadasosat eivät ole suurempia kuin kymmenesosat, mutta luvussa on niitä lisäksi. "
       "Muuta luvut samoiksi paikka-arvoiksi (0,4 = 0,40) ja vertaa.")
SAME = "Luvuilla on eri arvot. Kirjoita lyhyempi luku samalla desimaalimäärällä (0,4 = 0,40) ja vertaa."
UNSURE = "Luvut voi aina vertailla, esimerkiksi muuttamalla ne samoiksi paikka-arvoiksi."


def pair(rng, whole):
    """(short, long): the longer decimal shares the tenths digit and is numerically LARGER."""
    while True:
        d = rng.randint(1, 8)
        n = 10 * d + rng.randint(1, 9)
        return tenths(whole, d), hundredths(whole, n)


def make_items(run, date, count=5, start=1):
    rng = random.Random(403)
    items, seen = [], set()
    for k in range(count):
        level, mis = ("T" if k < 3 else "H"), ["NUM-02"]
        if k < 3:
            whole = 0 if k == 0 else rng.randint(1, 4)
            short, long_ = pair(rng, whole)
            a, b = (short, long_) if rng.random() < 0.5 else (long_, short)
            if k == 0:
                prompt, unit = f"Kumpi luvuista on suurempi: {fmt(a)} vai {fmt(b)}?", ""
            else:
                intro, q, u = CTX[rng.randrange(len(CTX))]
                prompt, unit = f"{intro.format(a=fmt(a), b=fmt(b))} {q}", " " + u
            assert long_ > short and digits(long_) > digits(short)
            correct = (f"{fmt(long_)}{unit}", f"Oikein: {fmt(short)}0 < {fmt(long_)}, kun luvut vertaillaan sadasosina.")
            wrongs = [(f"{fmt(short)}{unit}", "NUM-02", BAD), ("Ne ovat yhtä suuret" if unit else "Luvut ovat yhtä suuret", None, SAME),
                      ("Sitä ei voi päätellä", None, UNSURE)]
            options, cid = mc_options(rng, correct, wrongs)
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{fmt(short)}0 < {fmt(long_)}"]
            params, final, key = {"short": fmt(short), "long": fmt(long_), "context": k}, fmt(long_), (short, long_)
        elif k == 3:
            whole = rng.randint(1, 3)
            short, long_ = pair(rng, whole)
            while True:
                lower = hundredths(whole, rng.randint(11, 99))
                t2 = tenths(whole, rng.randint(1, 9))
                if lower % Decimal("0.1") and len({short, long_, lower, t2}) == 4:
                    break
            vals = [short, long_, lower, t2]
            big = max(vals)
            # trap = the largest one-decimal number that is not the largest overall (shorter read as larger)
            shorts = [x for x in vals if digits(x) == 1 and x != big]
            trap = max(shorts)
            intro, q, unit = CTX4[1]
            order = vals[:]
            rng.shuffle(order)
            prompt = intro.format(a=fmt(order[0]), b=fmt(order[1]), c=fmt(order[2]), d=fmt(order[3])) + " " + q
            rest = [x for x in vals if x not in (big, trap)]
            correct = (f"{fmt(big)} {unit}", f"Oikein: {fmt(big)} on suurin, kun luvut vertaillaan samoilla paikka-arvoilla.")
            wrongs = [(f"{fmt(trap)} {unit}", "NUM-02", BAD)] + [
                (f"{fmt(x)} {unit}", None, "Vertaa ensin kokonaisosia ja sitten desimaaleja.") for x in rest]
            options, cid = mc_options(rng, correct, wrongs)
            steps = [", ".join(fmt(x) for x in sorted(vals)) + " (pienimmästä suurimpaan)"]
            params, final, key = {"values": [fmt(x) for x in vals], "context": 1}, fmt(big), tuple(sorted(vals))
        else:
            short, long_ = pair(rng, 0)
            prompt = f"Kumpi luku on suurempi, {fmt(short)} vai {fmt(long_)}? Valitse oikea perustelu."
            s100, l100 = int(short * 100), int(long_ * 100)
            correct = (f"{fmt(short)} = {fmt(short)}0 eli {s100} sadasosaa, ja {l100} > {s100}",
                       "Oikein: luvut vertaillaan samoissa paikka-arvoissa.")
            wrongs = [(f"{fmt(short)} on suurempi, koska kymmenesosa on suurempi kuin sadasosa", "NUM-02", BAD),
                      (f"{fmt(long_)} on suurempi, koska siinä on enemmän numeroita", "NUM-01",
                       "Tulos on oikea, mutta perustelu ei ole: numeroiden määrä ei ratkaise. Muuta luvut samoiksi paikka-arvoiksi."),
                      ("Luvut ovat yhtä suuret, koska ne alkavat samalla numerolla", None, SAME)]
            options, cid = mc_options(rng, correct, wrongs)
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{l100} sadasosaa > {s100} sadasosaa"]
            params, final, key = {"short": fmt(short), "long": fmt(long_), "justify": True}, f"{fmt(long_)} > {fmt(short)}", (short, long_, "j")
            mis = ["NUM-02", "NUM-01"]
        assert key not in seen, "duplicate numbers"
        seen.add(key)
        tt = ["T11", "T12"]
        items.append(base_item(TID, CODE, start + k, ["S2.06", "S2.08"], tt, 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: desimaaliluvut vertaillaan paikka-arvoittain.", TEMPLATE, params, date, run,
                               misconceptions=mis))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
