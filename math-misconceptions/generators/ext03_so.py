#!/usr/bin/env python3
"""EXT-03 (inequality sign not reversed when multiplying or dividing by a negative number), type SO (step
ordering). Every line has the same solution set as line 1 (checked by verify.py); the sign is reversed in the
last step. Lines are listed in the correct order and shuffled by the app."""
import random

from gen_common import MINUS, base_item, cli, lin, num

TEMPLATE = "ext03_so"
TID, CODE = "EXT-03", "SO"
FLIP = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
ASK = "Järjestä rivit oikeaan järjestykseen niin, että epäyhtälö ratkeaa vaihe vaiheelta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1304)
    items, seen = [], set()
    for k in range(count):
        ctx, var = "", "x"
        if k == 0:
            a, r, q, rel = 2, -3, 5, ">"
            lines = [f"{q} {MINUS} {a}x {rel} {num(q - a * r)}", f"{q} {MINUS} {a}x {MINUS} {q} {rel} {num(q - a * r)} {MINUS} {q}",
                     f"{MINUS}{a}x {rel} {num(-a * r)}", f"x {FLIP[rel]} {num(r)}"]
            expl = f"Vähennetään {q} molemmilta puolilta ja jaetaan luvulla {num(-a)}; merkki kääntyy."
            level, params = "T", {"a": a, "r": r, "q": q}
        elif k == 1:
            a, r, q, rel = 3, 4, 2, "≤"
            lines = [f"{q} {MINUS} {a}x {rel} {num(q - a * r)}", f"{MINUS}{a}x {rel} {num(-a * r)}", f"x {FLIP[rel]} {num(r)}"]
            expl = f"Vähennetään {q} molemmilta puolilta ja jaetaan luvulla {num(-a)}; merkki kääntyy."
            level, params = "T", {"a": a, "r": r, "q": q}
        elif k == 2:
            a, r, rel = 4, 2, ">"
            var = "t"
            ctx = f"Vesisäiliössä on 20 litraa vettä, ja siitä valuu {a} litraa minuutissa. Milloin vettä on alle {20 - a * r} litraa? "
            lines = [f"20 {MINUS} {a}t < {20 - a * r}", f"{MINUS}{a}t < {num(-a * r)}", f"t > {r}"]
            expl = f"Vähennetään 20 molemmilta puolilta ja jaetaan luvulla {num(-a)}; merkki kääntyy."
            level, params = "T", {"a": a, "r": r}
        elif k == 3:
            p1, p2, q1, r, rel = 1, 4, 2, 3, ">"
            q2 = q1 + (p1 - p2) * r
            lines = [f"{lin(p1, q1)} {rel} {lin(p2, q2)}", f"x {MINUS} {p2}x {rel} {num(q2 - q1)}",
                     f"{num(p1 - p2)}x {rel} {num(q2 - q1)}", f"x {FLIP[rel]} {num(r)}"]
            expl = f"Siirretään x-termit vasemmalle ja vakiot oikealle, sievennetään ja jaetaan luvulla {num(p1 - p2)}; merkki kääntyy."
            level, params = "H", {"p1": p1, "p2": p2, "q1": q1, "r": r}
        else:
            a, b, r, rel = 2, 3, 2, "≥"
            d = -a * r - a * b
            lines = [f"{MINUS}{a}(x + {b}) {rel} {num(d)}", f"{MINUS}{a}x {MINUS} {a * b} {rel} {num(d)}",
                     f"{MINUS}{a}x {rel} {num(d + a * b)}", f"x {FLIP[rel]} {num(r)}"]
            expl = f"Avataan sulut, siirretään vakio oikealle ja jaetaan luvulla {num(-a)}; merkki kääntyy."
            level, params = "H", {"a": a, "b": b, "r": r}
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        payload = {"lines": lines, "accept": "exact"}
        items.append(base_item(TID, CODE, start + k, ["S3.07"], ["T14"], 9, level, ctx + ASK, payload,
                               [expl, f"Ratkaisu: {lines[-1]}"], lines[-1],
                               "Oikein: negatiivisella luvulla jaettaessa epäyhtälömerkin suunta kääntyy.",
                               TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
