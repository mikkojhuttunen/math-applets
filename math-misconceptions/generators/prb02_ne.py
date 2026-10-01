#!/usr/bin/env python3
"""PRB-02 (more black marbles means higher chance), type NE. Answers come from Fraction arithmetic;
the typical wrong answer is the count (or the other jar's value) that the count-over-proportion belief gives."""
import random
from fractions import Fraction

from gen_common import base_item, cli

TEMPLATE = "prb02_ne"
TID, CODE = "PRB-02", "NE"
BAD = ("Todennäköisyys ei riipu pelkästä mustien kuulien lukumäärästä vaan niiden osuudesta kaikista kuulista.")


def pct(f):
    v = f * 100
    assert v.denominator == 1
    return int(v)


def make_items(run, date, count=5, start=1):
    rng = random.Random(904)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            while True:
                b1, b2 = rng.choice([8, 10, 20, 25]), rng.choice([4, 5, 10])
                a1, a2 = rng.randint(2, b1 - 1), rng.randint(1, b2 - 1)
                if a1 > a2 and Fraction(a1, b1) < Fraction(a2, b2):
                    break
            ans, wrong = 2, [1]
            prompt = (f"Purkissa 1 on {a1} mustaa kuulaa {b1}:stä. Purkissa 2 on {a2} mustaa kuulaa {b2}:sta. "
                      "Kummasta purkista on parempi mahdollisuus nostaa musta kuula? Kirjoita purkin numero.")
            steps = [f"{a1}/{b1} = {float(Fraction(a1, b1)):.3f}".replace(".", ","), f"{a2}/{b2} = {float(Fraction(a2, b2)):.3f}".replace(".", ","), "Purkin 2 osuus on suurempi"]
            params = {"a1": a1, "b1": b1, "a2": a2, "b2": b2}
        elif k == 1:
            b = rng.choice([8, 20, 25, 50])
            a = rng.choice([x for x in range(3, b) if (Fraction(x, b) * 100).denominator == 1])
            ans, wrong = pct(Fraction(a, b)), [a]
            prompt = (f"Purkissa on {a} mustaa kuulaa {b}:stä. Kuinka monta prosenttia on todennäköisyys nostaa musta kuula?")
            steps = [f"{a}/{b} = {ans} %"]
            params = {"a": a, "b": b}
        elif k == 2:
            b, d = rng.choice([(12, 8), (20, 10), (15, 10)])
            a = rng.choice([x for x in range(2, b) if (Fraction(x * d, b)).denominator == 1 and x * d // b < d])
            ans, wrong = a * d // b, [a]
            prompt = (f"Purkissa 1 on {a} mustaa kuulaa {b}:stä. Purkissa 2 on {d} kuulaa. "
                      "Montako mustaa kuulaa purkissa 2 pitää olla, jotta mustan nostamisen todennäköisyys on sama kuin purkissa 1?")
            steps = [f"{a}/{b} = x/{d}", f"x = {a} · {d} / {b} = {ans}"]
            params = {"a": a, "b": b, "d": d}
        elif k == 3:
            while True:
                b1, b2 = rng.choice([10, 20, 25, 40]), rng.choice([4, 5, 8, 10])
                a1, a2 = rng.randint(3, b1 - 1), rng.randint(1, b2 - 1)
                p1, p2 = Fraction(a1, b1), Fraction(a2, b2)
                if a1 > a2 and p1 < p2 and (p1 * 100).denominator == 1 and (p2 * 100).denominator == 1:
                    break
            ans, wrong = pct(p2), [pct(p1)]
            prompt = (f"Purkissa 1 on {a1} mustaa kuulaa {b1}:stä ja purkissa 2 on {a2} mustaa kuulaa {b2}:sta. "
                      "Kuinka monta prosenttia on todennäköisyys nostaa musta kuula siitä purkista, josta mahdollisuus on parempi?")
            steps = [f"Purkki 1: {a1}/{b1} = {pct(p1)} %", f"Purkki 2: {a2}/{b2} = {pct(p2)} %", f"Parempi on purkki 2: {ans} %"]
            params = {"a1": a1, "b1": b1, "a2": a2, "b2": b2, "higher_pct": True}
        else:
            a, b, add = rng.choice([(2, 8, 2), (3, 12, 3), (6, 20, 5)])
            assert (a + add) * 100 % (b + add) == 0
            ans = (a + add) * 100 // (b + add)
            wrong = [a + add]
            prompt = (f"Pussissa on {a} punaista kuulaa {b}:stä. Pussiin lisätään {add} punaista kuulaa, "
                      "valkoisia ei lisätä. Kuinka monta prosenttia on nyt todennäköisyys nostaa punainen kuula?")
            steps = [f"Punaisia {a + add}, kuulia yhteensä {b + add}", f"{a + add}/{b + add} = {ans} %"]
            params = {"a": a, "b": b, "add": add}
        assert all(w != ans for w in wrong)
        key = str(params)
        assert key not in seen
        seen.add(key)
        payload = {"answer": {"kind": "number", "value": float(ans)},
                   "wrong": [{"match": float(w), "misconception": "PRB-02", "feedback": BAD} for w in wrong],
                   "input_hint": "Kirjoita luku"}
        items.append(base_item(TID, CODE, start + k, ["S6.06", "S2.02"], ["T11", "T19"], 9, "T" if k < 3 else "H", prompt,
                               payload, steps, str(ans), "Oikein: todennäköisyys on suotuisten tulosten osuus kaikista tuloksista.",
                               TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
