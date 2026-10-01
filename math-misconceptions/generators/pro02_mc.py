#!/usr/bin/env python3
"""PRO-02 (illusion of linearity: volume), type MC. Options are computed from the same scale factor k."""
import random

from gen_common import base_item, cli, mc_options

TEMPLATE = "pro02_mc"
TID, CODE = "PRO-02", "MC"
LIN = "Tilavuus ei kasva samassa suhteessa kuin pituudet. Kuutiolla on kolme ulottuvuutta, joten tilavuus muuttuu kertoimella k³."
SQ = "Kertoimella k² muuttuu pinta-ala, ei tilavuus. Tilavuudessa kasvaa myös kolmas ulottuvuus."


def alt(k):
    """A second linear-looking guess that never equals k² (k=2: 3k; otherwise 2k)."""
    return 3 * k if k == 2 else 2 * k


def times(n):
    return f"{n}-kertainen"


def make_items(run, date, count=5, start=1):
    rng = random.Random(631)
    items = []
    ks = rng.sample([2, 3, 4], 3) + [rng.choice([2, 3]), 2]
    for n in range(count):
        k = ks[n]
        k3 = k ** 3
        if n == 0:
            level = "T"
            s = rng.randint(2, 5)
            prompt = f"Kuution särmä {s} cm kasvatetaan {k}-kertaiseksi. Kuinka moninkertaiseksi kuution tilavuus muuttuu?"
            ok = (times(k3), f"Oikein: tilavuus muuttuu k³-kertaiseksi, eli {k}³ = {k3}.")
            wrongs = [(times(k), "PRO-02", LIN), (times(alt(k)), "PRO-02", LIN), (times(k * k), None, SQ)]
            steps = [f"Alkuperäinen tilavuus {s}³ = {s ** 3} cm³", f"Uusi tilavuus {k * s}³ = {(k * s) ** 3} cm³", f"{(k * s) ** 3} / {s ** 3} = {k3}"]
            final, params = times(k3), {"k": k, "edge": s}
        elif n == 1:
            level = "T"
            a, b, c = rng.randint(2, 4), rng.randint(3, 5), rng.randint(2, 6)
            prompt = f"Suorakulmaisen särmiön mitat ovat {a} cm, {b} cm ja {c} cm. Jokainen mitta kasvatetaan {k}-kertaiseksi. Kuinka moninkertaiseksi tilavuus muuttuu?"
            ok = (times(k3), f"Oikein: {k * a} · {k * b} · {k * c} = {k3} · {a * b * c}.")
            wrongs = [(times(k), "PRO-02", LIN), (times(alt(k)), "PRO-02", LIN), (times(k * k), None, SQ)]
            steps = [f"Alkuperäinen tilavuus {a} · {b} · {c} = {a * b * c} cm³", f"Uusi tilavuus {k * a} · {k * b} · {k * c} = {k3 * a * b * c} cm³", f"{k3 * a * b * c} / {a * b * c} = {k3}"]
            final, params = times(k3), {"k": k, "a": a, "b": b, "c": c}
        elif n == 2:
            level = "T"
            vol = rng.choice([20, 30, 40, 50])
            prompt = (f"Pienoismallin tilavuus on {vol} cm³. Oikea esine on muodoltaan samanlainen, ja sen jokainen mitta on {k}-kertainen pienoismalliin verrattuna. "
                      "Mikä on esineen tilavuus?")
            ok = (f"{vol * k3} cm³", f"Oikein: {vol} · {k}³ = {vol * k3}.")
            wrongs = [(f"{vol * k} cm³", "PRO-02", LIN), (f"{vol + k} cm³", "PRO-02", LIN), (f"{vol * k * k} cm³", None, SQ)]
            steps = [f"Tilavuuden kerroin {k}³ = {k3}", f"{vol} · {k3} = {vol * k3}"]
            final, params = f"{vol * k3} cm³", {"k": k, "volume": vol}
        elif n == 3:
            level = "H"
            l = rng.choice([1, 2, 3])
            prompt = (f"Pieneen kuutionmuotoiseen astiaan mahtuu {l} l vettä. Toinen kuutionmuotoinen astia on {k}-kertainen joka suunnassa. "
                      "Kuinka monta litraa vettä siihen mahtuu?")
            ok = (f"{l * k3} l", f"Oikein: tilavuus on {k3}-kertainen, joten {l} · {k3} = {l * k3} l.")
            wrongs = [(f"{l * k} l", "PRO-02", LIN), (f"{l + k} l", "PRO-02", LIN), (f"{l * k * k} l", None, SQ)]
            steps = [f"Tilavuuden kerroin {k}³ = {k3}", f"{l} · {k3} = {l * k3}"]
            final, params = f"{l * k3} l", {"k": k, "litres": l}
        else:
            level = "H"
            prompt = f"Kappaleen kaikki pituudet kasvatetaan {k}-kertaisiksi. Miksi tilavuus ei ole silloin {k}-kertainen?"
            ok = (f"Tilavuudessa on kolme ulottuvuutta (pituus, leveys, korkeus), joten se on {k}³ = {k3}-kertainen.", "Oikein: tilavuus riippuu kolmesta pituudesta.")
            wrongs = [(f"Tilavuus on aina {k}-kertainen, kun pituudet ovat {k}-kertaiset.", "PRO-02", LIN),
                      ("Tilavuus ei muutu, kun kappaletta suurennetaan.", None, "Suurennettu kappale vie enemmän tilaa."),
                      (f"Tilavuus on {k * k}-kertainen, koska kappale kasvaa kahteen suuntaan.", None, SQ)]
            steps = ["Tilavuus = pituus · leveys · korkeus", f"Kaikki kolme kasvavat {k}-kertaisiksi, joten tilavuus kasvaa {k} · {k} · {k} = {k3}-kertaiseksi"]
            final, params = ok[0], {"k": k}
        options, cid = mc_options(rng, ok, wrongs)
        items.append(base_item(TID, CODE, start + n, ["S5.05"], ["T16", "T18"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: kun pituudet kasvavat k-kertaisiksi, tilavuus kasvaa k³-kertaiseksi.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
