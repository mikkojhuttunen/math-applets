#!/usr/bin/env python3
"""ALG-04 (conjoining terms), type ES (error spotting). Lines before the error line are equivalent to line 1
(checked by verify.py); the error line merges all terms into one x-term."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg04_es"
TID, CODE = "ALG-04", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."


def make_items(run, date, count=5, start=1):
    rng = random.Random(715)
    items = []
    for k in range(count):
        a, c = rng.sample(range(2, 8), 2)
        b, d = rng.sample(range(2, 9), 2)
        if b < d:
            b, d = d, b
        if k == 0:
            level, err = "T", 2
            lines = [f"{a}x + {b}", f"{a + b}x", f"x · {a + b}"]
            ctx = "Oppilas sieventää lausekkeen rivi riviltä. "
            fix = f"{a}x ja {b} ovat eri muotoisia termejä, joten {a}x + {b} on jo sievin."
        elif k == 1:
            level, err = "T", 3
            lines = [f"{a}x + {b} + {c}x", f"{a + c}x + {b}", f"{a + b + c}x"]
            ctx = "Oppilas sieventää lausekkeen rivi riviltä. "
            fix = f"Rivi 2 on oikein: {a}x + {c}x = {a + c}x. Luku {b} ei yhdisty x-termiin."
        elif k == 2:
            level, err = "T", 3
            lines = [f"{b} + {a}x + {d}", f"{a}x + {b} + {d}", f"{a + b + d}x"]
            ctx = "Oppilas sieventää lausekkeen rivi riviltä. "
            fix = f"Rivi 2 on oikein. Luvut: {b} + {d} = {b + d}, joten tulos on {a}x + {b + d}."
        elif k == 3:
            level, err = "H", 4
            lines = [f"{a}x + {b} + {c}x {MINUS} {d}", f"{a}x + {c}x + {b} {MINUS} {d}", f"{a + c}x + {b - d}",
                     f"{a + c + b - d}x"]
            ctx = "Oppilas sieventää lausekkeen rivi riviltä. "
            fix = f"Rivi 3 on oikein: {a + c}x + {b - d}. Termejä {a + c}x ja {b - d} ei voi yhdistää."
        else:
            level, err = "H", 3
            lines = [f"{a}x + {b} + {c}x", f"{a}x + {c}x + {b}", f"{a + c + b}x"]
            ctx = (f"Retkellä jokainen osallistuja maksaa x euroa. Ryhmä A maksaa {a}x euroa, ryhmä B {c}x euroa ja lisäksi "
                   f"ostetaan yhteinen eväspaketti hintaan {b} euroa. Oppilas sieventää kokonaishinnan rivi riviltä. ")
            fix = f"Rivi 2 on oikein. Eväspaketin hinta {b} € ei ole osallistujien määrästä riippuva, joten tulos on {a + c}x + {b}."
        payload = {"lines": lines, "error_line": err, "error_type": "joins_unlike_terms"}
        steps = [fix, f"Oikea tulos: {a + c}x + {b}" if k in (1, 4) else
                 (f"Oikea tulos: {a}x + {b}" if k == 0 else (f"Oikea tulos: {a}x + {b + d}" if k == 2 else f"Oikea tulos: {a + c}x + {b - d}"))]
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, ctx + ASK, payload, steps,
                               f"Virhe on rivillä {err}",
                               "Oikein: vain samanmuotoiset termit voi laskea yhteen; luku ja x-termi pysyvät erillään.",
                               TEMPLATE, {"a": a, "b": b, "c": c, "d": d}, date, run,
                               generic_wrong="Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen kaikilla x:n arvoilla? "
                                             "Kokeile vaikka x = 1."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
