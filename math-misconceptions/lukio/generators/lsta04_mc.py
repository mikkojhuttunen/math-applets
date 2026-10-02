#!/usr/bin/env python3
"""LSTA-04 MC: a confidence interval read as a probability about the true value (MAB only).
Margins and counts are computed in code; the distractor tagged LSTA-04 is the probability reading."""
import math
import random

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "lsta04_mc"
TID, CODE = "LSTA-04", "MC"
GENERIC = ("Luottamusväli kuvaa menetelmää: jos otanta toistettaisiin ja väli laskettaisiin samalla tavalla, noin 95 % väleistä peittäisi "
           "todellisen arvon. Todellinen arvo on kiinteä luku, ei satunnainen.")


def make_items(run, date, count=5, start=1):
    rng = random.Random(9401)
    items = []
    # 1: interpretation
    opts, cid = mc_options(
        rng, ("Jos otanta toistettaisiin monta kertaa ja väli laskettaisiin joka kerta samalla tavalla, noin 95 % väleistä sisältäisi todellisen keskiarvon.",
              "Oikein: 95 % kuvaa menetelmän onnistumista toistoissa."),
        [("Todellinen keskiarvo on tällä välillä 95 %:n todennäköisyydellä.", "LSTA-04",
          "Todellinen keskiarvo on kiinteä luku; se joko on välillä tai ei ole. Prosentti kuvaa menetelmää, ei tätä yksittäistä väliä."),
         ("95 % kaikista oppilaista nukkuu 12,1–13,4 tuntia.", None, "Luottamusväli koskee keskiarvoa, ei yksittäisiä havaintoja.")])
    items.append(base_item(TID, CODE, start, ["MAB9.04"], ["G3"], "MAB", "P", "none",
                           "Otoksesta lasketaan oppilaiden viikoittaisen liikunnan keskiarvolle 95 %:n luottamusväli 12,1–13,4 tuntia. Mikä väite kuvaa luottamusvälin merkitystä oikein?",
                           {"options": opts, "correct": [cid]},
                           ["95 % liittyy menetelmään: noin 95 % samalla tavalla lasketuista väleistä peittää todellisen keskiarvon.",
                            "Yksittäinen väli joko sisältää todellisen keskiarvon tai ei."], "Menetelmän onnistumisprosentti", "Oikein.",
                           TEMPLATE, {"lo": 12.1, "hi": 13.4}, date, run, generic_wrong=GENERIC))
    # 2: margin of error (cas)
    p, n, z = 0.52, 1000, 1.96
    right = z * math.sqrt(p * (1 - p) / n) * 100
    half = right / 2
    nosqrt = z * p * (1 - p) / n * 100
    r, h_, s_ = num(round(right, 1)), num(round(half, 1)), num(round(nosqrt, 1))
    assert len({r, h_}) == 2
    opts, cid = mc_options(
        rng, (f"±{r} %-yksikköä", "Oikein: 1,96 · √(0,52 · 0,48 / 1000) ≈ 0,031."),
        [(f"±{h_} %-yksikköä", None, "Tämä on puolet oikeasta virhemarginaalista."),
         ("±5 %-yksikköä", TID, "95 % on luottamustaso eli menetelmän onnistumisprosentti, ei virhemarginaalin suuruus.")])
    items.append(base_item(TID, CODE, start + 1, ["MAB9.04"], ["G3", "G8"], "MAB", "H", "cas",
                           "Kyselyssä 1000 vastaajasta 52 % kannattaa ehdotusta. Mikä on kannatusosuuden 95 %:n virhemarginaali, kun käytetään kaavaa 1,96 · √(p(1 − p)/n)?",
                           {"options": opts, "correct": [cid]},
                           ["Keskivirhe = √(0,52 · 0,48 / 1000) ≈ 0,0158.", "Virhemarginaali ≈ 1,96 · 0,0158 ≈ 0,031 eli 3,1 %-yksikköä."], f"±{r} %-yksikköä",
                           "Oikein.", TEMPLATE, {"p": p, "n": n}, date, run, generic_wrong=GENERIC))
    # 3: sample size effect
    n1, n2 = 100, 400
    ratio = math.sqrt(n1 / n2)
    assert ratio == 0.5
    opts, cid = mc_options(
        rng, ("Virhemarginaali puolittuu.", "Oikein: virhemarginaali on verrannollinen lukuun 1/√n ja √(100/400) = 1/2."),
        [("Virhemarginaali neljännekseen.", None, "Otoskoko nelinkertaistui, mutta marginaali riippuu neliöjuuresta: √4 = 2."),
         ("Todennäköisyys, että todellinen arvo on välillä, kasvaa 95 %:sta lähelle 100 %:a.", "LSTA-04",
          "Luottamustaso pysyy 95 %:ssa. Suurempi otos kapeuttaa väliä, ei muuta menetelmän luottamustasoa.")])
    items.append(base_item(TID, CODE, start + 2, ["MAB9.04"], ["G3"], "MAB", "T", "none",
                           "Kyselyn otoskoko kasvatetaan 100:sta 400:aan ja muut asiat pysyvät ennallaan. Mitä tapahtuu 95 %:n virhemarginaalille?",
                           {"options": opts, "correct": [cid]},
                           ["Virhemarginaali on verrannollinen lukuun 1/√n.", "√(100/400) = 1/2, joten marginaali puolittuu."], "Puolittuu", "Oikein.",
                           TEMPLATE, {"n1": n1, "n2": n2}, date, run, generic_wrong=GENERIC))
    # 4: count of covering intervals
    k, conf = 40, 0.95
    right = round(k * conf)
    assert right == 38
    opts, cid = mc_options(
        rng, (f"Noin {right}", "Oikein: 0,95 · 40 = 38."),
        [(f"Kaikki {k}, koska jokaisen välin todennäköisyys on 95 %", TID, "Prosentti kuvaa menetelmän onnistumista toistoissa; noin 5 % väleistä jää todellisen arvon ohi."),
         (f"Noin {k - right}", None, "Tämä on ohi menevien välien määrä (5 %), ei peittävien.")])
    items.append(base_item(TID, CODE, start + 3, ["MAB9.04"], ["G3"], "MAB", "T", "none",
                           f"Tutkija poimii {k} erillistä satunnaisotosta samasta väestöstä ja laskee jokaisesta 95 %:n luottamusvälin keskiarvolle. Noin kuinka moni välistä sisältää väestön todellisen keskiarvon?",
                           {"options": opts, "correct": [cid]},
                           ["Menetelmä onnistuu noin 95 %:ssa toistoista.", "0,95 · 40 = 38."], str(right), "Oikein.",
                           TEMPLATE, {"k": k, "conf": conf}, date, run, generic_wrong=GENERIC))
    # 5: plausibility, poll
    p, m = 48, 3
    lo, hi = p - m, p + m
    assert lo <= 50 <= hi
    opts, cid = mc_options(
        rng, (f"Kyllä: 50 % kuuluu väliin {lo}–{hi} %, joten tulos ei sulje sitä pois.", "Oikein."),
        [("Ei: todellinen kannatus on alle 50 % 95 %:n todennäköisyydellä.", "LSTA-04",
          "Tällainen todennäköisyys todelliselle arvolle ei seuraa luottamusvälistä."),
         ("Ei: otoksessa kannatus oli 48 %, ei 50 %.", None, "Otososuus ja todellinen osuus voivat poiketa toisistaan virhemarginaalin verran.")])
    items.append(base_item(TID, CODE, start + 4, ["MAB9.04"], ["G3", "G8"], "MAB", "P", "none",
                           f"Kyselyn mukaan {p} % kannattaa ehdotusta, ja 95 %:n virhemarginaali on ±{m} %-yksikköä. Voiko todellinen kannatus olla 50 %? Perustele.",
                           {"options": opts, "correct": [cid]},
                           [f"Väli on {lo}–{hi} %.", "50 % kuuluu väliin, joten se on mahdollinen."], "Kyllä", "Oikein.",
                           TEMPLATE, {"p": p, "m": m}, date, run, generic_wrong=GENERIC))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
