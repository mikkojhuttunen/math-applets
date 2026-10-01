#!/usr/bin/env python3
"""ALG-05 (juxtaposition read as place value), type MC. Fixed seed, options computed from the numbers."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "alg05_mc"
TID, CODE = "ALG-05", "MC"
OP = "Luku ja kirjain vierekkäin tarkoittavat kertolaskua, eivät kymmeniä ja ykkösiä: 2a = 2 · a."


def make_items(run, date, count=5, start=1):
    rng = random.Random(321)
    items = []
    for k in range(count):
        c, v = rng.randint(2, 8), rng.randint(2, 9)
        while v == c:
            v = rng.randint(2, 9)
        letter = "amkns"[k]
        if k < 2:
            level = "T"
            prompt = f"Mikä on lausekkeen {c}{letter} arvo, kun {letter} = {v}?"
            ans = c * v
            options, cid = mc_options(rng, (str(ans), f"Oikein: {c}{letter} = {c} · {letter} = {c} · {v}."), [
                (str(10 * c + v), "ALG-05", OP),
                (str(c + v), None, f"Luku ja kirjain vierekkäin tarkoittavat kertolaskua, ei yhteenlaskua."),
                (str(10 * v + c), "ALG-05", OP),
            ])
            steps = [f"{c}{letter} = {c} · {letter}", f"= {c} · {v}", f"= {ans}"]
            final = str(ans)
        elif k == 2:
            level = "T"
            e = rng.randint(2, 6)
            prompt = f"Mikä on lausekkeen {c}{letter} + {e} arvo, kun {letter} = {v}?"
            ans = c * v + e
            options, cid = mc_options(rng, (str(ans), f"Oikein: ensin {c} · {v}, sitten + {e}."), [
                (str(10 * c + v + e), "ALG-05", OP),
                (str(c + v + e), None, "Luku ja kirjain vierekkäin tarkoittavat kertolaskua."),
                (str(c * (v + e)), None, f"Kertolasku koskee vain kirjainta: {c}{letter} + {e}."),
            ])
            steps = [f"{c}{letter} + {e} = {c} · {v} + {e}", f"= {c * v} + {e}", f"= {ans}"]
            final = str(ans)
        elif k == 3:
            level = "H"
            prompt = (f"Oppilas sanoo: 'Kun {letter} = {v}, niin {c}{letter} = {10 * c + v}, koska {c} ja {v} kirjoitetaan "
                      f"peräkkäin niin kuin luvussa {10 * c + v}.' Mikä on oikea arvio?")
            options, cid = mc_options(rng, (f"Väärin: {c}{letter} tarkoittaa kertolaskua {c} · {v} = {c * v}", "Oikein: kirjaimen vieressä oleva luku on kerroin."), [
                ("Oikein: vierekkäin kirjoitetut merkit muodostavat yhden luvun", "ALG-05", OP),
                (f"Väärin: oikea arvo on {c} + {v} = {c + v}", None, "Yhteenlasku ei ole lausekkeen tarkoitus."),
                (f"Oikein, mutta vain kun {letter} on yksinumeroinen", "ALG-05", OP),
            ])
            steps = [f"{c}{letter} = {c} · {letter}", f"{c} · {v} = {c * v}", f"Oppilaan {10 * c + v} ei ole sama kuin {c * v}"]
            final = f"{c}{letter} = {c * v}"
        else:
            level = "H"
            u, w = "ab"
            prompt = f"Mikä on lausekkeen {u}{w} arvo, kun {u} = {c} ja {w} = {v}?"
            ans = c * v
            options, cid = mc_options(rng, (str(ans), f"Oikein: {u}{w} = {u} · {w}."), [
                (str(10 * c + v), "ALG-05", OP),
                (str(c + v), None, "Kirjainten välissä ei ole plusmerkkiä: vierekkäin tarkoittaa kertolaskua."),
                (str(c ** v), None, "Kyse ei ole potenssista."),
            ])
            steps = [f"{u}{w} = {u} · {w}", f"= {c} · {v}", f"= {ans}"]
            final = str(ans)
        payload = {"options": options, "correct": [cid]}
        items.append(base_item(TID, CODE, start + k, ["S3.01"], ["T15"], 7, level, prompt, payload, steps, final,
                               "Oikein: luku ja kirjain vierekkäin tarkoittavat kertolaskua.", TEMPLATE,
                               {"c": c, "v": v}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
