#!/usr/bin/env python3
"""EXT-08 (mean taken as the "typical value"; median read from unsorted data), type MC. Medians and means are
computed with exact fractions after sorting; the tagged distractors are the middle of the list as written and the
mean offered as the typical value where outliers make it misleading."""
import random

from ext08_common import dec, mean, median, pick_list, txt, written_middle
from gen_common import base_item, cli, mc_options

TEMPLATE = "ext08_mc"
TID, CODE = "EXT-08", "MC"
BAD = ("Mediaani ei ole listan keskimmäinen luku sellaisenaan. Järjestä luvut ensin pienimmästä suurimpaan ja "
       "valitse sitten keskimmäinen (parillisella määrällä kahden keskimmäisen keskiarvo).")
GOOD = "Oikein: luvut järjestetään ensin, ja mediaani on keskimmäinen arvo."
MEANFB = "Tämä on keskiarvo, ei mediaani. Mediaani on järjestetyn aineiston keskimmäinen arvo."


def make_items(run, date, count=5, start=1):
    rng = random.Random(1802)
    items = []
    for k in range(count):
        if k == 0:
            vals = pick_list(rng, 5, 2, 20, want_mean=True)
            level = "T"
            md, wm, mn = median(vals), written_middle(vals), mean(vals)
            prompt = f"Oppilaat saivat kokeesta pisteet {txt(vals)}. Mikä on pisteiden mediaani?"
            correct = (dec(md), GOOD)
            wrongs = [(dec(wm), TID, BAD), (dec(mn), None, MEANFB), (str(max(vals)), None, "Tämä on suurin arvo, ei keskimmäinen.")]
            steps = [f"Järjestys: {txt(sorted(vals))}", f"Keskimmäinen arvo on {dec(md)}"]
        elif k == 1:
            vals = pick_list(rng, 6, 3, 40, want_mean=True)
            level = "T"
            md, wm = median(vals), written_middle(vals)
            s = sorted(vals)
            prompt = f"Kuuden kävelylenkin pituudet olivat {txt(vals)} minuuttia. Mikä on pituuksien mediaani?"
            correct = (dec(md), GOOD)
            wrongs = [(dec(wm), TID, BAD), (dec(mean(vals)), None, MEANFB), (str(s[len(s) // 2]), None,
                      "Tämä on vain toinen kahdesta keskimmäisestä arvosta. Parillisella määrällä otetaan niiden keskiarvo.")]
            steps = [f"Järjestys: {txt(s)}", f"Kaksi keskimmäistä: {s[2]} ja {s[3]}, keskiarvo {dec(md)}"]
        elif k == 2:
            vals = pick_list(rng, 7, 1, 30)
            level = "T"
            prompt = (f"Oppilas laskee lukujen {txt(vals)} mediaania. Mikä on mediaanin laskemisen ensimmäinen vaihe?")
            md = median(vals)
            correct = ("Luvut järjestetään pienimmästä suurimpaan", GOOD)
            wrongs = [("Valitaan luettelon keskimmäinen luku sellaisenaan", TID, BAD),
                      ("Lasketaan kaikki luvut yhteen ja jaetaan niiden lukumäärällä", None, MEANFB),
                      ("Etsitään luku, joka esiintyy useimmin", None, "Tämä on tyyppiarvo, ei mediaani.")]
            steps = [f"Järjestys: {txt(sorted(vals))}", f"Mediaani on {dec(md)}"]
        elif k == 3:
            while True:
                base = pick_list(rng, 6, 10, 25)
                big = max(base) * 9
                vals = [v for v in base if v != max(base)] + [big]
                rng.shuffle(vals)
                md, mn = median(vals), mean(vals)
                if mn.denominator in (1, 2, 4, 5, 10) and mn > 2 * md:
                    break
            level = "H"
            prompt = (f"Kuuden hengen yrityksessä kuukausipalkat ovat {txt(vals)} (luvut ovat satoja euroja). "
                      f"Keskiarvo on {dec(mn)} ja mediaani {dec(md)}. Kumpi kuvaa paremmin tyypillistä palkkaa ja miksi?")
            correct = ("Mediaani, koska yksi erittäin suuri palkka nostaa keskiarvoa mutta ei muuta keskimmäistä arvoa paljon", GOOD)
            wrongs = [("Keskiarvo, koska se on aina tyypillisin arvo", TID,
                       "Keskiarvo ei aina kuvaa tyypillistä arvoa: yksi poikkeava arvo vetää sen kauas useimmista arvoista."),
                      ("Keskiarvo, koska se ottaa huomioon kaikki arvot, joten se on paras", TID,
                       "Juuri siksi poikkeava arvo vaikuttaa siihen paljon. Tässä useimmat palkat ovat selvästi keskiarvoa pienempiä."),
                      ("Kumpikaan ei kuvaa, koska ne ovat eri lukuja", None, "Molemmat ovat keskilukuja; kysymys on, kumpi sopii aineistoon.")]
            steps = [f"Järjestys: {txt(sorted(vals))}", f"Mediaani {dec(md)}, keskiarvo {dec(mn)}",
                     "Poikkeava suuri arvo nostaa keskiarvoa, joten mediaani kuvaa tyypillistä palkkaa paremmin"]
        else:
            vals = pick_list(rng, 5, 4, 30, want_mean=True)
            wm, md = written_middle(vals), median(vals)
            level = "H"
            prompt = (f"Oppilas sanoo: \"Luvuista {txt(vals)} mediaani on {dec(wm)}, koska se on listan keskellä.\" "
                      f"Mikä on oikea arvio?")
            correct = (f"Väite on väärä: luvut pitää järjestää ensin, ja silloin mediaani on {dec(md)}", GOOD)
            wrongs = [("Väite on oikea, koska mediaani on aina keskimmäinen luku listassa", TID, BAD),
                      ("Väite on oikea, koska mediaani on aina sama kuin keskiarvo", TID, "Mediaani ja keskiarvo ovat eri keskilukuja, eivätkä yleensä ole yhtä suuret."),
                      (f"Väite on väärä, mediaani on keskiarvo {dec(mean(vals))}", None, MEANFB)]
            steps = [f"Järjestys: {txt(sorted(vals))}", f"Mediaani on {dec(md)}, ei {dec(wm)}"]
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S6.02", "S6.03"], ["T19"], 7, level, prompt,
                               {"options": options, "correct": [cid]}, steps, correct[0], GOOD, TEMPLATE,
                               {"values": vals}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
