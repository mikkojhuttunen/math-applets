#!/usr/bin/env python3
"""NUM-02 (shorter decimal is larger), type NE (number entry). Answers computed from Decimal values."""
import random
from decimal import Decimal

from gen_common import base_item, cli
from gen_decimal import CTX, CTX3, digits, fmt, hundredths, tenths

TEMPLATE = "num02_ne"
TID, CODE = "NUM-02", "NE"
BAD = ("Sadasosat eivät ole suurempia kuin kymmenesosat, mutta luvussa on niitä lisäksi. "
       "Muuta luvut samoiksi paikka-arvoiksi (0,4 = 0,40) ja vertaa.")


def pair(rng, whole):
    """(short, long): the longer decimal shares the tenths digit and is numerically larger."""
    d = rng.randint(1, 8)
    return tenths(whole, d), hundredths(whole, 10 * d + rng.randint(1, 9))


def make_items(run, date, count=5, start=1):
    rng = random.Random(404)
    items, seen = [], set()
    for k in range(count):
        level, tt = ("T" if k < 3 else "H"), ["T11", "T12"]
        if k in (0, 1):
            whole = 0 if k == 0 else rng.randint(1, 4)
            short, long_ = pair(rng, whole)
            a, b = (short, long_) if rng.random() < 0.5 else (long_, short)
            if k == 0:
                prompt = f"Kirjoita suurempi luvuista {fmt(a)} ja {fmt(b)}."
            else:
                intro, q, unit = CTX[rng.randrange(len(CTX))]
                prompt = f"{intro.format(a=fmt(a), b=fmt(b))} {q} Kirjoita suurempi luku ({unit})."
            ans, wrong, key = long_, [short], (short, long_)
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{fmt(short)}0 < {fmt(long_)}"]
        elif k == 2:
            whole = rng.randint(1, 3)
            short, long_ = pair(rng, whole)
            long3 = short + Decimal("0.001") * rng.randint(1, 9)  # three decimals, between short and long_
            assert short < long3 < long_
            vals = [short, long_, long3]
            rng.shuffle(vals)
            intro, q, unit = CTX3[0]
            prompt = intro.format(a=fmt(vals[0]), b=fmt(vals[1]), c=fmt(vals[2])) + f" {q} Kirjoita luku ({unit})."
            ans, wrong, key = long_, [short], tuple(sorted(vals))
            steps = [", ".join(fmt(x) for x in sorted(vals)) + " (pienimmästä suurimpaan)"]
        elif k == 3:
            whole = rng.randint(1, 3)
            short, long_ = pair(rng, whole)
            prompt = (f"Luvuista {fmt(short)} ja {fmt(long_)} suurempi on x. "
                      f"Montako sadasosaa x:ssä on? Kirjoita luku.")
            ans, wrong, key = int(long_ * 100), [int(short * 100)], (short, long_, "h")
            steps = [f"{fmt(short)}0 < {fmt(long_)}, joten x = {fmt(long_)}", f"{fmt(long_)} on {ans} sadasosaa"]
        else:
            while True:
                d = rng.randint(2, 7)
                lst = [tenths(0, d), hundredths(0, 10 * d + rng.randint(1, 9)), hundredths(0, 10 * (d - 1) + rng.randint(1, 9)),
                       tenths(0, d + 1)]
                if len(set(lst)) == 4:
                    break
            thr = tenths(0, d)
            ans = sum(1 for x in lst if x > thr)
            trap = sum(1 for x in lst if x > thr and digits(x) == 1)  # only the shorter numbers counted as larger
            assert trap != ans
            rng.shuffle(lst)
            prompt = f"Montako luvuista {', '.join(fmt(x) for x in lst)} on suurempia kuin {fmt(thr)}? Kirjoita lukumäärä."
            wrong, key = [trap], tuple(sorted(lst))
            steps = [f"{fmt(x)} {'>' if x > thr else '<'} {fmt(thr)}" for x in lst]
        assert all(w != ans for w in wrong) and key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "NUM-02", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        final = fmt(ans) if isinstance(ans, Decimal) else str(ans)
        items.append(base_item(TID, CODE, start + k, ["S2.06", "S2.08"], tt, 7, level, prompt, payload, steps, final,
                               "Oikein: desimaaliluvut vertaillaan paikka-arvoittain.", TEMPLATE,
                               {"key": [str(x) for x in key]}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
