#!/usr/bin/env python3
"""FUN-02 (slope-height confusion), type NE. The speed is computed from two tabulated points of a distance-time line;
the wrong entries are the heights read from the graph instead of the slope."""
import random

from gen_common import base_item, cli

TEMPLATE = "fun02_ne"
TID, CODE = "FUN-02", "NE"
HEIGHT = ("Kuvaajan korkeus kertoo matkan, ei nopeutta. Nopeus on kuvaajan jyrkkyys: matkan muutos jaettuna ajan muutoksella.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(642)
    items = []
    for n in range(count):
        v = rng.randint(2, 9)
        c = rng.randint(0, 6)
        if n == 0:
            level, (t1, t2) = "T", (2, 5)
            s1, s2 = c + v * t1, c + v * t2
            prompt = (f"Pyöräilijän etäisyys lähtöpisteestä on {t1} tunnin kohdalla {s1} km ja {t2} tunnin kohdalla {s2} km. "
                      "Kuinka monta kilometriä tunnissa hän pyöräilee? Nopeus on vakio.")
            ans, wrong = v, [s2, s1]
            steps = [f"({s2} − {s1}) / ({t2} − {t1}) = {s2 - s1} / {t2 - t1}", f"= {v}"]
            params, unit = {"v": v, "c": c, "t": [t1, t2]}, "km/h"
        elif n == 1:
            level, (t1, t2) = "T", (1, 4)
            s1, s2 = c + v * t1, c + v * t2
            prompt = (f"Juoksijan matka–aika-kuvaaja kulkee pisteiden ({t1}; {s1}) ja ({t2}; {s2}) kautta, kun aika on tunteina ja matka kilometreinä. "
                      "Mikä on juoksijan nopeus (km/h)?")
            ans, wrong = v, [s2, s1]
            steps = [f"({s2} − {s1}) / ({t2} − {t1}) = {s2 - s1} / {t2 - t1}", f"= {v}"]
            params, unit = {"v": v, "c": c, "t": [t1, t2]}, "km/h"
        elif n == 2:
            level, q = "T", 3
            v2 = v + rng.randint(1, 3)
            c2 = max(0, c - 1)
            s_a, s_b = c2 + v2 * q, c + v * q
            prompt = (f"Kaksi kulkijaa lähtee samaan suuntaan. A:n matka on s = {v2}t + {c2} ja B:n matka s = {v}t + {c}, missä s on kilometreinä ja t tunteina. "
                      "Kuinka monta km/h nopeammin A kulkee kuin B?")
            ans, wrong = v2 - v, [s_a - s_b, abs(c2 - c)] if s_a != s_b else [abs(c2 - c)]
            wrong = [w for w in wrong if w != ans]
            steps = [f"A:n nopeus {v2} km/h, B:n nopeus {v} km/h", f"{v2} − {v} = {v2 - v}"]
            params, unit = {"vA": v2, "cA": c2, "vB": v, "cB": c}, "km/h"
        elif n == 3:
            level, t2 = "H", 3
            l0 = rng.choice([4, 6, 10, 15])
            r = rng.randint(3, 8)
            l2 = l0 + r * t2
            prompt = (f"Vesisäiliössä on aluksi {l0} l vettä. Kolmen minuutin kuluttua vettä on {l2} l. "
                      "Kuinka monta litraa minuutissa säiliöön tulee vettä, kun täyttö on tasaista?")
            ans, wrong = r, [l2, l0]
            steps = [f"({l2} − {l0}) / {t2} = {l2 - l0} / {t2}", f"= {r}"]
            params, unit = {"start": l0, "rate": r, "t": t2}, "l/min"
        else:
            level = "H"
            t0 = rng.randint(3, 6)
            cA = rng.randint(2, 4)
            vA = rng.randint(2, 6)
            sx = cA + vA * t0
            cB = rng.randint(0, cA - 1)
            prompt = (f"Kahden kohteen matka–aika-kuvaajat leikkaavat hetkellä t = {t0} h kohdassa s = {sx} km. "
                      f"A lähti lähtöpisteestä {cA} km:n päästä ja B {cB} km:n päästä. Kuinka monta km/h A:n nopeus on?")
            ans, wrong = vA, [sx, cA]
            wrong = [w for w in wrong if w != ans]
            steps = [f"({sx} − {cA}) / {t0} = {sx - cA} / {t0}", f"= {vA}"]
            params, unit = {"vA": vA, "cA": cA, "cB": cB, "t0": t0}, "km/h"
        wrong = [w for i, w in enumerate(wrong) if w != ans and w not in wrong[:i] and w > 0]
        assert wrong
        payload = {"answer": {"kind": "number", "value": ans, "unit": unit},
                   "wrong": [{"match": w, "misconception": "FUN-02", "feedback": HEIGHT} for w in wrong],
                   "input_hint": "Kirjoita kokonaisluku"}
        items.append(base_item(TID, CODE, start + n, ["S4.07"], ["T8", "T15"], 9, level, prompt, payload, steps, str(ans),
                               "Oikein: nopeus on kuvaajan jyrkkyys eli matkan muutos aikayksikössä.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
