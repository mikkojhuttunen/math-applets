#!/usr/bin/env python3
"""LDER-04 MC: graph of f' read as graph of f. Derivatives and signs are computed with sympy;
distractors read the height of f' as the height of f."""
import random

import sympy as sp

from gen_common import base_item, cli, mc_options, show

TEMPLATE = "lder04_mc"
TID, CODE = "LDER-04", "MC"
X = sp.Symbol("x")
GENERIC = "Derivaatan kuvaaja kertoo funktion kulmakertoimen: f′ > 0 tarkoittaa, että f kasvaa, ja f′ < 0, että f vähenee. Se ei kerro f:n korkeutta."


def disp(e):
    return show(sp.expand(e)).replace(" · ", "").replace("^2", "²").replace("^3", "³")


def sign_item(rng, n, d_val, lops, syll, level, date, run):
    """f'(x) = a - x^2 style: f' positive at d_val, so f is increasing there."""
    fp = 9 - X**2
    val = fp.subs(X, d_val)
    assert val > 0
    opts, cid = mc_options(
        rng, ("f on kasvava kohdassa x = " + show(d_val), f"Oikein: f′({show(d_val)}) = {show(val)} > 0, joten f kasvaa."),
        [("f on vähenevä kohdassa x = " + show(d_val), "LDER-04", "Positiivinen f′ ei tarkoita laskevaa funktiota. Derivaatan merkki kertoo kasvun suunnan."),
         ("f on positiivinen kohdassa x = " + show(d_val), "LDER-04", "f′:n merkki ei kerro f:n merkkiä. Päättele vain kasvusta tai vähenemisestä.")])
    return base_item(TID, CODE, n, [lops], ["G2"], syll, level, "none",
                     f"Funktion f derivaatta on f′(x) = 9 − x². Mitä tiedät f:stä kohdassa x = {show(d_val)}?",
                     {"options": opts, "correct": [cid]},
                     [f"f′({show(d_val)}) = 9 − {show(d_val**2)} = {show(val)}.", "f′ > 0, joten f on kasvava."],
                     f"f kasvaa kohdassa x = {show(d_val)}", "Oikein.", TEMPLATE, {"x": d_val}, date, run, generic_wrong=GENERIC)


def peak_item(rng, n, date, run):
    fp = 4 * X - X**2  # f' = 4x - x^2 peaks at x = 2
    peak = sp.solve(sp.diff(fp, X), X)[0]
    zeros = sorted(sp.solve(fp, X))
    assert peak == 2 and zeros == [0, 4]
    # f increases where f' > 0 -> on (0, 4); local max of f at x = 4
    fmax = sp.solve(fp, X)[-1]
    opts, cid = mc_options(
        rng, (f"x = {show(fmax)}", f"Oikein: f′ vaihtaa merkkiä plussasta miinukseen kohdassa x = {show(fmax)}, joten f:llä on siinä suurin arvo."),
        [(f"x = {show(peak)}", "LDER-04", f"Kohdassa x = {show(peak)} derivaatta on suurimmillaan, eli f kasvaa nopeimmin, mutta f ei ole vielä suurimmillaan."),
         ("x = 0", None, "Kohdassa x = 0 derivaatta vaihtaa merkkiä miinuksesta plussaan, joten f:llä on siinä pienin arvo.")])
    return base_item(TID, CODE, n, ["MAA6.08"], ["G2"], "MAA", "T", "none",
                     "Funktion f derivaatta on f′(x) = 4x − x². Derivaatan kuvaaja on alaspäin aukeava paraabeli, jonka huippu on kohdassa x = 2. Millä x:n arvolla f:llä on suurin arvo?",
                     {"options": opts, "correct": [cid]},
                     ["f′(x) = x(4 − x), nollakohdat 0 ja 4.", "f′ > 0, kun 0 < x < 4, ja f′ < 0, kun x > 4.", "f saa suurimman arvonsa kohdassa x = 4."],
                     f"x = {show(fmax)}", "Oikein.", TEMPLATE, {"fprime": str(fp)}, date, run, generic_wrong=GENERIC)


def speed_item(rng, n, date, run):
    # MAB: f(t) = height, f'(t) = growth speed of a plant's height in cm/day, f'(t) = 6 - t on [0, 5]
    t = sp.Symbol("t")
    fp = 6 - t
    assert fp.subs(t, 5) > 0 and sp.diff(fp, t) < 0
    opts, cid = mc_options(
        rng, ("Kasvi on päivänä 5 korkeampi kuin päivänä 4", "Oikein: nopeus on koko ajan positiivinen, joten korkeus kasvaa joka päivä, vaikka kasvunopeus pienenee."),
        [("Kasvi on päivänä 5 matalampi kuin päivänä 4, koska kuvaaja laskee", "LDER-04", "Laskeva kuvaaja kertoo, että kasvunopeus pienenee, ei että kasvin korkeus pienenee."),
         ("Kasvi lakkaa kasvamasta päivänä 5", "LDER-04", "Päivänä 5 kasvunopeus on 1 cm/vrk, joten kasvi kasvaa yhä.")])
    return base_item(TID, CODE, n, ["MAB8.03"], ["G2"], "MAB", "P", "none",
                     "Kasvin korkeuden muutosnopeus (cm/vrk) on f′(t) = 6 − t, kun 0 ≤ t ≤ 5. Kuvaaja on laskeva suora, mutta pysyy x-akselin yläpuolella. Mitä tämä kertoo kasvin korkeudesta?",
                     {"options": opts, "correct": [cid]},
                     ["f′(t) = 6 − t ≥ 1 > 0 koko välillä.", "Siis korkeus kasvaa joka päivä; vain kasvun nopeus hidastuu."],
                     "Korkeus kasvaa joka päivä", "Oikein.", TEMPLATE, {"fprime": str(fp)}, date, run, generic_wrong=GENERIC)


def negative_item(rng, n, date, run):
    fp = X**2 - 4  # f' < 0 on (-2, 2) -> f decreasing, f' < 0 doesn't mean f < 0
    assert fp.subs(X, 0) < 0
    opts, cid = mc_options(
        rng, ("f on vähenevä välillä −2 < x < 2, mutta f:n arvot voivat olla positiivisia", "Oikein: f′ < 0 kertoo vain, että f vähenee. Funktion arvo voi silti olla positiivinen."),
        [("f saa negatiivisia arvoja välillä −2 < x < 2", "LDER-04", "f′:n merkki ei kerro f:n merkkiä. Esimerkiksi f(x) = x³/3 − 4x + 20 on aina positiivinen tällä välillä."),
         ("f on kasvava välillä −2 < x < 2", "LDER-04", "f′ < 0 tarkoittaa vähenevää funktiota.")])
    return base_item(TID, CODE, n, ["MAB8.03"], ["G2"], "MAB", "H", "none",
                     "Funktion f derivaatta on f′(x) = x² − 4. Välillä −2 < x < 2 derivaatan kuvaaja on x-akselin alapuolella. Mikä väite pitää paikkansa?",
                     {"options": opts, "correct": [cid]},
                     ["f′(x) = x² − 4 < 0, kun −2 < x < 2.", "Siis f on vähenevä tällä välillä; f:n arvojen merkistä ei voi sanoa mitään."],
                     "f on vähenevä", "Oikein.", TEMPLATE, {"fprime": str(fp)}, date, run, generic_wrong=GENERIC)


def justify_item(rng, n, date, run):
    fp = 2 * X - 6
    zero = sp.solve(fp, X)[0]
    assert zero == 3
    opts, cid = mc_options(
        rng, ("f:llä on pienin arvo kohdassa x = 3, koska f′ vaihtaa merkkiä miinuksesta plussaan", "Oikein: f′ < 0, kun x < 3, ja f′ > 0, kun x > 3, joten f vähenee ja sitten kasvaa."),
        [("f on nolla kohdassa x = 3, koska f′(3) = 0", "LDER-04", "f′(3) = 0 kertoo vaakasuoran tangentin, ei sitä että f(3) = 0."),
         ("f:llä on suurin arvo kohdassa x = 3, koska f′ on siinä nollassa", "LDER-03", "Nollakohta ei yksin kerro, onko kyse suurimmasta vai pienimmästä arvosta; tarkista merkinvaihto.")])
    return base_item(TID, CODE, n, ["MAA6.08"], ["G2"], "MAA", "K", "none",
                     "Funktion f derivaatta on f′(x) = 2x − 6. Perustele, mitä f:lle tapahtuu kohdassa x = 3.",
                     {"options": opts, "correct": [cid]},
                     ["f′(x) = 2(x − 3), nollakohta x = 3.", "x < 3: f′ < 0, f vähenee. x > 3: f′ > 0, f kasvaa.", "Kohdassa x = 3 f:llä on pienin arvo."],
                     "Pienin arvo kohdassa x = 3", "Oikein.", TEMPLATE, {"fprime": str(fp)}, date, run,
                     misconceptions=[TID, "LDER-03"], generic_wrong=GENERIC)


def make_items(run, date, count=5, start=1):
    rng = random.Random(4103)
    items = [sign_item(rng, start, 1, "MAA6.08", "MAA", "P", date, run), peak_item(rng, start + 1, date, run),
             speed_item(rng, start + 2, date, run), negative_item(rng, start + 3, date, run), justify_item(rng, start + 4, date, run)]
    return items[:count]


if __name__ == "__main__":
    cli(make_items, TID, CODE)
