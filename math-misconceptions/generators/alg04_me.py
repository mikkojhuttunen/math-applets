#!/usr/bin/env python3
"""ALG-04 (conjoining terms), type ME (multi-select equivalence). Equivalence flags are checked by verify.py with sympy."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg04_me"
TID, CODE = "ALG-04", "ME"


def make_items(run, date, count=5, start=1):
    rng = random.Random(827)
    items = []
    for k in range(count):
        a, c = rng.sample(range(2, 8), 2)
        b, d = rng.sample(range(2, 9), 2)
        if b < d:
            b, d = d, b
        vars_, samples = ["x"], [[-2], [1], [3]]
        if k == 0:
            level, ref = "T", f"{a}x + {b}"
            eq = [f"{b} + {a}x", f"{a - 1}x + x + {b}", f"x · {a} + {b}"]
            bad = [(f"{a + b}x", TID), (f"{a * b}x", TID), (f"{b}x + {a}", None)]
            prompt = f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref} kaikilla x:n arvoilla."
            steps = [f"{a}x ja {b} ovat eri muotoisia termejä", f"{ref} on jo sievin"]
        elif k == 1:
            level, ref = "T", f"{a}x + {b} + {c}x"
            eq = [f"{a + c}x + {b}", f"{b} + {c + a}x", f"{a}x + {c}x + {b}"]
            bad = [(f"{a + b + c}x", TID), (f"{a + c}bx".replace("b", str(b)), TID), (f"{a + c + b}", None)]
            prompt = f"Mitkä seuraavista ovat yhtä suuria kuin {ref}? Valitse kaikki oikeat."
            steps = [f"{a}x + {c}x = {a + c}x", f"{a + c}x + {b}"]
        elif k == 2:
            level, ref = "T", f"{b} + {a}x + {d}"
            eq = [f"{a}x + {b + d}", f"{b + d} + {a}x", f"{d} + {b} + {a}x"]
            bad = [(f"{a + b + d}x", TID), (f"{a}x + {b}{d}".replace(f"{b}{d}", str(b * d)), None), (f"{a * (b + d)}x", TID)]
            prompt = f"Valitse kaikki lausekkeet, jotka ovat yhtä suuria kuin {ref}."
            steps = [f"Luvut: {b} + {d} = {b + d}", f"{a}x + {b + d}"]
        elif k == 3:
            level, ref = "H", f"{a}x + {b} {MINUS} {d}"
            eq = [f"{a}x + {b - d}", f"{b - d} + {a}x", f"{b} {MINUS} {d} + {a}x"]
            bad = [(f"{a + b - d}x", TID), (f"{a}x + {b + d}", None), (f"{a * (b - d)}x", TID)]
            prompt = f"Valitse kaikki lausekkeet, joiden arvo on sama kuin lausekkeen {ref}."
            steps = [f"Luvut: {b} {MINUS} {d} = {b - d}", f"{a}x + {b - d}"]
        else:
            level, ref = "H", f"{a}x + {b}"
            eq = [f"{b} + {a}x", f"x + {a - 1}x + {b}"]
            bad = [(f"{a + b}x", TID), (f"{a * b}x", TID), (f"{a}x{b}".replace(f"{a}x{b}", f"{b}x + {a}"), None)]
            prompt = (f"Yksi lippu maksaa x euroa. Ostetaan {a} lippua ja lisäksi yksi ohjelmalehtinen hintaan {b} euroa. "
                      "Valitse kaikki lausekkeet, jotka kuvaavat kokonaishintaa euroina.")
            steps = [f"{a} lippua maksaa {a}x euroa", f"Kokonaishinta {a}x + {b}"]
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        opts = [o for i, o in enumerate(opts) if o[0] not in [p[0] for p in opts[:i]]]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t.replace("-", MINUS), "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": vars_, "samples": samples, "options": options}
        items.append(base_item(TID, CODE, start + k, ["S3.02"], ["T14"], 7, level, prompt, payload, steps, steps[-1],
                               "Oikein: vain samanmuotoiset termit lasketaan yhteen.", TEMPLATE,
                               {"a": a, "b": b, "c": c, "d": d}, date, run,
                               generic_wrong="Kokeile sijoittaa x:n paikalle luku, esimerkiksi x = 1, ja vertaa lausekkeiden arvoja."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
