#!/usr/bin/env python3
"""ALG-08 (distributive law applied to one term), type ES (error spotting). Lines before the error line are
equivalent to line 1 and the error line breaks equivalence (both checked by verify.py); the injected error
multiplies only the first term in the bracket."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg08_es"
TID, CODE = "ALG-08", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = "Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen kaikilla x:n arvoilla? Kokeile vaikka x = 1."
INTRO = "Oppilas sieventää lausekkeen rivi riviltä. "


def make_items(run, date, count=5, start=1):
    rng = random.Random(8302)
    items = []
    for k in range(count):
        a, b, c, d = rng.randint(2, 7), rng.randint(2, 8), rng.randint(2, 6), rng.randint(2, 6)
        ctx = INTRO
        if k == 0:
            level, err = "T", 2
            lines = [f"{a}(x + {b}) + {c}x", f"{a}x + {b} + {c}x", f"{a + c}x + {b}"]
            fix = f"Kerroin {a} kertoo molemmat termit: {a}(x + {b}) = {a}x + {a * b}. Oikea tulos on {a + c}x + {a * b}."
        elif k == 1:
            level, err = "T", 2
            cc = rng.randint(a * b + 1, a * b + 9)
            lines = [f"{a}(x {MINUS} {b}) + {cc}", f"{a}x {MINUS} {b} + {cc}", f"{a}x + {cc - b}"]
            fix = (f"Kerroin {a} kertoo myös luvun {b}: {a}(x {MINUS} {b}) = {a}x {MINUS} {a * b}. "
                   f"Oikea tulos on {a}x + {cc - a * b}.")
        elif k == 2:
            level, err = "T", 3
            lines = [f"{a}(x + {b}) + {c}(x + {d})", f"{a}x + {a * b} + {c}(x + {d})",
                     f"{a}x + {a * b} + {c}x + {d}", f"{a + c}x + {a * b + d}"]
            fix = (f"Rivi 2 on oikein. Kerroin {c} kertoo toisenkin termin: {c}(x + {d}) = {c}x + {c * d}. "
                   f"Oikea tulos on {a + c}x + {a * b + c * d}.")
        elif k == 3:
            level, err = "H", 2
            m = rng.randint(2, 4)
            dd = rng.randint(1, a * m - 1)
            lines = [f"{a}({m}x + {b}) {MINUS} {dd}x", f"{a * m}x + {b} {MINUS} {dd}x", f"{a * m - dd}x + {b}"]
            fix = (f"Kerroin {a} kertoo myös luvun {b}: {a}({m}x + {b}) = {a * m}x + {a * b}. "
                   f"Oikea tulos on {a * m - dd}x + {a * b}.")
        else:
            level, err = "H", 2
            cc = rng.randint(2, 9)
            ctx = (f"Siivousyritys veloittaa {a} euroa tunnilta. Työ kestää x + {b} tuntia, ja lisäksi veloitetaan "
                   f"{cc} euron kulkumaksu. Oppilas kirjoittaa kokonaishinnan lausekkeen ja sieventää sen rivi riviltä. ")
            lines = [f"{a}(x + {b}) + {cc}", f"{a}x + {b} + {cc}", f"{a}x + {b + cc}"]
            fix = (f"Tuntihinta {a} euroa kerrotaan koko työajalla x + {b}: {a}(x + {b}) = {a}x + {a * b}. "
                   f"Oikea tulos on {a}x + {a * b + cc}.")
        payload = {"lines": lines, "error_line": err, "error_type": "distributes_to_first_term_only"}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, ctx + ASK, payload,
                               [fix], f"Virhe on rivillä {err}",
                               "Oikein: kerroin kertoo jokaisen sulun sisällä olevan termin.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
