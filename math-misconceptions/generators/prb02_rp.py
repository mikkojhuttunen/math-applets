#!/usr/bin/env python3
"""PRB-02 (more black marbles means higher chance), type RP. Valid and invalid equations are built from the same
numbers with exact integers and fractions; verify.py checks their solution sets. Invalid equations follow the
count-over-proportion belief (the count itself, or the count added to the total)."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "prb02_rp"
TID, CODE = "PRB-02", "RP"
GOOD = "Oikein: todennäköisyys on suotuisten tulosten osuus kaikista tuloksista."
GENERIC = "Tarkista sijoittamalla: todennäköisyys on mustien kuulien osuus kaikista kuulista, ei pelkkä mustien kuulien lukumäärä."


def c(x):
    """Decimal comma display text."""
    return str(x).replace(".", ",")


def make_items(run, date, count=5, start=1):
    rng = random.Random(931)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            while True:
                b, d = rng.choice([(12, 8), (20, 10), (15, 10), (25, 10)])
                a = rng.randint(2, b - 1)
                if (a * d) % b == 0 and a * d // b < d and a * d // b != a and (a, b, d) not in seen:
                    break
            seen.add((a, b, d))
            v = a * d // b
            level = "T"
            prompt = (f"Purkissa 1 on {a} mustaa kuulaa {b}:stä. Purkissa 2 on {d} kuulaa, joista x on mustia. "
                      f"Kirjoita yhtälö, jonka ratkaisu on x = {v}, kun mustan nostamisen todennäköisyys on molemmissa purkeissa sama.")
            valid = [f"x / {d} = {a} / {b}", f"x = {a} * {d} / {b}"]
            invalid = [f"x = {a}", f"x / {b} = {a} / {d}", f"x = {a} + {d} - {b}"]
            steps = [f"Todennäköisyys purkissa 1 on {a}/{b}", f"Purkissa 2 on x/{d}", f"x/{d} = {a}/{b}", f"x = {v}"]
            value, params = v, {"a": a, "b": b, "d": d}
        elif k == 1:
            b = rng.choice([8, 20, 25, 50])
            a = rng.choice([x for x in range(3, b) if (Fraction(x, b) * 100).denominator == 1 and (b, x) not in seen])
            seen.add((b, a))
            value = int(Fraction(a, b) * 100)
            level = "T"
            prompt = (f"Purkissa on {a} mustaa kuulaa {b}:stä. Kirjoita yhtälö, jossa x on mustan kuulan nostamisen "
                      f"todennäköisyys prosentteina ja jonka ratkaisu on x = {value}.")
            valid = [f"x = {a} / {b} * 100", f"x / 100 = {a} / {b}"]
            invalid = [f"x = {a}", f"x = {b} / {a} * 100", f"x = {a} / 100"]
            steps = [f"Mustien osuus kaikista kuulista on {a}/{b}", f"x = {a}/{b} · 100 = {value}"]
            params = {"a": a, "b": b, "percent": True}
        elif k == 2:
            a, w = rng.choice([(1, 3), (2, 3), (3, 7), (1, 4), (3, 2)])
            if (a, w) in seen:
                a, w = 1, 3
            seen.add((a, w))
            p = Fraction(a, a + w)
            value = float(p)
            assert Fraction(str(value)) == p
            level = "T"
            prompt = (f"Pussissa on {a} mustaa ja {w} valkoista kuulaa. Kirjoita yhtälö, jossa x on mustan kuulan "
                      f"nostamisen todennäköisyys desimaalilukuna ja jonka ratkaisu on x = {c(value)}.")
            valid = [f"x = {a} / ({a} + {w})", f"x * ({a} + {w}) = {a}"]
            invalid = [f"x = {a} / {w}", f"x = {a}", f"x = {w} / ({a} + {w})"]
            steps = [f"Kuulia on yhteensä {a} + {w} = {a + w}", f"x = {a}/{a + w} = {c(value)}"]
            params = {"black": a, "white": w}
        elif k == 3:
            a, b, add = rng.choice([(1, 4, 1), (3, 7, 3), (2, 8, 2), (4, 16, 4)])
            if (a, b, add) in seen:
                a, b, add = 1, 4, 1
            seen.add((a, b, add))
            value = (a + add) * 100 // (b + add)
            assert (a + add) * 100 % (b + add) == 0
            level = "H"
            prompt = (f"Pussissa on {a} mustaa kuulaa {b}:stä. Pussiin lisätään {add} mustaa kuulaa. Kirjoita yhtälö, "
                      f"jossa x on mustan kuulan nostamisen todennäköisyys prosentteina lisäyksen jälkeen ja jonka ratkaisu on x = {value}.")
            valid = [f"x = ({a} + {add}) / ({b} + {add}) * 100", f"x / 100 = ({a} + {add}) / ({b} + {add})"]
            invalid = [f"x = {a} + {add}", f"x = ({a} + {add}) / {b} * 100", f"x = {a} / ({b} + {add}) * 100"]
            steps = [f"Mustia on {a + add} ja kuulia yhteensä {b + add}", f"x = {a + add}/{b + add} · 100 = {value}"]
            params = {"a": a, "b": b, "add": add}
        else:
            while True:
                b1, b2 = rng.choice([10, 20, 25]), rng.choice([4, 5, 10])
                a1, a2 = rng.randint(3, b1 - 1), rng.randint(1, b2 - 1)
                p1, p2 = Fraction(a1, b1), Fraction(a2, b2)
                if a1 > a2 and p1 < p2 and (p1 * 100).denominator == 1 and (p2 * 100).denominator == 1 \
                        and (a1, b1, a2, b2) not in seen:
                    break
            seen.add((a1, b1, a2, b2))
            value = int((p2 - p1) * 100)
            level = "H"
            prompt = (f"Purkissa 1 on {a1} mustaa kuulaa {b1}:stä ja purkissa 2 on {a2} mustaa kuulaa {b2}:sta. Kirjoita yhtälö, "
                      f"jossa x on purkin 2 mustan todennäköisyyden ja purkin 1 mustan todennäköisyyden erotus prosenttiyksikköinä "
                      f"ja jonka ratkaisu on x = {value}.")
            valid = [f"x = {a2} / {b2} * 100 - {a1} / {b1} * 100", f"x = ({a2} / {b2} - {a1} / {b1}) * 100"]
            invalid = [f"x = {a2} - {a1}", f"x = {a1} / {b1} * 100 - {a2} / {b2} * 100", f"x = {a1} - {a2}"]
            steps = [f"Purkki 1: {a1}/{b1} = {int(p1 * 100)} %", f"Purkki 2: {a2}/{b2} = {int(p2 * 100)} %",
                     f"x = {int(p2 * 100)} − {int(p1 * 100)} = {value}"]
            params = {"a1": a1, "b1": b1, "a2": a2, "b2": b2}
        payload = {"constraint": {"type": "solution_equals", "variable": "x", "value": value},
                   "checks": {"valid": valid, "invalid": invalid}}
        final = f"x = {c(value)}".replace("-", "−")
        items.append(base_item(TID, CODE, start + k, ["S6.06", "S2.02"], ["T11", "T19"], 9, level, prompt, payload,
                               steps, final, GOOD, TEMPLATE, params, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
