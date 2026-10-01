#!/usr/bin/env python3
"""EXT-04 (x² = 9 gives only x = 3), type ME (multi-select equivalence). The reference is x² − a² (or a scaled
version); equivalent options are factorisations with both roots, distractors keep only one root (tagged) or are
other expressions. Equivalence flags are checked by verify.py with sympy."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "ext04_me"
TID, CODE = "EXT-04", "ME"
GOOD = "Oikein: neliöiden erotus x² − a² = (x − a)(x + a), joten lausekkeella on kaksi nollakohtaa, a ja −a."
GENERIC = ("Kokeile sijoittaa x:n paikalle luku, esimerkiksi x = 1, ja vertaa lausekkeiden arvoja. "
           "Tulon (x − a)(x + a) nollakohdat ovat sekä a että −a.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1407)
    items, seen = [], set()
    for k in range(count):
        a = rng.choice([2, 3, 4, 5, 6, 7])
        p = 1
        ctx = ""
        if k == 0:
            level, ref = "T", f"x² {MINUS} {a * a}"
            eq = [f"(x {MINUS} {a})(x + {a})", f"(x + {a})(x {MINUS} {a})", f"x² {MINUS} {a}²"]
            bad = [(f"(x {MINUS} {a})²", TID), (f"x {MINUS} {a}", TID), (f"x² + {a * a}", None)]
        elif k == 1:
            p = rng.choice([2, 3])
            level, ref = "T", f"{p}x² {MINUS} {p * a * a}"
            eq = [f"{p}(x {MINUS} {a})(x + {a})", f"{p}(x² {MINUS} {a * a})", f"({p}x {MINUS} {p * a})(x + {a})"]
            bad = [(f"{p}(x {MINUS} {a})²", TID), (f"{p}(x {MINUS} {a})", TID), (f"{p}x² + {p * a * a}", None)]
        elif k == 2:
            level, ref = "T", f"x² {MINUS} {a * a}"
            eq = [f"(x {MINUS} {a})(x + {a})", f"(x {MINUS} {a}) · (x + {a})", f"x² {MINUS} {a} · {a}"]
            bad = [(f"(x {MINUS} {a})(x {MINUS} {a})", TID), (f"(x + {a})²", TID), (f"x² {MINUS} {a}", None)]
        elif k == 3:
            level, ref = "H", f"x² {MINUS} {a * a}"
            ctx = (f"Neliönmuotoisen laatan sivu on x ja siitä leikataan pois neliö, jonka sivu on {a}. "
                   "Valitse kaikki lausekkeet, jotka kuvaavat jäljelle jäävää pinta-alaa kaikilla x:n arvoilla. ")
            eq = [f"(x {MINUS} {a})(x + {a})", f"x² {MINUS} {a * a}", f"(x + {a})(x {MINUS} {a})"]
            bad = [(f"(x {MINUS} {a})²", TID), (f"x {MINUS} {a}", TID), (f"(x {MINUS} {a * a})", None)]
        else:
            p = rng.choice([2, 3])
            level, ref = "H", f"{p}x² {MINUS} {p * a * a}"
            ctx = (f"Yhtälön {p}x² = {p * a * a} ratkaisut ovat nollakohtia lausekkeelle {p}x² {MINUS} {p * a * a}. "
                   "Valitse kaikki lausekkeet, jotka ovat samat kuin tämä lauseke kaikilla x:n arvoilla. ")
            eq = [f"{p}(x {MINUS} {a})(x + {a})", f"{p}x² {MINUS} {p * a * a}", f"{p}(x² {MINUS} {a * a})"]
            bad = [(f"{p}(x {MINUS} {a})(x {MINUS} {a})", TID), (f"{p}(x {MINUS} {a})", TID), (f"{p}x² {MINUS} {a * a}", None)]
        key = (k, a, p)
        assert key not in seen
        seen.add(key)
        steps = [f"{ref} = " + eq[0], "Tulo on nolla, kun x − a = 0 tai x + a = 0, eli x = " + f"{a} tai x = {MINUS}{a}"]
        prompt = ctx or f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref} kaikilla x:n arvoilla."
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t, "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": ["x"], "samples": [[-3], [2], [5]], "options": options}
        items.append(base_item(TID, CODE, start + k, ["S3.08"], ["T14"], 9, level, prompt, payload, steps, steps[0],
                               GOOD, TEMPLATE, {"a": a, "p": p}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
