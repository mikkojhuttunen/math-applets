#!/usr/bin/env python3
"""EXT-08 (mean taken as the "typical value"; median read from unsorted data), type ES (error spotting). Lines are
numeric expressions; lines before the error line equal line 1 (the median taken from the sorted list) and the error
line uses the middle of the list as written or the mean. Medians and means are exact fractions."""
import random

from ext08_common import dec, mean, median, pick_list, txt, written_middle
from gen_common import base_item, cli

TEMPLATE = "ext08_es"
TID, CODE = "EXT-08", "ES"
ASK = "Missä rivissä on ensimmäinen virhe? Napauta riviä."
GENERIC = ("Tarkista rivi kerrallaan: onko uusi rivi yhtä suuri kuin edellinen? Mediaani on järjestetyn listan "
           "keskimmäinen arvo (parillisella määrällä kahden keskimmäisen keskiarvo), ei keskiarvo.")
GOOD = "Oikein: luvut järjestetään ensin, ja mediaani luetaan järjestetystä listasta."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1811)
    items = []
    for k in range(count):
        if k == 0:
            vals = pick_list(rng, 5, 2, 20)
            c = rng.choice([3, 4, 5, 6])
            med, wm = median(vals), written_middle(vals)
            intro = (f"Oppilaat saivat kokeesta pisteet {txt(vals)}. Oppilas laskee mediaanin ja lisää siihen {c} "
                     f"bonuspistettä. Rivi 1 on laskun alku.")
            lines = [f"{c} + {dec(med)}", f"{c} + {dec(wm)}", f"{dec(c + wm)}"]
            err, etype = 2, "unsorted_middle"
            steps = [f"Järjestys: {txt(sorted(vals))}, mediaani on {dec(med)}",
                     f"Rivillä 2 on käytetty listan keskimmäistä lukua {dec(wm)} sellaisenaan, vaikka lista ei ollut järjestyksessä"]
            final_val = c + med
        elif k == 1:
            vals = pick_list(rng, 7, 1, 30)
            med, wm = median(vals), written_middle(vals)
            intro = (f"Seitsemän päivän lämpötilat olivat {txt(vals)} astetta. Oppilas laskee mediaanilämpötilan "
                     f"kaksinkertaisen. Rivi 1 on laskun alku.")
            lines = [f"2 · {dec(med)}", f"{dec(2 * med)}", f"{dec(2 * wm)}"]
            err, etype = 3, "unsorted_middle"
            steps = [f"Järjestys: {txt(sorted(vals))}, mediaani on {dec(med)}, ja 2 · {dec(med)} = {dec(2 * med)}",
                     f"Rivi 3 käyttää lukua {dec(wm)}, joka on listan keskimmäinen luku vasta järjestämättä"]
            final_val = 2 * med
        elif k == 2:
            vals = pick_list(rng, 6, 3, 40)
            s = sorted(vals)
            a, b = s[2], s[3]
            wa, wb = vals[2], vals[3]
            intro = (f"Kuuden kävelylenkin pituudet olivat {txt(vals)} minuuttia. Oppilas laskee mediaanin kahden "
                     f"keskimmäisen keskiarvona. Rivi 1 on laskun alku.")
            lines = [f"({a} + {b}) / 2", f"({wa} + {wb}) / 2", f"{dec(median(vals))}"]
            err, etype = 2, "unsorted_middle"
            steps = [f"Järjestys: {txt(s)}, keskimmäiset ovat {a} ja {b}",
                     f"Rivi 2 käyttää järjestämättömän listan keskimmäisiä lukuja {wa} ja {wb}"]
            final_val = median(vals)
        elif k == 3:
            while True:
                vals = pick_list(rng, 6, 5, 40)
                s = sorted(vals)
                if (vals[2] + vals[3]) != (s[2] + s[3]) and (s[2] + s[3]) % 2 == 0:
                    break
            a, b = s[2], s[3]
            wa, wb = vals[2], vals[3]
            intro = (f"Kuuden oppilaan lukemat kirjat ovat {txt(vals)}. Oppilas laskee mediaanin ja kertoo sen "
                     f"kolmella. Rivi 1 on laskun alku.")
            lines = [f"3 · ({a} + {b}) / 2", f"3 · ({wa} + {wb}) / 2", f"{3 * ((a + b) // 2)}"]
            err, etype = 2, "unsorted_middle"
            steps = [f"Järjestys: {txt(s)}, keskimmäiset {a} ja {b}, mediaani {dec(median(vals))}",
                     f"Rivi 2 käyttää järjestämättömän listan keskimmäisiä lukuja {wa} ja {wb}"]
            final_val = 3 * median(vals)
        else:
            while True:
                base = pick_list(rng, 7, 10, 30)
                big = max(base) * 8
                data = [v for v in base if v != max(base)] + [big]
                rng.shuffle(data)
                med, mn = median(data), mean(data)
                if mn != med and mn.denominator in (1, 2, 4, 5, 10) and med.denominator in (1, 2):
                    break
            intro = (f"Seitsemän työntekijän kuukausipalkat ovat {txt(data)} (luvut ovat satoja euroja). Oppilas "
                     f"laskee mediaanipalkan euroina. Rivi 1 on laskun alku.")
            lines = [f"{dec(med)} · 100", f"{dec(mn)} · 100", f"{dec(mn * 100)}"]
            err, etype = 2, "mean_for_median"
            steps = [f"Järjestys: {txt(sorted(data))}, mediaani on {dec(med)}, eli {dec(med * 100)} €",
                     f"Rivi 2 käyttää keskiarvoa {dec(mn)}, joka on suuren arvon takia suurempi kuin tyypillinen palkka"]
            final_val = med * 100
            vals = data
        steps.append(f"Oikea tulos on {dec(final_val)}")
        payload = {"lines": lines, "error_line": err, "error_type": etype}
        level = "T" if k < 3 else "H"
        items.append(base_item(TID, CODE, start + k, ["S6.02", "S6.03"], ["T19"], 7, level, f"{intro} {ASK}", payload,
                               steps, f"Virhe on rivillä {err}", GOOD, TEMPLATE, {"values": vals, "form": k},
                               date, run, generic_wrong=GENERIC))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
