#!/usr/bin/env python3
"""ALG-06 (operational reading of '='), type ES (error spotting). Lines are checked by verify.py:
the lines before the error line are equivalent to line 1, the error line is not."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg06_es"
TID, CODE = "ALG-06", "ES"
ASK = "Kirjaimella x on merkitty laatikon tilalle tuntematon luku. Missä rivissä on ensimmäinen virhe? Napauta riviä."


def make_items(run, date, count=5, start=1):
    rng = random.Random(203)
    items, seen = [], set()
    for k in range(count):
        while True:
            a, b, c, d = (rng.randint(3, 9) for _ in range(4))
            if len({a, b, c}) == 3 and a > b and a + b > c + 1 and a - b > d and (a, b, c) not in seen:
                break
        seen.add((a, b, c))
        s = a + b
        if k == 0:
            level, form, etype = "T", "sum_left", "ignores_right_side"
            lines = [f"{a} + {b} = x + {c}", f"{s} = x + {c}", f"x = {s}"]
            err, good = 3, s - c
        elif k == 1:
            level, form, etype = "T", "box_left", "ignores_right_side"
            lines = [f"x + {c} = {a} + {b}", f"x + {c} = {s}", f"x = {s}"]
            err, good = 3, s - c
        elif k == 2:
            level, form, etype = "T", "box_last", "adds_instead_of_balancing"
            lines = [f"{a} + {b} = {c} + x", f"{s} = {c} + x", f"x = {s} + {c}"]
            err, good = 3, s - c
        elif k == 3:
            m = a - b
            level, form, etype = "H", "minus", "ignores_right_side"
            lines = [f"{a} {MINUS} {b} = x + {d}", f"{m} = x + {d}", f"{m} {MINUS} {d} = x", f"x = {m}"]
            err, good = 4, m - d
        else:
            level, form, etype = "H", "balance", "adds_instead_of_balancing"
            lines = [f"{a} + {b} = {c} + x", f"{s} = {c} + x", f"{s} {MINUS} {c} = x", f"x = {s} + {c}"]
            err, good = 4, s - c
        if k < 3:
            ctx = ""
        elif k == 3:
            ctx = ""
        else:
            ctx = f"Vaa'an vasemmassa kupissa on {a} kg:n ja {b} kg:n painot, oikeassa {c} kg:n paino ja painolla x. "
        prompt = f"{ctx}Oppilas ratkaisee yhtälön rivi riviltä. {ASK}"
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        steps = [f"Rivi {err - 1} on oikein: molempien puolten arvojen on oltava yhtä suuret.",
                 f"Oikea ratkaisu: x = {s if k != 3 else a - b} {MINUS} {c if k != 3 else d} = {good}"]
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, prompt, payload, steps,
                               f"Virhe on rivillä {err}",
                               "Oikein: yhtäsuuruusmerkki tarkoittaa, että molemmat puolet ovat yhtä suuret.", TEMPLATE,
                               {"a": a, "b": b, "c": c, "d": d, "form": form}, date, run,
                               generic_wrong="Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? "
                                             "Yhtäsuuruusmerkki ei tarkoita 'tulos tulee seuraavaksi'."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
