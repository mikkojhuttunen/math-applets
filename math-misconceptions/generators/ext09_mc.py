#!/usr/bin/env python3
"""EXT-09 (slope and intercept confused; steeper line means larger y), type MC. Lines are y = m x + b with integer
m and b; every option is computed from the same m and b. The tagged wrong options read the intercept as the slope
(or the slope as the intercept) or judge steepness by the size of y."""
import random

from gen_common import MINUS, base_item, cli, mc_options, num

TEMPLATE = "ext09_mc"
TID, CODE = "EXT-09", "MC"
BAD_SLOPE = ("Kulmakerroin on x:n kerroin, ei vakiotermi. Suoralla y = mx + b luku m kertoo, kuinka paljon y muuttuu, "
             "kun x kasvaa yhdellä, ja b on y:n arvo kohdassa x = 0.")
BAD_STEEP = ("Jyrkkyyden kertoo kulmakerroin, ei se, kumman suoran y-arvot ovat suurempia. Vakiotermi siirtää suoraa "
             "ylös tai alas mutta ei muuta sen jyrkkyyttä.")
GOOD = "Oikein: kulmakerroin on x:n kerroin ja vakiotermi on suoran ja y-akselin leikkauskohta."


def eq(m, b):
    mx = ("" if m == 1 else MINUS if m == -1 else num(m)) + "x"
    return f"y = {mx} {'+' if b > 0 else MINUS} {abs(b)}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(1901)
    items = []
    for k in range(count):
        m, b = rng.choice([2, 3, 4, 5]), rng.choice([1, 2, 6, 7, 8, 9])
        if k == 1:
            m = -rng.choice([2, 3, 4])
        if k == 0:
            prompt = f"Suoran yhtälö on {eq(m, b)}. Mikä on suoran kulmakerroin?"
            correct = (num(m), f"Oikein: kulmakerroin on x:n kerroin, {num(m)}.")
            wrongs = [(num(b), TID, BAD_SLOPE), (num(m + b), None, "Kulmakerrointa ei saa summaamalla luvuista."),
                      (num(-m), None, "Kulmakerroin on x:n kerroin sellaisenaan.")]
            steps = [f"Yhtälö on muotoa y = mx + b, ja tässä m = {num(m)}", f"Vakiotermi {b} kertoo leikkauskohdan, ei kulmakerrointa"]
            final, level = num(m), "T"
        elif k == 1:
            prompt = f"Suoran yhtälö on y = {b} {MINUS} {abs(m)}x. Mikä on suoran kulmakerroin?"
            correct = (num(m), f"Oikein: x:n kerroin on {num(m)}, joten suora laskee.")
            wrongs = [(num(b), TID, BAD_SLOPE), (str(abs(m)), None, "Kulmakertoimen merkki kuuluu x:n kertoimeen: suora laskee."),
                      (num(b - abs(m)), None, "Kulmakerrointa ei saa vähentämällä luvuista.")]
            steps = [f"Kirjoitetaan muotoon y = {num(m)}x + {b}", f"Kulmakerroin on {num(m)}"]
            final, level = num(m), "T"
        elif k == 2:
            prompt = f"Mihin kohtaan suora {eq(m, b)} leikkaa y-akselin?"
            correct = (f"(0, {b})", f"Oikein: kun x = 0, y = {b}.")
            wrongs = [(f"({m}, 0)", TID, BAD_SLOPE), (f"({b}, 0)", None, "Leikkauspiste y-akselin kanssa on muotoa (0, y)."),
                      (f"(0, {m})", None, "Kun x = 0, termi mx katoaa ja jäljelle jää vakiotermi.")]
            steps = [f"Sijoitetaan x = 0: y = {m} · 0 + {b} = {b}"]
            final, level = f"(0, {b})", "T"
        elif k == 3:
            m2 = m + rng.choice([2, 3])
            b2 = b + rng.choice([4, 5, 6])
            prompt = f"Suorat ovat {eq(m, b2)} ja {eq(m2, b)}. Kumpi suora nousee jyrkemmin?"
            first, second = eq(m, b2), eq(m2, b)
            correct = (f"Suora {second}, koska sen kulmakerroin {m2} on suurempi", f"Oikein: {m2} > {m}, joten toinen suora nousee jyrkemmin.")
            wrongs = [(f"Suora {first}, koska sen y-arvot ovat suurempia", TID, BAD_STEEP),
                      ("Suorat nousevat yhtä jyrkästi", None, "Suorien kulmakertoimet ovat eri suuria."),
                      (f"Suora {first}, koska sen vakiotermi {b2} on suurempi", TID, BAD_STEEP)]
            steps = [f"Kulmakertoimet ovat {m} ja {m2}", f"Suurempi kulmakerroin {m2} tarkoittaa jyrkempää nousua"]
            final, level = second, "H"
        else:
            m2 = m + rng.choice([2, 3])
            b2 = b + rng.choice([4, 5, 6])
            prompt = (f"Oppilas väittää: ”Suora {eq(m, b2)} on jyrkempi kuin suora {eq(m2, b)}, koska sen y-arvot ovat "
                      f"aina suurempia.” Mikä väite on oikein?")
            correct = (f"Väite on väärin: jyrkkyyden kertoo kulmakerroin, ja suoran {eq(m2, b)} kulmakerroin {m2} on suurempi",
                       GOOD)
            wrongs = [("Väite on oikein, koska suurempi y-arvo tarkoittaa jyrkempää suoraa", TID, BAD_STEEP),
                      ("Väite on oikein, koska suoran vakiotermi on suurempi", TID, BAD_STEEP),
                      ("Suorien jyrkkyyttä ei voi verrata yhtälöistä", None, "Jyrkkyyden voi lukea kulmakertoimesta.")]
            steps = [f"Kulmakertoimet ovat {m} ja {m2}", f"Kun x on suuri, suoran {eq(m2, b)} y-arvot ohittavat toisen suoran"]
            final, level = "Väite on väärin", "H"
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S4.05"], ["T15"], 8, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final, GOOD, TEMPLATE,
                               {"m": m, "b": b, "form": k}, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
