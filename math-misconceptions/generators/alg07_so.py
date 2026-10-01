#!/usr/bin/env python3
"""ALG-07 (sign errors and one-sided operations), type SO (step ordering). Every line is equivalent to line 1
(solution set unchanged); the lines are listed in the correct order and shuffled by the app."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg07_so"
TID, CODE = "ALG-07", "SO"
ASK = "Järjestä rivit oikeaan järjestykseen niin, että yhtälö ratkeaa vaihe vaiheelta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(8202)
    items = []
    for k in range(count):
        a, b, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 9)
        ctx = ""
        if k == 0:
            level, c = "T", a * x + b
            lines = [f"{a}x + {b} = {c}", f"{a}x + {b} {MINUS} {b} = {c} {MINUS} {b}", f"{a}x = {c - b}", f"x = {x}"]
            expl = f"Vähennetään {b} molemmilta puolilta ja jaetaan luvulla {a}."
        elif k == 1:
            level, c = "T", a * x - b
            lines = [f"{a}x {MINUS} {b} = {c}", f"{a}x {MINUS} {b} + {b} = {c} + {b}", f"{a}x = {c + b}", f"x = {x}"]
            expl = f"Lisätään {b} molemmille puolille ja jaetaan luvulla {a}."
        elif k == 2:
            level, c = "T", b + a * x
            lines = [f"{b} + {a}x = {c}", f"{a}x = {c} {MINUS} {b}", f"{a}x = {c - b}", f"x = {x}"]
            expl = f"Vähennetään {b} molemmilta puolilta ja jaetaan luvulla {a}."
        elif k == 3:
            level = "H"
            a = max(a, 4)
            e = rng.randint(2, a - 1)
            d = b + (a - e) * x
            lines = [f"{a}x + {b} = {e}x + {d}", f"{a}x {MINUS} {e}x + {b} = {d}", f"{a}x {MINUS} {e}x = {d} {MINUS} {b}",
                     f"{a - e}x = {d - b}", f"x = {x}"]
            expl = f"Vähennetään {e}x ja {b} molemmilta puolilta, sievennetään ja jaetaan luvulla {a - e}."
        else:
            level, c = "H", a * x + b
            ctx = (f"Mökin vuokra on {b} euroa kiinteää maksua ja {a} euroa vuorokaudelta. Vuokra oli yhteensä {c} euroa, "
                   f"ja vuorokausien määrä x ratkaistaan yhtälöstä. ")
            lines = [f"{a}x + {b} = {c}", f"{a}x + {b} {MINUS} {b} = {c} {MINUS} {b}", f"{a}x = {c - b}", f"x = {x}"]
            expl = f"Vähennetään kiinteä maksu {b} molemmilta puolilta ja jaetaan luvulla {a}."
        payload = {"lines": lines, "accept": "exact"}
        items.append(base_item(TID, CODE, start + k, ["S3.05"], ["T14"], 7, level, ctx + ASK, payload,
                               [expl, f"Ratkaisu: x = {x}"], f"x = {x}",
                               "Oikein: jokainen toimitus tehdään yhtälön molemmille puolille, joten yhtälö pysyy tosi.",
                               TEMPLATE, {"a": a, "b": b, "x": x}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
