#!/usr/bin/env python3
"""PRB-02 (more black marbles means higher chance), type MC. Proportions are computed with Fraction."""
import random
from fractions import Fraction

from gen_common import base_item, cli, mc_options

TEMPLATE = "prb02_mc"
TID, CODE = "PRB-02", "MC"
BAD = ("Todennäköisyys ei riipu pelkästä mustien kuulien lukumäärästä vaan niiden osuudesta kaikista kuulista. "
       "Vertaa osuuksia, esimerkiksi sieventämällä murtoluvut.")


def fr(f):
    return f"{f.numerator}/{f.denominator}"


def make_items(run, date, count=5, start=1):
    rng = random.Random(903)
    items, seen = [], set()
    for k in range(count):
        if k == 0:
            a, b = rng.choice([(3, 4), (2, 5), (3, 5), (1, 4)])
            m = rng.choice([2, 3])
            p = Fraction(a, b)
            assert Fraction(a * m, b * m) == p
            prompt = (f"Purkissa 1 on {a * m} mustaa kuulaa {b * m}:stä. Purkissa 2 on {a} mustaa kuulaa {b}:stä. "
                      "Kummasta purkista on parempi mahdollisuus nostaa musta kuula?")
            correct = (f"Mahdollisuus on sama, {fr(p)}", f"Oikein: molemmissa mustien osuus on {fr(p)}.")
            wrongs = [("Purkista 1, koska siinä on enemmän mustia kuulia", "PRB-02", BAD),
                      ("Purkista 2, koska siinä on vähemmän kuulia", None, "Kuulien kokonaismäärä yksin ei ratkaise: vertaa mustien osuutta."),
                      ("Sitä ei voi tietää", None, "Osuudet voidaan laskea ja verrata.")]
            steps = [f"{a * m}/{b * m} = {fr(p)}", f"{a}/{b} = {fr(p)}"]
            final, params, level = "Yhtä hyvä", {"a": a, "b": b, "k": m}, "T"
        elif k == 1:
            while True:
                b1, b2 = rng.choice([8, 10, 12, 20]), rng.choice([4, 5, 6, 10])
                a1, a2 = rng.randint(2, b1 - 1), rng.randint(1, b2 - 1)
                if a1 > a2 and Fraction(a1, b1) < Fraction(a2, b2):
                    break
            p1, p2 = Fraction(a1, b1), Fraction(a2, b2)
            prompt = (f"Purkissa 1 on {a1} mustaa kuulaa {b1}:stä. Purkissa 2 on {a2} mustaa kuulaa {b2}:sta. "
                      "Kummasta purkista on parempi mahdollisuus nostaa musta kuula?")
            correct = ("Purkista 2", f"Oikein: {fr(p2)} > {fr(p1)}.")
            wrongs = [("Purkista 1, koska siinä on enemmän mustia kuulia", "PRB-02", BAD),
                      ("Molemmista yhtä hyvä", None, f"Osuudet ovat {fr(p1)} ja {fr(p2)}, eli eri suuret."),
                      ("Sitä ei voi tietää", None, "Osuudet voidaan laskea ja verrata.")]
            steps = [f"{a1}/{b1} = {float(p1):.3f}".replace(".", ","), f"{a2}/{b2} = {float(p2):.3f}".replace(".", ","), "Purkin 2 osuus on suurempi"]
            final, params, level = "Purkki 2", {"a1": a1, "b1": b1, "a2": a2, "b2": b2}, "T"
        elif k == 2:
            while True:
                n1, n2 = rng.choice([24, 30, 20, 36]), rng.choice([10, 12, 15, 9])
                g1, g2 = rng.randint(3, n1 - 1), rng.randint(2, n2 - 1)
                if g1 > g2 and Fraction(g1, n1) < Fraction(g2, n2):
                    break
            p1, p2 = Fraction(g1, n1), Fraction(g2, n2)
            prompt = (f"Luokalla 8A on {n1} oppilasta, joista {g1} on pelannut lätkää. Luokalla 8B on {n2} oppilasta, "
                      f"joista {g2} on pelannut lätkää. Kummalta luokalta arvotulla oppilaalla on suurempi todennäköisyys olla lätkänpelaaja?")
            correct = ("Luokalta 8B", f"Oikein: {fr(p2)} > {fr(p1)}.")
            wrongs = [("Luokalta 8A, koska siellä on enemmän lätkänpelaajia", "PRB-02", BAD),
                      ("Todennäköisyydet ovat samat", None, f"Osuudet ovat {fr(p1)} ja {fr(p2)}, eli eri suuret."),
                      ("Luokalta 8A, koska siellä on enemmän oppilaita", None, "Suurempi luokka ei tee osuudesta suurempaa.")]
            steps = [f"8A: {g1}/{n1} = {float(p1):.3f}".replace(".", ","), f"8B: {g2}/{n2} = {float(p2):.3f}".replace(".", ","), "8B:n osuus on suurempi"]
            final, params, level = "8B", {"g1": g1, "n1": n1, "g2": g2, "n2": n2}, "T"
        elif k == 3:
            r, w = rng.choice([(6, 2), (9, 3), (8, 2)])
            add = rng.choice([4, 6])
            p0, p1 = Fraction(r, r + w), Fraction(r + add, r + w + 2 * add)
            assert p1 < p0
            prompt = (f"Pussissa on {r} punaista ja {w} sinistä kuulaa. Pussiin lisätään {add} punaista ja {add} sinistä kuulaa. "
                      "Mitä tapahtuu todennäköisyydelle nostaa punainen kuula?")
            correct = (f"Se pienenee: {fr(p0)} → {fr(p1)}", f"Oikein: {r + add}/{r + w + 2 * add} = {fr(p1)} < {fr(p0)}.")
            wrongs = [("Se kasvaa, koska punaisia kuulia on nyt enemmän", "PRB-02", BAD),
                      ("Se pysyy samana, koska kumpaakin lisättiin saman verran", None, "Lisäys muuttaa osuutta, koska kuulia oli eri määrät."),
                      ("Sitä ei voi päätellä", None, "Uudet osuudet voidaan laskea.")]
            steps = [f"Ennen: {r}/{r + w} = {fr(p0)}", f"Jälkeen: {r + add}/{r + w + 2 * add} = {fr(p1)}"]
            final, params, level = "Pienenee", {"red": r, "blue": w, "add": add}, "H"
        else:
            m = rng.choice([2, 3])
            a, b = rng.choice([(3, 5), (2, 5)])
            p = Fraction(a, b)
            assert Fraction(a * 4 * m, b * 4 * m) == p
            prompt = (f"Purkissa 1 on {a * 4 * m} mustaa kuulaa {b * 4 * m}:stä. Purkissa 2 on {a} mustaa kuulaa {b}:stä. "
                      "Mikä päättely on oikea?")
            correct = (f"Mahdollisuudet ovat samat, koska mustien osuus on molemmissa {fr(p)}", f"Oikein: {a * 4 * m}/{b * 4 * m} = {a}/{b} = {fr(p)}.")
            wrongs = [("Purkki 1 on parempi, koska siinä on enemmän mustia kuulia", "PRB-02", BAD),
                      ("Purkki 2 on parempi, koska siinä on vähemmän kuulia yhteensä", None, "Kokonaismäärä yksin ei ratkaise: vertaa osuuksia."),
                      ("Mahdollisuudet ovat samat, koska mustia on molemmissa yhtä paljon", None, "Mustien määrät ovat eri suuret; samaksi osuudet tekee niiden suhde kaikkiin kuuliin.")]
            steps = [f"{a * 4 * m}/{b * 4 * m} = {fr(p)}", f"{a}/{b} = {fr(p)}"]
            final, params, level = "Sama osuus", {"a": a, "b": b, "k": 4 * m, "justify": True}, "H"
        key = (k, str(params))
        assert key not in seen
        seen.add(key)
        options, cid = mc_options(rng, correct, wrongs)
        items.append(base_item(TID, CODE, start + k, ["S6.06", "S2.02"], ["T11", "T19"], 9, level, prompt,
                               {"options": options, "correct": [cid]}, steps, final,
                               "Oikein: todennäköisyys on suotuisten tulosten osuus kaikista tuloksista.", TEMPLATE, params, date, run))
    return items


if __name__ == "__main__":
    cli(make_items, TID, CODE)
