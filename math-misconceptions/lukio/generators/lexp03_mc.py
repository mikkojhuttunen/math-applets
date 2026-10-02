#!/usr/bin/env python3
"""LEXP-03 MC: exponential growth judged as linear. Growth factors computed with sympy."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, num

TEMPLATE = "lexp03_mc"
TID, CODE = "LEXP-03", "MC"
GENERIC = "Prosentuaalinen kasvu kertautuu: joka vuosi muutos lasketaan edellisen vuoden arvosta, ei alkuarvosta."


def pct(x, nd=0):
    return num(round(float(x), nd) if nd else int(round(float(x))))


def item(n, lops, syll, level, g, prompt, correct, wrongs, steps, final, params, date, run, rng):
    opts, cid = mc_options(rng, correct, wrongs)
    return base_item(TID, CODE, n, lops, g, syll, level, "none", prompt, {"options": opts, "correct": [cid]},
                     steps, final, "Oikein.", TEMPLATE, params, date, run, generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(4302)
    items = []
    # 1: 3 % for 20 years
    r, n = sp.Rational(3, 100), 20
    growth = (1 + r) ** n - 1
    lin = r * n
    items.append(item(start, ["MAB4.02"], "MAB", "T", ["G5"],
                      f"Hinta nousee {pct(r * 100)} % vuodessa. Kuinka monta prosenttia hinta on noussut {n} vuodessa?",
                      (f"Noin {pct(growth * 100)} %", f"Oikein: 1,03^{n} ≈ {num(round(float(1 + growth), 2))}, joten nousu on noin {pct(growth * 100)} %."),
                      [(f"{pct(lin * 100)} %", TID, "Tämä olettaa saman euromääräisen nousun joka vuosi. Korko kertautuu: kerroin on 1,03^20."),
                       (f"Noin {pct(growth * 100 / 2)} %", None, "Kerroin 1,03 korotetaan potenssiin 20, ei jaeta.")],
                      [f"Vuosikerroin on 1 + {num(float(r))} = {num(float(1 + r))}.", f"{n} vuodessa kerroin on {num(float(1 + r))}^{n} ≈ {num(round(float(1 + growth), 2))}."],
                      f"Noin {pct(growth * 100)} %", {"rate": str(r), "years": n}, date, run, rng))
    # 2: doubling time at 7 %
    r = sp.Rational(7, 100)
    t = float(sp.log(2) / sp.log(1 + r))
    assert 10 < t < 11
    items.append(item(start + 1, ["MAB4.02"], "MAB", "P", ["G5"],
                      f"Väkiluku kasvaa {pct(r * 100)} % vuodessa. Noin kuinka monessa vuodessa väkiluku kaksinkertaistuu?",
                      ("Noin 10 vuodessa", "Oikein: 1,07^10 ≈ 1,97, joten väkiluku on kymmenessä vuodessa lähes kaksinkertainen."),
                      [(f"Noin {pct(100 / (r * 100))} vuodessa", TID, "100 / 7 olettaa lineaarisen kasvun. Kasvu kertautuu, joten aikaa kuluu vähemmän."),
                       ("Noin 7 vuodessa", None, "Kokeile: 7 vuodessa kerroin on 1,07^7 ≈ 1,6, ei vielä 2.")],
                      ["Kokeillaan: 1,07^10 ≈ 1,97 ja 1,07^11 ≈ 2,10."], "Noin 10 vuodessa", {"rate": str(r)}, date, run, rng))
    # 3: doubling bacteria, MAA
    n0, h = 1000, 6
    right = n0 * 2**h
    lin = n0 + h * n0
    items.append(item(start + 2, ["MAA5.06"], "MAA", "P", ["G5"],
                      f"Bakteeriviljelmässä on aluksi {n0} bakteeria, ja määrä kaksinkertaistuu tunnissa. Montako bakteeria on {h} tunnin kuluttua?",
                      (num(right), f"Oikein: {n0} · 2^{h} = {right}."),
                      [(num(lin), TID, "Tämä lisää saman määrän joka tunti. Kaksinkertaistuminen kertoo määrän luvulla 2 joka tunti."),
                       (num(n0 * 2 * h), None, "Kaksinkertaistuminen tunnissa tarkoittaa kerrointa 2^6, ei 2 · 6.")],
                      [f"Kerroin on 2^{h} = {2**h}.", f"{n0} · {2**h} = {right}."], num(right), {"n0": n0, "h": h}, date, run, rng))
    # 4: 50 % for 4 years, MAA
    r, n = sp.Rational(1, 2), 4
    growth = (1 + r) ** n - 1
    lin = r * n
    items.append(item(start + 3, ["MAA5.06"], "MAA", "T", ["G4"],
                      f"Yrityksen liikevaihto kasvaa {pct(r * 100)} % vuodessa neljä vuotta peräkkäin. Kuinka monta prosenttia liikevaihto on silloin kasvanut yhteensä?",
                      (f"Noin {pct(growth * 100)} %", "Oikein: 1,5^4 ≈ 5,06, joten kasvu on noin 406 %."),
                      [(f"{pct(lin * 100)} %", TID, "4 · 50 % olettaa lineaarisen kasvun. Joka vuosi 50 % lasketaan jo kasvaneesta liikevaihdosta."),
                       (f"{pct(lin * 100 + 100)} %", None, "Vuosikerroin 1,5 kertautuu: 1,5^4, ei 1 + 4 · 0,5.")],
                      ["Vuosikerroin on 1,5.", "1,5^4 = 5,0625, joten kasvu on 4,0625 eli noin 406 %."],
                      f"Noin {pct(growth * 100)} %", {"rate": str(r), "years": n}, date, run, rng))
    # 5: plausibility check of estimate, MAB
    p, r, n = 2000, sp.Rational(4, 100), 25
    final = p * (1 + r) ** n
    lin_est = p * (1 + r * n)
    assert final > lin_est
    items.append(item(start + 4, ["MAB4.02", "MAB7.01"], "MAB", "H", ["G4"],
                      f"Sijoitat {num(p)} € vuosikorolla {pct(r * 100)} %, ja korko liitetään pääomaan joka vuosi. Arvioit {n} vuoden päästä, että pääoma on kaksinkertaistunut ({num(lin_est)} €). Mitä arviostasi voi sanoa?",
                      ("Arvio on liian pieni, koska korkoa saa myös aiemmin kertyneelle korolle", f"Oikein: 2000 · 1,04^25 ≈ {num(int(round(float(final), -1)))} €."),
                      [("Arvio on oikea, koska 25 · 4 % = 100 %", TID, "Tämä olettaa, että korkoa maksetaan vain alkupääomalle. Kun korko liitetään pääomaan, kasvu kertautuu."),
                       ("Arvio on liian suuri, koska korko pienenee ajan myötä", None, "Korkoprosentti ei pienene. Korkoa lasketaan kasvavalle pääomalle.")],
                      ["Vuosikerroin on 1,04.", f"1,04^25 ≈ {num(round(float((1 + r) ** n), 2))}, joten pääoma on noin {num(int(round(float(final), -1)))} €."],
                      "Arvio on liian pieni", {"p": p, "rate": str(r), "years": n}, date, run, rng))
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
