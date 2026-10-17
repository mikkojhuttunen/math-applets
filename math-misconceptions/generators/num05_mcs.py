#!/usr/bin/env python3
"""NUM-05 (division always makes smaller), type MC select-all (a reverse problem). The pupil ticks every equation
whose solution is the result of a division by a number below 1 (or the divisor itself). Correct equations divide by
that number (written as an exact fraction, which the prompt names) or multiply back; wrong ones are built from the
same numbers and multiply instead, subtract, or arrange the division so that the result is smaller, as a pupil does
who thinks division always makes smaller. verify.py checks the solution sets."""
import random
from decimal import Decimal
from fractions import Fraction

from gen_common import base_item, cli
from gen_select import pretty, select_all

TEMPLATE = "num05_mcs"
TID, CODE = "NUM-05", "MC"
GOOD = "Kun jaetaan luvulla, joka on pienempi kuin 1, osamäärä on suurempi kuin jaettava."


def c(x):
    """Decimal comma display text."""
    return str(x).replace(".", ",")


def d(x):
    """Decimal with a decimal comma; the checker reads it as an exact fraction."""
    f = Fraction(str(x))
    return str(Decimal(f.numerator) / Decimal(f.denominator)).replace(".", ",")



def whole(f):
    return int(f) if f.denominator == 1 else float(f)


def make_items(run, date, count=5, start=1):
    rng = random.Random(714)
    items, seen = [], set()
    for k in range(count):
        while True:
            p = rng.choice([0.5, 0.25, 0.2, 0.4])
            q = rng.choice([3, 6, 9, 12, 15])
            if (p, q) not in seen and (Fraction(q) / Fraction(str(p))).denominator == 1:
                break
        seen.add((p, q))
        fp = Fraction(str(p))
        v = q / fp
        if k == 0:
            level = "T"
            prompt = (f"Luku {q} jaetaan luvulla {c(p)}. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on osamäärä x = {int(v)}.")
            valid = [f"x = {q} / {d(p)}", f"{d(p)} * x = {q}"]
            invalid = [(f"x = {q} * {d(p)}", TID), (f"x = {q} - {d(p)}", None), (f"x = {q} / {d(1 + fp)}", None)]
            steps = [f"{q} ÷ {c(p)} = {int(v)}", f"x = {q} ÷ {c(p)}"]
            value = int(v)
        elif k == 1:
            level = "T"
            prompt = (f"Nauhaa on {q} metriä, ja siitä leikataan {c(p)} metrin pituisia pätkiä. Pätkien lukumäärä on x. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {int(v)}.")
            valid = [f"x = {q} / {d(p)}", f"{d(p)} * x = {q}"]
            invalid = [(f"x = {q} * {d(p)}", TID), (f"x = {q}", None), (f"x = {q} - {d(p)}", None)]
            steps = [f"Pätkien määrä = nauhan pituus ÷ pätkän pituus = {q} ÷ {c(p)}", f"x = {int(v)}"]
            value = int(v)
        elif k == 2:
            level = "T"
            r = int(v)
            prompt = (f"Luku {q} jaetaan luvulla x, ja osamäärä on {r}. Valitse kaikki yhtälöt, jotka kuvaavat "
                      f"tilannetta ja joiden ratkaisu on x = {c(p)}.")
            valid = [f"{q} / x = {r}", f"x = {q} / {r}"]
            invalid = [(f"{q} * x = {r}", TID), (f"x = {r} / {q}", TID), (f"x = {q} * {r}", None)]
            steps = [f"Osamäärä {r} on suurempi kuin {q}, joten jakajan täytyy olla alle 1", f"{q} ÷ x = {r}", f"x = {q} ÷ {r} = {c(p)}"]
            value = float(fp)
        elif k == 3:
            level = "H"
            v2 = v / fp
            prompt = (f"Luku {q} jaetaan ensin luvulla {c(p)} ja saatu osamäärä jaetaan vielä luvulla {c(p)}. "
                      f"Lopputulos on x. Valitse kaikki yhtälöt, joiden ratkaisu on x = {c(whole(v2))}.")
            valid = [f"x = {q} / {d(p)} / {d(p)}", f"x = ({q} / {d(p)}) / {d(p)}"]
            invalid = [(f"x = {q} * {d(p)} * {d(p)}", TID), (f"x = {q} / {d(p)}", None),
                       (f"x = {q} - {d(p)} - {d(p)}", None)]
            steps = [f"{q} ÷ {c(p)} = {c(whole(v))}", f"{c(whole(v))} ÷ {c(p)} = {c(whole(v2))}",
                     f"x = {q} ÷ {c(p)} ÷ {c(p)}"]
            value = whole(v2)
        else:
            level = "H"
            n = rng.choice([2, 3, 4, 5])
            prompt = (f"Pizzoja on {q} kappaletta, ja jokainen annos on 1/{n} pizzasta. Annosten lukumäärä on x. "
                      f"Valitse kaikki yhtälöt, joiden ratkaisu on x = {q * n}.")
            valid = [f"x = {q} / (1/{n})", f"x = {q} * {n}"]
            invalid = [(f"x = {q} / {n}", TID), (f"x = {q} * (1/{n})", TID), (f"x = {q}", None)]
            steps = [f"1/{n} < 1, joten annoksia on enemmän kuin {q}", f"x = {q} ÷ 1/{n} = {q * n}"]
            value = q * n
            p = Fraction(1, n)
        payload = select_all(f"{TEMPLATE}-{start + k}", "x", value, valid, invalid)
        items.append(base_item(TID, CODE, start + k, ["S2.03", "S2.06"], ["T11"], 7, level, prompt, payload, steps,
                               "; ".join(pretty(e) for e in valid), GOOD, TEMPLATE, {"p": str(p), "q": q, "form": k}, date, run,
                               generic_wrong="Tarkista sijoittamalla: jakolasku luvulla, joka on alle 1, antaa suuremman luvun kuin jaettava."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
