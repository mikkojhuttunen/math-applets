#!/usr/bin/env python3
"""EXT-08 (mean taken as the "typical value"; median read from unsorted data), type FS. All lines are numeric
expressions with the same value; the blanked line (line 2) is computed by code and verify.py checks the chain for
equivalence (the variable x is only a schema placeholder). Means and medians are exact fractions."""
import random

from ext08_common import dec, mean, median, pick_list, txt
from gen_common import MINUS, base_item, cli

TEMPLATE = "ext08_fs"
TID, CODE = "EXT-08", "FS"
SAMPLES = [[1], [2], [3]]
GOOD = ("Oikein: keskiarvo on summa jaettuna lukujen määrällä, ja mediaani luetaan järjestetystä listasta "
        "(parillisella määrällä kahden keskimmäisen keskiarvo).")
GENERIC = ("Tarkista rivi kerrallaan: keskiarvossa lasketaan kaikki luvut yhteen ja jaetaan lukujen määrällä. "
           "Mediaani on järjestetyn listan keskimmäinen arvo.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(1813)
    items = []
    for k in range(count):
        if k == 0:
            vals = pick_list(rng, 5, 2, 30, want_mean=True)
            s, n = sum(vals), 5
            terms = " + ".join(str(v) for v in vals)
            lines = [f"({terms}) / {n}", f"{s} / {n}", dec(mean(vals))]
            intro = f"Viiden oppilaan koepisteet ovat {txt(vals)}. Laske keskiarvo."
            hint, level = "Kirjoita välivaihe, jossa summa on laskettu", "T"
            params = {"values": vals}
        elif k == 1:
            while True:
                vals = pick_list(rng, 6, 3, 40)
                a, b = sorted(vals)[2:4]
                if a + b != 2 * a and (a + b) % 2 == 0:
                    break
            lines = [f"({a} + {b}) / 2", f"{a + b} / 2", dec(median(vals))]
            intro = (f"Kuuden kävelylenkin pituudet ovat {txt(vals)} minuuttia. Laske mediaani: järjestä luvut ja "
                     f"laske kahden keskimmäisen keskiarvo ({a} ja {b}).")
            hint, level = "Kirjoita välivaihe, jossa keskimmäisten summa on laskettu", "T"
            params = {"values": vals}
        elif k == 2:
            while True:
                vals = pick_list(rng, 7, 1, 40, want_mean=True)
                med, mn = median(vals), mean(vals)
                if mn.denominator in (1, 2, 4, 5, 10) and (mn - med).denominator in (1, 2, 4, 5, 10, 20):
                    break
            s = sum(vals)
            lines = [f"{s} / 7 {MINUS} {dec(med)}", f"{dec(mn)} {MINUS} {dec(med)}", dec(mn - med)]
            intro = (f"Viikon päivälämpötilat ovat {txt(vals)} astetta. Mediaani on {dec(med)}. "
                     f"Laske keskiarvon ja mediaanin erotus.")
            hint, level = "Kirjoita välivaihe, jossa keskiarvo on laskettu", "T"
            params = {"values": vals}
        elif k == 3:
            while True:
                vals = pick_list(rng, 4, 5, 30)
                o = rng.randint(40, 90)
                if (sum(vals) + o) % 5 == 0:
                    break
            n = 4
            lines = [f"({' + '.join(str(v) for v in vals)} + {o}) / 5", f"{sum(vals) + o} / 5", dec(mean(vals + [o]))]
            intro = (f"Neljän ostoksen hinnat ovat {txt(vals)} euroa. Viides ostos maksaa {o} euroa. "
                     f"Laske kaikkien viiden hintojen keskiarvo.")
            hint, level = "Kirjoita välivaihe, jossa summa on laskettu", "H"
            params = {"values": vals, "outlier": o}
        else:
            m, p = rng.choice([6, 7, 8, 9]), rng.choice([10, 11, 12, 14])
            lines = [f"({m} · 3 + {p}) / 4", f"{3 * m + p} / 4", dec(mean([m, m, m, p]))]
            intro = (f"Kolmen kokeen keskiarvo on {m}. Neljännen kokeen tulos on {p}. "
                     f"Laske nelijen kokeen keskiarvo; kolmen ensimmäisen summa on {m} · 3.")
            intro = intro.replace("nelijen", "neljän")
            hint, level = "Kirjoita välivaihe, jossa summa on laskettu", "H"
            params = {"mean": m, "last": p}
        assert len(set(lines)) == 3, lines
        blank = 2
        ref = lines[blank - 1]
        prompt = f"{intro} {hint}: {lines[0]} = □ = {lines[2]}"
        answer = {"kind": "expression", "variables": ["x"], "reference": ref, "samples": SAMPLES}
        steps = [f"{lines[i]} = {lines[i + 1]}" for i in range(len(lines) - 1)]
        payload = {"lines": lines, "blank_index": blank, "answer": answer}
        items.append(base_item(TID, CODE, start + k, ["S6.02", "S6.03"], ["T19"], 7, level, prompt, payload, steps,
                               ref, GOOD, TEMPLATE, params | {"form": k}, date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
