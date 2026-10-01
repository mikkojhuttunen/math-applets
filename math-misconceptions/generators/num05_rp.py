#!/usr/bin/env python3
"""NUM-05 (division always makes smaller), type RP. Valid and invalid equations are built from the same numbers
with exact fractions; verify.py checks their solution sets."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "num05_rp"
TID, CODE = "NUM-05", "RP"
GOOD = "Oikein: kun jaetaan luvulla, joka on pienempi kuin 1, osamäärä on suurempi kuin jaettava."


def c(x):
    """Decimal comma display text."""
    return str(x).replace(".", ",")


def d(x):
    """Exact fraction text, so the checker compares rationals (no floats)."""
    f = Fraction(str(x))
    return f"({f.numerator}/{f.denominator})"


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
            prompt = f"Luku {q} jaetaan luvulla {c(p)}. Kirjoita yhtälö, jonka ratkaisu on x = {int(v)}."
            valid = [f"x = {q} / {d(p)}", f"{d(p)} * x = {q}"]
            invalid = [f"x = {q} * {d(p)}", f"x = {q} - {d(p)}", f"x = {q} / {d(1 + fp)}"]
            steps = [f"{q} ÷ {c(p)} = {int(v)}", f"x = {q} ÷ {c(p)}"]
            value = int(v)
        elif k == 1:
            level = "T"
            prompt = (f"Nauhaa on {q} metriä, ja siitä leikataan {c(p)} metrin pituisia pätkiä. Kirjoita yhtälö, "
                      f"jossa x on pätkien lukumäärä ja jonka ratkaisu on x = {int(v)}.")
            valid = [f"x = {q} / {d(p)}", f"{d(p)} * x = {q}"]
            invalid = [f"x = {q} * {d(p)}", f"x = {q}", f"x = {q} - {d(p)}"]
            steps = [f"Pätkien määrä = nauhan pituus ÷ pätkän pituus = {q} ÷ {c(p)}", f"x = {int(v)}"]
            value = int(v)
        elif k == 2:
            level = "T"
            r = int(v)
            prompt = (f"Luku {q} jaetaan tuntemattomalla luvulla x, ja osamäärä on {r}. Kirjoita yhtälö, "
                      f"jonka ratkaisu on x = {c(p)}.")
            valid = [f"{q} / x = {r}", f"x = {q} / {r}"]
            invalid = [f"{q} * x = {r}", f"x = {r} / {q}", f"x = {q} * {r}"]
            steps = [f"Osamäärä {r} on suurempi kuin {q}, joten jakajan täytyy olla alle 1", f"{q} ÷ x = {r}", f"x = {q} ÷ {r} = {c(p)}"]
            value = float(fp)
        elif k == 3:
            level = "H"
            prompt = (f"Luku {q} jaetaan ensin luvulla {c(p)} ja saatu osamäärä jaetaan vielä luvulla {c(p)}. "
                      f"Kirjoita yhtälö, jossa x on lopputulos.")
            v2 = v / fp
            valid = [f"x = {q} / {d(p)} / {d(p)}", f"x = ({q} / {d(p)}) / {d(p)}"]
            invalid = [f"x = {q} / {d(p)}", f"x = {q} * {d(p)} * {d(p)}", f"x = {q} - {d(p)} - {d(p)}"]
            steps = [f"{q} ÷ {c(p)} = {c(whole(v))}", f"{c(whole(v))} ÷ {c(p)} = {c(whole(v2))}",
                     f"x = {q} ÷ {c(p)} ÷ {c(p)}"]
            value = whole(v2)
        else:
            level = "H"
            n = rng.choice([2, 3, 4, 5])
            prompt = (f"Pizzaa on {q} kappaletta ja jokainen annos on 1/{n} pizzasta. Kirjoita yhtälö, "
                      f"jossa x on annosten lukumäärä ja jonka ratkaisu on x = {q * n}.")
            valid = [f"x = {q} / (1/{n})", f"x = {q} * {n}"]
            invalid = [f"x = {q} / {n}", f"x = {q} * (1/{n})", f"x = {q}"]
            steps = [f"1/{n} < 1, joten annoksia on enemmän kuin {q}", f"x = {q} ÷ 1/{n} = {q * n}"]
            value = q * n
            p = Fraction(1, n)
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        items.append(base_item(TID, CODE, start + k, ["S2.03", "S2.06"], ["T11"], 7, level, prompt, payload, steps,
                               f"x = {c(value)}", GOOD, TEMPLATE, {"p": str(p), "q": q, "form": k}, date, run,
                               generic_wrong="Tarkista sijoittamalla: jakolasku luvulla, joka on alle 1, antaa suuremman luvun kuin jaettava."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
