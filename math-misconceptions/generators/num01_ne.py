#!/usr/bin/env python3
"""NUM-01 (longer decimal is larger), type NE (number entry). Answers computed from Decimal values."""
import random
from decimal import Decimal

from gen_common import base_item, cli
from gen_decimal import CTX, CTX3, digits, fmt, hundredths, tenths

TEMPLATE = "num01_ne"
TID, CODE = "NUM-01", "NE"
BAD = ("Desimaaliluvun numeroita ei lueta kokonaislukuna. Muuta luvut samoiksi paikka-arvoiksi "
       "(esimerkiksi 0,6 = 0,60) ja vertaa.")


def pair(rng, whole):
    """(short, long): the longer decimal is numerically smaller."""
    while True:
        d = rng.randint(3, 9)
        n = rng.randint(11, 10 * d - 1)
        if n % 10:
            return tenths(whole, d), hundredths(whole, n)


def make_items(run, date, count=5, start=1):
    rng = random.Random(402)
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
            ans, wrong, key = short, [long_], (short, long_)
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{fmt(short)}0 > {fmt(long_)}"]
        elif k == 2:
            whole = rng.randint(1, 3)
            short, long_ = pair(rng, whole)
            mid = tenths(whole, 1)
            long3 = long_ + Decimal("0.001") * rng.randint(1, 9)
            assert long3 < short
            vals = [short, long_, long3]
            rng.shuffle(vals)
            intro, q, unit = CTX3[0]
            prompt = intro.format(a=fmt(vals[0]), b=fmt(vals[1]), c=fmt(vals[2])) + f" {q} Kirjoita luku ({unit})."
            ans, wrong, key = short, [long3, long_], tuple(sorted(vals))
            steps = [", ".join(fmt(x) for x in sorted(vals)) + " (pienimmästä suurimpaan)"]
        elif k == 3:
            short, _ = pair(rng, 0)
            prompt = f"Montako sadasosaa luvussa {fmt(short)} on? Kirjoita luku."
            ans, wrong, key = int(short * 100), [int(short * 10)], (short, "h")
            steps = [f"{fmt(short)} = {fmt(short)}0", f"{fmt(short)}0 on {ans} sadasosaa"]
        else:
            while True:
                lst = [hundredths(0, rng.randint(11, 99)) for _ in range(3)] + [tenths(0, rng.randint(3, 9))]
                lst = [x for x in lst if x % Decimal("0.1") or digits(x) == 1]
                thr = Decimal("0.5")
                if len(lst) == 4 and len(set(lst)) == 4 and thr not in lst:
                    ans = sum(1 for x in lst if x > thr)
                    trap = sum(1 for x in lst if digits(x) == 2)  # longer string read as larger
                    if 0 < ans < 4 and trap != ans:
                        break
            rng.shuffle(lst)
            prompt = f"Montako luvuista {', '.join(fmt(x) for x in lst)} on suurempia kuin 0,5? Kirjoita lukumäärä."
            wrong, key = [trap], tuple(sorted(lst))
            steps = [f"{fmt(x)} {'>' if x > thr else '<'} 0,5" for x in lst]
        assert all(w != ans for w in wrong) and key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "NUM-01", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        final = fmt(ans) if isinstance(ans, Decimal) else str(ans)
        items.append(base_item(TID, CODE, start + k, ["S2.06", "S2.08"], tt, 7, level, prompt, payload, steps, final,
                               "Oikein: desimaaliluvut vertaillaan paikka-arvoittain.", TEMPLATE,
                               {"key": [str(x) for x in (key if isinstance(key, tuple) else [key])]}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
