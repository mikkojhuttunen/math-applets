#!/usr/bin/env python3
"""ALG-05 (juxtaposition read as place value), type ME. Equivalence flags are checked by verify.py with sympy."""
import random

from gen_common import MINUS, base_item, cli

TEMPLATE = "alg05_me"
TID, CODE = "ALG-05", "ME"


def make_items(run, date, count=5, start=1):
    rng = random.Random(341)
    items = []
    for k in range(count):
        c = rng.randint(2, 5)
        d = rng.randint(2, 9)
        L = "nmkpt"[k]
        if k < 2:
            level, ref, vars_, samples = "T", f"{c}{L}", [L], [[-2], [1], [4]]
            eq = [f"{L} · {c}", " + ".join([L] * c), f"{c} · {L}"]
            bad = [(f"{10 * c} + {L}", TID), (f"{c} + {L}", None), (f"{L}{c}".replace(f"{L}{c}", f"{L}^{c}"), None)]
            prompt = f"Valitse kaikki lausekkeet, joiden arvo on sama kuin {ref}."
            steps = [f"{c}{L} = {c} · {L}", f"{L} · {c} ja {L} + … + {L} ({c} kertaa) ovat samat"]
        elif k == 2:
            level, ref, vars_, samples = "T", f"{c}{L} + {d}", [L], [[-2], [1], [4]]
            eq = [f"{d} + {c}{L}", f"{c} · {L} + {d}", f"{L} · {c} + {d}"]
            bad = [(f"{10 * c} + {L} + {d}", TID), (f"{c} + {L} + {d}", None), (f"{c + d}{L}", None)]
            prompt = f"Mitkä seuraavista ovat yhtä suuria kuin {ref}? Valitse kaikki oikeat."
            steps = [f"{c}{L} = {c} · {L}", f"{c}{L} + {d}"]
        elif k == 3:
            level, ref, vars_, samples = "H", "ab", ["a", "b"], [[2, 3], [-1, 4], [5, 2]]
            eq = ["a · b", "b · a", "ba"]
            bad = [("10a + b", TID), ("a + b", None), ("a^b", None)]
            prompt = "Valitse kaikki lausekkeet, joiden arvo on sama kuin ab, kun a ja b ovat lukuja."
            steps = ["ab = a · b", "Kertolaskussa tekijöiden järjestys ei vaikuta tulokseen: a · b = b · a"]
        else:
            level, ref, vars_, samples = "H", f"{c}{L}", [L], [[-2], [1], [4]]
            eq = [f"{L} · {c}", " + ".join([L] * c)]
            bad = [(f"{10 * c} + {L}", TID), (f"{c} + {L}", None)]
            prompt = (f"Yksi mehupullo maksaa {L} euroa. Ostetaan {c} pulloa. "
                      "Valitse kaikki lausekkeet, jotka kuvaavat hintaa euroina.")
            steps = [f"{c} pulloa maksaa {c} · {L} = {c}{L} euroa", f"Sama kuin {L} + … + {L} ({c} kertaa)"]
        opts = [(t, True, None) for t in eq] + [(t, False, m) for t, m in bad]
        opts = [o for i, o in enumerate(opts) if o[0] not in [p[0] for p in opts[:i]]]
        rng.shuffle(opts)
        options = [{"id": "abcdefgh"[i], "text": t.replace("-", MINUS), "equivalent": e, "misconception": m}
                   for i, (t, e, m) in enumerate(opts)]
        payload = {"reference": ref, "variables": vars_, "samples": samples, "options": options}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15"], 7, level, prompt, payload, steps, steps[0],
                               "Oikein: luku ja kirjain vierekkäin tarkoittavat kertolaskua.", TEMPLATE,
                               {"c": c, "d": d, "letter": L}, date, run,
                               generic_wrong="Sijoita kirjaimen paikalle luku, esimerkiksi 3, ja laske lausekkeiden arvot. "
                                             "Vierekkäin kirjoitetut luku ja kirjain eivät ole kymmenet ja ykköset."))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
