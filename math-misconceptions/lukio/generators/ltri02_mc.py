#!/usr/bin/env python3
"""LTRI-02 MC (lukio level): sine treated as a factor that can be split. Values are computed with
sympy; each wrong option that pulls the argument's coefficient in front of sin carries the topic tag."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "ltri02_mc"
TID, CODE = "LTRI-02", "MC"
GENERIC = "Sini ei ole tekijä, jonka voi jakaa: sin 2x ≠ 2 sin x. Kokeile lukuarvolla tai käytä kaksoiskulmakaavaa."
X = sp.Symbol("x")


def make_items(run, date, count=5, start=1):
    rng = random.Random(2310)
    items = []

    def add(n, level, prompt, correct, wrongs, steps, final, params):
        opts, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, n, ["MAA5.03"], ["G2"], "MAA", level, "none", prompt,
                               {"options": opts, "correct": [cid]}, steps, final, "Oikein.", TEMPLATE, params, date, run,
                               generic_wrong=GENERIC))

    # 1: identity
    assert sp.simplify(sp.expand_trig(sp.sin(2 * X)) - 2 * sp.sin(X) * sp.cos(X)) == 0
    assert sp.simplify(sp.sin(2 * X) - 2 * sp.sin(X)) != 0
    add(start, "P", "Mikä seuraavista on voimassa kaikilla x?",
        ("sin 2x = 2 sin x cos x", "Oikein: tämä on sinin kaksoiskulmakaava."),
        [("sin 2x = 2 sin x", TID, "Kerroin 2 ei siirry sinin eteen. Kokeile x = 30°: sin 60° ≈ 0,87, mutta 2 sin 30° = 1."),
         ("sin 2x = sin x + 2", None, "Kokeile x = 0: vasen puoli on 0, oikea on 2."),
         ("sin 2x = sin² x", None, "Kokeile x = 90°: vasen puoli on 0, oikea on 1.")],
        ["Kaksoiskulmakaava: sin 2x = 2 sin x cos x.", "Tarkistus x = 30°: sin 60° = 2 · (1/2) · (√3/2) = √3/2."], "sin 2x = 2 sin x cos x", {})
    # 2: value at x = 30 degrees
    x0 = sp.pi / 6
    v = sp.simplify(sp.sin(2 * x0))
    w = sp.simplify(2 * sp.sin(x0))
    assert v == sp.sqrt(3) / 2 and w == 1
    add(start + 1, "P", "Kun x = 30°, mikä on sin 2x?",
        (f"{show(v)} ≈ 0,87", "Oikein: sin 60° = √3/2."),
        [("1", TID, "Tämä on 2 sin 30°. Kulma kaksinkertaistuu sinin sisällä, ja sin 60° ≠ 2 · sin 30°."),
         ("1/4", None, "Tämä on sin² 30°, ei sin 60°."),
         ("√3/4", None, "Tämä on sin 30° · cos 30°, eli puolet oikeasta arvosta.")],
        ["2x = 60°.", "sin 60° = √3/2 ≈ 0,87."], f"{show(v)}", {"x_deg": 30})
    # 3: plausibility of sin 3x = 3 sin x
    x0 = sp.pi / 6
    assert 3 * sp.sin(x0) == sp.Rational(3, 2) and sp.sin(3 * x0) == 1
    add(start + 2, "T", "Oppilas väittää, että sin 3x = 3 sin x kaikilla x. Kun x = π/6, väite antaisi arvon 3/2. Mikä perustelu osoittaa väitteen vääräksi?",
        ("Sinin arvo on korkeintaan 1, mutta 3 sin(π/6) = 1,5. Siksi väite ei voi päteä.", "Oikein: yksi vastaesimerkki riittää."),
        [("Väite on tosi, koska 3 on vakio ja sen voi siirtää sinin eteen.", TID, "Sinifunktiossa kerroin argumentissa ei ole sinin kerroin. Sinin arvo ei voi olla 1,5."),
         ("Väite on tosi, jos x on radiaaneina.", "LTRI-03", "Yksikkö ei muuta asiaa. Sinin arvo on aina välillä −1 ja 1."),
         ("Väite on väärä vain, koska sin(π/6) on murtoluku.", None, "Murtoluvulla ei ole merkitystä. Ristiriita syntyy siitä, että tulos ylittää 1.")],
        ["sin(3 · π/6) = sin(π/2) = 1.", "3 sin(π/6) = 3 · 1/2 = 3/2 > 1, mikä on mahdotonta sinin arvolle."], "Vastaesimerkki x = π/6", {"x": "pi/6"})
    # 4: simplify sin x / x
    add(start + 3, "T", "Sievennä lauseke (sin x)/x, kun x ≠ 0.",
        ("Lauseketta ei voi sieventää: (sin x)/x on sellaisenaan yksinkertaisin muoto.", "Oikein: sin x ei ole tulo sin · x."),
        [("sin", TID, "Sini ei ole tekijä sin · x, joten x ei supistu pois."),
         ("1", TID, "Tämä olisi tosi vain, jos sin x olisi sama kuin x. Kokeile x = π/2: (sin x)/x = 2/π ≈ 0,64."),
         ("0", None, "Kokeile x = π/2: (sin x)/x = 2/π ≠ 0.")],
        ["sin x on funktion arvo, ei kertoja.", "Tarkistus x = π/2: (sin x)/x = 1/(π/2) = 2/π ≈ 0,64."], "Ei sievene", {})
    # 5: when does sin 2x = 2 sin x hold
    sol = sp.solveset(sp.Eq(sp.sin(2 * X), 2 * sp.sin(X)), X, sp.Interval(0, 2 * sp.pi))
    assert sol == sp.FiniteSet(0, sp.pi, 2 * sp.pi)
    add(start + 4, "K", "Oppilas väittää, että sin 2x = 2 sin x kaikilla x. Millä x:n arvoilla yhtälö todella on tosi?",
        ("Vain kun sin x = 0, eli x = nπ (n kokonaisluku).", "Oikein: 2 sin x cos x = 2 sin x pätee, kun sin x = 0 tai cos x = 1, ja kumpikin johtaa arvoihin x = nπ."),
        [("Kaikilla x.", TID, "Väite pätee vain erikoistapauksissa. Esimerkiksi x = 30°: sin 60° ≈ 0,87, mutta 2 sin 30° = 1."),
         ("Vain kun x = π/2 + nπ.", None, "Näissä pisteissä cos x = 0, jolloin sin 2x = 0 mutta 2 sin x = ±2."),
         ("Millään x:n arvolla.", None, "Esimerkiksi x = 0 toteuttaa yhtälön: sin 0 = 0 = 2 sin 0.")],
        ["sin 2x = 2 sin x cos x, joten 2 sin x cos x = 2 sin x.", "2 sin x (cos x − 1) = 0, joten sin x = 0 tai cos x = 1.", "Molemmat johtavat arvoihin x = nπ."],
        "x = nπ", {})
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
