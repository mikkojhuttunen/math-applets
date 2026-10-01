#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type SO (step ordering). Every line is an expression
equivalent to line 1 (checked by verify.py); lines are listed in the correct order and shuffled by the app."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg08_so"
TID, CODE = "ALG-08", "SO"
ASK = "Järjestä rivit oikeaan järjestykseen niin, että lauseke sievenee vaihe vaiheelta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(8303)
    items = []
    for k in range(count):
        a, b, c, d = rng.randint(2, 7), rng.randint(2, 8), rng.randint(2, 6), rng.randint(2, 6)
        ctx = ""
        if k == 0:
            level = "T"
            lines = [f"{a}(x + {b}) + {c}x", f"{a}x + {a * b} + {c}x", f"{a}x + {c}x + {a * b}", f"{a + c}x + {a * b}"]
            expl = f"Kerrotaan sulku luvulla {a}, järjestetään x-termit vierekkäin ja lasketaan ne yhteen."
        elif k == 1:
            level = "T"
            cc = rng.randint(a * b + 1, a * b + 9)
            lines = [f"{a}(x {MINUS} {b}) + {cc}", f"{a}x {MINUS} {a * b} + {cc}", f"{a}x + {cc - a * b}"]
            expl = f"Kerrotaan sulku luvulla {a} ja lasketaan luvut yhteen: {MINUS}{a * b} + {cc} = {cc - a * b}."
        elif k == 2:
            level = "T"
            lines = [f"{a}(x + {b}) + {c}(x + {d})", f"{a}x + {a * b} + {c}(x + {d})",
                     f"{a}x + {a * b} + {c}x + {c * d}", f"{a + c}x + {a * b + c * d}"]
            expl = f"Avataan ensin ensimmäinen sulku, sitten toinen, ja lopuksi lasketaan samanmuotoiset termit yhteen."
        elif k == 3:
            level = "H"
            m = rng.randint(2, 4)
            dd = rng.randint(1, a * m - 1)
            lines = [f"{a}({m}x + {b}) {MINUS} {dd}x", f"{a * m}x + {a * b} {MINUS} {dd}x",
                     f"{a * m}x {MINUS} {dd}x + {a * b}", f"{a * m - dd}x + {a * b}"]
            expl = f"Kerroin {a} kertoo molemmat termit: {a * m}x ja {a * b}. Sitten x-termit lasketaan yhteen."
        else:
            level = "H"
            cc = rng.randint(2, 9)
            ctx = (f"Siivousyritys veloittaa {a} euroa tunnilta. Työ kestää x + {b} tuntia, ja lisäksi veloitetaan "
                   f"{cc} euron kulkumaksu. ")
            lines = [f"{a}(x + {b}) + {cc}", f"{a}x + {a * b} + {cc}", f"{a}x + {a * b + cc}"]
            expl = f"Tuntihinta kerrotaan sekä x:llä että luvulla {b}, ja kulkumaksu lisätään."
        payload = {"lines": lines, "accept": "exact"}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, ctx + ASK, payload,
                               [expl, f"Sievin muoto: {lines[-1]}"], lines[-1],
                               "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin, ja sen jälkeen lasketaan samanmuotoiset termit yhteen.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
