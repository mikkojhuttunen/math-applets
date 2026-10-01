#!/usr/bin/env python3
"""PRO-01 (illusion of linearity: area), type MC. Options are computed from the same scale factor k."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "pro01_mc"
TID, CODE = "PRO-01", "MC"
LIN = "Mittakaavan kerroin k kertoo pituuksien muutoksen. Pinta-ala muuttuu kertoimella k², koska kuvio kasvaa sekä leveys- että korkeussuunnassa."


def times(n):
    return f"{n}-kertainen"


def make_items(run, date, count=5, start=1):
    rng = random.Random(621)
    items = []
    ks = rng.sample([2, 3, 4], 3) + [rng.choice([2, 3]), 2]
    for n in range(count):
        k = ks[n]
        if n == 0:
            level = "T"
            s = rng.randint(2, 6)
            prompt = f"Neliön sivu {s} cm kasvatetaan {k}-kertaiseksi. Kuinka moninkertaiseksi neliön pinta-ala muuttuu?"
            ok = (times(k * k), f"Oikein: pinta-ala muuttuu k²-kertaiseksi, eli {k}² = {k * k}.")
            wrongs = [(times(k), "PRO-01", LIN), (times(2 * k), "PRO-01", LIN), (times(k + k * k), None, "Tarkista: sivujen kerroin korotetaan toiseen potenssiin.")]
            steps = [f"Uusi sivu on {k * s} cm", f"Alkuperäinen ala {s}² = {s * s} cm², uusi ala {(k * s) ** 2} cm²", f"{(k * s) ** 2} / {s * s} = {k * k}"]
            final, params = times(k * k), {"k": k, "side": s}
        elif n == 1:
            level = "T"
            a, b = rng.randint(2, 5), rng.randint(6, 9)
            prompt = f"Suorakulmion mitat {a} cm ja {b} cm kaksinkertaistetaan molemmat {k}-kertaisiksi. Kuinka moninkertaiseksi pinta-ala muuttuu?"
            ok = (times(k * k), f"Oikein: {k * a} · {k * b} = {k * k} · {a * b}.")
            wrongs = [(times(k), "PRO-01", LIN), (times(2 * k), "PRO-01", LIN), (times(k * k * k), None, "Kolmas potenssi kuvaa tilavuutta, ei pinta-alaa.")]
            steps = [f"Alkuperäinen ala {a} · {b} = {a * b} cm²", f"Uusi ala {k * a} · {k * b} = {k * a * k * b} cm²", f"{k * a * k * b} / {a * b} = {k * k}"]
            final, params = times(k * k), {"k": k, "a": a, "b": b}
            prompt = prompt.replace("kaksinkertaistetaan molemmat ", "kasvatetaan molemmat ").replace("molemmat molemmat", "molemmat")
        elif n == 2:
            level = "T"
            area = rng.choice([30, 40, 50, 60])
            prompt = (f"Valokuvan pinta-ala on {area} cm². Kuva suurennetaan niin, että sen jokainen mitta on {k}-kertainen. "
                      "Mikä on suurennoksen pinta-ala?")
            ok = (f"{area * k * k} cm²", f"Oikein: {area} · {k}² = {area * k * k}.")
            wrongs = [(f"{area * k} cm²", "PRO-01", LIN), (f"{area + k} cm²", "PRO-01", LIN), (f"{area * k * k * k} cm²", None, "Pinta-alaan ei käytetä kolmatta potenssia.")]
            steps = [f"Pinta-alan kerroin on {k}² = {k * k}", f"{area} · {k * k} = {area * k * k}"]
            final, params = f"{area * k * k} cm²", {"k": k, "area": area}
        elif n == 3:
            level = "H"
            cans = rng.choice([1, 2])
            prompt = (f"Seinän maalaamiseen tarvitaan {cans} purkki{'a' if cans > 1 else ''} maalia. Toinen seinä on muodoltaan samanlainen, mutta sen jokainen mitta on {k}-kertainen. "
                      "Montako purkkia maalia toisen seinän maalaamiseen tarvitaan?")
            ok = (f"{cans * k * k}", f"Oikein: ala on {k * k}-kertainen, joten maalia tarvitaan {cans} · {k * k} = {cans * k * k} purkkia.")
            wrongs = [(f"{cans * k}", "PRO-01", LIN), (f"{cans + k}", "PRO-01", LIN), (f"{cans * k * k * k}", None, "Maalin tarve riippuu pinta-alasta eikä tilavuudesta.")]
            steps = [f"Pinta-alan kerroin {k}² = {k * k}", f"{cans} · {k * k} = {cans * k * k}"]
            final, params = str(cans * k * k), {"k": k, "cans": cans}
        else:
            level = "H"
            prompt = f"Kuvion kaikki pituudet kasvatetaan {k}-kertaisiksi. Miksi pinta-ala ei ole silloin {k}-kertainen?"
            ok = (f"Pinta-ala kasvaa sekä leveys- että korkeussuunnassa, joten se on {k}² = {k * k}-kertainen.", "Oikein: pinta-ala riippuu kahdesta pituudesta.")
            wrongs = [(f"Pinta-ala on aina {k}-kertainen, kun pituudet ovat {k}-kertaiset.", "PRO-01", LIN),
                      ("Pinta-ala ei muutu, kun kuviota suurennetaan.", None, "Suurennettu kuvio peittää suuremman alan."),
                      (f"Pinta-ala on {k}-kertainen, jos kuvio on neliö, mutta muuten ei.", "PRO-01", LIN)]
            steps = ["Ala = pituus · leveys", f"Molemmat kasvavat {k}-kertaisiksi, joten ala kasvaa {k} · {k} = {k * k}-kertaiseksi"]
            final, params = ok[0], {"k": k}
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + n, ["S5.05"], ["T16", "T18"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: kun pituudet kasvavat k-kertaisiksi, pinta-ala kasvaa k²-kertaiseksi.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
