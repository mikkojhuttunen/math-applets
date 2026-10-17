#!/usr/bin/env python3
"""EXT-08 (mean taken as the "typical value"; median read from unsorted data), type MC select-all (a reverse
problem). The unknown x is a missing value of a list; the pupil ticks every equation whose solution is that value.
Correct equations express the mean or the median condition; wrong ones take the mean or median (or the middle of the
unsorted list) as the missing value itself, average the old mean with the new value, or use a wrong divisor.
The solution x is computed by code; verify.py checks the solution sets."""
import random

from ext08_common import written_middle
from gen_common import base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "ext08_mcs"
TID, CODE = "EXT-08", "MC"
GOOD = "Keskiarvo on kaikkien lukujen summa jaettuna lukujen määrällä; mediaani on järjestetyn listan keskikohta."
GENERIC = ("Sijoita yhtälöön pyydetty x ja tarkista, tuleeko keskiarvoksi tai mediaaniksi annettu luku. "
           "Keskiarvo ei ole yksittäinen puuttuva arvo, vaan kaikkien lukujen summa jaettuna lukujen määrällä.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1814)
    items = []
    for k in range(count):
        level = "T"
        if k in (0, 2):
            n = (5, 4)[k // 2]
            while True:
                vals = rng.sample(range(3, 30), n - 1)
                m = rng.randint(max(vals) - 3, max(vals) + 6)
                x = n * m - sum(vals)
                if 1 <= x <= 40 and x != m:
                    break
            s = " + ".join(str(v) for v in vals)
            ctx = ("Viiden oppilaan koepisteistä neljä on" if k == 0 else "Neljän ostoksen hinnoista kolme on")
            unit = "" if k == 0 else " euroa"
            last = "viides" if k == 0 else "neljäs"
            noun = "Pisteiden" if k == 0 else "Hintojen"
            what = "pistemäärä" if k == 0 else "hinta"
            listed = ", ".join(str(v) for v in vals[:-1]) + f" ja {vals[-1]}"
            prompt = (f"{ctx} {listed}{unit}, ja {last} on x{unit}. {noun} keskiarvo on {m}{unit}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on oikea {what} x = {x}.")
            valid = [f"({s} + x) / {n} = {m}", f"{s} + x = {n * m}"]
            invalid = [("x = " + str(m), TID), (f"({s} + x) / {n + 1} = {m}", None), (f"x / {n} = {m}", None)]
            steps = [f"Keskiarvo = summa / {n}", f"({s} + x) / {n} = {m}", f"x = {n * m} {chr(8722)} {sum(vals)} = {x}"]
            params = {"values": vals, "mean": m}
        elif k == 1:
            while True:
                p = rng.randint(4, 25)
                m = rng.randint(p + 2, p + 12)
                x = 2 * m - p
                if x != m and x > p:
                    break
            prompt = (f"Kuuden luvun lista on järjestetty pienimmästä suurimpaan, ja kaksi keskimmäistä lukua ovat {p} ja x. "
                      f"Listan mediaani on {m}. Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            valid = [f"({p} + x) / 2 = {m}", f"{p} + x = {2 * m}"]
            invalid = [(f"x = {m}", TID), (f"x / 2 = {m}", None), (f"{p} + x = {m}", None)]
            steps = ["Mediaani on kahden keskimmäisen keskiarvo", f"({p} + x) / 2 = {m}", f"x = {2 * m} {chr(8722)} {p} = {x}"]
            params = {"p": p, "median": m}
        elif k == 3:
            level = "H"
            while True:
                n = rng.choice([4, 5])
                m0 = rng.randint(6, 15)
                m1 = m0 + rng.randint(1, 3)
                x = (n + 1) * m1 - n * m0
                if x > 0 and x != m1:
                    break
            prompt = (f"{n} mittauksen keskiarvo on {m0}. Kun listaan lisätään yksi uusi mittaus x, keskiarvoksi tulee {m1}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            valid = [f"({n} * {m0} + x) / {n + 1} = {m1}", f"{n} * {m0} + x = {(n + 1) * m1}"]
            invalid = [(f"x = {m1}", TID), (f"({m0} + x) / 2 = {m1}", TID), (f"({n} * {m0} + x) / {n} = {m1}", None)]
            steps = [f"Vanhojen summa on {n} · {m0} = {n * m0}", f"({n * m0} + x) / {n + 1} = {m1}",
                     f"x = {(n + 1) * m1} {chr(8722)} {n * m0} = {x}"]
            params = {"n": n, "old_mean": m0, "new_mean": m1}
        else:
            level = "H"
            while True:
                vals = rng.sample(range(2, 25), 5)
                if sum(vals) % 5 == 0:
                    break
            x = sum(vals) // 5
            s = " + ".join(str(v) for v in vals)
            prompt = (f"Lukujen {', '.join(str(v) for v in vals)} ja x keskiarvo on x. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {x}.")
            middle = written_middle(vals)
            assert middle.denominator == 1 and middle != x
            valid = [f"({s} + x) / 6 = x", f"{s} + x = 6x"]
            invalid = [(f"x = {middle}", TID), (f"x = {sum(vals)} / 6", None), (f"({s}) / 5 = x / 5", None),
                       (f"({s} + x) / 5 = x", None)]
            steps = ["Keskiarvo on x, joten summa on 6x", f"{s} + x = 6x", f"5x = {sum(vals)}, joten x = {x}"]
            params = {"values": vals}
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", x, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S6.02", "S6.03"], ["T19"], 7, level, prompt, payload, steps,
                               "; ".join(pretty(v) for v in valid), GOOD, TEMPLATE, params | {"form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
